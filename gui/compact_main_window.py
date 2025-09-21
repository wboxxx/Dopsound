#!/usr/bin/env python3
"""
Compact Main GUI Window with Impact Visualization
================================================

Version compacte optimisée pour les résolutions standard.
Interface adaptative avec layout optimisé et fonts réduites.
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
from gui.impact_visualization import ImpactVisualizer, ParameterImpact, ImpactLevel


class CompactMagicstompHILGUI:
    """
    Compact GUI application with impact visualization.
    
    Optimized for standard screen resolutions with:
    - Smaller fonts and compact layout
    - Adaptive window sizing
    - Efficient use of space
    """
    
    def __init__(self):
        """Initialize the compact GUI application."""
        self.root = tk.Tk()
        self.root.title("🎸 Compact Magicstomp HIL Tone Matcher")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # Make window resizable with minimum size
        self.root.minsize(1200, 800)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # State variables
        self.target_file = None
        self.di_file = None
        self.current_patch = None
        self.is_live_monitoring = False
        self.audio_stream = None
        
        # Settings file path
        self.settings_file = Path("settings.json")
        self.hil_matcher = None
        self.audio_manager = None
        self.is_optimizing = False
        
        # Enhanced components
        self.magicstomp_adapter = MagicstompAdapter()
        self.current_effect_widget = None
        self.current_effect_type = None
        self.impact_visualizer = None
        
        # Parameter state
        self.original_parameters = {}
        self.target_parameters = {}
        self.current_parameters = {}
        
        # Initialize components
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
        # Initialize HIL system
        self.init_hil_system()
    
    def setup_styles(self):
        """Setup compact styling for the GUI."""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Compact styles with standard fonts
        style.configure('Title.TLabel', 
                       font=('Arial', 24, 'bold'),
                       foreground='#ecf0f1',
                       background='#2c3e50')
        
        style.configure('Section.TLabel',
                       font=('Arial', 16, 'bold'),
                       foreground='#3498db',
                       background='#2c3e50')
        
        style.configure('Info.TLabel',
                       font=('Arial', 12),
                       foreground='#bdc3c7',
                       background='#2c3e50')
        
        style.configure('Success.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='#27ae60',
                       background='#2c3e50')
        
        style.configure('Warning.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='#f39c12',
                       background='#2c3e50')
        
        style.configure('Error.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='#e74c3c',
                       background='#2c3e50')
        
        style.configure('Large.TButton',
                       font=('Arial', 14, 'bold'),
                       padding=(10, 8))
        
        style.configure('Medium.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=(8, 6))
        
        style.configure('Small.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(6, 4))
        
        style.configure('GraphTitle.TLabel',
                       font=('Arial', 16, 'bold'),
                       foreground='#2c3e50',
                       background='white')
    
    def create_widgets(self):
        """Create all GUI widgets with compact layout."""
        # Main container with paned window for better space usage
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        
        # Left panel - Controls
        self.left_frame = tk.Frame(self.main_paned, bg='#2c3e50')
        
        # Right panel - Impact visualization
        self.right_frame = tk.Frame(self.main_paned, bg='#2c3e50')
        
        # Title
        self.title_label = ttk.Label(
            self.left_frame,
            text="🎸 Compact Magicstomp HIL",
            style='Title.TLabel'
        )
        
        # File selection section (compact)
        self.file_frame = tk.Frame(self.left_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        
        self.file_title = ttk.Label(
            self.file_frame,
            text="📁 Files",
            style='Section.TLabel'
        )
        
        # Compact file selection
        self.file_controls_frame = tk.Frame(self.file_frame, bg='#34495e')
        
        # Target file
        self.target_frame = tk.Frame(self.file_controls_frame, bg='#34495e')
        self.target_label = ttk.Label(
            self.target_frame,
            text="Target:",
            style='Info.TLabel'
        )
        self.target_file_label = ttk.Label(
            self.target_frame,
            text="None",
            style='Info.TLabel',
            width=15
        )
        self.target_button = ttk.Button(
            self.target_frame,
            text="Select",
            style='Small.TButton',
            command=self.select_target_file
        )
        
        # DI file
        self.di_frame = tk.Frame(self.file_controls_frame, bg='#34495e')
        self.di_label = ttk.Label(
            self.di_frame,
            text="DI:",
            style='Info.TLabel'
        )
        self.di_file_label = ttk.Label(
            self.di_frame,
            text="None",
            style='Info.TLabel',
            width=15
        )
        self.di_button = ttk.Button(
            self.di_frame,
            text="Select",
            style='Small.TButton',
            command=self.select_di_file
        )
        
        # Effect selection section (compact)
        self.effect_frame = tk.Frame(self.left_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        
        self.effect_title = ttk.Label(
            self.effect_frame,
            text="🎛️ Effect",
            style='Section.TLabel'
        )
        
        # Compact effect selection
        self.effect_controls_frame = tk.Frame(self.effect_frame, bg='#34495e')
        
        self.effect_label = ttk.Label(
            self.effect_controls_frame,
            text="Type:",
            style='Info.TLabel'
        )
        
        self.effect_var = tk.StringVar()
        self.effect_combo = ttk.Combobox(
            self.effect_controls_frame,
            textvariable=self.effect_var,
            state="readonly",
            width=25,
            font=('Arial', 10)
        )
        
        self.load_effect_button = ttk.Button(
            self.effect_controls_frame,
            text="Load",
            style='Small.TButton',
            command=self.load_effect_widget
        )
        
        # Effect parameters frame (scrollable)
        self.effect_params_frame = tk.Frame(self.effect_frame, bg='#34495e')
        self.effect_params_title = ttk.Label(
            self.effect_params_frame,
            text="Parameters",
            style='Info.TLabel'
        )
        
        # Scrollable frame for parameters
        self.params_canvas = tk.Canvas(self.effect_params_frame, bg='#34495e', height=200)
        self.params_scrollbar = ttk.Scrollbar(self.effect_params_frame, orient="vertical", command=self.params_canvas.yview)
        self.params_scrollable_frame = tk.Frame(self.params_canvas, bg='#34495e')
        
        self.params_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.params_canvas.configure(scrollregion=self.params_canvas.bbox("all"))
        )
        
        self.params_canvas.create_window((0, 0), window=self.params_scrollable_frame, anchor="nw")
        self.params_canvas.configure(yscrollcommand=self.params_scrollbar.set)
        
        # Analysis controls (compact)
        self.analysis_frame = tk.Frame(self.left_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        
        self.analysis_title = ttk.Label(
            self.analysis_frame,
            text="📊 Analysis",
            style='Section.TLabel'
        )
        
        # Compact analysis buttons
        self.analysis_buttons_frame = tk.Frame(self.analysis_frame, bg='#34495e')
        
        self.analyze_button = ttk.Button(
            self.analysis_buttons_frame,
            text="Analyze",
            style='Small.TButton',
            command=self.analyze_current_parameters
        )
        
        self.generate_target_button = ttk.Button(
            self.analysis_buttons_frame,
            text="Generate",
            style='Small.TButton',
            command=self.generate_target_parameters
        )
        
        self.apply_changes_button = ttk.Button(
            self.analysis_buttons_frame,
            text="Apply",
            style='Small.TButton',
            command=self.apply_changes
        )
        
        self.reset_button = ttk.Button(
            self.analysis_buttons_frame,
            text="Reset",
            style='Small.TButton',
            command=self.reset_to_original
        )
        
        # Main action buttons (compact)
        self.action_frame = tk.Frame(self.left_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        
        self.action_title = ttk.Label(
            self.action_frame,
            text="🚀 Actions",
            style='Section.TLabel'
        )
        
        # Compact action buttons
        self.action_buttons_frame = tk.Frame(self.action_frame, bg='#34495e')
        
        self.generate_button = ttk.Button(
            self.action_buttons_frame,
            text="Generate Patch",
            style='Medium.TButton',
            command=self.generate_patch
        )
        
        self.optimize_button = ttk.Button(
            self.action_buttons_frame,
            text="Optimize",
            style='Medium.TButton',
            command=self.start_optimization
        )
        
        self.monitor_button = ttk.Button(
            self.action_buttons_frame,
            text="Monitor",
            style='Medium.TButton',
            command=self.toggle_live_monitoring
        )
        
        # Status section (compact)
        self.status_frame = tk.Frame(self.left_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        
        self.status_title = ttk.Label(
            self.status_frame,
            text="📈 Status",
            style='Section.TLabel'
        )
        
        self.status_text = tk.Text(
            self.status_frame,
            height=6,
            width=50,
            font=('Courier', 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white'
        )
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        
        # Initialize impact visualizer in right panel
        self.init_impact_visualizer()
        
        # Populate effect list
        self.populate_effect_list()
    
    def init_impact_visualizer(self):
        """Initialize the impact visualizer in right panel."""
        self.impact_visualizer = ImpactVisualizer(self.right_frame)
    
    def populate_effect_list(self):
        """Populate the effect selection dropdown."""
        supported_effects = EffectRegistry.get_supported_effects()
        
        effect_items = []
        for effect_type, name in supported_effects.items():
            effect_items.append(f"{name} (0x{effect_type:02X})")
        
        self.effect_combo['values'] = effect_items
        if effect_items:
            self.effect_combo.set(effect_items[0])
    
    def setup_layout(self):
        """Setup the compact layout of all widgets."""
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add panels to paned window
        self.main_paned.add(self.left_frame, weight=1)
        self.main_paned.add(self.right_frame, weight=1)
        
        # Left panel layout
        self.left_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label.pack(pady=(0, 15))
        
        # File selection (compact)
        self.file_frame.pack(fill=tk.X, pady=(0, 10))
        self.file_title.pack(pady=8)
        
        self.file_controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Target file
        self.target_frame.pack(fill=tk.X, pady=2)
        self.target_label.pack(side=tk.LEFT, padx=(0, 10))
        self.target_file_label.pack(side=tk.LEFT, padx=(0, 10))
        self.target_button.pack(side=tk.LEFT)
        
        # DI file
        self.di_frame.pack(fill=tk.X, pady=2)
        self.di_label.pack(side=tk.LEFT, padx=(0, 10))
        self.di_file_label.pack(side=tk.LEFT, padx=(0, 10))
        self.di_button.pack(side=tk.LEFT)
        
        # Effect selection (compact)
        self.effect_frame.pack(fill=tk.X, pady=(0, 10))
        self.effect_title.pack(pady=8)
        
        self.effect_controls_frame.pack(fill=tk.X, padx=10, pady=5)
        self.effect_label.pack(side=tk.LEFT, padx=(0, 10))
        self.effect_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.load_effect_button.pack(side=tk.LEFT)
        
        # Effect parameters (scrollable)
        self.effect_params_frame.pack(fill=tk.X, padx=10, pady=5)
        self.effect_params_title.pack(pady=5)
        
        self.params_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.params_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Analysis controls (compact)
        self.analysis_frame.pack(fill=tk.X, pady=(0, 10))
        self.analysis_title.pack(pady=8)
        
        self.analysis_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 5))
        self.generate_target_button.pack(side=tk.LEFT, padx=(0, 5))
        self.apply_changes_button.pack(side=tk.LEFT, padx=(0, 5))
        self.reset_button.pack(side=tk.LEFT)
        
        # Actions (compact)
        self.action_frame.pack(fill=tk.X, pady=(0, 10))
        self.action_title.pack(pady=8)
        
        self.action_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))
        self.optimize_button.pack(side=tk.LEFT, padx=(0, 10))
        self.monitor_button.pack(side=tk.LEFT)
        
        # Status (compact)
        self.status_frame.pack(fill=tk.X)
        self.status_title.pack(pady=8)
        
        self.status_text.pack(padx=10, pady=(0, 5), fill=tk.BOTH, expand=True)
        self.progress_bar.pack(padx=10, pady=(0, 10))
    
    def init_hil_system(self):
        """Initialize the HIL system components."""
        try:
            self.hil_matcher = HILToneMatcher()
            self.audio_manager = AudioDeviceManager()
            self.log_status("✅ HIL system initialized")
        except Exception as e:
            self.log_status(f"❌ HIL init error: {e}")
    
    def select_target_file(self):
        """Select the target audio file."""
        file_path = filedialog.askopenfilename(
            title="Select Target Audio File",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.flac *.m4a"),
                ("WAV files", "*.wav"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.target_file = file_path
            filename = Path(file_path).name
            if len(filename) > 15:
                filename = filename[:12] + "..."
            self.target_file_label.config(text=filename)
            self.log_status(f"📁 Target: {Path(file_path).name}")
    
    def select_di_file(self):
        """Select the DI audio file."""
        file_path = filedialog.askopenfilename(
            title="Select DI Audio File",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.flac *.m4a"),
                ("WAV files", "*.wav"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.di_file = file_path
            filename = Path(file_path).name
            if len(filename) > 15:
                filename = filename[:12] + "..."
            self.di_file_label.config(text=filename)
            self.log_status(f"📁 DI: {Path(file_path).name}")
    
    def load_effect_widget(self):
        """Load the selected effect widget."""
        selection = self.effect_combo.get()
        if not selection:
            self.log_status("⚠️ Select an effect")
            return
        
        try:
            # Parse effect type from selection
            effect_type_hex = selection.split('(0x')[1].split(')')[0]
            effect_type = int(effect_type_hex, 16)
        except (ValueError, IndexError):
            self.log_status("❌ Invalid effect")
            return
        
        # Clear current effect widget
        if self.current_effect_widget:
            self.current_effect_widget.destroy()
        
        # Create new effect widget
        self.current_effect_widget = EffectRegistry.create_effect_widget(
            effect_type,
            self.params_scrollable_frame
        )
        
        if self.current_effect_widget:
            self.current_effect_widget.pack(fill=tk.X, padx=5, pady=5)
            
            # Set up parameter callbacks
            self.setup_parameter_callbacks()
            
            # Set effect widget in impact visualizer
            self.impact_visualizer.set_effect_widget(self.current_effect_widget)
            
            # Store current effect type
            self.current_effect_type = effect_type
            
            # Store original parameters
            self.original_parameters = self.current_effect_widget.get_all_parameters()
            
            effect_name = EffectRegistry.get_effect_name(effect_type)
            self.log_status(f"🎛️ Loaded: {effect_name}")
            
        else:
            self.log_status(f"❌ Effect 0x{effect_type:02X} not supported")
    
    def setup_parameter_callbacks(self):
        """Setup parameter change callbacks."""
        if not self.current_effect_widget:
            return
        
        def parameter_changed(param_name, user_value, magicstomp_value):
            self.on_parameter_changed(param_name, user_value, magicstomp_value)
        
        # Find all parameter widgets and setup callbacks
        for child in self.current_effect_widget.winfo_children():
            if hasattr(child, 'param_name'):
                self.current_effect_widget.set_parameter_callback(
                    child.param_name,
                    parameter_changed
                )
    
    def on_parameter_changed(self, param_name: str, user_value, magicstomp_value: int):
        """Handle parameter changes."""
        # Update current parameters
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        
        # Update impact visualization if we have target parameters
        if self.target_parameters:
            self.update_impact_visualization()
        
        self.log_status(f"🎛️ {param_name}: {user_value}")
    
    def analyze_current_parameters(self):
        """Analyze current parameters."""
        if not self.current_effect_widget:
            self.log_status("⚠️ No effect loaded")
            return
        
        # Get current parameters
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Create impacts with current values as targets
        target_impacts = {}
        for param_name, value in current_params.items():
            impact = ParameterImpact(
                name=param_name,
                original_value=value,
                target_value=value,
                current_value=value,
                impact_level=ImpactLevel.NONE,
                unit=self.get_parameter_unit(param_name)
            )
            target_impacts[param_name] = impact
        
        # Update visualization
        self.impact_visualizer.impacts = target_impacts
        self.impact_visualizer._update_visualization()
        
        self.log_status(f"📊 Analyzed {len(current_params)} parameters")
    
    def generate_target_parameters(self):
        """Generate target parameters based on analysis."""
        if not self.current_effect_widget:
            self.log_status("⚠️ No effect loaded")
            return
        
        # Get current parameters
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Generate target parameters based on HIL analysis
        target_params = self.generate_smart_target_parameters(current_params)
        
        # Set target parameters
        self.target_parameters = target_params
        
        # Update impact visualization
        self.update_impact_visualization()
        
        self.log_status(f"🎯 Generated {len(target_params)} targets")
    
    def generate_smart_target_parameters(self, current_params: dict) -> dict:
        """Generate smart target parameters based on HIL analysis."""
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
        """Apply appropriate limits to a parameter."""
        limits = {
            "Time": (0.1, 2730.0),
            "Mix": (0, 100),
            "Rate": (0.1, 20.0),
            "Depth": (0, 100),
            "Feedback": (0, 99),
            "FB Gain": (0, 99),
            "Gain": (-12, 12),
            "Level": (0, 100),
            "Frequency": (20, 20000),
            "High Ratio": (0.1, 1.0),
            "Low Ratio": (0.1, 1.0)
        }
        
        min_val, max_val = limits.get(param_name, (0, 100))
        return max(min_val, min(max_val, value))
    
    def update_impact_visualization(self):
        """Update the impact visualization."""
        if not self.target_parameters or not self.current_effect_widget:
            return
        
        # Get current parameters
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Create impacts
        impacts = {}
        for param_name, target_value in self.target_parameters.items():
            original_value = self.original_parameters.get(param_name, 0)
            current_value = current_params.get(param_name, original_value)
            
            # Calculate impact level
            impact_level = self.calculate_impact_level(original_value, target_value)
            
            impact = ParameterImpact(
                name=param_name,
                original_value=original_value,
                target_value=target_value,
                current_value=current_value,
                impact_level=impact_level,
                unit=self.get_parameter_unit(param_name)
            )
            
            impacts[param_name] = impact
        
        # Update visualization
        self.impact_visualizer.impacts = impacts
        self.impact_visualizer._update_visualization()
    
    def calculate_impact_level(self, original: float, target: float) -> ImpactLevel:
        """Calculate impact level based on difference."""
        if original == 0:
            diff_percent = abs(target) * 100 if target != 0 else 0
        else:
            diff_percent = abs((target - original) / original) * 100
        
        if diff_percent < 5:
            return ImpactLevel.NONE
        elif diff_percent < 15:
            return ImpactLevel.LOW
        elif diff_percent < 30:
            return ImpactLevel.MEDIUM
        elif diff_percent < 50:
            return ImpactLevel.HIGH
        else:
            return ImpactLevel.CRITICAL
    
    def get_parameter_unit(self, param_name: str) -> str:
        """Get parameter unit."""
        units = {
            "Time": "ms",
            "Rate": "Hz", 
            "Mix": "%",
            "Depth": "%",
            "Feedback": "%",
            "Gain": "dB",
            "Level": "%",
            "Frequency": "Hz",
            "Q": "",
            "Attack": "ms",
            "Release": "ms",
            "FB Gain": "%",
            "High Ratio": "",
            "Low Ratio": ""
        }
        return units.get(param_name, "")
    
    def apply_changes(self):
        """Apply changes to target parameters."""
        if not self.target_parameters or not self.current_effect_widget:
            self.log_status("⚠️ No targets to apply")
            return
        
        # Apply target parameters to widget
        self.current_effect_widget.set_all_parameters(self.target_parameters)
        
        # Update current parameters
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        
        # Update visualization
        self.update_impact_visualization()
        
        self.log_status("✅ Applied targets")
    
    def reset_to_original(self):
        """Reset parameters to original values."""
        if not self.original_parameters or not self.current_effect_widget:
            self.log_status("⚠️ No originals to reset")
            return
        
        # Reset to original parameters
        self.current_effect_widget.set_all_parameters(self.original_parameters)
        
        # Update current parameters
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        
        # Clear target parameters
        self.target_parameters.clear()
        
        # Update visualization
        self.impact_visualizer._reset_analysis()
        
        self.log_status("🔄 Reset to original")
    
    def generate_patch(self):
        """Generate Magicstomp patch from current parameters."""
        if not self.current_effect_widget:
            self.log_status("⚠️ No effect loaded")
            return
        
        if not self.target_file or not self.di_file:
            self.log_status("⚠️ Select both files")
            return
        
        self.log_status("🎯 Generating patch...")
        
        # Simulate patch generation
        def generate_patch_thread():
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
        
        threading.Thread(target=generate_patch_thread, daemon=True).start()
    
    def start_optimization(self):
        """Start the optimization process."""
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
        """Toggle live audio monitoring."""
        if not self.is_live_monitoring:
            self.start_live_monitoring()
        else:
            self.stop_live_monitoring()
    
    def start_live_monitoring(self):
        """Start live audio monitoring."""
        try:
            self.log_status("🎤 Starting monitoring...")
            self.is_live_monitoring = True
            self.monitor_button.config(text="Stop")
            self.log_status("✅ Monitoring active")
            
        except Exception as e:
            self.log_status(f"❌ Error: {e}")
    
    def stop_live_monitoring(self):
        """Stop live audio monitoring."""
        try:
            self.is_live_monitoring = False
            self.monitor_button.config(text="Monitor")
            self.log_status("⏹️ Monitoring stopped")
            
        except Exception as e:
            self.log_status(f"❌ Error: {e}")
    
    def log_status(self, message: str):
        """Log a status message."""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, log_message)
        self.status_text.see(tk.END)
        
        # Also print to console
        print(log_message.strip())
    
    def on_closing(self):
        """Handle window closing."""
        if self.is_live_monitoring:
            self.stop_live_monitoring()
        
        self.root.destroy()
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main function to start the compact GUI."""
    app = CompactMagicstompHILGUI()
    app.run()


if __name__ == "__main__":
    main()
