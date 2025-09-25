"""Effect identification and widget cascade helpers."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Dict, List, Optional

import tkinter as tk
from tkinter import ttk

from magicstomp_effects import EffectRegistry

from gui.split_vertical_shared import EffectMatch


class SplitVerticalGUIEffectsMixin:
    """Effect identification and widget cascade helpers."""

    def clear_effect_widgets(self):
        """Clear all existing effect widgets from the cascade."""
        try:
            from debug_logger import debug_logger
debug_logger.log(f"🔍 DEBUG: Clearing existing effect widgets")
            
            # Clear the cascade list
            if hasattr(self, 'effect_widget_cascade'):
                self.effect_widget_cascade.clear()
            
            # Clear current effect widget
            self.current_effect_widget = None
            self.current_effect_type = None
            
            # Clear effect tabs if they exist
            if hasattr(self, 'notebook'):
                # Find and remove effect tabs (they usually have "Effect" in the name)
                tabs_to_remove = []
                for i in range(self.notebook.index('end')):
                    tab_text = self.notebook.tab(i, 'text')
                    if 'Effect' in tab_text and tab_text != 'Effects':
                        tabs_to_remove.append(i)
                
                # Remove tabs in reverse order to avoid index shifting
                for i in reversed(tabs_to_remove):
                    try:
                        self.notebook.forget(i)
debug_logger.log(f"🔍 DEBUG: Removed effect tab: {i}")
                    except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error removing tab {i}: {e}")
            
debug_logger.log(f"🔍 DEBUG: Effect widgets cleared successfully")
            
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error clearing effect widgets: {e}")
            import traceback
            traceback.print_exc()

    def apply_patch_parameters_to_widgets(self):
        """Apply current patch parameters to all loaded effect widgets."""
        try:
            if not self.current_patch or not self.effect_widget_cascade:
debug_logger.log(f"🔍 DEBUG: No patch or widgets to apply parameters to")
                return
            
debug_logger.log(f"🔍 DEBUG: Applying patch parameters to widgets")
            self.log_status("🔄 Applying patch parameters to widgets...")
            
            # Convert patch parameters to widget parameters
            widget_params = self.convert_patch_to_widget_params(self.current_patch)
debug_logger.log(f"🔍 DEBUG: Converted widget params: {widget_params}")
            
            if widget_params:
                # Apply parameters to all widgets in the cascade
                for widget in self.effect_widget_cascade:
                    if hasattr(widget, 'set_all_parameters'):
                        try:
                            widget.set_all_parameters(widget_params)
debug_logger.log(f"🔍 DEBUG: Applied parameters to widget: {widget}")
                        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error applying parameters to widget: {e}")
                
                self.log_status("✅ Patch parameters applied to widgets")
debug_logger.log(f"🔍 DEBUG: Patch parameters applied successfully")
            else:
debug_logger.log(f"🔍 DEBUG: No widget parameters to apply")
                
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error applying patch parameters to widgets: {e}")
            import traceback
            traceback.print_exc()
    
    def apply_sysex_data_to_widgets(self, sysex_data):
        """Apply SYSEX data directly to effect widgets."""
        try:
            if not sysex_data or not self.effect_widget_cascade:
debug_logger.log(f"🔍 DEBUG: No SYSEX data or widgets to apply to")
                return
            
debug_logger.log(f"🔍 DEBUG: Applying SYSEX data to widgets")
            self.log_status("🔄 Applying SYSEX data to widgets...")
            
            # Extract common and effect data
            common_data = sysex_data.get('common', [])
            effect_data = sysex_data.get('effect', [])
            
debug_logger.log(f"🔍 DEBUG: Common data: {len(common_data)} bytes")
debug_logger.log(f"🔍 DEBUG: Effect data: {len(effect_data)} bytes")
            
            # Apply to all widgets in the cascade
            for widget in self.effect_widget_cascade:
                if hasattr(widget, 'apply_magicstomp_data'):
                    try:
                        # Apply effect data to the widget
                        applied_params = widget.apply_magicstomp_data(effect_data)
debug_logger.log(f"🔍 DEBUG: Applied SYSEX data to widget: {widget}")
debug_logger.log(f"🔍 DEBUG: Applied parameters: {applied_params}")
                    except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error applying SYSEX data to widget: {e}")
                        import traceback
                        traceback.print_exc()
            
            self.log_status("✅ SYSEX data applied to widgets")
debug_logger.log(f"🔍 DEBUG: SYSEX data applied successfully")
                
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error applying SYSEX data to widgets: {e}")
            import traceback
            traceback.print_exc()

    def normalize_effect_name(self, name):
        """Normalize effect names for comparison."""
        if not name:
            return ""
        return re.sub(r"[\s\.]+", "", name).lower()

    def is_section_enabled(self, section_data: Dict) -> bool:
        """Return True if the section is enabled or has no explicit flag."""

        if not isinstance(section_data, dict):
            return False

        if "enabled" not in section_data:
            return True

        enabled_value = section_data.get("enabled")
        if isinstance(enabled_value, str):
            normalized = enabled_value.strip().lower()
            return normalized not in {"", "0", "false", "off", "no"}
        if isinstance(enabled_value, (int, float)):
            return enabled_value != 0
        return bool(enabled_value)

    def collect_lower_values(self, section_data: Dict, *keys: str) -> List[str]:
        """Collect non-empty values from the section as lowercase strings."""

        values: List[str] = []
        for key in keys:
            if key not in section_data:
                continue
            raw = section_data.get(key)
            if raw is None:
                continue
            if isinstance(raw, str):
                lowered = raw.strip().lower()
            else:
                lowered = str(raw).strip().lower()
            if lowered:
                values.append(lowered)
        return values

    def value_is_truthy(self, value) -> bool:
        """Evaluate heterogeneous values to a boolean."""

        if isinstance(value, str):
            return value.strip().lower() not in {"", "0", "false", "off", "no"}
        if isinstance(value, (int, float)):
            return value != 0
        return bool(value)

    def match_effect_by_name(self, effect_name: str, section_name: str, reason: str = "") -> Optional[EffectMatch]:
        """Build an effect match from a candidate name using catalog metadata."""

        if not effect_name:
            return None

        normalized = self.normalize_effect_name(effect_name)
        if not normalized:
            return None

        canonical_name = self.supported_effect_normalized_to_name.get(normalized)
        effect_type = self.supported_effect_normalized_to_type.get(normalized)

        official_name = self.official_effect_lookup.get(normalized)
        if not official_name and canonical_name:
            official_name = self.canonical_to_official_name.get(canonical_name)

        is_official = bool(official_name)
        is_supported = effect_type is not None

        return EffectMatch(
            section=section_name,
            candidate=effect_name,
            canonical_name=canonical_name,
            official_name=official_name,
            normalized_name=normalized,
            effect_type=effect_type,
            is_official=is_official,
            is_supported=is_supported,
            reason=reason or "",
        )

    def load_official_effect_catalog(self):
        """Load official Magicstomp effect names from the CSV reference."""
        catalog_path = Path(__file__).parent.parent / "magicstomp_Effects+List.csv"
debug_logger.log(f"🔍 DEBUG: Loading official effect catalog from {catalog_path}")

        self.official_effect_names = set()
        self.official_effect_lookup = {}

        if catalog_path.exists():
            try:
                with open(catalog_path, newline='', encoding='utf-8-sig') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if not row:
                            continue
                        raw_name = row[0].strip()
                        if not raw_name:
                            continue

                        upper_name = raw_name.upper()
                        if upper_name.startswith("EFFECT TYPE") or upper_name.startswith("EFFECT TYPE LIST"):
                            continue
                        if upper_name.startswith("EFFECT PARAMETERS"):
                            break

                        normalized = self.normalize_effect_name(raw_name)
                        if not normalized:
                            continue

                        self.official_effect_names.add(raw_name)
                        self.official_effect_lookup[normalized] = raw_name

debug_logger.log(f"🔍 DEBUG: Loaded {len(self.official_effect_names)} official effect names")
            except Exception as exc:
debug_logger.log(f"🔍 DEBUG: Failed to load official effect catalog: {exc}")
                self.official_effect_names = set()
                self.official_effect_lookup = {}
        else:
debug_logger.log(f"🔍 DEBUG: Official effect catalog not found; falling back to registry names only")

        # Build supported effect lookup from EffectRegistry
        supported_effects = EffectRegistry.get_supported_effects()
        self.supported_effect_name_to_type = {
            name: effect_type for effect_type, name in supported_effects.items()
        }
        self.supported_effect_normalized_to_name = {
            self.normalize_effect_name(name): name for name in self.supported_effect_name_to_type
        }
        self.supported_effect_normalized_to_type = {
            self.normalize_effect_name(name): effect_type
            for effect_type, name in supported_effects.items()
        }

        # Handle naming differences between CSV and registry
        alias_map = {
            self.normalize_effect_name("Early Ref."): self.normalize_effect_name("Early Reflections"),
            self.normalize_effect_name("M.Band Dyna."): self.normalize_effect_name("M. Band Dynamic Processor"),
            self.normalize_effect_name("Dyna. Filter"): self.normalize_effect_name("Dynamic Filter"),
            self.normalize_effect_name("Dyna. Flange"): self.normalize_effect_name("Dynamic Flange"),
            self.normalize_effect_name("Dyna. Phaser"): self.normalize_effect_name("Dynamic Phaser"),
        }

        for alias_norm, target_norm in alias_map.items():
            if target_norm in self.supported_effect_normalized_to_name:
                canonical_name = self.supported_effect_normalized_to_name[target_norm]
                effect_type = self.supported_effect_normalized_to_type[target_norm]
                self.supported_effect_normalized_to_name[alias_norm] = canonical_name
                self.supported_effect_normalized_to_type[alias_norm] = effect_type

        # Map canonical registry names back to official CSV labels when possible
        self.canonical_to_official_name = {}
        if self.official_effect_lookup:
            for normalized, official_name in self.official_effect_lookup.items():
                canonical_name = self.supported_effect_normalized_to_name.get(normalized)
                if canonical_name:
                    self.canonical_to_official_name[canonical_name] = official_name

        self.effect_metadata_loaded = True
debug_logger.log(f"🔍 DEBUG: Supported effects (widgets): {len(self.supported_effect_name_to_type)}")

    def get_canonical_effect_name(self, effect_name):
        """Return the canonical registry name for an effect if supported."""
        if not effect_name:
            return None
        normalized = self.normalize_effect_name(effect_name)
        canonical = self.supported_effect_normalized_to_name.get(normalized)
        if canonical:
            return canonical
        return None

    def get_effect_type_for_name(self, effect_name):
        """Retrieve the effect type for a canonical effect name."""
        if not effect_name:
            return None
        normalized = self.normalize_effect_name(effect_name)
        return self.supported_effect_normalized_to_type.get(normalized)

    def get_display_name_for_effect(self, effect_name):
        """Return the official CSV label when available for display/logs."""
        if not effect_name:
            return ""
        return self.canonical_to_official_name.get(effect_name, effect_name)

    def is_effect_official(self, effect_name):
        """Check if an effect belongs to the official Magicstomp catalog."""
        if not effect_name:
            return False
        if not self.official_effect_lookup:
            # No catalog available; accept supported registry entries
            return True

        normalized = self.normalize_effect_name(effect_name)
        if normalized in self.official_effect_lookup:
            return True

        display_name = self.get_display_name_for_effect(effect_name)
        display_normalized = self.normalize_effect_name(display_name)
        return display_normalized in self.official_effect_lookup

    def map_section_to_effect(self, section_name, section_data):
        """Map patch sections to official Magicstomp effect names."""

        if not isinstance(section_data, dict):
debug_logger.log(f"🔍 DEBUG: Section {section_name} ignored (not a mapping)")
            return None

        section_key = section_name.lower()
        if section_key == 'meta':
            return None

        if not self.is_section_enabled(section_data):
debug_logger.log(f"🔍 DEBUG: Section {section_name} disabled or bypassed")
            return None

        direct_mapping = {
            'compressor': 'Compressor',
            'comp': 'Compressor',
            'eq': '3 Band Parametric EQ',
            'eq3band': '3 Band Parametric EQ',
            'three_band_eq': '3 Band Parametric EQ',
            'amp': 'Amp Simulator',
            'amp_sim': 'Amp Simulator',
            'amp_simulator': 'Amp Simulator',
            'ampmodel': 'Amp Simulator',
            'stereo_delay': 'Stereo Delay',
            'tape_echo': 'Tape Echo',
            'echo': 'Echo',
            'mod_delay': 'Mod. Delay',
            'moddelay': 'Mod. Delay',
            'delay_lcr': 'Delay LCR',
            'chorus': 'Chorus',
            'flanger': 'Flange',
            'phaser': 'Phaser',
            'tremolo': 'Tremolo',
            'symphonic': 'Symphonic',
            'rotary': 'Rotary',
            'ring_mod': 'Ring Mod.',
            'ringmod': 'Ring Mod.',
            'ring': 'Ring Mod.',
            'auto_pan': 'Auto Pan',
            'autopan': 'Auto Pan',
            'distortion': 'Distortion',
            'fuzz': 'Distortion',
            'overdrive': 'Distortion',
            'gate': 'Gate Reverb',
            'reverse_gate': 'Reverse Gate',
            'spring_reverb': 'Spring Reverb',
            'early_ref': 'Early Reflections',
            'early_reflections': 'Early Reflections',
            'limiter': 'Multi Filter',
            'multi_filter': 'Multi Filter',
            'dynamic_filter': 'Dynamic Filter',
            'dynamic_flange': 'Dynamic Flange',
            'dynamic_phaser': 'Dynamic Phaser',
            'mod_filter': 'Mod. Filter',
            'dual_pitch': 'Dual Pitch',
            'hq_pitch': 'HQ Pitch',
            'mband': 'M. Band Dynamic Processor',
            'm_band': 'M. Band Dynamic Processor',
            'mband_dyna': 'M. Band Dynamic Processor',
            'mband_dynamic': 'M. Band Dynamic Processor',
            'dynamics': 'M. Band Dynamic Processor',
        }

        if section_key in direct_mapping:
            match = self.match_effect_by_name(direct_mapping[section_key], section_name)
            if match:
                print(
                    f"🔍 DEBUG: Section {section_name} direct-mapped to {match.display_name} "
                    f"(official={match.is_official}, supported={match.is_supported})"
                )
            else:
debug_logger.log(f"🔍 DEBUG: Direct mapping failed for section {section_name}")
            return match

        match: Optional[EffectMatch] = None

        if section_key == 'delay':
            match = self.infer_delay_effect(section_name, section_data)
        elif section_key == 'reverb':
            match = self.infer_reverb_effect(section_name, section_data)
        elif section_key == 'mod':
            match = self.infer_mod_effect(section_name, section_data)
        elif section_key == 'booster':
            match = self.infer_booster_effect(section_name, section_data)
        elif section_key in {'pitch', 'pitch_shift', 'harmonizer'}:
            match = self.infer_pitch_effect(section_name, section_data)
        elif section_key in {'filter', 'tone'}:
            match = self.infer_filter_effect(section_name, section_data)

        if match:
            print(
                f"🔍 DEBUG: Section {section_name} heuristically mapped to {match.display_name} "
                f"(official={match.is_official}, supported={match.is_supported})"
            )
        else:
debug_logger.log(f"🔍 DEBUG: No mapping found for section: {section_name}")
        return match

    def infer_delay_effect(self, section_name: str, section_data: Dict) -> Optional[EffectMatch]:
        """Infer a delay-based effect from section details."""

        keywords = set(
            self.collect_lower_values(
                section_data, 'type', 'mode', 'variant', 'algorithm', 'style'
            )
        )
        has_left_right = any(
            token in key.lower()
            for key in section_data.keys()
            for token in ('left', 'right')
        )
        has_modulation = any(
            key in section_data for key in ('mod_depth', 'mod_rate', 'wow', 'flutter')
        )

        if any('stereo' in kw for kw in keywords) or self.value_is_truthy(section_data.get('ping_pong')):
            candidate = 'Stereo Delay'
        elif has_left_right or section_data.get('lcr_mix') is not None:
            candidate = 'Delay LCR'
        elif any('tape' in kw for kw in keywords) or any('analog' in kw for kw in keywords):
            candidate = 'Tape Echo'
        elif any('echo' in kw for kw in keywords):
            candidate = 'Echo'
        elif any('mod' in kw for kw in keywords) or has_modulation:
            candidate = 'Mod. Delay'
        else:
            candidate = 'Mono Delay'

        return self.match_effect_by_name(candidate, section_name)

    def infer_reverb_effect(self, section_name: str, section_data: Dict) -> Optional[EffectMatch]:
        """Infer a reverb effect from section details."""

        keywords = set(
            self.collect_lower_values(
                section_data, 'type', 'mode', 'variant', 'algorithm', 'character'
            )
        )

        if any('spring' in kw for kw in keywords):
            candidate = 'Spring Reverb'
        elif any('reverse' in kw for kw in keywords):
            candidate = 'Reverse Gate'
        elif any('gate' in kw for kw in keywords):
            candidate = 'Gate Reverb'
        elif any('early' in kw for kw in keywords) or self.value_is_truthy(section_data.get('early_reflections')):
            candidate = 'Early Reflections'
        else:
            candidate = 'Reverb'

        return self.match_effect_by_name(candidate, section_name)

    def infer_mod_effect(self, section_name: str, section_data: Dict) -> Optional[EffectMatch]:
        """Infer a modulation effect from section details."""

        keywords = self.collect_lower_values(
            section_data, 'type', 'mode', 'variant', 'algorithm', 'waveform'
        )
        candidate = None

        for value in keywords:
            if 'chorus' in value:
                candidate = 'Chorus'
                break
            if 'symph' in value or 'ensemble' in value:
                candidate = 'Symphonic'
                break
            if 'flang' in value:
                candidate = 'Flange'
                break
            if 'phaser' in value:
                candidate = 'Phaser'
                break
            if 'trem' in value or 'vibrato' in value:
                candidate = 'Tremolo'
                break
            if 'rotary' in value or 'leslie' in value:
                candidate = 'Rotary'
                break
            if 'ring' in value:
                candidate = 'Ring Mod.'
                break
            if 'auto pan' in value or 'autopan' in value or value == 'pan':
                candidate = 'Auto Pan'
                break
            if 'filter' in value or 'wah' in value:
                candidate = 'Mod. Filter'
                break

        if candidate is None:
            if any(self.value_is_truthy(section_data.get(flag)) for flag in ('ring_mod', 'ringmod')):
                candidate = 'Ring Mod.'
            elif any(self.value_is_truthy(section_data.get(flag)) for flag in ('auto_pan', 'autopan')):
                candidate = 'Auto Pan'

        if candidate is None:
            return None

        return self.match_effect_by_name(candidate, section_name)

    def infer_booster_effect(self, section_name: str, section_data: Dict) -> Optional[EffectMatch]:
        """Infer a booster effect from section details."""

        keywords = self.collect_lower_values(section_data, 'type', 'mode', 'variant')
        candidate = None

        for value in keywords:
            if 'clean' in value or 'compress' in value:
                candidate = 'Compressor'
                break
            if any(token in value for token in ('dist', 'drive', 'fuzz', 'tube', 'over')):
                candidate = 'Distortion'
                break

        if candidate is None and self.value_is_truthy(section_data.get('clean_boost')):
            candidate = 'Compressor'

        if candidate is None:
            candidate = 'Distortion'

        return self.match_effect_by_name(candidate, section_name)

    def infer_pitch_effect(self, section_name: str, section_data: Dict) -> Optional[EffectMatch]:
        """Infer a pitch-based effect from section details."""

        keywords = self.collect_lower_values(section_data, 'type', 'mode', 'variant', 'algorithm', 'quality')
        voices = section_data.get('voices') or section_data.get('voice_count')
        candidate = None

        if any('dual' in value for value in keywords):
            candidate = 'Dual Pitch'
        elif any('harm' in value for value in keywords):
            candidate = 'Dual Pitch'
        elif isinstance(voices, (int, float)) and voices and voices > 1:
            candidate = 'Dual Pitch'

        if candidate is None:
            candidate = 'HQ Pitch'

        return self.match_effect_by_name(candidate, section_name)

    def infer_filter_effect(self, section_name: str, section_data: Dict) -> Optional[EffectMatch]:
        """Infer a filter-style effect from section details."""

        keywords = self.collect_lower_values(section_data, 'type', 'mode', 'variant', 'algorithm')
        candidate = None

        for value in keywords:
            if 'dynamic' in value or 'dyna' in value:
                candidate = 'Dynamic Filter'
                break
            if 'multi' in value:
                candidate = 'Multi Filter'
                break
            if 'mod' in value or 'wah' in value:
                candidate = 'Mod. Filter'
                break

        if candidate is None and section_name.lower() == 'filter':
            candidate = 'Multi Filter'

        if candidate is None:
            return None

        return self.match_effect_by_name(candidate, section_name)

    def identify_effects_from_patch(self, patch):
        """Identify effects from patch data."""

debug_logger.log(f"🔍 DEBUG: Starting identify_effects_from_patch()")
debug_logger.log(f"🔍 DEBUG: Analyzing patch: {patch}")

        report: Dict[str, List[EffectMatch]] = {
            'official': [],
            'unsupported': [],
            'unverified': [],
            'duplicates': [],
        }
        seen_effects = set()

        try:
            for section_name, section_data in patch.items():
                if isinstance(section_data, dict) and section_name != 'meta':
debug_logger.log(f"🔍 DEBUG: Analyzing section: {section_name}")

                    match = self.map_section_to_effect(section_name, section_data)
                    if not match:
                        continue

                    normalized = match.normalized_name
                    if normalized and normalized in seen_effects:
                        match.reason = match.reason or "Duplicate section match"
                        report['duplicates'].append(match)
                        print(
                            f"🔍 DEBUG: Duplicate effect ignored: {match.display_name} (section: {section_name})"
                        )
                        continue

                    if normalized:
                        seen_effects.add(normalized)

                    if match.is_official and match.is_supported:
                        report['official'].append(match)
                        print(
                            f"🔍 DEBUG: Official effect identified: {match.display_name} (section: {section_name})"
                        )
                    elif match.is_official:
                        match.reason = match.reason or "Official effect without widget support"
                        report['unsupported'].append(match)
                        print(
                            f"🔍 DEBUG: Official effect unsupported: {match.display_name}"
                            f" (reason: {match.reason})"
                        )
                    else:
                        match.reason = match.reason or "Effect not present in official catalog"
                        report['unverified'].append(match)
                        print(
                            f"🔍 DEBUG: Unverified effect candidate: {match.display_name}"
                            f" (reason: {match.reason})"
                        )

            summary = {key: [m.display_name for m in value] for key, value in report.items()}
debug_logger.log(f"🔍 DEBUG: Identification report: {summary}")
            self.last_identified_effects = report
            return report

        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error identifying effects: {e}")
            self.last_identified_effects = {
                'official': [],
                'unsupported': [],
                'unverified': [],
                'duplicates': [],
            }
            return self.last_identified_effects

    def add_effect_to_cascade(self, effect_match: EffectMatch):
        """Add an effect widget to the cascade without replacing existing ones."""

debug_logger.log(f"🔍 DEBUG: Starting add_effect_to_cascade: {effect_match}")

        if not isinstance(effect_match, EffectMatch):
debug_logger.log(f"🔍 DEBUG: Invalid effect match provided to add_effect_to_cascade")
            return False, "Invalid effect description"

        try:
            display_name = effect_match.display_name

            if not effect_match.should_attempt_load():
                reason = effect_match.describe_failure() or "Unsupported effect"
debug_logger.log(f"🔍 DEBUG: Cannot load effect {display_name}: {reason}")
                return False, reason

            effect_type = effect_match.effect_type
            if effect_type is None and effect_match.canonical_name:
                effect_type = self.get_effect_type_for_name(effect_match.canonical_name)

            if effect_type is None:
                reason = effect_match.describe_failure() or "No widget available"
debug_logger.log(f"🔍 DEBUG: No widget available for {display_name}")
                return False, reason

debug_logger.log(f"🔍 DEBUG: Loading widget for type {effect_type} ({display_name})")
            effect_widget = self.load_effect_widget_by_type(effect_type)

            if effect_widget:
debug_logger.log(f"🔍 DEBUG: Successfully added {display_name} to cascade")
                self.current_effect_widget = effect_widget
                self.current_effect_type = effect_type
                return True, display_name

            reason = f"Widget load failed for {display_name}"
debug_logger.log(f"🔍 DEBUG: Failed to add {display_name} to cascade")
            return False, reason

        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error adding effect to cascade: {e}")
            return False, str(e)
    
    def get_last_effect_widget(self):
        """Get the last (most recently added) effect widget from the scrollable frame."""
        children = self.params_scrollable_frame.winfo_children()
        effect_widgets = [child for child in children if hasattr(child, 'set_all_parameters')]
        return effect_widgets[-1] if effect_widgets else None
    
    def load_effect_by_name(self, effect_name):
        """Load an effect by name."""
debug_logger.log(f"🔍 DEBUG: Starting load_effect_by_name: {effect_name}")
        
        try:
            # Map effect names to real Magicstomp effect types (from effect_registry.py)
            effect_type_mapping = {
                '3 Band Parametric EQ': 0x21,  # ThreeBandEQWidget
                'Mono Delay': 0x0D,       # MonoDelayWidget
                'Stereo Delay': 0x0E,     # StereoDelayWidget
                'Echo': 0x11,             # EchoWidget
                'Chorus': 0x12,           # ChorusWidget
                'Flange': 0x13,           # FlangeWidget
                'Phaser': 0x15,           # PhaserWidget
                'Amp Simulator': 0x08,    # AmpSimulatorWidget
                'Distortion': 0x2F,       # DistortionWidget
                'Reverb': 0x09,           # ReverbWidget
                'Gate Reverb': 0x0B,      # GateReverbWidget
                'Multi Filter': 0x2D,     # MultiFilterWidget
                'Dynamic Filter': 0x1E,   # DynamicFilterWidget
                'Mod. Delay': 0x0F,       # ModDelayWidget
                'Tremolo': 0x17,          # TremoloWidget
                'Spring Reverb': 0x22,    # SpringReverbWidget
                'HQ Pitch': 0x18,         # HQPitchWidget
                'Dual Pitch': 0x19        # DualPitchWidget
            }
            
            if effect_name in effect_type_mapping:
                effect_type = effect_type_mapping[effect_name]
debug_logger.log(f"🔍 DEBUG: Effect type for {effect_name}: {effect_type}")
                
                # Load the effect widget
                success = self.load_effect_widget_by_type(effect_type)
                if success:
debug_logger.log(f"🔍 DEBUG: Successfully loaded effect widget for {effect_name}")
                    return True
                else:
debug_logger.log(f"🔍 DEBUG: Failed to load effect widget for {effect_name}")
                    return False
            elif effect_name == 'Compressor':
                # Use real Compressor widget
debug_logger.log(f"🔍 DEBUG: Loading real Compressor widget")
                effect_type = 0x36  # CompressorWidget
                success = self.load_effect_widget_by_type(effect_type)
                if success:
debug_logger.log(f"🔍 DEBUG: Successfully loaded Compressor widget")
                    return True
                else:
debug_logger.log(f"🔍 DEBUG: Failed to load Compressor widget")
                    return False
            else:
debug_logger.log(f"🔍 DEBUG: Unknown effect name: {effect_name}")
                return False
                
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error loading effect by name: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_effect_widget_by_type(self, effect_type):
        """Load effect widget by type number."""
debug_logger.log(f"🔍 DEBUG: Starting load_effect_widget_by_type: {effect_type}")
        
        try:
            # Get effect widget from registry (using static class)
debug_logger.log(f"🔍 DEBUG: Using EffectRegistry static class")
            effect_class = EffectRegistry.create_effect_widget(effect_type, None)
debug_logger.log(f"🔍 DEBUG: Effect class for type {effect_type}: {effect_class}")
            
            if effect_class:
                # Create and load the effect widget
debug_logger.log(f"🔍 DEBUG: Creating effect widget with parent: {self.params_scrollable_frame}")
                effect_widget = EffectRegistry.create_effect_widget(effect_type, self.params_scrollable_frame)
                self.current_effect_type = effect_type
                
                # Debug widget properties
debug_logger.log(f"🔍 DEBUG: Widget created: {effect_widget}")
debug_logger.log(f"🔍 DEBUG: Widget type: {type(effect_widget)}")
                
                # Pack the widget in the scrollable frame
debug_logger.log(f"🔍 DEBUG: Packing widget in scrollable frame")
                effect_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
debug_logger.log(f"🔍 DEBUG: Widget packed successfully")
                
                # Force widget to update and show
debug_logger.log(f"🔍 DEBUG: Forcing widget update")
                effect_widget.update_idletasks()
                effect_widget.update()
debug_logger.log(f"🔍 DEBUG: Widget update completed")
                
                # Force grid layout update
debug_logger.log(f"🔍 DEBUG: Forcing grid layout update")
                effect_widget.grid_rowconfigure(0, weight=1)
                effect_widget.grid_columnconfigure(0, weight=1)
                effect_widget.grid_propagate(True)
debug_logger.log(f"🔍 DEBUG: Grid layout update completed")
debug_logger.log(f"🔍 DEBUG: Widget methods: {dir(effect_widget)}")
                
                # Check if widget has required methods
                if hasattr(effect_widget, 'set_all_parameters'):
debug_logger.log(f"🔍 DEBUG: Widget has set_all_parameters method")
                else:
debug_logger.log(f"🔍 DEBUG: Widget MISSING set_all_parameters method")
                
                if hasattr(effect_widget, 'get_all_parameters'):
debug_logger.log(f"🔍 DEBUG: Widget has get_all_parameters method")
                else:
debug_logger.log(f"🔍 DEBUG: Widget MISSING get_all_parameters method")
                
                # Update UI
                if hasattr(self, 'current_effect_var'):
                    effect_name = EffectRegistry.get_effect_name(effect_type)
                    display_name = self.get_display_name_for_effect(effect_name)
                    self.current_effect_var.set(f"Loaded: {display_name}")
debug_logger.log(f"🔍 DEBUG: Updated current_effect_var to: Loaded: {display_name}")
                else:
debug_logger.log(f"🔍 DEBUG: No current_effect_var found")
                
                # Check patch builder frame
debug_logger.log(f"🔍 DEBUG: Patch builder frame: {self.patch_builder_frame}")
debug_logger.log(f"🔍 DEBUG: Params scrollable frame: {self.params_scrollable_frame}")
debug_logger.log(f"🔍 DEBUG: Params scrollable frame children: {self.params_scrollable_frame.winfo_children()}")
                
                # Check if widget is visible
                if effect_widget:
debug_logger.log(f"🔍 DEBUG: Widget visible: {effect_widget.winfo_viewable()}")
debug_logger.log(f"🔍 DEBUG: Widget mapped: {effect_widget.winfo_ismapped()}")
debug_logger.log(f"🔍 DEBUG: Widget geometry: {effect_widget.winfo_geometry()}")
debug_logger.log(f"🔍 DEBUG: Widget size: {effect_widget.winfo_reqwidth()}x{effect_widget.winfo_reqheight()}")
debug_logger.log(f"🔍 DEBUG: Widget children: {effect_widget.winfo_children()}")
debug_logger.log(f"🔍 DEBUG: Widget children count: {len(effect_widget.winfo_children())}")
                
                # Add widget to cascade
                self.effect_widget_cascade.append(effect_widget)
debug_logger.log(f"🔍 DEBUG: Added widget to cascade. Cascade size: {len(self.effect_widget_cascade)}")
                
debug_logger.log(f"🔍 DEBUG: Successfully loaded effect widget type {effect_type}")
debug_logger.log(f"🔍 DEBUG: Created effect widget: {effect_widget}")
                return effect_widget
            else:
debug_logger.log(f"🔍 DEBUG: Effect class not found for type {effect_type}")
debug_logger.log(f"🔍 DEBUG: Available effects in registry: {list(EffectRegistry.EFFECT_WIDGETS.keys())}")
                return False
                
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error loading effect widget by type: {e}")
            import traceback
            traceback.print_exc()
            return False
    
