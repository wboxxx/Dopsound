#!/usr/bin/env python3
"""
Tabbed Compact GUI Window with Impact Visualization
=================================================

Version ultra-compacte avec interface en onglets.
Optimisée pour les écrans standard avec utilisation maximale de l'espace.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import soundfile as sf

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_tone_match_magicstomp import AutoToneMatcher
from cli.auto_match_hil import HILToneMatcher
from hil.io import AudioDeviceManager

# Import Magicstomp effects and visualization
from magicstomp_effects import EffectRegistry
from adapter_magicstomp import MagicstompAdapter
from realtime_magicstomp import RealtimeMagicstomp
from gui.impact_visualization import ImpactVisualizer, ParameterImpact, ImpactLevel


class TabbedCompactGUI:
    """
    Ultra-compact GUI with tabbed interface.
    
    Features:
    - Tabbed layout for maximum space efficiency
    - Standard font sizes
    - Responsive design
    - All functionality in organized tabs
    """
    
    def __init__(self):
        """Initialize the tabbed compact GUI."""
        self.root = tk.Tk()
        self.root.title("🎸 Magicstomp HIL - Compact")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Minimum size
        self.root.minsize(1000, 700)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # State variables
        self.target_file = None
        self.di_file = None
        self.current_patch = None
        self.is_live_monitoring = False
        self.audio_stream = None
        
        # HIL system
        self.hil_matcher = None
        self.audio_manager = None
        self.is_optimizing = False
        
        # Enhanced components
        self.magicstomp_adapter = MagicstompAdapter()
        self.realtime_magicstomp = None
        self.current_effect_widget = None
        self.current_effect_type = None
        self.impact_visualizer = None
        
        # Parameter state
        self.original_parameters = {}
        self.target_parameters = {}
        self.current_parameters = {}
        
        # Initialize
        self.setup_styles()
        self.create_widgets()
        self.init_hil_system()
    
    def setup_styles(self):
        """Setup compact styling."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Standard font sizes
        style.configure('Title.TLabel', 
                       font=('Arial', 14, 'bold'),
                       foreground='#ecf0f1',
                       background='#2c3e50')
        
        style.configure('Section.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='#3498db',
                       background='#2c3e50')
        
        style.configure('Info.TLabel',
                       font=('Arial', 10),
                       foreground='#bdc3c7',
                       background='#2c3e50')
        
        style.configure('TButton',
                       font=('Arial', 10),
                       padding=(8, 4))
        
        style.configure('Large.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=(10, 6))
    
    def create_widgets(self):
        """Create tabbed interface."""
        # Main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_files_tab()
        self.create_effects_tab()
        self.create_analysis_tab()
        self.create_monitoring_tab()
        self.create_status_tab()
    
    def create_files_tab(self):
        """Create files selection tab."""
        self.files_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.files_frame, text="📁 Files")
        
        # Title
        title = ttk.Label(self.files_frame, text="File Selection", style='Title.TLabel')
        title.pack(pady=10)
        
        # Target file
        target_frame = ttk.LabelFrame(self.files_frame, text="Target Audio", padding=10)
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.target_var = tk.StringVar(value="No file selected")
        target_label = ttk.Label(target_frame, textvariable=self.target_var, width=50)
        target_label.pack(side=tk.LEFT, padx=(0, 10))
        
        target_btn = ttk.Button(target_frame, text="Select Target", 
                               command=self.select_target_file)
        target_btn.pack(side=tk.LEFT)
        
        # DI file
        di_frame = ttk.LabelFrame(self.files_frame, text="DI Audio", padding=10)
        di_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.di_var = tk.StringVar(value="No file selected")
        di_label = ttk.Label(di_frame, textvariable=self.di_var, width=50)
        di_label.pack(side=tk.LEFT, padx=(0, 10))
        
        di_btn = ttk.Button(di_frame, text="Select DI", 
                           command=self.select_di_file)
        di_btn.pack(side=tk.LEFT)
        
        # Generate patch button
        generate_btn = ttk.Button(self.files_frame, text="🎯 Generate Patch", 
                                 style='Large.TButton',
                                 command=self.generate_patch)
        generate_btn.pack(pady=20)
    
    def create_effects_tab(self):
        """Create effects configuration tab."""
        self.effects_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.effects_frame, text="🎛️ Effects")
        
        # Title
        title = ttk.Label(self.effects_frame, text="Magicstomp Effects", style='Title.TLabel')
        title.pack(pady=10)
        
        # Effect selection
        selection_frame = ttk.LabelFrame(self.effects_frame, text="Effect Selection", padding=10)
        selection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.effect_var = tk.StringVar()
        self.effect_combo = ttk.Combobox(selection_frame, textvariable=self.effect_var,
                                        state="readonly", width=40)
        self.effect_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        load_btn = ttk.Button(selection_frame, text="Load Effect",
                             command=self.load_effect_widget)
        load_btn.pack(side=tk.LEFT)

        download_btn = ttk.Button(selection_frame, text="📥 Download Current",
                                  command=self.download_current_patch)
        download_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Effect parameters (scrollable)
        params_frame = ttk.LabelFrame(self.effects_frame, text="Parameters", padding=10)
        params_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas for scrolling
        self.params_canvas = tk.Canvas(params_frame, height=300)
        self.params_scrollbar = ttk.Scrollbar(params_frame, orient="vertical", 
                                            command=self.params_canvas.yview)
        self.params_scrollable_frame = tk.Frame(self.params_canvas)
        
        self.params_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.params_canvas.configure(scrollregion=self.params_canvas.bbox("all"))
        )
        
        self.params_canvas.create_window((0, 0), window=self.params_scrollable_frame, anchor="nw")
        self.params_canvas.configure(yscrollcommand=self.params_scrollbar.set)
        
        self.params_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.params_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate effect list
        self.populate_effect_list()
    
    def create_analysis_tab(self):
        """Create analysis and impact visualization tab."""
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="📊 Analysis")
        
        # Title
        title = ttk.Label(self.analysis_frame, text="Parameter Impact Analysis", style='Title.TLabel')
        title.pack(pady=10)
        
        # Analysis controls
        controls_frame = ttk.Frame(self.analysis_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        analyze_btn = ttk.Button(controls_frame, text="📊 Analyze Current", 
                               command=self.analyze_current_parameters)
        analyze_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        generate_btn = ttk.Button(controls_frame, text="🎯 Generate Target", 
                                command=self.generate_target_parameters)
        generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        apply_btn = ttk.Button(controls_frame, text="✅ Apply Changes", 
                              command=self.apply_changes)
        apply_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        reset_btn = ttk.Button(controls_frame, text="🔄 Reset", 
                              command=self.reset_to_original)
        reset_btn.pack(side=tk.LEFT)
        
        # Impact visualization
        self.init_impact_visualizer()
    
    def create_monitoring_tab(self):
        """Create monitoring and optimization tab."""
        self.monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monitoring_frame, text="🎤 Monitor")
        
        # Title
        title = ttk.Label(self.monitoring_frame, text="Live Monitoring & Optimization", style='Title.TLabel')
        title.pack(pady=10)
        
        # Monitoring controls
        monitor_frame = ttk.LabelFrame(self.monitoring_frame, text="Live Monitoring", padding=10)
        monitor_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.monitor_btn = ttk.Button(monitor_frame, text="🎤 Start Monitoring", 
                                     style='Large.TButton',
                                     command=self.toggle_live_monitoring)
        self.monitor_btn.pack(pady=10)
        
        # Optimization controls
        opt_frame = ttk.LabelFrame(self.monitoring_frame, text="Optimization", padding=10)
        opt_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.optimize_btn = ttk.Button(opt_frame, text="🔄 Start Optimization", 
                                      style='Large.TButton',
                                      command=self.start_optimization)
        self.optimize_btn.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.monitoring_frame, variable=self.progress_var,
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=20)
    
    def create_status_tab(self):
        """Create status and logs tab."""
        self.status_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.status_frame, text="📈 Status")
        
        # Title
        title = ttk.Label(self.status_frame, text="Status & Logs", style='Title.TLabel')
        title.pack(pady=10)
        
        # Status text
        self.status_text = tk.Text(self.status_frame, height=20, width=80,
                                  font=('Courier', 9),
                                  bg='#2c3e50', fg='#ecf0f1',
                                  insertbackground='white')
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Clear button
        clear_btn = ttk.Button(self.status_frame, text="Clear Logs", 
                              command=self.clear_logs)
        clear_btn.pack(pady=5)
    
    def init_impact_visualizer(self):
        """Initialize impact visualizer in analysis tab."""
        self.impact_visualizer = ImpactVisualizer(self.analysis_frame)
    
    def populate_effect_list(self):
        """Populate effect selection dropdown."""
        supported_effects = EffectRegistry.get_supported_effects()
        
        effect_items = []
        for effect_type, name in supported_effects.items():
            effect_items.append(f"{name} (0x{effect_type:02X})")
        
        self.effect_combo['values'] = effect_items
        if effect_items:
            self.effect_combo.set(effect_items[0])
    
    def init_hil_system(self):
        """Initialize HIL system."""
        try:
            self.hil_matcher = HILToneMatcher()
            self.audio_manager = AudioDeviceManager()
            self.log_status("✅ HIL system initialized")
        except Exception as e:
            self.log_status(f"❌ HIL init error: {e}")
    
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

        if not self._set_effect_widget(effect_type):
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

    def _select_effect_in_combo(self, effect_name: str, effect_type: int) -> None:
        target = f"(0x{effect_type:02X})"
        values = self.effect_combo['values'] if self.effect_combo else []
        for item in values:
            if item.endswith(target) or item.startswith(effect_name):
                self.effect_combo.set(item)
                return

    def _set_effect_widget(self, effect_type: int, log_load: bool = True) -> bool:
        if self.current_effect_widget:
            self.current_effect_widget.destroy()

        widget = EffectRegistry.create_effect_widget(effect_type, self.params_scrollable_frame)
        if not widget:
            self.current_effect_widget = None
            return False

        widget.pack(fill=tk.X, padx=5, pady=5)
        self.current_effect_widget = widget

        self.setup_parameter_callbacks()
        if self.impact_visualizer:
            self.impact_visualizer.set_effect_widget(widget)

        self.current_effect_type = effect_type
        self.original_parameters = widget.get_all_parameters()
        self.current_parameters = self.original_parameters.copy()

        effect_name = EffectRegistry.get_effect_name(effect_type)
        self._select_effect_in_combo(effect_name, effect_type)

        if log_load:
            self.log_status(f"🎛️ Loaded: {effect_name}")

        return True

    @staticmethod
    def _extract_patch_name(common_section) -> str:
        if not common_section or len(common_section) < 28:
            return "Magicstomp Patch"

        name_bytes = bytes(common_section[16:28])
        try:
            name = name_bytes.decode('ascii', errors='ignore').strip()
        except Exception:
            name = ''.join(chr(b) for b in name_bytes if 32 <= b <= 126).strip()

        return name or "Magicstomp Patch"

    def download_current_patch(self):
        """Download current patch from Magicstomp and display it."""

        if self.realtime_magicstomp is None:
            try:
                self.realtime_magicstomp = RealtimeMagicstomp()
            except Exception as exc:  # pragma: no cover - dépend du matériel
                self.log_status(f"❌ MIDI init error: {exc}")
                messagebox.showerror("Magicstomp", f"Failed to initialize MIDI connection:\n{exc}")
                return

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

        effect_type = common_section[0]
        effect_name = EffectRegistry.get_effect_name(effect_type)

        if not EffectRegistry.is_effect_supported(effect_type):
            self.log_status(f"⚠️ Effect {effect_name} not supported in editor")
            messagebox.showwarning("Magicstomp", f"Effect {effect_name} (0x{effect_type:02X}) is not supported in the editor.")
            return

        if not self._set_effect_widget(effect_type, log_load=False):
            self.log_status(f"❌ Effect widget for {effect_name} not available")
            messagebox.showerror("Magicstomp", f"Unable to load widget for effect {effect_name}.")
            return

        applied_params = {}
        if hasattr(self.current_effect_widget, 'apply_magicstomp_data'):
            applied_params = self.current_effect_widget.apply_magicstomp_data(effect_section)

        self.current_parameters = self.current_effect_widget.get_all_parameters()
        self.original_parameters = self.current_parameters.copy()

        patch_name = self._extract_patch_name(common_section)
        self.current_patch = {
            'patch_index': patch_data.get('patch_index'),
            'effect_type': effect_type,
            'effect_name': effect_name,
            'patch_name': patch_name,
            'parameters': self.current_parameters,
            'common': common_section,
            'effect_bytes': effect_section,
        }

        self._select_effect_in_combo(effect_name, effect_type)

        self.log_status(f"✅ Patch downloaded: {patch_name} ({effect_name})")
        if applied_params:
            self.log_status(f"🎚️ Parameters applied: {len(applied_params)} values")
        else:
            self.log_status("ℹ️ Patch applied with default parameter mapping")

        messagebox.showinfo("Magicstomp", f"Patch '{patch_name}' downloaded from Magicstomp.")
    
    def on_parameter_changed(self, param_name: str, user_value, magicstomp_value: int):
        """Handle parameter changes."""
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        
        if self.target_parameters:
            self.update_impact_visualization()
        
        self.log_status(f"🎛️ {param_name}: {user_value}")
    
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
    
    def generate_patch(self):
        """Generate patch."""
        if not self.current_effect_widget:
            self.log_status("⚠️ No effect loaded")
            return
        
        if not self.target_file or not self.di_file:
            self.log_status("⚠️ Select both files")
            return
        
        self.log_status("🎯 Generating patch...")
        
        def generate_thread():
            try:
                current_params = self.current_effect_widget.get_all_parameters()
                
                magicstomp_params = {}
                for param_name, value in current_params.items():
                    for child in self.current_effect_widget.winfo_children():
                        if hasattr(child, 'param_name') and child.param_name == param_name:
                            magicstomp_value = self.current_effect_widget._convert_to_magicstomp(child, value)
                            magicstomp_params[param_name] = magicstomp_value
                            break
                
                for i in range(101):
                    self.root.after(0, lambda p=i: self.progress_var.set(p))
                    time.sleep(0.05)
                
                self.current_patch = {
                    "effect_type": self.current_effect_type,
                    "parameters": magicstomp_params,
                    "target_file": self.target_file,
                    "di_file": self.di_file
                }
                
                self.root.after(0, lambda: self.log_status(f"✅ Patch generated ({len(magicstomp_params)} params)"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_status(f"❌ Error: {e}"))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def start_optimization(self):
        """Start optimization."""
        if not self.current_patch:
            self.log_status("⚠️ Generate patch first")
            return
        
        if self.is_optimizing:
            self.log_status("⚠️ Already optimizing")
            return
        
        self.log_status("🔄 Optimizing...")
        self.is_optimizing = True
        
        def optimize_thread():
            try:
                for i in range(101):
                    self.root.after(0, lambda p=i: self.progress_var.set(p))
                    time.sleep(0.1)
                
                optimized_params = self.generate_smart_target_parameters(self.current_parameters)
                self.target_parameters = optimized_params
                
                self.root.after(0, self.update_impact_visualization)
                self.root.after(0, lambda: self.log_status("✅ Optimization done"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_status(f"❌ Error: {e}"))
            finally:
                self.root.after(0, lambda: setattr(self, 'is_optimizing', False))
        
        threading.Thread(target=optimize_thread, daemon=True).start()
    
    def toggle_live_monitoring(self):
        """Toggle live monitoring."""
        if not self.is_live_monitoring:
            self.start_live_monitoring()
        else:
            self.stop_live_monitoring()
    
    def start_live_monitoring(self):
        """Start live monitoring."""
        try:
            self.log_status("🎤 Starting monitoring...")
            self.is_live_monitoring = True
            self.monitor_btn.config(text="⏹️ Stop Monitoring")
            self.log_status("✅ Monitoring active")
        except Exception as e:
            self.log_status(f"❌ Error: {e}")
    
    def stop_live_monitoring(self):
        """Stop live monitoring."""
        try:
            self.is_live_monitoring = False
            self.monitor_btn.config(text="🎤 Start Monitoring")
            self.log_status("⏹️ Monitoring stopped")
        except Exception as e:
            self.log_status(f"❌ Error: {e}")
    
    def clear_logs(self):
        """Clear status logs."""
        self.status_text.delete(1.0, tk.END)
    
    def log_status(self, message: str):
        """Log status message."""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, log_message)
        self.status_text.see(tk.END)
        print(log_message.strip())
    
    def on_closing(self):
        """Handle window closing."""
        if self.is_live_monitoring:
            self.stop_live_monitoring()
        self.root.destroy()
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()


def main():
    """Main function."""
    app = TabbedCompactGUI()
    app.run()


if __name__ == "__main__":
    main()
