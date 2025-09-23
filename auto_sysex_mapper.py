#!/usr/bin/env python3
"""Magicstomp SysEx Mapping Generator.

Ce script automatise l'extraction du mapping effet → paramètres → messages
SysEx à partir des fichiers de référence *MagicstompFrenzy* présents dans le
répertoire ``magicstompfrenzy_reference``.  Il parcourt l'ensemble des effets
et des réglages disponibles, calcule le message SysEx correspondant à chaque
paramètre et peut optionnellement exporter le résultat au format JSON.

Usage rapide::

    python auto_sysex_mapper.py --output sysex_map.json --pretty

Cela génère ``sysex_map.json`` contenant toutes les informations de mapping et
affiche également un résumé lisible dans la console.

Le script sait aussi filtrer le résumé pour retrouver rapidement un message
SysEx précis :

    python auto_sysex_mapper.py --effect Delay --parameter "Delay Level" --value 96

Ici, seule l'entrée du paramètre « Delay Level » est affichée et le message
SysEx correspond à la valeur 96.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from magicstomp_parameter_map import COMMON_PARAMETERS, EFFECT_PARAMETERS


# ---------------------------------------------------------------------------
# Constantes SysEx Magicstomp (extraites de realtime_magicstomp.py)
# ---------------------------------------------------------------------------
SYX_HEADER = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42]
PARAM_SEND_CMD = 0x20
SYX_FOOTER = 0xF7
PATCH_COMMON_LENGTH = 0x20  # 32 octets pour la section "common"


def calculate_checksum(data: Iterable[int]) -> int:
    """Calcule le checksum Yamaha sur 7 bits."""

    checksum = 0
    for byte in data:
        checksum += byte
    return (-checksum) & 0x7F


def build_sysex_message(global_offset: int, value: int) -> List[int]:
    """Construit un message SysEx (liste d'entiers) pour ``global_offset``."""

    message: List[int] = []
    message.extend(SYX_HEADER)
    message.append(PARAM_SEND_CMD)

    if global_offset < PATCH_COMMON_LENGTH:
        section = 0x00
        section_offset = global_offset
    else:
        section = 0x01
        section_offset = global_offset - PATCH_COMMON_LENGTH

    message.extend([section, section_offset])
    message.append(value & 0x7F)

    checksum = calculate_checksum(message[1:])
    message.append(checksum)
    message.append(SYX_FOOTER)
    return message


def format_sysex_hex(message: Iterable[int]) -> str:
    """Retourne une chaîne hexadécimale lisible pour ``message``."""

    return " ".join(f"{byte:02X}" for byte in message)


# ---------------------------------------------------------------------------
# Parsing des fichiers MagicstompFrenzy
# ---------------------------------------------------------------------------


def parse_effect_ids(header_path: Path) -> Dict[str, int]:
    """Extrait le mapping ``NomEffet -> ID`` depuis ``magicstomp.h``."""

    effect_id_pattern = re.compile(r"^(\s*)([A-Za-z0-9_]+)\s*=\s*0x([0-9A-Fa-f]{2}),")
    effect_ids: Dict[str, int] = {}

    with header_path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            match = effect_id_pattern.match(line)
            if not match:
                continue
            name = match.group(2)
            value = int(match.group(3), 16)
            effect_ids[name] = value

    return effect_ids


def parse_knobparameters_file(header_path: Path) -> Dict[str, Dict[int, str]]:
    """Extrait les paramètres de ``knobparameters.h``.

    Retourne un dictionnaire ``NomEffet -> {offset: libellé}`` où ``offset`` est
    l'offset **dans la section effet** (c'est-à-dire sans les 32 octets communs).
    """

    effect_pattern = re.compile(
        r"const\s+QMap<int,\s*QString>\s+(?P<name>[A-Za-z0-9_]+)KnobParameters\s*="
    )
    entry_pattern = re.compile(
        r"\{\s*(0x[0-9A-Fa-f]+|\d+)\s*,\s*QStringLiteral\(\"([^\"]+)\"\)\s*\}"
    )

    effect_parameters: Dict[str, Dict[int, str]] = {}
    current_effect: Optional[str] = None

    with header_path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()

            effect_match = effect_pattern.match(line)
            if effect_match:
                current_effect = effect_match.group("name")
                effect_parameters[current_effect] = {}
                continue

            if current_effect is None:
                continue

            if line.startswith("};"):
                current_effect = None
                continue

            entry_match = entry_pattern.search(line)
            if not entry_match:
                continue

            offset_str, label = entry_match.groups()
            offset = int(offset_str, 0)
            effect_parameters[current_effect][offset] = label

    return effect_parameters


# ---------------------------------------------------------------------------
# Génération du mapping complet
# ---------------------------------------------------------------------------


def camel_to_words(name: str) -> str:
    """Transforme ``AmpMultiFlange`` en ``Amp Multi Flange``."""

    spaced = re.sub(r"(?<!^)(?=[A-Z])", " ", name)
    return spaced.replace("  ", " ").strip()


def build_entry(offset: int, label: str, value: int, section_hint: str) -> Dict[str, object]:
    """Crée l'entrée de mapping pour un paramètre donné."""

    if section_hint == "common":
        global_offset = offset
        effect_offset = None
        section_name = "common"
    elif section_hint == "effect":
        effect_offset = offset
        global_offset = PATCH_COMMON_LENGTH + offset
        section_name = "effect"
    else:
        raise ValueError(f"Section inconnue: {section_hint}")

    sysex = build_sysex_message(global_offset, value)

    entry: Dict[str, object] = {
        "label": label,
        "raw_offset": offset,
        "section": section_name,
        "global_offset": global_offset,
        "sysex": sysex,
        "sysex_hex": format_sysex_hex(sysex),
        "value": value,
    }

    if effect_offset is not None:
        entry["effect_offset"] = effect_offset

    return entry


def generate_mapping(sample_value: int) -> Dict[str, object]:
    """Construit le mapping complet (common + effets)."""

    base_path = Path(__file__).resolve().parent
    reference_path = base_path / "magicstompfrenzy_reference"

    knobparameters_path = reference_path / "knobparameters.h"
    effect_ids_path = reference_path / "magicstomp.h"

    effect_parameters = parse_knobparameters_file(knobparameters_path)
    effect_ids = parse_effect_ids(effect_ids_path)

    mapping: Dict[str, object] = {
        "sample_value": sample_value,
        "common_parameters": [],
        "global_effect_parameters": [],
        "effects": {},
    }

    for offset, label in sorted(COMMON_PARAMETERS.items()):
        mapping["common_parameters"].append(
            build_entry(offset, label, sample_value, section_hint="common")
        )

    for offset, label in sorted(EFFECT_PARAMETERS.items()):
        mapping["global_effect_parameters"].append(
            build_entry(offset, label, sample_value, section_hint="effect")
        )

    for effect_name in sorted(effect_parameters):
        params = effect_parameters[effect_name]
        effect_info = {
            "effect_id": effect_ids.get(effect_name),
            "effect_id_hex": (
                f"0x{effect_ids[effect_name]:02X}"
                if effect_name in effect_ids
                else None
            ),
            "friendly_name": camel_to_words(effect_name),
            "parameters": [],
        }

        for offset, label in sorted(params.items()):
            entry = build_entry(offset, label, sample_value, section_hint="effect")
            effect_info["parameters"].append(entry)

        mapping["effects"][effect_name] = effect_info

    return mapping


def _matches_filter(value: str, filter_value: Optional[str]) -> bool:
    return not filter_value or filter_value in value.lower()


def print_summary(
    mapping: Dict[str, object],
    *,
    effect_filter: Optional[str] = None,
    parameter_filter: Optional[str] = None,
    include_common: bool = True,
    include_global: bool = True,
    include_effects: bool = True,
) -> None:
    """Affiche un résumé lisible (avec filtres optionnels) du mapping SysEx."""

    effect_filter = effect_filter.lower() if effect_filter else None
    parameter_filter = parameter_filter.lower() if parameter_filter else None

    print("🎛️  Magicstomp SysEx Mapping Generator")
    print("=" * 50)
    print(f"Sample value used for examples: {mapping['sample_value']}")
    print()

    matches_found = False

    if include_common:
        filtered_entries = [
            entry
            for entry in mapping["common_parameters"]
            if _matches_filter(entry["label"].lower(), parameter_filter)
        ]
        if filtered_entries:
            matches_found = True
            print("📂 Common parameters")
            for entry in filtered_entries:
                print(
                    f"  - Offset 0x{entry['global_offset']:02X}"
                    f" → {entry['label']} | SysEx: {entry['sysex_hex']}"
                )
            print()

    if include_global:
        filtered_entries = [
            entry
            for entry in mapping["global_effect_parameters"]
            if _matches_filter(entry["label"].lower(), parameter_filter)
        ]
        if filtered_entries:
            matches_found = True
            print("📂 Generic effect parameters (MagicstompFrenzy map)")
            for entry in filtered_entries:
                print(
                    f"  - Effect offset 0x{entry['effect_offset']:02X}"
                    f" (global 0x{entry['global_offset']:02X})"
                    f" → {entry['label']} | SysEx: {entry['sysex_hex']}"
                )
            print()

    if include_effects:
        printed_any_effect = False
        effect_candidates = False
        for effect_name, info in mapping["effects"].items():
            matches_effect = not effect_filter or (
                _matches_filter(effect_name.lower(), effect_filter)
                or _matches_filter(info["friendly_name"].lower(), effect_filter)
            )
            if not matches_effect:
                continue

            effect_candidates = True
            filtered_entries = [
                entry
                for entry in info["parameters"]
                if _matches_filter(entry["label"].lower(), parameter_filter)
            ]
            if not filtered_entries:
                continue

            matches_found = True
            printed_any_effect = True
            header = f"- {info['friendly_name']}"
            if info["effect_id_hex"]:
                header += f" (ID {info['effect_id_hex']})"
            print(header)
            for entry in filtered_entries:
                print(
                    f"    • offset 0x{entry['effect_offset']:02X}"
                    f" (global 0x{entry['global_offset']:02X})"
                    f" → {entry['label']} | {entry['sysex_hex']}"
                )
            print()

        if include_effects:
            if effect_filter and not effect_candidates:
                matches_found = True
                print("Aucun effet ne correspond au filtre donné.")
            elif (
                effect_filter
                and parameter_filter
                and effect_candidates
                and not printed_any_effect
            ):
                matches_found = True
                print(
                    "Les effets correspondent au filtre, mais aucun paramètre ne"
                    " vérifie le filtre demandé."
                )

    if not matches_found:
        if parameter_filter or effect_filter:
            print("Aucun paramètre ne correspond aux filtres fournis.")
        else:
            print("(Aucun paramètre trouvé – vérifiez les données source.)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Génère le mapping complet Effet/Paramètre → message SysEx en se"
            " basant sur les données MagicstompFrenzy."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Fichier JSON de sortie (optionnel)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Écrit le JSON avec indentation pour une lecture aisée.",
    )
    parser.add_argument(
        "--value",
        type=int,
        default=64,
        help="Valeur (0-127) utilisée dans les exemples de messages SysEx.",
    )
    parser.add_argument(
        "--effect",
        type=str,
        help="Filtre sur le nom d'effet (insensible à la casse).",
    )
    parser.add_argument(
        "--parameter",
        type=str,
        help="Filtre sur le nom du paramètre (insensible à la casse).",
    )
    parser.add_argument(
        "--no-common",
        action="store_true",
        help="Masque la section des paramètres communs.",
    )
    parser.add_argument(
        "--no-global",
        action="store_true",
        help="Masque les paramètres d'effet génériques.",
    )
    parser.add_argument(
        "--no-effects",
        action="store_true",
        help="Masque les paramètres spécifiques à chaque effet.",
    )

    args = parser.parse_args()

    sample_value = max(0, min(127, args.value))
    mapping = generate_mapping(sample_value)

    print_summary(
        mapping,
        effect_filter=args.effect,
        parameter_filter=args.parameter,
        include_common=not args.no_common,
        include_global=not args.no_global,
        include_effects=not args.no_effects,
    )

    if args.output:
        json_kwargs = {"indent": 2, "ensure_ascii": False} if args.pretty else {}
        args.output.write_text(
            json.dumps(mapping, **json_kwargs), encoding="utf-8"
        )
        print(f"📄 Mapping écrit dans {args.output}")


if __name__ == "__main__":
    main()

