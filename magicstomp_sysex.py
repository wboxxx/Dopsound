"""Common SysEx helpers for Yamaha Magicstomp.

This module centralises the low-level details extracted from the
MagicstompFrenzy project so that every part of the codebase builds SysEx
messages in exactly the same way.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

SYSEX_HEADER: List[int] = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42]
"""Prefix used for parameter-send messages (MagicstompFrenzy format)."""

PARAMETER_SEND_CMD: int = 0x20
"""Command byte used when updating parameters in real time."""

SYSEX_FOOTER: int = 0xF7
"""End of exclusive marker."""

PATCH_COMMON_LENGTH: int = 0x20
PATCH_EFFECT_LENGTH: int = 0x7F
PATCH_TOTAL_LENGTH: int = PATCH_COMMON_LENGTH + PATCH_EFFECT_LENGTH


def calculate_checksum(data: Iterable[int]) -> int:
    """Return the 7-bit Yamaha checksum for *data*.

    MagicstompFrenzy computes the checksum by summing the payload bytes and
    negating the result on 7 bits.  Adopting the exact same implementation
    avoids the XOR variant that had slipped into some utilities.
    """

    total = 0
    for byte in data:
        total += byte
    return (-total) & 0x7F


def build_parameter_message(global_offset: int, values: Iterable[int]) -> List[int]:
    """Build a SysEx message that writes *values* at *global_offset*.

    Args:
        global_offset: Absolute offset inside the Magicstomp patch (0-158).
        values: Sequence of 7-bit values to store starting at *global_offset*.
    """

    message: List[int] = []
    message.extend(SYSEX_HEADER)
    message.append(PARAMETER_SEND_CMD)

    if global_offset < PATCH_COMMON_LENGTH:
        section = 0x00
        section_offset = global_offset
    else:
        section = 0x01
        section_offset = global_offset - PATCH_COMMON_LENGTH

    message.append(section)
    message.append(section_offset)

    for value in values:
        message.append(value & 0x7F)

    checksum = calculate_checksum(message[1:])
    message.append(checksum)
    message.append(SYSEX_FOOTER)
    return message


@dataclass(frozen=True)
class ParameterLocation:
    """Small helper describing where a parameter lives in the patch."""

    global_offset: int
    label: str

    @property
    def section(self) -> int:
        return 0 if self.global_offset < PATCH_COMMON_LENGTH else 1

    @property
    def section_offset(self) -> int:
        if self.section == 0:
            return self.global_offset
        return self.global_offset - PATCH_COMMON_LENGTH
