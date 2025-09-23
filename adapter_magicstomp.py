#!/usr/bin/env python3
"""Magicstomp Adapter - JSON to SysEx Converter
=============================================

Convertit un patch JSON généré par :mod:`analyze2json` vers une série de
messages SysEx compatibles avec le format « parameter send » de
MagicstompFrenzy.  L'ancien code envoyait un bloc fictif ``patch_write`` avec
un checksum XOR ; cette version se réaligne sur le protocole Yamaha officiel
(header ``F0 43 7D 40 55 42``, commande ``0x20`` et checksum somme négative sur
7 bits) afin d'obtenir exactement le même comportement que MagicstompFrenzy.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union

import mido

from magicstomp_sysex import ParameterLocation, build_parameter_message

# ---------------------------------------------------------------------------
# Chargement du mapping MagicstompFrenzy
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _MappingEntry:
    effect: str
    label: str
    transform: Callable[["MagicstompAdapter", Any], Optional[int]]


class _SysexInventory:
    """Expose les offsets calculés par :mod:`auto_sysex_mapper`."""

    def __init__(self, inventory_path: Optional[Path] = None) -> None:
        if inventory_path is None:
            inventory_path = Path(__file__).with_name("sysex_inventory.json")

        with inventory_path.open(encoding="utf-8") as handle:
            data = json.load(handle)

        self._effects: Dict[str, Dict[str, ParameterLocation]] = {}
        for effect_name, info in data.get("effects", {}).items():
            effect_map: Dict[str, ParameterLocation] = {}
            for entry in info.get("parameters", []):
                location = ParameterLocation(entry["global_offset"], entry["label"])
                effect_map[entry["label"]] = location
            self._effects[effect_name] = effect_map

    def get(self, effect: str, label: str) -> ParameterLocation:
        try:
            return self._effects[effect][label]
        except KeyError as exc:  # pragma: no cover - garde-fou
            raise KeyError(
                f"Paramètre '{label}' introuvable pour l'effet '{effect}'"
            ) from exc


# ---------------------------------------------------------------------------
# Adaptateur principal
# ---------------------------------------------------------------------------


class MagicstompAdapter:
    """Convertit un patch JSON en messages SysEx Magicstomp."""

    ValueTransform = Callable[["MagicstompAdapter", Any], Optional[int]]

    def __init__(self, device_id: int = 0x00):
        self.device_id = device_id
        self.inventory = _SysexInventory()

        # Tables de correspondance issues de MagicstompFrenzy
        self.amp_models = {
            "BRIT_TOP_BOOST": 0x01,
            "TWEED_BASSMAN": 0x02,
            "JCM800": 0x03,
            "AC30": 0x04,
            "FENDER_TWIN": 0x05,
            "MESA_BOOGIE": 0x06,
        }

        self.reverb_types = {
            "ROOM": 0x01,
            "PLATE": 0x02,
            "HALL": 0x03,
            "SPRING": 0x04,
            "CHURCH": 0x05,
        }

        self.mod_types = {
            "CHORUS": "Chorus",
            "PHASER": "Phaser",
            "TREMOLO": "Tremolo",
        }

        # Mapping JSON → (effet, paramètre, transformation)
        self.parameter_mappings: Dict[Tuple[str, str], _MappingEntry] = {
            # Amplificateur (AmpMultiFlange regroupe les contrôles amp)
            ("amp", "model"): _MappingEntry(
                "AmpMultiFlange", "Amp Type", self._transform_amp_model
            ),
            ("amp", "gain"): _MappingEntry(
                "AmpMultiFlange", "Gain", self._transform_normalized
            ),
            ("amp", "bass"): _MappingEntry(
                "AmpMultiFlange", "Bass", self._transform_normalized
            ),
            ("amp", "mid"): _MappingEntry(
                "AmpMultiFlange", "Middle", self._transform_normalized
            ),
            ("amp", "treble"): _MappingEntry(
                "AmpMultiFlange", "Treble", self._transform_normalized
            ),
            ("amp", "presence"): _MappingEntry(
                "AmpMultiFlange", "Presence", self._transform_normalized
            ),
            # Delay (MonoDelay)
            ("delay", "time_ms"): _MappingEntry(
                "MonoDelay", "Time", self._transform_delay_time
            ),
            ("delay", "feedback"): _MappingEntry(
                "MonoDelay", "Feedback", self._transform_normalized
            ),
            ("delay", "mix"): _MappingEntry(
                "MonoDelay", "Level", self._transform_normalized
            ),
            # Reverb
            ("reverb", "type"): _MappingEntry(
                "Reverb", "Type", self._transform_reverb_type
            ),
            ("reverb", "decay_s"): _MappingEntry(
                "Reverb", "Decay", self._transform_reverb_decay
            ),
            ("reverb", "mix"): _MappingEntry(
                "Reverb", "Mix", self._transform_normalized
            ),
            # Modulation : on se base sur l'effet Chorus pour la vitesse/profondeur
            ("mod", "rate_hz"): _MappingEntry(
                "Chorus", "Frequency", self._transform_mod_rate
            ),
            ("mod", "depth"): _MappingEntry(
                "Chorus", "Depth", self._transform_normalized
            ),
            ("mod", "mix"): _MappingEntry(
                "Chorus", "Feedback", self._transform_normalized
            ),
        }

    # ------------------------------------------------------------------
    # Transformations de valeurs
    # ------------------------------------------------------------------

    @staticmethod
    def _clamp_7bit(value: float) -> int:
        return int(max(0, min(127, round(value))))

    def _transform_normalized(self, value: Any) -> Optional[int]:
        if value is None:
            return None
        return self._clamp_7bit(float(value) * 127)

    def _transform_amp_model(self, value: Any) -> Optional[int]:
        if not isinstance(value, str):
            return None
        return self.amp_models.get(value.upper(), 0)

    def _transform_delay_time(self, value: Any) -> Optional[int]:
        if value is None:
            return None
        milliseconds = max(1.0, float(value))
        milliseconds = min(2000.0, milliseconds)
        ratio = (math.log(milliseconds) - math.log(1.0)) / (
            math.log(2000.0) - math.log(1.0)
        )
        return self._clamp_7bit(ratio * 127)

    def _transform_reverb_type(self, value: Any) -> Optional[int]:
        if not isinstance(value, str):
            return None
        return self.reverb_types.get(value.upper(), 0x02)

    def _transform_reverb_decay(self, value: Any) -> Optional[int]:
        if value is None:
            return None
        decay = max(0.0, min(6.0, float(value)))
        return self._clamp_7bit((decay / 6.0) * 127)

    def _transform_mod_rate(self, value: Any) -> Optional[int]:
        if value is None:
            return None
        rate = max(0.1, min(10.0, float(value)))
        ratio = (math.log(rate) - math.log(0.1)) / (math.log(10.0) - math.log(0.1))
        return self._clamp_7bit(ratio * 127)

    # ------------------------------------------------------------------
    # Conversion principale
    # ------------------------------------------------------------------

    def _load_patch(self, patch_json: Union[Dict[str, Any], str]) -> Dict[str, Any]:
        if isinstance(patch_json, str):
            with open(patch_json, "r", encoding="utf-8") as handle:
                return json.load(handle)
        return patch_json

    def _iter_parameter_messages(
        self, patch: Dict[str, Any]
    ) -> Iterable[List[int]]:
        for (section, key), mapping in self.parameter_mappings.items():
            section_data = patch.get(section)
            if not isinstance(section_data, dict):
                continue

            if section != "amp" and section_data.get("enabled", True) is False:
                continue

            if key not in section_data:
                continue

            raw_value = section_data[key]
            value = mapping.transform(self, raw_value)
            if value is None:
                continue

            location = self.inventory.get(mapping.effect, mapping.label)
            yield build_parameter_message(location.global_offset, [value])

    def json_to_syx(
        self, patch_json: Union[Dict[str, Any], str], patch_number: int = 0
    ) -> List[List[int]]:
        """Convertit un patch JSON vers une liste de messages SysEx."""

        print("🔄 Conversion JSON → SysEx (MagicstompFrenzy)...")
        patch = self._load_patch(patch_json)
        messages = list(self._iter_parameter_messages(patch))

        print(f"✅ {len(messages)} message(s) SysEx généré(s)")
        return messages

    # ------------------------------------------------------------------
    # Entrées/Sorties
    # ------------------------------------------------------------------

    @staticmethod
    def _normalise_messages(
        syx_data: Union[Sequence[int], Sequence[Sequence[int]]]
    ) -> List[List[int]]:
        if not syx_data:
            return []

        first = syx_data[0]  # type: ignore[index]
        if isinstance(first, (list, tuple)):
            return [list(msg) for msg in syx_data]  # type: ignore[return-value]
        return [list(syx_data)]  # type: ignore[list-item]

    def save_to_file(
        self, syx_data: Union[Sequence[int], Sequence[Sequence[int]]], filename: str
    ) -> None:
        messages = self._normalise_messages(syx_data)
        print(f"💾 Sauvegarde de {len(messages)} message(s) vers {filename}...")
        with open(filename, "wb") as handle:
            for message in messages:
                handle.write(bytes(message))
        print("✅ Fichier SysEx sauvegardé")

    def send_to_device(
        self,
        syx_data: Union[Sequence[int], Sequence[Sequence[int]]],
        port_name: Optional[str] = None,
        existing_port=None,
    ) -> bool:
        messages = self._normalise_messages(syx_data)
        if not messages:
            print("⚠️ Aucun message à envoyer")
            return False

        try:
            if existing_port is not None:
                port = existing_port
                close_port = False
            else:
                output_ports = mido.get_output_names()
                if port_name:
                    candidates = [
                        name for name in output_ports if port_name.lower() in name.lower()
                    ]
                else:
                    candidates = [
                        name for name in output_ports if "magicstomp" in name.lower()
                    ]

                if not candidates:
                    print("❌ Aucun port Magicstomp trouvé")
                    print(f"   Ports disponibles: {output_ports}")
                    return False

                selected = candidates[0]
                port = mido.open_output(selected)
                close_port = True
                print(f"🔌 Port MIDI ouvert: {selected}")

            for message in messages:
                port.send(mido.Message("sysex", data=message[1:-1]))
            print(f"✅ {len(messages)} message(s) envoyé(s) au Magicstomp")

            if close_port:
                port.close()

            return True

        except Exception as exc:
            print(f"❌ Erreur lors de l'envoi MIDI: {exc}")
            return False

    @staticmethod
    def list_midi_ports() -> None:
        print("🔌 Ports MIDI disponibles:")
        print("   Entrées:", mido.get_input_names())
        print("   Sorties:", mido.get_output_names())


# ---------------------------------------------------------------------------
# Script de test manuel
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Test de l'adaptateur Magicstomp")
    parser.add_argument("json_file", help="Fichier JSON de patch")
    parser.add_argument("--output", "-o", help="Fichier SysEx de sortie")
    parser.add_argument("--send", "-s", action="store_true", help="Envoyer vers le device")
    args = parser.parse_args()

    adapter = MagicstompAdapter()
    messages = adapter.json_to_syx(args.json_file)

    if args.output:
        adapter.save_to_file(messages, args.output)

    if args.send:
        adapter.send_to_device(messages)

    adapter.list_midi_ports()


if __name__ == "__main__":
    main()
