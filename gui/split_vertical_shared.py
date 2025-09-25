"""Shared data structures for the split vertical GUI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class EffectMatch:
    """Represents an effect inferred from a patch section."""

    section: str
    candidate: str
    canonical_name: Optional[str]
    official_name: Optional[str]
    normalized_name: str
    effect_type: Optional[int]
    is_official: bool
    is_supported: bool
    reason: str = ""

    @property
    def display_name(self) -> str:
        """Human friendly name prioritising official catalog labels."""

        if self.official_name:
            return self.official_name
        if self.canonical_name:
            return self.canonical_name
        if self.candidate:
            return self.candidate
        return self.section.title()

    def should_attempt_load(self) -> bool:
        """Return True when the match can be instantiated as a widget."""

        return bool(self.canonical_name) and self.is_official and self.is_supported

    def describe_failure(self) -> str:
        """Return a human-readable reason for a failure."""

        details = self.reason.strip()
        if not self.is_official and "official" not in details.lower():
            if details:
                details = f"{details}; not in official catalog"
            else:
                details = "Not in official catalog"
        if self.is_official and not self.is_supported and "widget" not in details.lower():
            extra = "No widget available"
            details = f"{details}; {extra}" if details else extra
        return details


