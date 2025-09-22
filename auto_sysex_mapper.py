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


def print_summary(mapping: Dict[str, object]) -> None:
    """Affiche un résumé lisible du mapping SysEx."""

    print("🎛️  Magicstomp SysEx Mapping Generator")
    print("=" * 50)
    print(f"Sample value used for examples: {mapping['sample_value']}")
    print()

    print("📂 Common parameters")
    for entry in mapping["common_parameters"]:
        print(
            f"  - Offset 0x{entry['global_offset']:02X}"
            f" → {entry['label']} | SysEx: {entry['sysex_hex']}"
        )

    print()
    print("📂 Generic effect parameters (MagicstompFrenzy map)")
    for entry in mapping["global_effect_parameters"]:
        print(
            f"  - Effect offset 0x{entry['effect_offset']:02X}"
            f" (global 0x{entry['global_offset']:02X})"
            f" → {entry['label']} | SysEx: {entry['sysex_hex']}"
        )

    print()
    print("🎚️  Effect-specific parameters")
    for effect_name, info in mapping["effects"].items():
        header = f"- {info['friendly_name']}"
        if info["effect_id_hex"]:
            header += f" (ID {info['effect_id_hex']})"
        print(header)
        for entry in info["parameters"]:
            print(
                f"    • offset 0x{entry['effect_offset']:02X}"
                f" (global 0x{entry['global_offset']:02X})"
                f" → {entry['label']} | {entry['sysex_hex']}"
            )
        print()


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

    args = parser.parse_args()

    sample_value = max(0, min(127, args.value))
    mapping = generate_mapping(sample_value)

    print_summary(mapping)

    if args.output:
        json_kwargs = {"indent": 2, "ensure_ascii": False} if args.pretty else {}
        args.output.write_text(
            json.dumps(mapping, **json_kwargs), encoding="utf-8"
        )
        print(f"📄 Mapping écrit dans {args.output}")


if __name__ == "__main__":
    main()

