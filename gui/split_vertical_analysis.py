"""Analysis, patch generation and file interaction helpers."""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import List, Tuple

import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from magicstomp_effects import EffectRegistry
from realtime_magicstomp import RealtimeMagicstomp

from gui.impact_visualization import ImpactLevel, ParameterImpact
from gui.split_vertical_shared import EffectMatch


class SplitVerticalGUIAnalysisMixin:
    """Analysis, patch generation and file interaction helpers."""

    def select_target_file(self):
        """Select target audio file."""
        file_path = filedialog.askopenfilename(
            title="Select Target Audio File",
            filetypes=[("Audio files", "*.wav *.mp3 *.flac *.m4a"),
                      ("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if file_path:
            self.target_file = file_path
            filename = Path(file_path).name
            if len(filename) > 40:
                filename = filename[:37] + "..."
            self.target_var.set(filename)
            self.log_status(f"📁 Target: {Path(file_path).name}")
            self.update_status_info()
            
            # Save the selection automatically
            self.save_last_file_selections()
    
    def select_di_file(self):
        """Select DI audio file."""
        file_path = filedialog.askopenfilename(
            title="Select DI Audio File",
            filetypes=[("Audio files", "*.wav *.mp3 *.flac *.m4a"),
                      ("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if file_path:
            self.di_file = file_path
            filename = Path(file_path).name
            if len(filename) > 40:
                filename = filename[:37] + "..."
            self.di_var.set(filename)
            self.log_status(f"📁 DI: {Path(file_path).name}")
            self.update_status_info()
            
            # Save the selection automatically
            self.save_last_file_selections()
    
    def load_effect_widget(self):
        """Load selected effect widget."""
        selection = self.effect_combo.get()
        if not selection:
            self.log_status("⚠️ Select an effect")
            return
        
        try:
            effect_type_hex = selection.split('(0x')[1].split(')')[0]
            effect_type = int(effect_type_hex, 16)
        except (ValueError, IndexError):
            self.log_status("❌ Invalid effect")
            return
        
        # Clear current widget
        if self.current_effect_widget:
            self.current_effect_widget.destroy()
        
        # Create new widget
        self.current_effect_widget = EffectRegistry.create_effect_widget(
            effect_type, self.params_scrollable_frame)
        
        if self.current_effect_widget:
            self.current_effect_widget.pack(fill=tk.X, padx=5, pady=5)
            
            self.setup_parameter_callbacks()
            self.impact_visualizer.set_effect_widget(self.current_effect_widget)
            
            self.current_effect_type = effect_type
            self.original_parameters = self.current_effect_widget.get_all_parameters()
            
            effect_name = EffectRegistry.get_effect_name(effect_type)
            display_name = self.get_display_name_for_effect(effect_name)
            self.log_status(f"🎛️ Loaded: {display_name}")
            self.update_status_info()
        else:
            self.log_status(f"❌ Effect 0x{effect_type:02X} not supported")
    
    def setup_parameter_callbacks(self):
        """Setup parameter callbacks."""
        if not self.current_effect_widget:
            return
        
        def parameter_changed(param_name, user_value, magicstomp_value):
            self.on_parameter_changed(param_name, user_value, magicstomp_value)
        
        for child in self.current_effect_widget.winfo_children():
            if hasattr(child, 'param_name'):
                self.current_effect_widget.set_parameter_callback(
                    child.param_name, parameter_changed)
    
    def download_current_patch(self):
        """Download current patch from Magicstomp and display it."""
        from debug_logger import debug_logger
        debug_logger.log("🔍 DEBUG: download_current_patch called")
        
        if self.realtime_magicstomp is None:
            try:
                self.realtime_magicstomp = RealtimeMagicstomp()
            except Exception as exc:
                self.log_status(f"❌ MIDI init error: {exc}")
                messagebox.showerror("Magicstomp", f"Failed to initialize MIDI connection:\n{exc}")
                return

        # Clear existing effect widgets before loading new patch
        if hasattr(self, 'effects_panel') and self.effects_panel:
            debug_logger.log("🔍 DEBUG: Clearing existing effect widgets before download")
            self.effects_panel.clear_effect_widgets()

        self.log_status("📥 Requesting current patch from Magicstomp...")
        patch_data = self.realtime_magicstomp.request_patch()

        if not patch_data:
            self.log_status("❌ Failed to download patch from Magicstomp")
            messagebox.showerror("Magicstomp", "Unable to download current patch. Check MIDI connection.")
            return

        common_section = patch_data.get('common')
        effect_section = patch_data.get('effect')
        if not common_section or not effect_section:
            self.log_status("❌ Invalid patch payload received")
            messagebox.showerror("Magicstomp", "Invalid patch data received from Magicstomp.")
            return

        # L'ID de l'effet est à l'octet 1 dans la structure SYSEX du Magicstomp (comme MagicstompFrenzy)
        effect_type = common_section[1] if len(common_section) > 1 else common_section[0]
        effect_name = EffectRegistry.get_effect_name(effect_type)
        
        # Debug: Afficher les informations sur l'effet détecté
debug_logger.log(f"🔍 DEBUG: Effect type detected: 0x{effect_type:02X} ({effect_type})")
debug_logger.log(f"🔍 DEBUG: Effect name: {effect_name}")
        self.log_status(f"🎛️ Effect detected: {effect_name} (0x{effect_type:02X})")

        if not EffectRegistry.is_effect_supported(effect_type):
            self.log_status(f"⚠️ Effect {effect_name} not supported in editor")
debug_logger.log(f"🔍 DEBUG: Effect {effect_name} not supported in editor")
            messagebox.showwarning("Magicstomp", f"Effect {effect_name} (0x{effect_type:02X}) is not supported in the editor.")
            return

        # Clear current widget
        if self.current_effect_widget:
            self.current_effect_widget.destroy()

        # Create new widget
        self.current_effect_widget = EffectRegistry.create_effect_widget(
            effect_type, self.params_scrollable_frame)
        
        if not self.current_effect_widget:
            self.log_status(f"❌ Effect widget for {effect_name} not available")
            messagebox.showerror("Magicstomp", f"Unable to load widget for effect {effect_name}.")
            return
        
        # Store the main widget before cascade creation changes current_effect_widget
        main_effect_widget = self.current_effect_widget
        debug_logger.log(f"🔍 DEBUG: Main effect widget stored: {main_effect_widget}")
        debug_logger.log(f"🔍 DEBUG: Main effect widget type: {type(main_effect_widget)}")

        # Apply parameters from Magicstomp data to main widget
        applied_params = {}
        debug_logger.log(f"🔍 DEBUG: About to apply Magicstomp data to main effect widget...")
        debug_logger.log(f"🔍 DEBUG: Main effect widget: {main_effect_widget}")
        debug_logger.log(f"🔍 DEBUG: Main effect widget type: {type(main_effect_widget)}")
        debug_logger.log(f"🔍 DEBUG: Has apply_magicstomp_data: {hasattr(main_effect_widget, 'apply_magicstomp_data')}")
        
        if hasattr(main_effect_widget, 'apply_magicstomp_data'):
            debug_logger.log(f"🔍 DEBUG: Applying Magicstomp data to main effect widget...")
            debug_logger.log_sysex_data(effect_section, "Effect section data")
            applied_params = main_effect_widget.apply_magicstomp_data(effect_section)
            debug_logger.log(f"🔍 DEBUG: Applied parameters to main widget: {applied_params}")
            self.log_status(f"📊 Parameters applied to main widget: {len(applied_params)} parameters")
        else:
            debug_logger.log(f"🔍 DEBUG: Main effect widget doesn't support apply_magicstomp_data")
            self.log_status("⚠️ Main effect widget doesn't support parameter application")
        
        # Apply parameters to all widgets in the cascade
        if hasattr(self, 'effect_widget_cascade') and self.effect_widget_cascade:
            debug_logger.log(f"🔍 DEBUG: Applying Magicstomp data to all {len(self.effect_widget_cascade)} widgets in cascade...")
            total_applied = 0
            for i, widget in enumerate(self.effect_widget_cascade):
                if hasattr(widget, 'apply_magicstomp_data'):
                    try:
                        widget_applied = widget.apply_magicstomp_data(effect_section)
                        widget_name = widget.__class__.__name__
                        debug_logger.log(f"🔍 DEBUG: Applied {len(widget_applied)} parameters to {widget_name} widget")
                        total_applied += len(widget_applied)
                    except Exception as e:
                        debug_logger.log(f"🔍 DEBUG: Error applying data to widget {i}: {e}")
                else:
                    debug_logger.log(f"🔍 DEBUG: Widget {i} doesn't support apply_magicstomp_data")
            
            if total_applied > 0:
                self.log_status(f"📊 Total parameters applied to cascade: {total_applied} parameters")
            else:
                self.log_status("⚠️ No parameters applied to cascade widgets")
        
        # For composite effects like "Distortion Multi (Flange)", create additional widgets
        if effect_type == 0x3C:  # Distortion Multi (Flange)
debug_logger.log(f"🔍 DEBUG: Detected composite effect - creating additional widgets")
            self._create_composite_effect_widgets(effect_section)

        # Pack the widget
        self.current_effect_widget.pack(fill=tk.X, padx=5, pady=5)
        
        # Setup callbacks and visualization
        self.setup_parameter_callbacks()
        self.impact_visualizer.set_effect_widget(self.current_effect_widget)
        
        # Store parameters
        self.current_effect_type = effect_type
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        self.original_parameters = self.current_parameters.copy()

        # Extract patch name
        patch_name = self._extract_patch_name(common_section)
        
        # Update current patch
        self.current_patch = {
            'patch_index': patch_data.get('patch_index'),
            'effect_type': effect_type,
            'effect_name': effect_name,
            'patch_name': patch_name,
            'parameters': self.current_parameters,
            'common': common_section,
            'effect_bytes': effect_section,
        }

        # Update effect selection in combo
        self._select_effect_in_combo(effect_name, effect_type)

        # Update status
        display_name = self.get_display_name_for_effect(effect_name)
        self.log_status(f"✅ Patch downloaded: {patch_name} ({display_name})")
        if applied_params:
            self.log_status(f"🎚️ Parameters applied: {len(applied_params)} values")
        else:
            self.log_status("ℹ️ Patch applied with default parameter mapping")
        
        self.update_status_info()
        messagebox.showinfo("Magicstomp", f"Patch '{patch_name}' downloaded from Magicstomp.")
    
    def _extract_patch_name(self, common_section):
        """Extract patch name from common section data."""
        if len(common_section) < 16:
            return "Magicstomp Patch"
        
        # Patch name is at offset 16, 12 characters long
        name_bytes = common_section[16:28]
        
        try:
            # Try to decode as ASCII
            name = ''.join(chr(b) for b in name_bytes if 32 <= b <= 126).strip()
            if name:
                return name
        except Exception:
            pass
        
        # Fallback: try to decode as best as possible
        try:
            name = ''.join(chr(b) for b in name_bytes if 32 <= b <= 126).strip()
        except Exception:
            name = ''.join(chr(b) for b in name_bytes if 32 <= b <= 126).strip()

        return name or "Magicstomp Patch"
    
    def _select_effect_in_combo(self, effect_name, effect_type):
        """Select the effect in the combo box."""
        try:
            # Find the matching item in the combo
            combo_values = list(self.effect_combo['values'])
            for item in combo_values:
                if f"{effect_name} (0x{effect_type:02X})" in item:
                    self.effect_combo.set(item)
                    break
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error selecting effect in combo: {e}")
    
    def find_sysex_offset(self, param_name: str, effect_type: str) -> int:
        """Find Sysex offset for a parameter based on effect type and parameter name."""
        # Create mapping based on effect type and parameter name
        effect_param_mapping = {
            # Compressor parameters
            'threshold': 4,
            'ratio': 34,
            'attack': 35,
            'release': 36,
            'knee': 37,
            'gain': 38,
            'makeup_gain': 38,
            
            # EQ parameters
            'eq1_gain': 36,  # Treble
            'eq1_freq': 36,
            'eq2_gain': 37,  # High Middle
            'eq2_freq': 37,
            'eq3_gain': 38,  # Low Middle
            'eq3_freq': 38,
            'bass': 39,
            
            # Delay parameters
            'time': 74,  # DelayTapL
            'feedback': 76,  # DelayFeedbackGain
            'mix': 78,  # DelayLevel
            'low_cut': 82,  # DelayHPF
            'high_cut': 83,  # DelayLPF
            
            # Modulation parameters
            'wave': 25,  # ModWave
            'freq': 63,  # ModSpeed
            'speed': 63,
            'depth': 64,  # ModDepth
            'level': 65,  # ChorusLevel
            
            # Reverb parameters
            'reverb_time': 85,  # ReverbTime
            'high_ratio': 86,  # ReverbHighRatio
            'diffusion': 87,  # ReverbDiffusion
            'density': 88,  # ReverbDensity
            'mix': 89,  # ReverbLevel
        }
        
        # Convert parameter name to lowercase for matching
        param_lower = param_name.lower().replace(' ', '_').replace('.', '_')
        
        # Try exact match first
        if param_lower in effect_param_mapping:
            return effect_param_mapping[param_lower]
        
        # Try partial matches
        for key, offset in effect_param_mapping.items():
            if key in param_lower or param_lower in key:
                return offset
        
        return None
    
    def on_parameter_changed(self, param_name: str, user_value, magicstomp_value: int):
        """Handle parameter changes."""
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        
        # Send Sysex message to Magicstomp if connected
        if hasattr(self, 'realtime_magicstomp') and self.realtime_magicstomp.output_port:
            # Try to find the offset for this parameter
            offset = self.find_sysex_offset(param_name, self.current_effect_type)
            if offset is not None:
                try:
                    # Convert magicstomp_value to 0-127 range if needed
                    sysex_value = int(magicstomp_value) & 0x7F  # Ensure 7-bit value
                    self.realtime_magicstomp.tweak_parameter(offset, sysex_value)
                    self.log_status(f"🎛️ {param_name}: {user_value} → Sysex offset {offset} = {sysex_value}")
                except Exception as e:
                    self.log_status(f"❌ Error sending Sysex for {param_name}: {e}")
            else:
                self.log_status(f"⚠️ No Sysex mapping found for parameter: {param_name}")
        else:
            self.log_status(f"🎛️ {param_name}: {user_value} (MIDI not connected)")
        
        if self.target_parameters:
            self.update_impact_visualization()
    
    def init_midi_connection(self):
        """Initialize MIDI connection to Magicstomp."""
        try:
            # Try to connect to Magicstomp
            self.realtime_magicstomp.connect()
            if self.realtime_magicstomp.output_port:
                self.log_status("✅ MIDI connection to Magicstomp established")
            else:
                self.log_status("⚠️ MIDI connection failed - no output port found")
        except Exception as e:
            self.log_status(f"❌ Error initializing MIDI connection: {e}")
    
    def analyze_current_parameters(self):
        """Analyze current parameters."""
        if not self.current_effect_widget:
            self.log_status("⚠️ No effect loaded")
            return
        
        current_params = self.current_effect_widget.get_all_parameters()
        
        target_impacts = {}
        for param_name, value in current_params.items():
            impact = ParameterImpact(
                name=param_name, original_value=value, target_value=value,
                current_value=value, impact_level=ImpactLevel.NONE,
                unit=self.get_parameter_unit(param_name))
            target_impacts[param_name] = impact
        
        self.impact_visualizer.impacts = target_impacts
        self.impact_visualizer._update_visualization()
        
        self.log_status(f"📊 Analyzed {len(current_params)} parameters")
    
    def generate_target_parameters(self):
        """Generate target parameters."""
        if not self.current_effect_widget:
            self.log_status("⚠️ No effect loaded")
            return
        
        current_params = self.current_effect_widget.get_all_parameters()
        target_params = self.generate_smart_target_parameters(current_params)
        
        self.target_parameters = target_params
        self.update_impact_visualization()
        
        self.log_status(f"🎯 Generated {len(target_params)} targets")
    
    def generate_smart_target_parameters(self, current_params: dict) -> dict:
        """Generate smart target parameters."""
        target_params = {}
        
        if self.current_effect_type == 0x0D:  # Mono Delay
            target_params = {
                "Time": current_params.get("Time", 100) * 1.5,
                "Mix": min(100, current_params.get("Mix", 50) + 20),
                "FB Gain": min(99, current_params.get("FB Gain", 30) + 15)
            }
        elif self.current_effect_type == 0x12:  # Chorus
            target_params = {
                "Rate": current_params.get("Rate", 1.0) * 2.0,
                "Depth": min(100, current_params.get("Depth", 50) + 30),
                "Mix": min(100, current_params.get("Mix", 50) + 25)
            }
        elif self.current_effect_type == 0x09:  # Reverb
            target_params = {
                "Time": current_params.get("Time", 1.0) * 2.0,
                "Mix": min(100, current_params.get("Mix", 50) + 30),
                "High Ratio": min(1.0, current_params.get("High Ratio", 0.5) + 0.2)
            }
        else:
            # Generic generation
            for param_name, value in current_params.items():
                if isinstance(value, (int, float)):
                    variation = np.random.uniform(0.8, 1.3)
                    target_params[param_name] = value * variation
        
        # Apply limits
        for param_name, value in target_params.items():
            target_params[param_name] = self.apply_parameter_limits(param_name, value)
        
        return target_params
    
    def apply_parameter_limits(self, param_name: str, value: float) -> float:
        """Apply parameter limits."""
        limits = {
            "Time": (0.1, 2730.0), "Mix": (0, 100), "Rate": (0.1, 20.0),
            "Depth": (0, 100), "Feedback": (0, 99), "FB Gain": (0, 99),
            "Gain": (-12, 12), "Level": (0, 100), "Frequency": (20, 20000),
            "High Ratio": (0.1, 1.0), "Low Ratio": (0.1, 1.0)
        }
        
        min_val, max_val = limits.get(param_name, (0, 100))
        return max(min_val, min(max_val, value))
    
    def update_impact_visualization(self):
        """Update impact visualization."""
        if not self.target_parameters or not self.current_effect_widget:
            return
        
        current_params = self.current_effect_widget.get_all_parameters()
        
        impacts = {}
        for param_name, target_value in self.target_parameters.items():
            original_value = self.original_parameters.get(param_name, 0)
            current_value = current_params.get(param_name, original_value)
            
            impact_level = self.calculate_impact_level(original_value, target_value)
            
            impact = ParameterImpact(
                name=param_name, original_value=original_value,
                target_value=target_value, current_value=current_value,
                impact_level=impact_level, unit=self.get_parameter_unit(param_name))
            
            impacts[param_name] = impact
        
        self.impact_visualizer.impacts = impacts
        self.impact_visualizer._update_visualization()
    
    def calculate_impact_level(self, original: float, target: float) -> ImpactLevel:
        """Calculate impact level."""
        if original == 0:
            diff_percent = abs(target) * 100 if target != 0 else 0
        else:
            diff_percent = abs((target - original) / original) * 100
        
        if diff_percent < 5: return ImpactLevel.NONE
        elif diff_percent < 15: return ImpactLevel.LOW
        elif diff_percent < 30: return ImpactLevel.MEDIUM
        elif diff_percent < 50: return ImpactLevel.HIGH
        else: return ImpactLevel.CRITICAL
    
    def get_parameter_unit(self, param_name: str) -> str:
        """Get parameter unit."""
        units = {
            "Time": "ms", "Rate": "Hz", "Mix": "%", "Depth": "%",
            "Feedback": "%", "Gain": "dB", "Level": "%", "Frequency": "Hz",
            "Q": "", "Attack": "ms", "Release": "ms", "FB Gain": "%",
            "High Ratio": "", "Low Ratio": ""
        }
        return units.get(param_name, "")
    
    def apply_changes(self):
        """Apply target parameters."""
        if not self.target_parameters or not self.current_effect_widget:
            self.log_status("⚠️ No targets to apply")
            return
        
        self.current_effect_widget.set_all_parameters(self.target_parameters)
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        self.update_impact_visualization()
        
        self.log_status("✅ Applied targets")
    
    def reset_to_original(self):
        """Reset to original parameters."""
        if not self.original_parameters or not self.current_effect_widget:
            self.log_status("⚠️ No originals to reset")
            return
        
        self.current_effect_widget.set_all_parameters(self.original_parameters)
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        self.target_parameters.clear()
        self.impact_visualizer._reset_analysis()
        
        self.log_status("🔄 Reset to original")
    
    def analyze_target_audio(self):
        """Analyze target audio file using AutoToneMatcher."""
        if not self.target_file:
            self.log_status("⚠️ No target file selected")
debug_logger.log(f"🔍 DEBUG: No target file selected")
            return
        
        def analyze_thread():
            try:
                self.log_status("📊 Starting target audio analysis...")
debug_logger.log(f"🔍 DEBUG: Starting analyze_target_audio()")
debug_logger.log(f"🔍 DEBUG: Target file: {self.target_file}")
                
                # Try to use AutoToneMatcher for real analysis
                try:
                    self.log_status("🔧 Creating tone matcher...")
debug_logger.log(f"🔍 DEBUG: Creating AutoToneMatcher...")
                    
                    from auto_tone_match_magicstomp import AutoToneMatcher
                    tone_matcher = AutoToneMatcher('essentia')  # Use essentia backend
debug_logger.log(f"🔍 DEBUG: AutoToneMatcher created successfully")
                    self.log_status("✅ Tone matcher created")
                    
                    # Analyze audio with detailed debug
                    self.log_status("🎵 Analyzing audio features...")
debug_logger.log(f"🔍 DEBUG: Calling tone_matcher.analyze_audio()...")
                    
                    features = tone_matcher.analyze_audio(self.target_file, verbose=True)
debug_logger.log(f"🔍 DEBUG: Analysis features: {features}")
                    self.log_status("✅ Audio features extracted")
                    
                    # Map to patch with debug
                    self.log_status("🎛️ Mapping features to patch...")
debug_logger.log(f"🔍 DEBUG: Calling tone_matcher.map_to_patch()...")
                    
                    patch = tone_matcher.map_to_patch()
debug_logger.log(f"🔍 DEBUG: Generated patch: {patch}")
                    self.log_status("✅ Patch generated from analysis")
                    
                    # Store results
                    self.current_patch = patch
                    self.analysis_data['target'] = {
                        'file': str(self.target_file),
                        'features': features,
                        'patch': patch,
                        'file_path': self.target_file
                    }
                    
                    # Display patch in GUI
                    self.root.after(0, self.display_patch_parameters)
                    self.root.after(0, lambda: self.log_status("✅ Target analysis completed - patch generated"))
                    
                    # Auto-load effects from generated patch first
                    self.root.after(50, self.auto_load_effects_from_patch)
                    
                    # Then auto-generate patch proposal if effect is loaded
                    if self.current_effect_widget:
                        self.root.after(100, self.auto_generate_patch_proposal)
                    
                except Exception as e:
debug_logger.log(f"🔍 DEBUG: AutoToneMatcher error: {e}")
                    import traceback
                    traceback.print_exc()
                    self.log_status(f"⚠️ Using fallback analysis: {e}")
                    
                    # Fallback to basic analysis
                    self.log_status("📊 Running fallback analysis...")
debug_logger.log(f"🔍 DEBUG: Running fallback analysis...")
                    
                    # Load audio file
                    audio_data, sample_rate = sf.read(self.target_file)
                    
                    # Basic analysis
                    duration = len(audio_data) / sample_rate
                    channels = audio_data.shape[1] if len(audio_data.shape) > 1 else 1
                    max_amplitude = np.max(np.abs(audio_data))
                    rms_level = np.sqrt(np.mean(audio_data**2))
                    
                    # Frequency analysis
                    if channels == 1:
                        fft = np.fft.fft(audio_data)
                        freqs = np.fft.fftfreq(len(audio_data), 1/sample_rate)
                        magnitude = np.abs(fft)
                        
                        # Find peak frequency
                        peak_freq_idx = np.argmax(magnitude[:len(magnitude)//2])
                        peak_frequency = freqs[peak_freq_idx]
                    else:
                        peak_frequency = "Multi-channel"
                    
                    # Display results
                    results = f"""Target Audio Analysis (Fallback):
Duration: {duration:.2f}s
Sample Rate: {sample_rate} Hz
Channels: {channels}
Max Amplitude: {max_amplitude:.4f}
RMS Level: {rms_level:.4f}
Peak Frequency: {peak_frequency} Hz
File: {Path(self.target_file).name}"""
                    
                    # Store analysis data
                    self.analysis_data['target'] = {
                        'duration': duration,
                        'sample_rate': sample_rate,
                        'channels': channels,
                        'max_amplitude': max_amplitude,
                        'rms_level': rms_level,
                        'peak_frequency': peak_frequency,
                        'file_path': self.target_file
                    }
                    
debug_logger.log(f"🔍 DEBUG: Fallback analysis completed: {self.analysis_data['target']}")
                    self.root.after(0, lambda: self.display_analysis_results(results))
                    self.root.after(0, lambda: self.log_status("✅ Fallback analysis completed"))
                    
                    # Generate basic patch from fallback analysis
                    self.root.after(0, self.generate_basic_patch_from_fallback)
                    
                    # Auto-load effects from generated patch first
                    self.root.after(50, self.auto_load_effects_from_patch)
                    
                    # Then auto-generate patch proposal if effect is loaded
                    if self.current_effect_widget:
                        self.root.after(100, self.auto_generate_patch_proposal)
                
            except Exception as e:
debug_logger.log(f"🔍 DEBUG: Fatal error in analyze_thread: {e}")
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: self.log_status(f"❌ Analysis error: {e}"))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def generate_basic_patch_from_fallback(self):
        """Generate basic patch from fallback analysis data."""
debug_logger.log(f"🔍 DEBUG: Starting generate_basic_patch_from_fallback()")
        
        if 'target' not in self.analysis_data:
debug_logger.log(f"🔍 DEBUG: No target analysis data for basic patch generation")
            return
        
        try:
            target_data = self.analysis_data['target']
debug_logger.log(f"🔍 DEBUG: Target data for basic patch: {target_data}")
            
            # Create a basic patch structure based on analysis
            duration = target_data.get('duration', 1.0)
            rms_level = target_data.get('rms_level', 0.5)
            max_amplitude = target_data.get('max_amplitude', 1.0)
            
            # Generate basic patch parameters
            basic_patch = {
                'meta': {
                    'name': f'Basic Patch - {Path(self.target_file).stem}',
                    'created_from': 'fallback_analysis',
                    'target_file': str(self.target_file)
                },
                'compressor': {
                    'enabled': True,
                    'threshold': max(0.1, min(0.9, 1.0 - rms_level * 2)),
                    'ratio': 4.0 if rms_level > 0.3 else 2.0,
                    'attack': 10.0,
                    'release': 100.0,
                    'makeup_gain': max(0, (0.5 - rms_level) * 10)
                },
                'eq': {
                    'enabled': True,
                    'low_gain': 0.0,
                    'mid_gain': 2.0 if rms_level < 0.2 else 0.0,
                    'high_gain': 1.0 if rms_level > 0.5 else 0.0,
                    'low_freq': 100.0,
                    'mid_freq': 1000.0,
                    'high_freq': 5000.0
                },
                'delay': {
                    'enabled': duration > 2.0,  # Only enable delay for longer files
                    'time': min(500, duration * 100),  # Scale delay time with duration
                    'feedback': 0.3,
                    'mix': 0.2,
                    'low_cut': 100.0,
                    'high_cut': 8000.0
                }
            }
            
            self.current_patch = basic_patch
debug_logger.log(f"🔍 DEBUG: Generated basic patch: {basic_patch}")
            
            # Display patch parameters
            self.display_patch_parameters()
            
            self.log_status("✅ Basic patch generated from fallback analysis")
            
            # Save the target file used for this patch
            self.save_last_file_selections()
            
            # Save state after generating patch
            self.save_settings()
            
            # Try to apply patch to current effect widget if available
            if self.current_effect_widget and hasattr(self.current_effect_widget, 'set_all_parameters'):
                try:
debug_logger.log(f"🔍 DEBUG: Applying basic patch to current effect widget...")
                    
                    # Convert patch to widget parameters
                    widget_params = self.convert_patch_to_widget_params(basic_patch)
debug_logger.log(f"🔍 DEBUG: Converted widget params: {widget_params}")
                    
                    if widget_params:
                        # Apply parameters to effect widget
                        self.current_effect_widget.set_all_parameters(widget_params)
                        self.current_parameters = widget_params
                        
                        # Store as target parameters for impact visualization
                        self.target_parameters = widget_params.copy()
                        
                        # Update impact visualization
                        if self.impact_visualizer:
debug_logger.log(f"🔍 DEBUG: Updating impact visualization with basic patch...")
                            self.update_impact_visualization()
                        
                        self.log_status("🎛️ Basic patch applied to current effect!")
                        self.log_status("💡 Go to Analysis tab to see the parameter impacts!")
debug_logger.log(f"🔍 DEBUG: Basic patch successfully applied to effect widget")
                    else:
                        self.log_status("⚠️ Could not convert patch to widget parameters")
                        self.log_status("💡 Load an effect in Effects tab to apply parameters")
                        
                except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error applying basic patch to effect: {e}")
                    import traceback
                    traceback.print_exc()
                    self.log_status(f"⚠️ Error applying patch to effect: {e}")
                    self.log_status("💡 Load an effect in Effects tab to apply parameters")
            else:
                self.log_status("💡 Load an effect in Effects tab to apply parameters")
debug_logger.log(f"🔍 DEBUG: No effect widget loaded - patch ready for manual application")
            
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error generating basic patch: {e}")
            import traceback
            traceback.print_exc()
            self.log_status(f"❌ Error generating basic patch: {e}")
    
    def display_patch_parameters(self):
        """Display patch parameters in the GUI."""
        if not self.current_patch:
            self.log_status("⚠️ No patch to display")
debug_logger.log(f"🔍 DEBUG: No patch to display")
            return
        
        try:
            self.log_status("🎛️ Displaying patch parameters...")
debug_logger.log(f"🔍 DEBUG: Displaying patch parameters...")
debug_logger.log(f"🔍 DEBUG: Patch data: {self.current_patch}")
            
            # Clear existing widgets
            if hasattr(self, 'patch_display_frame'):
                for widget in self.patch_display_frame.winfo_children():
                    widget.destroy()
                # Recreate scrollable components
                self.patch_canvas = tk.Canvas(self.patch_display_frame, height=300)
                self.patch_scrollbar = ttk.Scrollbar(self.patch_display_frame, orient="vertical", command=self.patch_canvas.yview)
                self.patch_scrollable_frame = ttk.Frame(self.patch_canvas)
                
                # Configure scrolling
                self.patch_scrollable_frame.bind(
                    "<Configure>",
                    lambda e: self.patch_canvas.configure(scrollregion=self.patch_canvas.bbox("all"))
                )
                
                self.patch_canvas.create_window((0, 0), window=self.patch_scrollable_frame, anchor="nw")
                self.patch_canvas.configure(yscrollcommand=self.patch_scrollbar.set)
                
                # Pack canvas and scrollbar
                self.patch_canvas.pack(side="left", fill="both", expand=True)
                self.patch_scrollbar.pack(side="right", fill="y")
            else:
                # Create frame if it doesn't exist
                self.patch_display_frame = ttk.LabelFrame(self.files_frame, 
                                                        text="🎛️ Generated Patch Parameters",
                                                        padding=10)
                self.patch_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # Create scrollable canvas for patch parameters
                self.patch_canvas = tk.Canvas(self.patch_display_frame, height=300)
                self.patch_scrollbar = ttk.Scrollbar(self.patch_display_frame, orient="vertical", command=self.patch_canvas.yview)
                self.patch_scrollable_frame = ttk.Frame(self.patch_canvas)
                
                # Configure scrolling
                self.patch_scrollable_frame.bind(
                    "<Configure>",
                    lambda e: self.patch_canvas.configure(scrollregion=self.patch_canvas.bbox("all"))
                )
                
                self.patch_canvas.create_window((0, 0), window=self.patch_scrollable_frame, anchor="nw")
                self.patch_canvas.configure(yscrollcommand=self.patch_scrollbar.set)
                
                # Pack canvas and scrollbar
                self.patch_canvas.pack(side="left", fill="both", expand=True)
                self.patch_scrollbar.pack(side="right", fill="y")
            
            # Display patch parameters in scrollable frame
            row = 0
            for section_name, section_data in self.current_patch.items():
                if isinstance(section_data, dict) and section_name != 'meta':
                    # Section header
                    ttk.Label(self.patch_scrollable_frame,
                             text=f"{section_name.upper()}:",
                             style='Section.TLabel').grid(row=row, column=0, columnspan=2, sticky='w', pady=(10, 5))
                    row += 1
                    
                    # Parameters in this section
                    for param_name, param_value in section_data.items():
                        if param_name != 'enabled':
                            ttk.Label(self.patch_scrollable_frame,
                                     text=f"  {param_name}:",
                                     style='Info.TLabel').grid(row=row, column=0, sticky='w', padx=20)
                            
                            value_text = f"{param_value:.4f}" if isinstance(param_value, (int, float)) else str(param_value)
                            ttk.Label(self.patch_scrollable_frame,
                                     text=value_text,
                                     style='Info.TLabel').grid(row=row, column=1, sticky='w', padx=10)
                            row += 1
            
            # Update scroll region after adding all widgets
            self.patch_scrollable_frame.update_idletasks()
            self.patch_canvas.configure(scrollregion=self.patch_canvas.bbox("all"))
            
            self.log_status("✅ Patch parameters displayed")
debug_logger.log(f"🔍 DEBUG: Patch parameters displayed successfully")
            
        except Exception as e:
            self.log_status(f"❌ Error displaying patch: {e}")
debug_logger.log(f"🔍 DEBUG: Error displaying patch: {e}")
            import traceback
            traceback.print_exc()
    
    def analyze_di_audio(self):
        """Analyze DI audio file."""
        if not self.di_file:
            self.log_status("⚠️ No DI file selected")
            return
        
        self.log_status("📊 Analyzing DI audio...")
        
        def analyze_thread():
            try:
                # Load audio file
                audio_data, sample_rate = sf.read(self.di_file)
                
                # Basic analysis
                duration = len(audio_data) / sample_rate
                channels = audio_data.shape[1] if len(audio_data.shape) > 1 else 1
                max_amplitude = np.max(np.abs(audio_data))
                rms_level = np.sqrt(np.mean(audio_data**2))
                
                # Frequency analysis
                if channels == 1:
                    fft = np.fft.fft(audio_data)
                    freqs = np.fft.fftfreq(len(audio_data), 1/sample_rate)
                    magnitude = np.abs(fft)
                    
                    # Find peak frequency
                    peak_freq_idx = np.argmax(magnitude[:len(magnitude)//2])
                    peak_frequency = freqs[peak_freq_idx]
                else:
                    peak_frequency = "Multi-channel"
                
                # Display results
                results = f"""DI Audio Analysis:
Duration: {duration:.2f}s
Sample Rate: {sample_rate} Hz
Channels: {channels}
Max Amplitude: {max_amplitude:.4f}
RMS Level: {rms_level:.4f}
Peak Frequency: {peak_frequency} Hz
File: {Path(self.di_file).name}"""
                
                self.root.after(0, lambda: self.display_analysis_results(results))
                self.root.after(0, lambda: self.log_status("✅ DI analysis completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_status(f"❌ Error analyzing DI: {e}"))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def compare_audio_files(self):
        """Compare target and DI audio files."""
        if not self.target_file or not self.di_file:
            self.log_status("⚠️ Both target and DI files must be selected")
            return
        
        self.log_status("🔄 Comparing audio files...")
        
        def compare_thread():
            try:
                # Load both files
                target_data, target_sr = sf.read(self.target_file)
                di_data, di_sr = sf.read(self.di_file)
                
                # Ensure same sample rate
                if target_sr != di_sr:
                    self.root.after(0, lambda: self.log_status("⚠️ Sample rates don't match"))
                    return
                
                # Basic comparison
                target_duration = len(target_data) / target_sr
                di_duration = len(di_data) / di_sr
                duration_diff = abs(target_duration - di_duration)
                
                # Amplitude comparison
                target_max = np.max(np.abs(target_data))
                di_max = np.max(np.abs(di_data))
                amplitude_ratio = target_max / di_max if di_max > 0 else 0
                
                # Display results
                results = f"""Audio Files Comparison:
Target Duration: {target_duration:.2f}s
DI Duration: {di_duration:.2f}s
Duration Difference: {duration_diff:.2f}s
Target Max Amplitude: {target_max:.4f}
DI Max Amplitude: {di_max:.4f}
Amplitude Ratio: {amplitude_ratio:.2f}
Sample Rate: {target_sr} Hz
Files Ready for Analysis: {'✅' if duration_diff < 0.1 else '⚠️'}"""
                
                self.root.after(0, lambda: self.display_analysis_results(results))
                self.root.after(0, lambda: self.log_status("✅ Comparison completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_status(f"❌ Error comparing files: {e}"))
        
        threading.Thread(target=compare_thread, daemon=True).start()
    
    def display_analysis_results(self, results):
        """Display analysis results in the text widget."""
        self.analysis_results.delete(1.0, tk.END)
        self.analysis_results.insert(tk.END, results)
    
    def toggle_live_di_capture(self):
        """Toggle live DI capture."""
        if not self.is_live_di_capturing:
            self.start_live_di_capture()
        else:
            self.stop_live_di_capture()
    
    def start_live_di_capture(self):
        """Start live DI capture."""
        try:
            self.log_status("🎤 Starting live DI capture...")
            
            # Get audio settings
            sample_rate = int(self.sample_rate_var.get())
            buffer_size = int(self.buffer_size_var.get())
            channels = int(self.audio_channels_var.get())
            
            # Get selected input device
            input_device = self.audio_input_var.get()
            if not input_device:
                self.log_status("⚠️ Please select an audio input device in Settings")
                return
            
            self.log_status(f"🎤 Audio settings: {sample_rate}Hz, {buffer_size} samples, {channels} channels")
            self.log_status(f"🎤 Input device: {input_device}")
            
            self.is_live_di_capturing = True
            self.live_di_btn.config(text="⏹️ Stop Live DI")
            self.live_di_var.set("Live DI: ON")
            self.update_status_info()
            
            # Start actual audio capture (replace simulation with real capture)
            self.start_audio_capture(sample_rate, buffer_size, channels)
            
            self.log_status("✅ Live DI capture started - play your guitar!")
            
        except Exception as e:
            self.log_status(f"❌ Error starting live DI capture: {e}")
    
    def start_audio_capture(self, sample_rate, buffer_size, channels):
        """Start actual audio capture."""
        try:
            import sounddevice as sd
            
            def audio_callback(indata, frames, callback_time, status):
                if status:
                    self.log_status(f"⚠️ Audio status: {status}")
                
                # Process audio data here
                # For now, just log that we're receiving audio
                current_time = time.time()  # Use Python's time module, not callback parameter
                if hasattr(self, '_last_audio_time'):
                    if current_time - self._last_audio_time > 5:  # Log every 5 seconds
                        self.log_status("🎸 Receiving live DI signal...")
                        self._last_audio_time = current_time
                else:
                    self._last_audio_time = current_time
                    self.log_status("🎸 Audio capture active - receiving signal")
            
            # Start audio stream
            self.live_di_stream = sd.InputStream(
                samplerate=sample_rate,
                blocksize=buffer_size,
                channels=channels,
                callback=audio_callback,
                dtype='float32'
            )
            
            self.live_di_stream.start()
            self.log_status("✅ Audio stream started successfully")
            
        except ImportError:
            self.log_status("⚠️ sounddevice not available - using simulation mode")
        except Exception as e:
            self.log_status(f"❌ Error starting audio capture: {e}")
    
    def stop_audio_capture(self):
        """Stop audio capture."""
        try:
            if self.live_di_stream:
                self.live_di_stream.stop()
                self.live_di_stream.close()
                self.live_di_stream = None
                self.log_status("✅ Audio stream stopped")
        except Exception as e:
            self.log_status(f"❌ Error stopping audio capture: {e}")
    
    def stop_live_di_capture(self):
        """Stop live DI capture."""
        try:
            self.is_live_di_capturing = False
            self.live_di_btn.config(text="🎤 Live DI Capture")
            self.live_di_var.set("Live DI: OFF")
            self.update_status_info()
            
            # Stop audio stream
            self.stop_audio_capture()
            
            self.log_status("⏹️ Live DI capture stopped")
            
        except Exception as e:
            self.log_status(f"❌ Error stopping live DI capture: {e}")
    
    def auto_generate_patch_proposal(self):
        """Auto-generate patch proposal based on analysis."""
debug_logger.log(f"🔍 DEBUG: Starting auto_generate_patch_proposal()")
        
        if not self.analysis_data.get('target'):
            self.log_status("⚠️ No target analysis data available")
debug_logger.log(f"🔍 DEBUG: No target analysis data")
            return
        
        self.log_status("🤖 Auto-generating patch proposal based on analysis...")
debug_logger.log(f"🔍 DEBUG: Auto-generating patch proposal based on analysis...")
        
        # Get target analysis data
        target_data = self.analysis_data['target']
debug_logger.log(f"🔍 DEBUG: Target data: {target_data}")
        
        # Generate smart parameters based on analysis
        proposed_params = self.generate_smart_parameters_from_analysis(target_data)
debug_logger.log(f"🔍 DEBUG: Generated proposed_params: {proposed_params}")
        
        if proposed_params:
debug_logger.log(f"🔍 DEBUG: Applying parameters to effect widget...")
            
            # Apply proposed parameters to widget
            if self.current_effect_widget and hasattr(self.current_effect_widget, 'set_all_parameters'):
                self.current_effect_widget.set_all_parameters(proposed_params)
debug_logger.log(f"🔍 DEBUG: Parameters applied to effect widget")
            else:
debug_logger.log(f"🔍 DEBUG: No effect widget or set_all_parameters method")
                self.log_status("⚠️ No effect widget loaded")
            
            self.current_parameters = proposed_params
            
            # Store as target parameters for impact visualization
            self.target_parameters = proposed_params.copy()
            
            # Update impact visualization
            if self.impact_visualizer:
debug_logger.log(f"🔍 DEBUG: Updating impact visualization...")
                self.update_impact_visualization()
debug_logger.log(f"🔍 DEBUG: Impact visualization updated")
            else:
debug_logger.log(f"🔍 DEBUG: No impact visualizer available")
            
            param_names = list(proposed_params.keys())
            self.log_status(f"🤖 Auto-generated {len(param_names)} parameters: {', '.join(param_names)}")
            self.log_status("💡 Go to Analysis tab to see the parameter impacts!")
debug_logger.log(f"🔍 DEBUG: Auto-generation completed with {len(param_names)} parameters")
        else:
            self.log_status("⚠️ Could not generate patch proposal")
debug_logger.log(f"🔍 DEBUG: Could not generate patch proposal")
    
    def generate_smart_parameters_from_analysis(self, target_data):
        """Generate smart parameters based on audio analysis."""
debug_logger.log(f"🔍 DEBUG: Starting generate_smart_parameters_from_analysis()")
        proposed_params = {}
        
        if not self.current_effect_type:
debug_logger.log(f"🔍 DEBUG: No current_effect_type")
            return proposed_params
        
debug_logger.log(f"🔍 DEBUG: Current effect type: {self.current_effect_type}")
debug_logger.log(f"🔍 DEBUG: Target data: {target_data}")
        
        # Get peak frequency for intelligent parameter setting
        peak_freq = target_data.get('peak_frequency', 1000)
        rms_level = target_data.get('rms_level', 0.5)
        duration = target_data.get('duration', 1.0)
        
debug_logger.log(f"🔍 DEBUG: Using analysis data - peak_freq: {peak_freq}, rms: {rms_level}, duration: {duration}")
        
        # Handle multi-channel peak frequency
        if isinstance(peak_freq, str) and peak_freq == "Multi-channel":
            peak_freq = 1000  # Default frequency for multi-channel
debug_logger.log(f"🔍 DEBUG: Multi-channel detected, using default frequency 1000Hz")
        
        if self.current_effect_type == 0x0D:  # Mono Delay
            # Smart delay time based on duration and frequency
            if duration > 0:
                delay_time = min(duration * 0.25, 500)  # Quarter note delay, max 500ms
            else:
                delay_time = 250  # Default 250ms
            
            proposed_params = {
                "Time": delay_time,
                "Mix": min(50 + int(rms_level * 30), 80),  # Mix based on RMS level
                "FB Gain": min(30 + int(rms_level * 20), 60)  # Feedback based on level
            }
            
        elif self.current_effect_type == 0x12:  # Chorus
            # Smart chorus settings based on frequency content
            if peak_freq > 0:
                rate = max(0.5, min(peak_freq / 1000, 3.0))  # Rate based on frequency
            else:
                rate = 1.0
            
            proposed_params = {
                "Rate": rate,
                "Depth": min(30 + int(rms_level * 40), 70),
                "Mix": min(40 + int(rms_level * 25), 65)
            }
            
        elif self.current_effect_type == 0x09:  # Reverb
            # Smart reverb settings based on duration
            reverb_time = min(duration * 0.5, 3.0)  # Reverb time based on duration
            
            proposed_params = {
                "Time": reverb_time,
                "Mix": min(40 + int(rms_level * 35), 75),
                "High Ratio": min(0.6 + rms_level * 0.3, 1.0)
            }
            
        else:
            # Generic parameter generation for other effects
            for param_name, value in self.current_parameters.items():
                if isinstance(value, (int, float)):
                    # Apply intelligent scaling based on analysis
                    if "gain" in param_name.lower() or "level" in param_name.lower():
                        # Adjust gain/level based on RMS
                        proposed_params[param_name] = value * (0.8 + rms_level * 0.4)
                    elif "time" in param_name.lower():
                        # Adjust time-based parameters based on duration
                        proposed_params[param_name] = value * (0.5 + duration * 0.1)
                    elif "rate" in param_name.lower() or "freq" in param_name.lower():
                        # Adjust rate/frequency based on peak frequency
                        if peak_freq > 0:
                            proposed_params[param_name] = value * (0.5 + peak_freq / 2000)
                        else:
                            proposed_params[param_name] = value
                    else:
                        # Default intelligent variation
                        proposed_params[param_name] = value * (0.8 + rms_level * 0.4)
        
        # Apply parameter limits
        for param_name, value in proposed_params.items():
            proposed_params[param_name] = self.apply_parameter_limits(param_name, value)
        
debug_logger.log(f"🔍 DEBUG: Final proposed_params: {proposed_params}")
        return proposed_params
    
    def generate_patch(self):
        """Generate patch."""
debug_logger.log(f"🔍 DEBUG: Starting generate_patch()")
        
        if not self.target_file:
            self.log_status("⚠️ Please select target file first")
debug_logger.log(f"🔍 DEBUG: No target file selected")
            return
        
        if not (self.di_file or self.is_live_di_capturing):
            self.log_status("⚠️ Please select DI file or start live DI capture")
debug_logger.log(f"🔍 DEBUG: No DI file or live capture")
            return
        
        if not self.current_effect_widget:
            self.log_status("⚠️ Please load an effect first (go to Effects tab)")
debug_logger.log(f"🔍 DEBUG: No current effect widget")
            return
        
        self.log_status("🎯 Generating patch...")
debug_logger.log(f"🔍 DEBUG: Starting patch generation...")
debug_logger.log(f"🔍 DEBUG: Target file: {self.target_file}")
debug_logger.log(f"🔍 DEBUG: DI file: {self.di_file}")
debug_logger.log(f"🔍 DEBUG: Live DI capturing: {self.is_live_di_capturing}")
debug_logger.log(f"🔍 DEBUG: Current effect type: {self.current_effect_type}")
        
        def generate_thread():
            try:
debug_logger.log(f"🔍 DEBUG: Getting current parameters from effect widget...")
                current_params = self.current_effect_widget.get_all_parameters()
debug_logger.log(f"🔍 DEBUG: Current parameters: {current_params}")
                
                magicstomp_params = {}
                for param_name, value in current_params.items():
debug_logger.log(f"🔍 DEBUG: Processing parameter: {param_name} = {value}")
                    for child in self.current_effect_widget.winfo_children():
                        if hasattr(child, 'param_name') and child.param_name == param_name:
                            magicstomp_value = self.current_effect_widget._convert_to_magicstomp(child, value)
                            magicstomp_params[param_name] = magicstomp_value
debug_logger.log(f"🔍 DEBUG: Converted {param_name}: {value} -> {magicstomp_value}")
                            break
                
debug_logger.log(f"🔍 DEBUG: Final magicstomp_params: {magicstomp_params}")
                
                # Simulate progress
                for i in range(101):
                    self.root.after(0, lambda p=i: self.progress_var.set(p))
                    time.sleep(0.05)
                
                self.current_patch = {
                    "effect_type": self.current_effect_type,
                    "parameters": magicstomp_params,
                    "target_file": self.target_file,
                    "di_file": self.di_file if self.di_file else "LIVE_DI_CAPTURE"
                }
                
debug_logger.log(f"🔍 DEBUG: Generated patch: {self.current_patch}")
                
                self.root.after(0, lambda: self.log_status(f"✅ Patch generated ({len(magicstomp_params)} params)"))
                def log_effect_label():
                    if self.current_effect_type is not None:
                        effect_name = EffectRegistry.get_effect_name(self.current_effect_type)
                        display_name = self.get_display_name_for_effect(effect_name)
                        self.log_status(f"🎛️ Effect: {display_name}")

                self.root.after(0, log_effect_label)
                
                # Display patch parameters
                self.root.after(0, self.display_patch_parameters)
                
            except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error in generate_thread: {e}")
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: self.log_status(f"❌ Error generating patch: {e}"))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def apply_patch_to_effects(self):
        """Apply current patch to loaded effect widgets."""
debug_logger.log(f"🔍 DEBUG: Starting apply_patch_to_effects()")
        
        if not self.current_patch:
            self.log_status("⚠️ No patch to apply")
debug_logger.log(f"🔍 DEBUG: No current patch to apply")
            return
        
        if not self.current_effect_widget:
            self.log_status("⚠️ No effect loaded - please load an effect in Effects tab first")
debug_logger.log(f"🔍 DEBUG: No current effect widget")
            return
        
        try:
            self.log_status("🎛️ Applying patch to current effect...")
debug_logger.log(f"🔍 DEBUG: Applying patch to current effect...")
debug_logger.log(f"🔍 DEBUG: Current patch: {self.current_patch}")
            
            # Convert patch to widget parameters
            widget_params = self.convert_patch_to_widget_params(self.current_patch)
debug_logger.log(f"🔍 DEBUG: Converted widget params: {widget_params}")
            
            if widget_params:
                # Apply parameters to effect widget
                if hasattr(self.current_effect_widget, 'set_all_parameters'):
                    self.current_effect_widget.set_all_parameters(widget_params)
debug_logger.log(f"🔍 DEBUG: Parameters applied to effect widget")
                else:
                    self.log_status("⚠️ Effect widget doesn't support set_all_parameters")
debug_logger.log(f"🔍 DEBUG: Effect widget doesn't support set_all_parameters")
                    return
                
                # Update current parameters
                self.current_parameters = widget_params
                
                # Store as target parameters for impact visualization
                self.target_parameters = widget_params.copy()
                
                # Update impact visualization
                if self.impact_visualizer:
debug_logger.log(f"🔍 DEBUG: Updating impact visualization...")
                    self.update_impact_visualization()
debug_logger.log(f"🔍 DEBUG: Impact visualization updated")
                else:
debug_logger.log(f"🔍 DEBUG: No impact visualizer available")
                
                param_names = list(widget_params.keys())
                self.log_status(f"✅ Applied {len(param_names)} parameters to effect")
                self.log_status("💡 Go to Analysis tab to see the parameter impacts!")
debug_logger.log(f"🔍 DEBUG: Successfully applied {len(param_names)} parameters: {param_names}")
                
            else:
                self.log_status("⚠️ Could not convert patch to widget parameters")
debug_logger.log(f"🔍 DEBUG: Could not convert patch to widget parameters")
                
        except Exception as e:
            self.log_status(f"❌ Error applying patch to effects: {e}")
debug_logger.log(f"🔍 DEBUG: Error applying patch to effects: {e}")
            import traceback
            traceback.print_exc()
    
    def save_patch(self):
        """Save current patch to file."""
debug_logger.log(f"🔍 DEBUG: Starting save_patch()")
        
        if not self.current_patch:
            self.log_status("⚠️ No patch to save")
debug_logger.log(f"🔍 DEBUG: No current patch to save")
            return
        
        try:
            # Ask user for file location
            patch_file = filedialog.asksaveasfilename(
                title="Save Patch",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=f"patch_{Path(self.target_file).stem if self.target_file else 'unnamed'}.json"
            )
            
            if not patch_file:
debug_logger.log(f"🔍 DEBUG: User cancelled patch save")
                return
            
debug_logger.log(f"🔍 DEBUG: Saving patch to: {patch_file}")
            
            # Add metadata
            patch_to_save = {
                'metadata': {
                    'created_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'target_file': str(self.target_file) if self.target_file else None,
                    'di_file': str(self.di_file) if self.di_file else None,
                    'effect_type': self.current_effect_type,
                    'effect_name': EffectRegistry.get_effect_name(self.current_effect_type) if self.current_effect_type else None,
                    'gui_version': 'split_vertical'
                },
                'patch': self.current_patch
            }
            
            # Save to file
            with open(patch_file, 'w') as f:
                json.dump(patch_to_save, f, indent=2)
            
            self.log_status(f"✅ Patch saved to: {Path(patch_file).name}")
debug_logger.log(f"🔍 DEBUG: Patch saved successfully to {patch_file}")
            
        except Exception as e:
            self.log_status(f"❌ Error saving patch: {e}")
debug_logger.log(f"🔍 DEBUG: Error saving patch: {e}")
            import traceback
            traceback.print_exc()
    
    def load_patch(self):
        """Load patch from file."""
debug_logger.log(f"🔍 DEBUG: Starting load_patch()")
        
        try:
            # Ask user for file location
            patch_file = filedialog.askopenfilename(
                title="Load Patch",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not patch_file:
debug_logger.log(f"🔍 DEBUG: User cancelled patch load")
                return
            
debug_logger.log(f"🔍 DEBUG: Loading patch from: {patch_file}")
            
            # Load from file
            with open(patch_file, 'r') as f:
                patch_data = json.load(f)
            
            # Extract patch and metadata
            if 'patch' in patch_data:
                self.current_patch = patch_data['patch']
                metadata = patch_data.get('metadata', {})
                
debug_logger.log(f"🔍 DEBUG: Loaded patch: {self.current_patch}")
debug_logger.log(f"🔍 DEBUG: Metadata: {metadata}")
                
                # Update status with metadata
                created_date = metadata.get('created_date', 'Unknown')
                effect_name = metadata.get('effect_name', 'Unknown')
                target_file = metadata.get('target_file', 'Unknown')
                
                self.log_status(f"✅ Patch loaded: {Path(patch_file).name}")
                self.log_status(f"📅 Created: {created_date}")
                self.log_status(f"🎛️ Effect: {effect_name}")
                if target_file != 'Unknown':
                    self.log_status(f"🎵 Target: {Path(target_file).name}")
                
                # Display patch parameters
                self.display_patch_parameters()
                
                # Save state after loading patch
                self.save_settings()
                
                # Try to identify and auto-load effects from patch
debug_logger.log(f"🔍 DEBUG: About to auto-load effects from patch: {self.current_patch}")
                self.auto_load_effects_from_patch()
                
                # Apply patch parameters to widgets after a short delay
                self.root.after(500, self.apply_patch_parameters_to_widgets)
                
                # If effect is loaded, apply parameters
                if self.current_effect_widget and hasattr(self.current_effect_widget, 'set_all_parameters'):
                    # Convert patch parameters to widget parameters
                    widget_params = self.convert_patch_to_widget_params(self.current_patch)
                    if widget_params:
                        self.current_effect_widget.set_all_parameters(widget_params)
                        self.current_parameters = widget_params
                        self.log_status("🎛️ Parameters applied to current effect")
                        self.log_status("💡 Go to Effects tab to see the visual representation!")
debug_logger.log(f"🔍 DEBUG: Applied parameters to effect: {widget_params}")
                        
                        # Auto-update impact visualization after applying patch
                        self.root.after(100, self.update_impact_visualization)
                        self.log_status("📊 Impact visualization updated automatically")
                else:
                    self.log_status("💡 Load an effect in Effects tab, then click '🎛️ Apply to Effects' to see visual representation")
debug_logger.log(f"🔍 DEBUG: No effect loaded - patch ready for manual application")
                
            else:
                self.log_status("⚠️ Invalid patch file format")
debug_logger.log(f"🔍 DEBUG: Invalid patch file - no 'patch' key found")
                
        except Exception as e:
            self.log_status(f"❌ Error loading patch: {e}")
debug_logger.log(f"🔍 DEBUG: Error loading patch: {e}")
            import traceback
            traceback.print_exc()
    
    def get_widget_specific_params(self, widget_type, all_params):
        """Retourne les paramètres spécifiques à un type de widget."""
        specific_params = {}
        
        if widget_type == "CompressorWidget":
            # Paramètres du compresseur (selon le CSV)
            compressor_keys = ['threshold', 'ratio', 'attack', 'release', 'slope', 'low_gain', 'mid_gain', 'high_gain', 'lookup', 'ceiling']
            specific_params = {k: all_params[k] for k in compressor_keys if k in all_params}
            
        elif widget_type == "ThreeBandEQWidget":
            # Paramètres de l'EQ 3 bandes
            eq_keys = ['eq1_gain', 'eq1_freq', 'eq1_q', 'eq2_gain', 'eq2_freq', 'eq2_q', 'eq3_gain', 'eq3_freq', 'eq3_q']
            specific_params = {k: all_params[k] for k in eq_keys if k in all_params}
            
        elif widget_type == "MonoDelayWidget":
            # Paramètres du delay mono
            delay_keys = ['time', 'feedback', 'mix', 'low_cut', 'high_cut', 'high_ratio']
            specific_params = {k: all_params[k] for k in delay_keys if k in all_params}
            
        elif widget_type == "StereoDelayWidget":
            # Paramètres du delay stéréo
            delay_keys = ['time', 'feedback', 'mix', 'low_cut', 'high_cut', 'high_ratio']
            specific_params = {k: all_params[k] for k in delay_keys if k in all_params}
            
        elif widget_type == "ModDelayWidget":
            # Paramètres du delay modulé
            delay_keys = ['time', 'feedback', 'mix', 'low_cut', 'high_cut', 'high_ratio', 'wave', 'freq']
            specific_params = {k: all_params[k] for k in delay_keys if k in all_params}
            
        elif widget_type == "EchoWidget":
            # Paramètres de l'echo
            echo_keys = ['time', 'feedback', 'mix', 'low_cut', 'high_cut', 'high_ratio']
            specific_params = {k: all_params[k] for k in echo_keys if k in all_params}
            
        elif widget_type == "MultiFilterWidget":
            # Paramètres du multi-filtre (utilisé comme substitut pour le compresseur)
            # Mapper les paramètres du compresseur vers des paramètres de filtre
            specific_params = {
                'type1': 0,  # Type de filtre par défaut
                'freq1': int(all_params.get('threshold', 0.5) * 100),  # Utiliser threshold comme fréquence
                'level1': int(all_params.get('ratio', 1.0) * 10),  # Utiliser ratio comme niveau
                'resonance1': int(all_params.get('attack', 10)),  # Utiliser attack comme résonance
                'mix': int(all_params.get('release', 100) / 10),  # Utiliser release comme mix
                'type2': 0,
                'freq2': int(all_params.get('makeup_gain', 0) * 10),
                'level2': 0,
                'resonance2': 0,
                'type3': 0,
                'freq3': 0,
                'level3': 0,
                'resonance3': 0
            }
            
        # Pour les autres widgets, utiliser tous les paramètres
        else:
            specific_params = all_params.copy()
        
        return specific_params
    
    def convert_patch_to_widget_params(self, patch):
        """Convert patch format to widget parameters format."""
debug_logger.log(f"🔍 DEBUG: Starting convert_patch_to_widget_params()")
debug_logger.log(f"🔍 DEBUG: Input patch: {patch}")
        
        try:
            widget_params = {}
            
            # Extract parameters from patch sections with proper mapping
            for section_name, section_data in patch.items():
                if isinstance(section_data, dict) and section_name != 'meta':
debug_logger.log(f"🔍 DEBUG: Processing section: {section_name}")
                    
                    if section_name == 'compressor':
                        # Map compressor parameters
                        if 'threshold' in section_data:
                            widget_params['threshold'] = section_data['threshold']
                        if 'ratio' in section_data:
                            widget_params['ratio'] = section_data['ratio']
                        if 'attack' in section_data:
                            widget_params['attack'] = section_data['attack']
                        if 'release' in section_data:
                            widget_params['release'] = section_data['release']
                        # Paramètres par défaut pour le compresseur
                        widget_params['slope'] = 0  # -6 dB par défaut
                        widget_params['low_gain'] = 0.0
                        widget_params['mid_gain'] = 0.0
                        widget_params['high_gain'] = 0.0
                        widget_params['lookup'] = 0.0
                        widget_params['ceiling'] = 0.0
                    
                    elif section_name == 'eq':
                        # Map EQ parameters to widget format
                        if 'low_gain' in section_data:
                            widget_params['eq1_gain'] = section_data['low_gain']
                        if 'low_freq' in section_data:
                            widget_params['eq1_freq'] = section_data['low_freq']
                        if 'mid_gain' in section_data:
                            widget_params['eq2_gain'] = section_data['mid_gain']
                        if 'mid_freq' in section_data:
                            widget_params['eq2_freq'] = section_data['mid_freq']
                        if 'high_gain' in section_data:
                            widget_params['eq3_gain'] = section_data['high_gain']
                        if 'high_freq' in section_data:
                            widget_params['eq3_freq'] = section_data['high_freq']
                        # Default Q values
                        widget_params['eq1_q'] = 1.0
                        widget_params['eq2_q'] = 1.0
                        widget_params['eq3_q'] = 1.0
                    
                    elif section_name == 'delay':
                        # Map delay parameters
                        if 'time' in section_data:
                            widget_params['time'] = section_data['time']
                        if 'feedback' in section_data:
                            widget_params['feedback'] = section_data['feedback']
                        if 'mix' in section_data:
                            widget_params['mix'] = section_data['mix']
                        if 'low_cut' in section_data:
                            widget_params['low_cut'] = section_data['low_cut']
                        if 'high_cut' in section_data:
                            widget_params['high_cut'] = section_data['high_cut']
                        # Paramètres par défaut pour le delay
                        widget_params['high_ratio'] = 0.0
            
debug_logger.log(f"🔍 DEBUG: Final converted widget params: {widget_params}")
            return widget_params
            
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error converting patch: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def auto_load_effects_from_patch(self):
        """Auto-identify and load effects from patch data."""
debug_logger.log(f"🔍 DEBUG: Starting auto_load_effects_from_patch()")
        
        if not self.current_patch:
debug_logger.log(f"🔍 DEBUG: No current patch to analyze")
            return
        
        # Clear existing effect widgets before loading new ones
        self.clear_effect_widgets()
        
        try:
            # Analyze patch to identify effects
            identification = self.identify_effects_from_patch(self.current_patch)
            official_matches = identification.get('official', [])
            unsupported_matches = identification.get('unsupported', [])
            unverified_matches = identification.get('unverified', [])
            duplicate_matches = identification.get('duplicates', [])

            official_names = [match.display_name for match in official_matches]
            unsupported_names = [match.display_name for match in unsupported_matches]
            unverified_names = [match.display_name for match in unverified_matches]
            duplicate_names = [match.display_name for match in duplicate_matches]

debug_logger.log(f"🔍 DEBUG: Official matches: {official_names}")
debug_logger.log(f"🔍 DEBUG: Unsupported matches: {unsupported_names}")
debug_logger.log(f"🔍 DEBUG: Unverified matches: {unverified_names}")
debug_logger.log(f"🔍 DEBUG: Duplicate matches: {duplicate_names}")

            if not official_matches:
                if unsupported_names:
                    self.log_status(f"⚠️ Official effects unsupported: {', '.join(unsupported_names)}")
                if unverified_names:
                    self.log_status(f"ℹ️ Effect hints outside official catalog: {', '.join(unverified_names)}")
                if duplicate_names:
                    self.log_status(f"ℹ️ Duplicate effect hints ignored: {', '.join(duplicate_names)}")
debug_logger.log(f"🔍 DEBUG: No official effects identified in patch")
                self.log_status("💡 No specific effects identified in patch - manual selection required")
                return

            self.log_status(f"🔍 Identified effects: {', '.join(official_names)}")
debug_logger.log(f"🔍 DEBUG: Loading effect cascade with {len(official_matches)} effects")
            self.log_status(f"🎛️ Loading effect cascade: {len(official_matches)} effects")

            loaded_effects: List[EffectMatch] = []
            load_failures: List[Tuple[EffectMatch, str]] = []

            for i, match in enumerate(official_matches, start=1):
                display_name = match.display_name
                print(
                    f"🔍 DEBUG: Auto-loading effect {i}/{len(official_matches)}: "
                    f"{display_name} (canonical: {match.canonical_name})"
                )
                self.log_status(f"🎛️ Loading effect {i}/{len(official_matches)}: {display_name}")

                success, info = self.add_effect_to_cascade(match)
debug_logger.log(f"🔍 DEBUG: add_effect_to_cascade returned: {success}, info: {info}")

                if success:
                    loaded_effects.append(match)
                    self.log_status(f"✅ Loaded: {display_name}")
debug_logger.log(f"🔍 DEBUG: Successfully loaded effect: {display_name}")
                else:
                    load_failures.append((match, info))
                    self.log_status(f"❌ Failed to load {display_name}: {info}")
debug_logger.log(f"🔍 DEBUG: Failed to load effect: {display_name} ({info})")

            # Report cascade status
            if loaded_effects:
                loaded_display_names = [match.display_name for match in loaded_effects]
                self.log_status(
                    f"🎛️ Effect cascade loaded: {len(loaded_effects)}/{len(official_matches)} effects"
                    f" ({', '.join(loaded_display_names)})"
                )
debug_logger.log(f"🔍 DEBUG: Effect cascade loaded: {[match.display_name for match in loaded_effects]}")
                    
                # Check if we need to restore a queued patch
debug_logger.log(f"🔍 DEBUG: Checking for queued patch restoration...")
                print(
                    f"🔍 DEBUG: - hasattr patch_to_restore: {hasattr(self, 'patch_to_restore')}"
                )
                if hasattr(self, 'patch_to_restore'):
debug_logger.log(f"🔍 DEBUG: - patch_to_restore value: {self.patch_to_restore}")
                if hasattr(self, 'patch_to_restore') and self.patch_to_restore:
debug_logger.log(f"🔍 DEBUG: Widgets loaded, triggering patch restoration")
                    self.root.after(
                        500, self.reload_restored_patch
                    )  # Small delay to ensure widgets are ready
                else:
debug_logger.log(f"🔍 DEBUG: No queued patch to restore")

                # Auto-apply patch parameters to the last loaded effect (current active one)
debug_logger.log(f"🔍 DEBUG: Checking auto-apply conditions:")
debug_logger.log(f"🔍 DEBUG: - current_patch: {bool(self.current_patch)}")
debug_logger.log(f"🔍 DEBUG: - current_effect_widget: {bool(self.current_effect_widget)}")
debug_logger.log(f"🔍 DEBUG: - has set_all_parameters: {hasattr(self.current_effect_widget, 'set_all_parameters') if self.current_effect_widget else False}")
                    
                    if (self.current_patch and self.effect_widget_cascade) or getattr(self, 'auto_apply_restored_patch', False):
debug_logger.log(f"🔍 DEBUG: All conditions met, proceeding with auto-apply")
                        is_restored_patch = getattr(self, 'auto_apply_restored_patch', False)
                        if is_restored_patch:
debug_logger.log(f"🔍 DEBUG: Auto-applying restored patch to widgets")
                        widget_params = self.convert_patch_to_widget_params(self.current_patch)
debug_logger.log(f"🔍 DEBUG: Converted widget params: {widget_params}")
                        
                        if widget_params:
                            # Appliquer les paramètres à tous les widgets de la cascade
debug_logger.log(f"🔍 DEBUG: Applying parameters to all widgets in cascade")
                            for i, effect_widget in enumerate(self.effect_widget_cascade):
                                try:
                                    widget_type = type(effect_widget).__name__
debug_logger.log(f"🔍 DEBUG: Applying to widget {i}: {widget_type}")
                                    
                                    # Obtenir les paramètres spécifiques à ce widget
                                    specific_params = self.get_widget_specific_params(widget_type, widget_params)
debug_logger.log(f"🔍 DEBUG: Specific params for {widget_type}: {specific_params}")
                                    
                                    if specific_params:
                                        effect_widget.set_all_parameters(specific_params)
debug_logger.log(f"🔍 DEBUG: set_all_parameters succeeded for widget {i}")
                                    else:
debug_logger.log(f"🔍 DEBUG: No specific params for {widget_type}")
                                        
                                except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error applying to widget {i}: {e}")
                            
                            # Mettre à jour les paramètres actuels et cibles
                            self.current_parameters = widget_params
                            self.target_parameters = widget_params.copy()
                            
                            # Update impact visualization
debug_logger.log(f"🔍 DEBUG: Scheduling impact visualization update")
                            self.root.after(100, self.update_impact_visualization)
                            self.log_status("📊 Impact visualization updated automatically")
                            self.log_status("🎛️ Patch parameters applied to all auto-loaded effects")
                            self.log_status("💡 Go to Effects tab to see the visual representation!")
                            self.log_status("💡 Go to Analysis tab to see the parameter impacts!")
debug_logger.log(f"🔍 DEBUG: Auto-applied patch parameters: {widget_params}")
                            
                            # Reset the flag only after successful application
                            if is_restored_patch:
                                self.auto_apply_restored_patch = False
debug_logger.log(f"🔍 DEBUG: Reset auto_apply_restored_patch flag after successful application")
                            
                            # Debug current state
debug_logger.log(f"🔍 DEBUG: Current effect widget: {self.current_effect_widget}")
debug_logger.log(f"🔍 DEBUG: Current effect type: {self.current_effect_type}")
debug_logger.log(f"🔍 DEBUG: Current parameters: {self.current_parameters}")
debug_logger.log(f"🔍 DEBUG: Target parameters: {self.target_parameters}")
                        else:
debug_logger.log(f"🔍 DEBUG: No widget params to apply")
                    else:
debug_logger.log(f"🔍 DEBUG: Cannot auto-apply - conditions not met")
debug_logger.log(f"🔍 DEBUG: - current_effect_widget: {self.current_effect_widget}")
debug_logger.log(f"🔍 DEBUG: - has set_all_parameters: {hasattr(self.current_effect_widget, 'set_all_parameters') if self.current_effect_widget else False}")
                        self.log_status("⚠️ Effect loaded but cannot apply parameters")
            else:
                failed_display_names = [match.display_name for match in official_matches]
                failed_list = ', '.join(failed_display_names) if failed_display_names else 'None'
                self.log_status(f"⚠️ Could not auto-load effects: {failed_list}")
debug_logger.log(f"🔍 DEBUG: Failed to auto-load any effects")

            summary_bits = []
            if loaded_effects:
                summary_bits.append(
                    "Loaded: " + ', '.join(match.display_name for match in loaded_effects)
                )
            if load_failures:
                summary_bits.append(
                    "Failed: "
                    + ', '.join(
                        f"{match.display_name} ({reason})" for match, reason in load_failures
                    )
                )
            if unsupported_matches:
                summary_bits.append(
                    "Unsupported: "
                    + ', '.join(
                        f"{match.display_name} ({match.describe_failure()})"
                        for match in unsupported_matches
                    )
                )
            if unverified_matches:
                summary_bits.append(
                    "Unverified: "
                    + ', '.join(
                        f"{match.display_name} ({match.describe_failure()})"
                        for match in unverified_matches
                    )
                )
            if duplicate_matches:
                summary_bits.append(
                    "Duplicates ignored: " + ', '.join(duplicate_names)
                )

            if summary_bits:
                self.log_status("🧾 Effect cascade summary -> " + " | ".join(summary_bits))
debug_logger.log(f"🔍 DEBUG: Summary bits: {summary_bits}")
                
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error in auto_load_effects_from_patch: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_composite_effect_widgets(self, effect_section):
        """Create additional widgets for composite effects like Distortion Multi (Flange)."""
        try:
debug_logger.log(f"🔍 DEBUG: Creating composite effect widgets from {len(effect_section)} bytes")
            
            # For Distortion Multi (Flange), create the 6 sub-effect widgets
debug_logger.log(f"🔍 DEBUG: Creating Distortion Multi (Flange) sub-effects")
            
            # 1. Create Distortion widget (Overdrive 1)
debug_logger.log(f"🔍 DEBUG: Creating Distortion widget")
            distortion_params = self._extract_distortion_params(effect_section[0:20])
            self._create_effect_widget("Distortion", distortion_params)
            
            # 2. Create Noise Gate widget
debug_logger.log(f"🔍 DEBUG: Creating Noise Gate widget")
            noise_gate_params = self._extract_noise_gate_params(effect_section[20:24])
            self._create_effect_widget("Noise Gate", noise_gate_params)
            
            # 3. Create Compressor widget
debug_logger.log(f"🔍 DEBUG: Creating Compressor widget")
            compressor_params = self._extract_compressor_params(effect_section[24:30])
            self._create_effect_widget("Compressor", compressor_params)
            
            # 4. Create Flange widget
debug_logger.log(f"🔍 DEBUG: Creating Flange widget")
            flange_params = self._extract_flange_params(effect_section[30:36])
            self._create_effect_widget("Flange", flange_params)
            
            # 5. Create Delay widget
debug_logger.log(f"🔍 DEBUG: Creating Delay widget")
            delay_params = self._extract_delay_params(effect_section[36:44])
            self._create_effect_widget("Mono Delay", delay_params)
            
            # 6. Create Reverb widget
debug_logger.log(f"🔍 DEBUG: Creating Reverb widget")
            reverb_params = self._extract_reverb_params(effect_section[44:52])
            self._create_effect_widget("Reverb", reverb_params)
            
            self.log_status("✅ Distortion Multi (Flange) widgets created successfully")
                
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error creating composite effect widgets: {e}")
            self.log_status(f"⚠️ Error creating composite effect widgets: {e}")
    
    def _extract_distortion_params(self, data):
        """Extract distortion parameters from effect section data using MagicstompFrenzy offsets."""
        if len(data) < 0x80:
            return {}
        
        # Distortion parameters using MagicstompFrenzy offsets
        # AmpType = 0x16, Gain = 0x1E, Master = 0x1F, Tone = 0x22
        amp_type = data[0x16] if len(data) > 0x16 else 0
        gain = data[0x1E] if len(data) > 0x1E else 0
        master = data[0x1F] if len(data) > 0x1F else 0
        tone = data[0x22] if len(data) > 0x22 else 0
        
        # EQ parameters
        treble = data[0x24] if len(data) > 0x24 else 0
        high_middle = data[0x25] if len(data) > 0x25 else 0
        low_middle = data[0x26] if len(data) > 0x26 else 0
        bass = data[0x27] if len(data) > 0x27 else 0
        presence = data[0x28] if len(data) > 0x28 else 0
        
        return {
            'Type': 'Overdrive 1',
            'Gain': gain,
            'Master': master,
            'Tone': tone,
            'EQ 1 Freq': 50.0,
            'EQ 1 Gain': (bass - 64) / 127.0 * 20.0,
            'EQ 1 Q': 0.1
        }
    
    def _extract_noise_gate_params(self, data):
        """Extract noise gate parameters from effect section data using MagicstompFrenzy offsets."""
        if len(data) < 0x80:
            return {}
        
        # Noise gate parameters using MagicstompFrenzy offsets
        # NoiseGateThreshold = 0x2A, NoiseGateAttack = 0x2B, NoiseGateHold = 0x2C, NoiseGateDecay = 0x2D
        threshold = data[0x2A] if len(data) > 0x2A else 0
        attack = data[0x2B] if len(data) > 0x2B else 0
        hold = data[0x2C] if len(data) > 0x2C else 0
        decay = data[0x2D] if len(data) > 0x2D else 0
        
        return {
            'threshold': threshold,
            'hold': hold,
            'attack': attack,
            'decay': decay
        }
    
    def _extract_compressor_params(self, data):
        """Extract compressor parameters from effect section data using MagicstompFrenzy offsets."""
        if len(data) < 0x80:
            return {}
        
        # Compressor parameters using MagicstompFrenzy offsets
        # CompressorThreshold = 0x04 (2 bytes), CompressorRatio = 0x34, CompressorAttack = 0x35, etc.
        threshold = (data[0x04] << 8) + data[0x05] if len(data) > 0x05 else 0
        ratio = data[0x34] if len(data) > 0x34 else 0
        attack = data[0x35] if len(data) > 0x35 else 0
        release = data[0x36] if len(data) > 0x36 else 0
        knee = data[0x37] if len(data) > 0x37 else 0
        gain = data[0x38] if len(data) > 0x38 else 0
        
        return {
            'Threshold': (threshold - 32768) / 32768.0 * 96.0,  # Convert to dB
            'Attack': attack,
            'Slope': knee,
            'Ratio': ratio,
            'Release': release,
            'Low Gain': (gain - 64) / 127.0 * 20.0
        }
    
    def _extract_flange_params(self, data):
        """Extract flange parameters from effect section data using MagicstompFrenzy offsets."""
        if len(data) < 0x80:
            return {}
        
        # Flange parameters using MagicstompFrenzy offsets
        # ModWave = 0x19, ModSpeed = 0x3F, ModDepth = 0x40, FlangePhaserLevel = 0x42
        wave = data[0x19] if len(data) > 0x19 else 0
        speed = data[0x3F] if len(data) > 0x3F else 0
        depth = data[0x40] if len(data) > 0x40 else 0
        level = data[0x42] if len(data) > 0x42 else 0
        
        # ChorusFlangerDelay = 0x06 (2 bytes)
        delay = (data[0x06] << 8) + data[0x07] if len(data) > 0x07 else 0
        
        return {
            'Wave': wave,
            'Freq.': speed,
            'Depth': depth,
            'FB. Gain': 0,
            'Mod. Delay': delay,
            'LSH Freq.': 0.0,
            'LSH Gain': 0.0,
            'EQ Freq.': 0.0,
            'EQ Gain': 0.0,
            'EQ Q': 0.0,
            'HSH Freq.': 0.0,
            'HSH Gain': 0.0,
            'Mix': level
        }
    
    def _extract_delay_params(self, data):
        """Extract delay parameters from effect section data using MagicstompFrenzy offsets."""
        if len(data) < 0x80:
            return {}
        
        # Delay parameters using MagicstompFrenzy offsets
        # DelayFeedback = 0x08 (2 bytes), DelayTapL = 0x4A, DelayTapR = 0x4B, etc.
        feedback = (data[0x08] << 8) + data[0x09] if len(data) > 0x09 else 0
        tap_l = data[0x4A] if len(data) > 0x4A else 0
        tap_r = data[0x4B] if len(data) > 0x4B else 0
        feedback_gain = data[0x4C] if len(data) > 0x4C else 0
        high = data[0x4D] if len(data) > 0x4D else 0
        level = data[0x4E] if len(data) > 0x4E else 0
        hpf = data[0x52] if len(data) > 0x52 else 0
        lpf = data[0x53] if len(data) > 0x53 else 0
        
        return {
            'level': level,
            'tap_l': tap_l,
            'tap_r': tap_r,
            'hpf': hpf,
            'feedback': feedback,
            'feedback_gain': feedback_gain,
            'high': high,
            'lpf': lpf
        }
    
    def _extract_reverb_params(self, data):
        """Extract reverb parameters from effect section data using MagicstompFrenzy offsets."""
        if len(data) < 0x80:
            return {}
        
        # Reverb parameters using MagicstompFrenzy offsets
        # ReverbIniDelay = 0x0A (2 bytes), ReverbTime = 0x55, etc.
        ini_delay = (data[0x0A] << 8) + data[0x0B] if len(data) > 0x0B else 0
        time = data[0x55] if len(data) > 0x55 else 0
        diffusion = data[0x56] if len(data) > 0x56 else 0
        density = data[0x57] if len(data) > 0x57 else 0
        level = data[0x58] if len(data) > 0x58 else 0
        
        return {
            'Reverb Type': 'Hall',
            'Initial Delay': ini_delay,
            'ER/Rev Delay': 0.0,
            'Reverb Time': time,
            'High Ratio': 0.0,
            'Low Ratio': 0.0,
            'Diffusion': diffusion,
            'Density': density,
            'ER/Rev Balance': 0.0,
            'High Pass Filter': 0.0,
            'Low Pass Filter': 0.0,
            'Gate Level': level,
            'Attack': 0.0,
            'Hold': 0.0,
            'Decay': 0.0
        }
    
    def _create_effect_widget(self, effect_name, params):
        """Create an effect widget with the given parameters."""
        try:
debug_logger.log(f"🔍 DEBUG: Creating {effect_name} widget with params: {params}")
            
            # Create an EffectMatch object for the effect
            from gui.split_vertical_shared import EffectMatch
            
            # Map effect names to their canonical names
            effect_name_mapping = {
                "Distortion": "Distortion",
                "Noise Gate": "Noise Gate", 
                "Compressor": "Compressor",
                "Flange": "Flange",
                "Mono Delay": "Mono Delay",
                "Reverb": "Reverb"
            }
            
            canonical_name = effect_name_mapping.get(effect_name, effect_name)
            
            # Create EffectMatch object
            effect_match = EffectMatch(
                section="composite_effect",
                candidate=effect_name,
                canonical_name=canonical_name,
                official_name=canonical_name,
                normalized_name=canonical_name.lower().replace(" ", "_"),
                effect_type=None,  # Will be determined by the system
                is_official=True,
                is_supported=True,
                reason="Composite effect sub-component"
            )
            
            # Add the effect to the cascade
            success, info = self.add_effect_to_cascade(effect_match)
            if success:
debug_logger.log(f"🔍 DEBUG: Successfully created {effect_name} widget")
                
                # Apply parameters if the widget supports it
                if hasattr(self, 'current_effect_widget') and self.current_effect_widget:
                    if hasattr(self.current_effect_widget, 'set_all_parameters'):
debug_logger.log(f"🔍 DEBUG: Applying parameters to {effect_name} widget: {params}")
                        self.current_effect_widget.set_all_parameters(params)
debug_logger.log(f"🔍 DEBUG: Applied parameters to {effect_name} widget")
                    else:
debug_logger.log(f"🔍 DEBUG: Widget doesn't support set_all_parameters")
                else:
debug_logger.log(f"🔍 DEBUG: No current_effect_widget available")
            else:
debug_logger.log(f"🔍 DEBUG: Failed to create {effect_name} widget: {info}")
            
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error creating {effect_name} widget: {e}")
            import traceback
            traceback.print_exc()

