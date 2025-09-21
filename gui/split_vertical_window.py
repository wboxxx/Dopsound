#!/usr/bin/env python3
"""
Split Vertical GUI Window with Impact Visualization
==================================================

Version avec split vertical permanent :
- 80% gauche : Interface principale avec onglets
- 20% droite : Status/Logs toujours visible
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


class SplitVerticalGUI:
    """
    GUI avec split vertical permanent.
    
    Layout:
    - 80% gauche : Interface principale avec onglets
    - 20% droite : Status/Logs toujours visible
    """
    
    def __init__(self):
        """Initialize the split vertical GUI."""
        self.root = tk.Tk()
        self.root.title("🎸 Magicstomp HIL - Split Vertical")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # Minimum size
        self.root.minsize(1200, 700)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # State variables
        self.target_file = None
        self.di_file = None
        self.current_patch = None
        self.is_live_monitoring = False
        self.is_live_di_capturing = False
        self.audio_stream = None
        self.live_di_stream = None
        self.analysis_data = {}
        
        # Audio/MIDI settings
        self.audio_input_device = None
        self.audio_output_device = None
        self.midi_input_device = None
        self.midi_output_device = None
        self.sample_rate = 44100
        self.buffer_size = 1024
        self.audio_channels = 2
        self.midi_channels = [1]  # Default to channel 1
        
        # HIL system
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
        
        # Settings file path
        self.settings_file = Path("magicstomp_gui_settings.json")
        
        # Initialize
        self.setup_styles()
        self.create_widgets()
        self.init_hil_system()
        self.load_settings()
    
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
        
        style.configure('StatusTitle.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='#e74c3c',
                       background='#34495e')
        
        style.configure('TButton',
                       font=('Arial', 10),
                       padding=(8, 4))
        
        style.configure('Large.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=(10, 6))
    
    def create_widgets(self):
        """Create split vertical interface."""
        # Main paned window with vertical split
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel (80%) - Main interface
        self.left_panel = ttk.Frame(self.main_paned)
        
        # Right panel (20%) - Status/Logs
        self.right_panel = ttk.Frame(self.main_paned)
        
        # Add panels to paned window
        self.main_paned.add(self.left_panel, weight=4)  # 80%
        self.main_paned.add(self.right_panel, weight=1)  # 20%
        
        # Create left panel content (main interface)
        self.create_main_interface()
        
        # Create right panel content (status/logs)
        self.create_status_panel()
        
        # Initialize devices after status panel is created
        self.initialize_devices()
    
    def initialize_devices(self):
        """Initialize audio and MIDI devices after GUI is created."""
        # Initialize devices in a separate thread to avoid blocking GUI
        def init_devices_thread():
            try:
                self.refresh_audio_devices()
                self.refresh_midi_devices()
            except Exception as e:
                # Fallback if status_text is still not available
                print(f"Error initializing devices: {e}")
        
        threading.Thread(target=init_devices_thread, daemon=True).start()
    
    def load_settings(self):
        """Load settings from file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                # Load audio settings
                if 'audio_input_device' in settings:
                    self.audio_input_var.set(settings['audio_input_device'])
                if 'audio_output_device' in settings:
                    self.audio_output_var.set(settings['audio_output_device'])
                if 'sample_rate' in settings:
                    self.sample_rate_var.set(str(settings['sample_rate']))
                if 'buffer_size' in settings:
                    self.buffer_size_var.set(str(settings['buffer_size']))
                if 'audio_channels' in settings:
                    self.audio_channels_var.set(str(settings['audio_channels']))
                
                # Load MIDI settings
                if 'midi_input_device' in settings:
                    self.midi_input_var.set(settings['midi_input_device'])
                if 'midi_output_device' in settings:
                    self.midi_output_var.set(settings['midi_output_device'])
                if 'midi_channels' in settings:
                    # Restore MIDI channel selections
                    for channel in settings['midi_channels']:
                        if channel in self.midi_channel_vars:
                            self.midi_channel_vars[channel].set(True)
                    self.midi_channels = settings['midi_channels']
                
                # Load window settings
                if 'window_geometry' in settings:
                    self.root.geometry(settings['window_geometry'])
                
                # Load last used files
                if 'last_target_file' in settings and settings['last_target_file']:
                    self.target_file = settings['last_target_file']
                    if hasattr(self, 'target_var'):
                        self.target_var.set(f"Target: {Path(self.target_file).name}")
                    self.log_status(f"📁 Restored target: {Path(self.target_file).name}")
                
                if 'last_di_file' in settings and settings['last_di_file']:
                    self.di_file = settings['last_di_file']
                    if hasattr(self, 'di_var'):
                        self.di_var.set(f"DI: {Path(self.di_file).name}")
                    self.log_status(f"📁 Restored DI: {Path(self.di_file).name}")
                
                self.log_status("✅ Settings loaded successfully")
            else:
                self.log_status("ℹ️ No settings file found - using defaults")
                
        except Exception as e:
            self.log_status(f"⚠️ Error loading settings: {e}")
    
    def save_last_file_selections(self):
        """Save last used file selections immediately."""
        try:
            # Load existing settings
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
            else:
                settings = {}
            
            # Update file selections
            settings['last_target_file'] = str(self.target_file) if self.target_file else ''
            settings['last_di_file'] = str(self.di_file) if self.di_file else ''
            
            # Save back to file
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            print(f"🔍 DEBUG: Saved file selections - Target: {self.target_file}, DI: {self.di_file}")
            
        except Exception as e:
            print(f"🔍 DEBUG: Error saving file selections: {e}")
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            settings = {
                # Audio settings
                'audio_input_device': self.audio_input_var.get() if hasattr(self, 'audio_input_var') else '',
                'audio_output_device': self.audio_output_var.get() if hasattr(self, 'audio_output_var') else '',
                'sample_rate': int(self.sample_rate_var.get()) if hasattr(self, 'sample_rate_var') else 44100,
                'buffer_size': int(self.buffer_size_var.get()) if hasattr(self, 'buffer_size_var') else 1024,
                'audio_channels': int(self.audio_channels_var.get()) if hasattr(self, 'audio_channels_var') else 2,
                
                # MIDI settings
                'midi_input_device': self.midi_input_var.get() if hasattr(self, 'midi_input_var') else '',
                'midi_output_device': self.midi_output_var.get() if hasattr(self, 'midi_output_var') else '',
                'midi_channels': self.midi_channels,
                
                # Window settings
                'window_geometry': self.root.geometry(),
                
                # Last used files
                'last_target_file': str(self.target_file) if self.target_file else '',
                'last_di_file': str(self.di_file) if self.di_file else '',
                
                # Current effect
                'last_effect_type': self.current_effect_type,
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            self.log_status("✅ Settings saved successfully")
            
        except Exception as e:
            self.log_status(f"⚠️ Error saving settings: {e}")
    
    def reset_settings(self):
        """Reset settings to default values."""
        try:
            # Reset audio settings to defaults
            if hasattr(self, 'sample_rate_var'):
                self.sample_rate_var.set("44100")
            if hasattr(self, 'buffer_size_var'):
                self.buffer_size_var.set("1024")
            if hasattr(self, 'audio_channels_var'):
                self.audio_channels_var.set("2")
            
            # Reset MIDI channels to default (channel 1 only)
            for channel, var in self.midi_channel_vars.items():
                var.set(channel == 1)
            self.midi_channels = [1]
            
            # Reset file selections
            self.target_file = None
            self.di_file = None
            if hasattr(self, 'target_var'):
                self.target_var.set("No file selected")
            if hasattr(self, 'di_var'):
                self.di_var.set("No file selected")
            
            # Reset effect
            self.current_effect_type = None
            if hasattr(self, 'current_effect_var'):
                self.current_effect_var.set("No effect loaded")
            
            self.log_status("🔄 Settings reset to defaults")
            self.settings_status.config(text="Settings reset to defaults")
            
        except Exception as e:
            self.log_status(f"⚠️ Error resetting settings: {e}")
    
    def create_main_interface(self):
        """Create main interface in left panel."""
        # Main notebook in left panel
        self.notebook = ttk.Notebook(self.left_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_files_tab()
        self.create_effects_tab()
        self.create_analysis_tab()
        self.create_monitoring_tab()
        self.create_settings_tab()
    
    def create_status_panel(self):
        """Create status panel in right panel."""
        # Status panel title
        status_title = ttk.Label(self.right_panel, text="📊 Status & Logs", 
                                style='StatusTitle.TLabel')
        status_title.pack(pady=10, padx=5)
        
        # Status info frame
        info_frame = ttk.LabelFrame(self.right_panel, text="Current Status", padding=5)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Current effect info
        self.current_effect_var = tk.StringVar(value="No effect loaded")
        effect_label = ttk.Label(info_frame, textvariable=self.current_effect_var, 
                                style='Info.TLabel')
        effect_label.pack(pady=2)
        
        # Files info
        self.files_status_var = tk.StringVar(value="No files selected")
        files_label = ttk.Label(info_frame, textvariable=self.files_status_var, 
                               style='Info.TLabel')
        files_label.pack(pady=2)
        
        # Monitoring status
        self.monitoring_var = tk.StringVar(value="Monitoring: OFF")
        monitoring_label = ttk.Label(info_frame, textvariable=self.monitoring_var, 
                                    style='Info.TLabel')
        monitoring_label.pack(pady=2)
        
        # Optimization status
        self.optimization_var = tk.StringVar(value="Optimization: IDLE")
        optimization_label = ttk.Label(info_frame, textvariable=self.optimization_var, 
                                      style='Info.TLabel')
        optimization_label.pack(pady=2)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.right_panel, variable=self.progress_var,
                                          maximum=100, length=200)
        self.progress_bar.pack(pady=10, padx=5)
        
        # Logs frame
        logs_frame = ttk.LabelFrame(self.right_panel, text="Live Logs", padding=5)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status text with scrollbar
        self.status_text = tk.Text(logs_frame, height=25, width=30,
                                  font=('Courier', 9),
                                  bg='#2c3e50', fg='#ecf0f1',
                                  insertbackground='white',
                                  wrap=tk.WORD)
        
        self.status_scrollbar = ttk.Scrollbar(logs_frame, orient="vertical", 
                                             command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=self.status_scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear logs button
        clear_btn = ttk.Button(self.right_panel, text="Clear Logs", 
                              command=self.clear_logs)
        clear_btn.pack(pady=5)
    
    def create_files_tab(self):
        """Create files selection tab."""
        self.files_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.files_frame, text="📁 Files")
        
        # Title
        title = ttk.Label(self.files_frame, text="File Selection & Analysis", style='Title.TLabel')
        title.pack(pady=10)
        
        # Workflow guide
        workflow_frame = ttk.LabelFrame(self.files_frame, text="📋 Workflow Guide", padding=10)
        workflow_frame.pack(fill=tk.X, padx=10, pady=5)
        
        workflow_text = """1. Select Target Audio (the sound you want to reproduce)
2. Select DI Audio (dry guitar signal)
3. Analyze files to verify they're compatible
4. Go to Effects tab to load a Magicstomp effect
5. Generate patch to create the initial configuration
6. Use Analysis tab to visualize parameter impacts
7. Use Monitor tab for live optimization"""
        
        workflow_label = ttk.Label(workflow_frame, text=workflow_text, 
                                  style='Info.TLabel', justify=tk.LEFT)
        workflow_label.pack(anchor=tk.W)
        
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
        di_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Live DI capture button
        self.live_di_btn = ttk.Button(di_frame, text="🎤 Live DI Capture", 
                                     command=self.toggle_live_di_capture)
        self.live_di_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Live DI status
        self.live_di_var = tk.StringVar(value="Live DI: OFF")
        self.live_di_status = ttk.Label(di_frame, textvariable=self.live_di_var, 
                                       style='Info.TLabel')
        self.live_di_status.pack(side=tk.LEFT, padx=(10, 0))
        
        # Audio Analysis section
        analysis_frame = ttk.LabelFrame(self.files_frame, text="Audio Analysis", padding=10)
        analysis_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Analysis buttons
        analysis_buttons_frame = ttk.Frame(analysis_frame)
        analysis_buttons_frame.pack(fill=tk.X)
        
        analyze_target_btn = ttk.Button(analysis_buttons_frame, text="📊 Analyze Target", 
                                       command=self.analyze_target_audio)
        analyze_target_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        analyze_di_btn = ttk.Button(analysis_buttons_frame, text="📊 Analyze DI", 
                                   command=self.analyze_di_audio)
        analyze_di_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        compare_btn = ttk.Button(analysis_buttons_frame, text="🔄 Compare Files", 
                                command=self.compare_audio_files)
        compare_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Analysis results display
        self.analysis_results = tk.Text(analysis_frame, height=8, width=70,
                                       font=('Courier', 9),
                                       bg='#2c3e50', fg='#ecf0f1',
                                       insertbackground='white')
        self.analysis_results.pack(fill=tk.X, pady=(10, 0))
        
        # Generate patch button
        # Generate Patch Button with Save/Load
        patch_buttons_frame = ttk.Frame(self.files_frame)
        patch_buttons_frame.pack(pady=10)
        
        generate_btn = ttk.Button(patch_buttons_frame, text="🎯 Generate Patch", 
                                 style='Large.TButton',
                                 command=self.generate_patch)
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_patch_btn = ttk.Button(patch_buttons_frame, text="💾 Save Patch", 
                                   command=self.save_patch)
        save_patch_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        load_patch_btn = ttk.Button(patch_buttons_frame, text="📂 Load Patch", 
                                   command=self.load_patch)
        load_patch_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        apply_patch_btn = ttk.Button(patch_buttons_frame, text="🎛️ Apply to Effects", 
                                    command=self.apply_patch_to_effects)
        apply_patch_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        send_patch_btn = ttk.Button(patch_buttons_frame, text="📤 Send to Magicstomp", 
                                   command=self.send_patch_to_magicstomp)
        send_patch_btn.pack(side=tk.LEFT)
    
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
        
        # Effect parameters (scrollable)
        params_frame = ttk.LabelFrame(self.effects_frame, text="Parameters", padding=10)
        params_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas for scrolling
        self.params_canvas = tk.Canvas(params_frame, height=400)
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
        
        analyze_btn = ttk.Button(controls_frame, text="📊 Analyze", 
                               command=self.analyze_current_parameters)
        analyze_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        generate_btn = ttk.Button(controls_frame, text="🎯 Generate", 
                                command=self.generate_target_parameters)
        generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        apply_btn = ttk.Button(controls_frame, text="✅ Apply", 
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
        
        # Quick actions
        actions_frame = ttk.LabelFrame(self.monitoring_frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        quick_analyze_btn = ttk.Button(actions_frame, text="Quick Analyze", 
                                      command=self.quick_analyze)
        quick_analyze_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        quick_generate_btn = ttk.Button(actions_frame, text="Quick Generate", 
                                       command=self.quick_generate)
        quick_generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        quick_apply_btn = ttk.Button(actions_frame, text="Quick Apply", 
                                    command=self.quick_apply)
        quick_apply_btn.pack(side=tk.LEFT)
    
    def create_settings_tab(self):
        """Create settings tab for audio and MIDI configuration."""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙️ Settings")
        
        # Title
        title = ttk.Label(self.settings_frame, text="Audio & MIDI Settings", style='Title.TLabel')
        title.pack(pady=10)
        
        # Audio Settings
        audio_frame = ttk.LabelFrame(self.settings_frame, text="🎤 Audio Settings", padding=10)
        audio_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Audio Input Device
        input_frame = ttk.Frame(audio_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Input Device:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.audio_input_var = tk.StringVar()
        self.audio_input_combo = ttk.Combobox(input_frame, textvariable=self.audio_input_var,
                                             state="readonly", width=40)
        self.audio_input_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_audio_btn = ttk.Button(input_frame, text="🔄 Refresh", 
                                      command=self.refresh_audio_devices)
        refresh_audio_btn.pack(side=tk.LEFT)
        
        # Audio Output Device
        output_frame = ttk.Frame(audio_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Output Device:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.audio_output_var = tk.StringVar()
        self.audio_output_combo = ttk.Combobox(output_frame, textvariable=self.audio_output_var,
                                              state="readonly", width=40)
        self.audio_output_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Audio Parameters
        params_frame = ttk.Frame(audio_frame)
        params_frame.pack(fill=tk.X, pady=10)
        
        # Sample Rate
        sample_frame = ttk.Frame(params_frame)
        sample_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(sample_frame, text="Sample Rate:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.sample_rate_var = tk.StringVar(value="44100")
        sample_rate_combo = ttk.Combobox(sample_frame, textvariable=self.sample_rate_var,
                                        values=["22050", "44100", "48000", "88200", "96000"],
                                        state="readonly", width=15)
        sample_rate_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Buffer Size
        buffer_frame = ttk.Frame(params_frame)
        buffer_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(buffer_frame, text="Buffer Size:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.buffer_size_var = tk.StringVar(value="1024")
        buffer_size_combo = ttk.Combobox(buffer_frame, textvariable=self.buffer_size_var,
                                        values=["256", "512", "1024", "2048", "4096"],
                                        state="readonly", width=15)
        buffer_size_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Audio Channels
        channels_frame = ttk.Frame(params_frame)
        channels_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(channels_frame, text="Channels:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.audio_channels_var = tk.StringVar(value="2")
        channels_combo = ttk.Combobox(channels_frame, textvariable=self.audio_channels_var,
                                     values=["1", "2", "4", "6", "8"],
                                     state="readonly", width=15)
        channels_combo.pack(side=tk.LEFT)
        
        # MIDI Settings
        midi_frame = ttk.LabelFrame(self.settings_frame, text="🎹 MIDI Settings", padding=10)
        midi_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # MIDI Input Device
        midi_input_frame = ttk.Frame(midi_frame)
        midi_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(midi_input_frame, text="MIDI Input:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.midi_input_var = tk.StringVar()
        self.midi_input_combo = ttk.Combobox(midi_input_frame, textvariable=self.midi_input_var,
                                            state="readonly", width=40)
        self.midi_input_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_midi_btn = ttk.Button(midi_input_frame, text="🔄 Refresh", 
                                     command=self.refresh_midi_devices)
        refresh_midi_btn.pack(side=tk.LEFT)
        
        # MIDI Output Device
        midi_output_frame = ttk.Frame(midi_frame)
        midi_output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(midi_output_frame, text="MIDI Output:", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.midi_output_var = tk.StringVar()
        self.midi_output_combo = ttk.Combobox(midi_output_frame, textvariable=self.midi_output_var,
                                             state="readonly", width=40)
        self.midi_output_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # MIDI Channels
        midi_channels_frame = ttk.Frame(midi_frame)
        midi_channels_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(midi_channels_frame, text="MIDI Channels:", style='Info.TLabel').pack(anchor=tk.W)
        
        # MIDI Channel selection (checkboxes for channels 1-16)
        self.midi_channel_vars = {}
        channels_grid = ttk.Frame(midi_channels_frame)
        channels_grid.pack(fill=tk.X, pady=5)
        
        for i in range(1, 17):
            var = tk.BooleanVar(value=(i == 1))  # Default to channel 1
            self.midi_channel_vars[i] = var
            
            cb = ttk.Checkbutton(channels_grid, text=f"Ch{i}", variable=var,
                                command=lambda ch=i: self.update_midi_channels(ch))
            cb.grid(row=(i-1)//4, column=(i-1)%4, padx=5, pady=2, sticky='w')
        
        # Test Audio Button
        test_audio_frame = ttk.LabelFrame(self.settings_frame, text="🎧 Test Audio", padding=10)
        test_audio_frame.pack(fill=tk.X, padx=10, pady=5)
        
        test_audio_btn = ttk.Button(test_audio_frame, text="🎵 Test Audio Setup", 
                                   style='Large.TButton',
                                   command=self.test_audio_setup)
        test_audio_btn.pack(pady=5)
        
        # Status display for audio test
        self.audio_test_status = ttk.Label(test_audio_frame, text="Ready to test", 
                                          style='Info.TLabel')
        self.audio_test_status.pack(pady=5)
        
        # Settings Management
        settings_mgmt_frame = ttk.LabelFrame(self.settings_frame, text="💾 Settings Management", padding=10)
        settings_mgmt_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Save/Load buttons
        buttons_frame = ttk.Frame(settings_mgmt_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        save_btn = ttk.Button(buttons_frame, text="💾 Save Settings", 
                             command=self.save_settings)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        load_btn = ttk.Button(buttons_frame, text="📂 Load Settings", 
                             command=self.load_settings)
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        reset_btn = ttk.Button(buttons_frame, text="🔄 Reset to Defaults", 
                              command=self.reset_settings)
        reset_btn.pack(side=tk.LEFT)
        
        # Settings status
        self.settings_status = ttk.Label(settings_mgmt_frame, text="Settings ready", 
                                        style='Info.TLabel')
        self.settings_status.pack(pady=5)
        
        # Note: Device refresh will be called after status panel is created
    
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
            self.update_status_info()
        except Exception as e:
            self.log_status(f"❌ HIL init error: {e}")
    
    def update_status_info(self):
        """Update status information in right panel."""
        # Update current effect
        if self.current_effect_type is not None:
            effect_name = EffectRegistry.get_effect_name(self.current_effect_type)
            self.current_effect_var.set(f"Effect: {effect_name}")
        else:
            self.current_effect_var.set("No effect loaded")
        
        # Update files status
        files_count = 0
        if self.target_file:
            files_count += 1
        if self.di_file or self.is_live_di_capturing:
            files_count += 1
        
        if files_count == 2:
            if self.is_live_di_capturing:
                self.files_status_var.set("Files: Ready (Live DI)")
            else:
                self.files_status_var.set("Files: Ready")
        elif files_count == 1:
            if self.is_live_di_capturing:
                self.files_status_var.set("Files: Target + Live DI")
            else:
                self.files_status_var.set("Files: 1/2 selected")
        else:
            self.files_status_var.set("Files: None selected")
        
        # Update monitoring status
        if self.is_live_monitoring:
            self.monitoring_var.set("Monitoring: ON")
        else:
            self.monitoring_var.set("Monitoring: OFF")
        
        # Update optimization status
        if self.is_optimizing:
            self.optimization_var.set("Optimization: RUNNING")
        else:
            self.optimization_var.set("Optimization: IDLE")
    
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
            self.log_status(f"🎛️ Loaded: {effect_name}")
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
    
    def analyze_target_audio(self):
        """Analyze target audio file using AutoToneMatcher."""
        if not self.target_file:
            self.log_status("⚠️ No target file selected")
            print("🔍 DEBUG: No target file selected")
            return
        
        def analyze_thread():
            try:
                self.log_status("📊 Starting target audio analysis...")
                print("🔍 DEBUG: Starting analyze_target_audio()")
                print(f"🔍 DEBUG: Target file: {self.target_file}")
                
                # Try to use AutoToneMatcher for real analysis
                try:
                    self.log_status("🔧 Creating tone matcher...")
                    print("🔍 DEBUG: Creating AutoToneMatcher...")
                    
                    from auto_tone_match_magicstomp import AutoToneMatcher
                    tone_matcher = AutoToneMatcher('essentia')  # Use essentia backend
                    print("🔍 DEBUG: AutoToneMatcher created successfully")
                    self.log_status("✅ Tone matcher created")
                    
                    # Analyze audio with detailed debug
                    self.log_status("🎵 Analyzing audio features...")
                    print("🔍 DEBUG: Calling tone_matcher.analyze_audio()...")
                    
                    features = tone_matcher.analyze_audio(self.target_file, verbose=True)
                    print(f"🔍 DEBUG: Analysis features: {features}")
                    self.log_status("✅ Audio features extracted")
                    
                    # Map to patch with debug
                    self.log_status("🎛️ Mapping features to patch...")
                    print("🔍 DEBUG: Calling tone_matcher.map_to_patch()...")
                    
                    patch = tone_matcher.map_to_patch()
                    print(f"🔍 DEBUG: Generated patch: {patch}")
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
                    
                    # Auto-generate patch proposal if effect is loaded
                    if self.current_effect_widget:
                        self.root.after(0, self.auto_generate_patch_proposal)
                    
                except Exception as e:
                    print(f"🔍 DEBUG: AutoToneMatcher error: {e}")
                    import traceback
                    traceback.print_exc()
                    self.log_status(f"⚠️ Using fallback analysis: {e}")
                    
                    # Fallback to basic analysis
                    self.log_status("📊 Running fallback analysis...")
                    print("🔍 DEBUG: Running fallback analysis...")
                    
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
                    
                    print(f"🔍 DEBUG: Fallback analysis completed: {self.analysis_data['target']}")
                    self.root.after(0, lambda: self.display_analysis_results(results))
                    self.root.after(0, lambda: self.log_status("✅ Fallback analysis completed"))
                    
                    # Generate basic patch from fallback analysis
                    self.root.after(0, self.generate_basic_patch_from_fallback)
                    
                    # Auto-generate patch proposal if effect is loaded
                    if self.current_effect_widget:
                        self.root.after(0, self.auto_generate_patch_proposal)
                
            except Exception as e:
                print(f"🔍 DEBUG: Fatal error in analyze_thread: {e}")
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: self.log_status(f"❌ Analysis error: {e}"))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def generate_basic_patch_from_fallback(self):
        """Generate basic patch from fallback analysis data."""
        print("🔍 DEBUG: Starting generate_basic_patch_from_fallback()")
        
        if 'target' not in self.analysis_data:
            print("🔍 DEBUG: No target analysis data for basic patch generation")
            return
        
        try:
            target_data = self.analysis_data['target']
            print(f"🔍 DEBUG: Target data for basic patch: {target_data}")
            
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
            print(f"🔍 DEBUG: Generated basic patch: {basic_patch}")
            
            # Display patch parameters
            self.display_patch_parameters()
            
            self.log_status("✅ Basic patch generated from fallback analysis")
            
            # Save the target file used for this patch
            self.save_last_file_selections()
            
            # Try to apply patch to current effect widget if available
            if self.current_effect_widget and hasattr(self.current_effect_widget, 'set_all_parameters'):
                try:
                    print("🔍 DEBUG: Applying basic patch to current effect widget...")
                    
                    # Convert patch to widget parameters
                    widget_params = self.convert_patch_to_widget_params(basic_patch)
                    print(f"🔍 DEBUG: Converted widget params: {widget_params}")
                    
                    if widget_params:
                        # Apply parameters to effect widget
                        self.current_effect_widget.set_all_parameters(widget_params)
                        self.current_parameters = widget_params
                        
                        # Store as target parameters for impact visualization
                        self.target_parameters = widget_params.copy()
                        
                        # Update impact visualization
                        if self.impact_visualizer:
                            print("🔍 DEBUG: Updating impact visualization with basic patch...")
                            self.update_impact_visualization()
                        
                        self.log_status("🎛️ Basic patch applied to current effect!")
                        self.log_status("💡 Go to Analysis tab to see the parameter impacts!")
                        print("🔍 DEBUG: Basic patch successfully applied to effect widget")
                    else:
                        self.log_status("⚠️ Could not convert patch to widget parameters")
                        self.log_status("💡 Load an effect in Effects tab to apply parameters")
                        
                except Exception as e:
                    print(f"🔍 DEBUG: Error applying basic patch to effect: {e}")
                    import traceback
                    traceback.print_exc()
                    self.log_status(f"⚠️ Error applying patch to effect: {e}")
                    self.log_status("💡 Load an effect in Effects tab to apply parameters")
            else:
                self.log_status("💡 Load an effect in Effects tab to apply parameters")
                print("🔍 DEBUG: No effect widget loaded - patch ready for manual application")
            
        except Exception as e:
            print(f"🔍 DEBUG: Error generating basic patch: {e}")
            import traceback
            traceback.print_exc()
            self.log_status(f"❌ Error generating basic patch: {e}")
    
    def display_patch_parameters(self):
        """Display patch parameters in the GUI."""
        if not self.current_patch:
            self.log_status("⚠️ No patch to display")
            print("🔍 DEBUG: No patch to display")
            return
        
        try:
            self.log_status("🎛️ Displaying patch parameters...")
            print("🔍 DEBUG: Displaying patch parameters...")
            print(f"🔍 DEBUG: Patch data: {self.current_patch}")
            
            # Clear existing widgets
            if hasattr(self, 'patch_display_frame'):
                for widget in self.patch_display_frame.winfo_children():
                    widget.destroy()
            else:
                # Create frame if it doesn't exist
                self.patch_display_frame = ttk.LabelFrame(self.files_frame, 
                                                        text="🎛️ Generated Patch Parameters",
                                                        padding=10)
                self.patch_display_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Display patch parameters
            row = 0
            for section_name, section_data in self.current_patch.items():
                if isinstance(section_data, dict) and section_name != 'meta':
                    # Section header
                    ttk.Label(self.patch_display_frame,
                             text=f"{section_name.upper()}:",
                             style='Section.TLabel').grid(row=row, column=0, columnspan=2, sticky='w', pady=(10, 5))
                    row += 1
                    
                    # Parameters in this section
                    for param_name, param_value in section_data.items():
                        if param_name != 'enabled':
                            ttk.Label(self.patch_display_frame,
                                     text=f"  {param_name}:",
                                     style='Info.TLabel').grid(row=row, column=0, sticky='w', padx=20)
                            
                            value_text = f"{param_value:.4f}" if isinstance(param_value, (int, float)) else str(param_value)
                            ttk.Label(self.patch_display_frame,
                                     text=value_text,
                                     style='Info.TLabel').grid(row=row, column=1, sticky='w', padx=10)
                            row += 1
            
            self.log_status("✅ Patch parameters displayed")
            print("🔍 DEBUG: Patch parameters displayed successfully")
            
        except Exception as e:
            self.log_status(f"❌ Error displaying patch: {e}")
            print(f"🔍 DEBUG: Error displaying patch: {e}")
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
        print("🔍 DEBUG: Starting auto_generate_patch_proposal()")
        
        if not self.analysis_data.get('target'):
            self.log_status("⚠️ No target analysis data available")
            print("🔍 DEBUG: No target analysis data")
            return
        
        self.log_status("🤖 Auto-generating patch proposal based on analysis...")
        print("🔍 DEBUG: Auto-generating patch proposal based on analysis...")
        
        # Get target analysis data
        target_data = self.analysis_data['target']
        print(f"🔍 DEBUG: Target data: {target_data}")
        
        # Generate smart parameters based on analysis
        proposed_params = self.generate_smart_parameters_from_analysis(target_data)
        print(f"🔍 DEBUG: Generated proposed_params: {proposed_params}")
        
        if proposed_params:
            print("🔍 DEBUG: Applying parameters to effect widget...")
            
            # Apply proposed parameters to widget
            if self.current_effect_widget and hasattr(self.current_effect_widget, 'set_all_parameters'):
                self.current_effect_widget.set_all_parameters(proposed_params)
                print("🔍 DEBUG: Parameters applied to effect widget")
            else:
                print("🔍 DEBUG: No effect widget or set_all_parameters method")
                self.log_status("⚠️ No effect widget loaded")
            
            self.current_parameters = proposed_params
            
            # Store as target parameters for impact visualization
            self.target_parameters = proposed_params.copy()
            
            # Update impact visualization
            if self.impact_visualizer:
                print("🔍 DEBUG: Updating impact visualization...")
                self.update_impact_visualization()
                print("🔍 DEBUG: Impact visualization updated")
            else:
                print("🔍 DEBUG: No impact visualizer available")
            
            param_names = list(proposed_params.keys())
            self.log_status(f"🤖 Auto-generated {len(param_names)} parameters: {', '.join(param_names)}")
            self.log_status("💡 Go to Analysis tab to see the parameter impacts!")
            print(f"🔍 DEBUG: Auto-generation completed with {len(param_names)} parameters")
        else:
            self.log_status("⚠️ Could not generate patch proposal")
            print("🔍 DEBUG: Could not generate patch proposal")
    
    def generate_smart_parameters_from_analysis(self, target_data):
        """Generate smart parameters based on audio analysis."""
        print("🔍 DEBUG: Starting generate_smart_parameters_from_analysis()")
        proposed_params = {}
        
        if not self.current_effect_type:
            print("🔍 DEBUG: No current_effect_type")
            return proposed_params
        
        print(f"🔍 DEBUG: Current effect type: {self.current_effect_type}")
        print(f"🔍 DEBUG: Target data: {target_data}")
        
        # Get peak frequency for intelligent parameter setting
        peak_freq = target_data.get('peak_frequency', 1000)
        rms_level = target_data.get('rms_level', 0.5)
        duration = target_data.get('duration', 1.0)
        
        print(f"🔍 DEBUG: Using analysis data - peak_freq: {peak_freq}, rms: {rms_level}, duration: {duration}")
        
        # Handle multi-channel peak frequency
        if isinstance(peak_freq, str) and peak_freq == "Multi-channel":
            peak_freq = 1000  # Default frequency for multi-channel
            print("🔍 DEBUG: Multi-channel detected, using default frequency 1000Hz")
        
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
        
        print(f"🔍 DEBUG: Final proposed_params: {proposed_params}")
        return proposed_params
    
    def generate_patch(self):
        """Generate patch."""
        print("🔍 DEBUG: Starting generate_patch()")
        
        if not self.target_file:
            self.log_status("⚠️ Please select target file first")
            print("🔍 DEBUG: No target file selected")
            return
        
        if not (self.di_file or self.is_live_di_capturing):
            self.log_status("⚠️ Please select DI file or start live DI capture")
            print("🔍 DEBUG: No DI file or live capture")
            return
        
        if not self.current_effect_widget:
            self.log_status("⚠️ Please load an effect first (go to Effects tab)")
            print("🔍 DEBUG: No current effect widget")
            return
        
        self.log_status("🎯 Generating patch...")
        print("🔍 DEBUG: Starting patch generation...")
        print(f"🔍 DEBUG: Target file: {self.target_file}")
        print(f"🔍 DEBUG: DI file: {self.di_file}")
        print(f"🔍 DEBUG: Live DI capturing: {self.is_live_di_capturing}")
        print(f"🔍 DEBUG: Current effect type: {self.current_effect_type}")
        
        def generate_thread():
            try:
                print("🔍 DEBUG: Getting current parameters from effect widget...")
                current_params = self.current_effect_widget.get_all_parameters()
                print(f"🔍 DEBUG: Current parameters: {current_params}")
                
                magicstomp_params = {}
                for param_name, value in current_params.items():
                    print(f"🔍 DEBUG: Processing parameter: {param_name} = {value}")
                    for child in self.current_effect_widget.winfo_children():
                        if hasattr(child, 'param_name') and child.param_name == param_name:
                            magicstomp_value = self.current_effect_widget._convert_to_magicstomp(child, value)
                            magicstomp_params[param_name] = magicstomp_value
                            print(f"🔍 DEBUG: Converted {param_name}: {value} -> {magicstomp_value}")
                            break
                
                print(f"🔍 DEBUG: Final magicstomp_params: {magicstomp_params}")
                
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
                
                print(f"🔍 DEBUG: Generated patch: {self.current_patch}")
                
                self.root.after(0, lambda: self.log_status(f"✅ Patch generated ({len(magicstomp_params)} params)"))
                self.root.after(0, lambda: self.log_status(f"🎛️ Effect: {EffectRegistry.get_effect_name(self.current_effect_type)}"))
                
                # Display patch parameters
                self.root.after(0, self.display_patch_parameters)
                
            except Exception as e:
                print(f"🔍 DEBUG: Error in generate_thread: {e}")
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: self.log_status(f"❌ Error generating patch: {e}"))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def apply_patch_to_effects(self):
        """Apply current patch to loaded effect widgets."""
        print("🔍 DEBUG: Starting apply_patch_to_effects()")
        
        if not self.current_patch:
            self.log_status("⚠️ No patch to apply")
            print("🔍 DEBUG: No current patch to apply")
            return
        
        if not self.current_effect_widget:
            self.log_status("⚠️ No effect loaded - please load an effect in Effects tab first")
            print("🔍 DEBUG: No current effect widget")
            return
        
        try:
            self.log_status("🎛️ Applying patch to current effect...")
            print("🔍 DEBUG: Applying patch to current effect...")
            print(f"🔍 DEBUG: Current patch: {self.current_patch}")
            
            # Convert patch to widget parameters
            widget_params = self.convert_patch_to_widget_params(self.current_patch)
            print(f"🔍 DEBUG: Converted widget params: {widget_params}")
            
            if widget_params:
                # Apply parameters to effect widget
                if hasattr(self.current_effect_widget, 'set_all_parameters'):
                    self.current_effect_widget.set_all_parameters(widget_params)
                    print("🔍 DEBUG: Parameters applied to effect widget")
                else:
                    self.log_status("⚠️ Effect widget doesn't support set_all_parameters")
                    print("🔍 DEBUG: Effect widget doesn't support set_all_parameters")
                    return
                
                # Update current parameters
                self.current_parameters = widget_params
                
                # Store as target parameters for impact visualization
                self.target_parameters = widget_params.copy()
                
                # Update impact visualization
                if self.impact_visualizer:
                    print("🔍 DEBUG: Updating impact visualization...")
                    self.update_impact_visualization()
                    print("🔍 DEBUG: Impact visualization updated")
                else:
                    print("🔍 DEBUG: No impact visualizer available")
                
                param_names = list(widget_params.keys())
                self.log_status(f"✅ Applied {len(param_names)} parameters to effect")
                self.log_status("💡 Go to Analysis tab to see the parameter impacts!")
                print(f"🔍 DEBUG: Successfully applied {len(param_names)} parameters: {param_names}")
                
            else:
                self.log_status("⚠️ Could not convert patch to widget parameters")
                print("🔍 DEBUG: Could not convert patch to widget parameters")
                
        except Exception as e:
            self.log_status(f"❌ Error applying patch to effects: {e}")
            print(f"🔍 DEBUG: Error applying patch to effects: {e}")
            import traceback
            traceback.print_exc()
    
    def save_patch(self):
        """Save current patch to file."""
        print("🔍 DEBUG: Starting save_patch()")
        
        if not self.current_patch:
            self.log_status("⚠️ No patch to save")
            print("🔍 DEBUG: No current patch to save")
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
                print("🔍 DEBUG: User cancelled patch save")
                return
            
            print(f"🔍 DEBUG: Saving patch to: {patch_file}")
            
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
            print(f"🔍 DEBUG: Patch saved successfully to {patch_file}")
            
        except Exception as e:
            self.log_status(f"❌ Error saving patch: {e}")
            print(f"🔍 DEBUG: Error saving patch: {e}")
            import traceback
            traceback.print_exc()
    
    def load_patch(self):
        """Load patch from file."""
        print("🔍 DEBUG: Starting load_patch()")
        
        try:
            # Ask user for file location
            patch_file = filedialog.askopenfilename(
                title="Load Patch",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not patch_file:
                print("🔍 DEBUG: User cancelled patch load")
                return
            
            print(f"🔍 DEBUG: Loading patch from: {patch_file}")
            
            # Load from file
            with open(patch_file, 'r') as f:
                patch_data = json.load(f)
            
            # Extract patch and metadata
            if 'patch' in patch_data:
                self.current_patch = patch_data['patch']
                metadata = patch_data.get('metadata', {})
                
                print(f"🔍 DEBUG: Loaded patch: {self.current_patch}")
                print(f"🔍 DEBUG: Metadata: {metadata}")
                
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
                
                # Try to identify and auto-load effects from patch
                self.auto_load_effects_from_patch()
                
                # If effect is loaded, apply parameters
                if self.current_effect_widget and hasattr(self.current_effect_widget, 'set_all_parameters'):
                    # Convert patch parameters to widget parameters
                    widget_params = self.convert_patch_to_widget_params(self.current_patch)
                    if widget_params:
                        self.current_effect_widget.set_all_parameters(widget_params)
                        self.current_parameters = widget_params
                        self.log_status("🎛️ Parameters applied to current effect")
                        self.log_status("💡 Go to Effects tab to see the visual representation!")
                        print(f"🔍 DEBUG: Applied parameters to effect: {widget_params}")
                        
                        # Auto-update impact visualization after applying patch
                        self.root.after(100, self.update_impact_visualization)
                        self.log_status("📊 Impact visualization updated automatically")
                else:
                    self.log_status("💡 Load an effect in Effects tab, then click '🎛️ Apply to Effects' to see visual representation")
                    print("🔍 DEBUG: No effect loaded - patch ready for manual application")
                
            else:
                self.log_status("⚠️ Invalid patch file format")
                print("🔍 DEBUG: Invalid patch file - no 'patch' key found")
                
        except Exception as e:
            self.log_status(f"❌ Error loading patch: {e}")
            print(f"🔍 DEBUG: Error loading patch: {e}")
            import traceback
            traceback.print_exc()
    
    def convert_patch_to_widget_params(self, patch):
        """Convert patch format to widget parameters format."""
        print("🔍 DEBUG: Starting convert_patch_to_widget_params()")
        print(f"🔍 DEBUG: Input patch: {patch}")
        
        try:
            widget_params = {}
            
            # Extract parameters from patch sections
            for section_name, section_data in patch.items():
                if isinstance(section_data, dict) and section_name != 'meta':
                    print(f"🔍 DEBUG: Processing section: {section_name}")
                    for param_name, param_value in section_data.items():
                        if param_name != 'enabled':
                            # Apply parameter limits if needed
                            limited_value = self.apply_parameter_limits(param_name, param_value)
                            widget_params[param_name] = limited_value
                            print(f"🔍 DEBUG: {param_name}: {param_value} -> {limited_value}")
            
            print(f"🔍 DEBUG: Final converted widget params: {widget_params}")
            return widget_params
            
        except Exception as e:
            print(f"🔍 DEBUG: Error converting patch: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def auto_load_effects_from_patch(self):
        """Auto-identify and load effects from patch data."""
        print("🔍 DEBUG: Starting auto_load_effects_from_patch()")
        
        if not self.current_patch:
            print("🔍 DEBUG: No current patch to analyze")
            return
        
        try:
            # Analyze patch to identify effects
            identified_effects = self.identify_effects_from_patch(self.current_patch)
            print(f"🔍 DEBUG: Identified effects: {identified_effects}")
            
            if identified_effects:
                # Try to load the first identified effect
                effect_to_load = identified_effects[0]  # Load the first/most important effect
                print(f"🔍 DEBUG: Auto-loading effect: {effect_to_load}")
                
                # Load the effect
                success = self.load_effect_by_name(effect_to_load)
                if success:
                    self.log_status(f"🎛️ Auto-loaded effect: {effect_to_load}")
                    print(f"🔍 DEBUG: Successfully auto-loaded effect: {effect_to_load}")
                    
                    # Auto-apply patch parameters to the loaded effect
                    if self.current_patch and self.current_effect_widget and hasattr(self.current_effect_widget, 'set_all_parameters'):
                        widget_params = self.convert_patch_to_widget_params(self.current_patch)
                        if widget_params:
                            self.current_effect_widget.set_all_parameters(widget_params)
                            self.current_parameters = widget_params
                            self.target_parameters = widget_params.copy()
                            
                            # Update impact visualization
                            self.root.after(100, self.update_impact_visualization)
                            self.log_status("📊 Impact visualization updated automatically")
                            self.log_status("🎛️ Patch parameters applied to auto-loaded effect")
                            print(f"🔍 DEBUG: Auto-applied patch parameters: {widget_params}")
                else:
                    self.log_status(f"⚠️ Could not auto-load effect: {effect_to_load}")
                    print(f"🔍 DEBUG: Failed to auto-load effect: {effect_to_load}")
            else:
                print("🔍 DEBUG: No effects identified in patch")
                self.log_status("💡 No specific effects identified in patch - manual selection required")
                
        except Exception as e:
            print(f"🔍 DEBUG: Error in auto_load_effects_from_patch: {e}")
            import traceback
            traceback.print_exc()
    
    def identify_effects_from_patch(self, patch):
        """Identify effects from patch data."""
        print("🔍 DEBUG: Starting identify_effects_from_patch()")
        print(f"🔍 DEBUG: Analyzing patch: {patch}")
        
        identified_effects = []
        
        try:
            # Check patch sections to identify effects
            for section_name, section_data in patch.items():
                if isinstance(section_data, dict) and section_name != 'meta':
                    print(f"🔍 DEBUG: Analyzing section: {section_name}")
                    
                    # Map section names to effect names
                    effect_mapping = {
                        'compressor': 'Compressor',
                        'eq': 'EQ',
                        'delay': 'Mono Delay',
                        'stereo_delay': 'Stereo Delay',
                        'tape_echo': 'Tape Echo',
                        'chorus': 'Chorus',
                        'flanger': 'Flanger',
                        'phaser': 'Phaser',
                        'overdrive': 'Overdrive',
                        'distortion': 'Distortion',
                        'fuzz': 'Fuzz',
                        'reverb': 'Reverb',
                        'gate': 'Gate',
                        'limiter': 'Limiter'
                    }
                    
                    if section_name in effect_mapping:
                        effect_name = effect_mapping[section_name]
                        if effect_name not in identified_effects:
                            identified_effects.append(effect_name)
                            print(f"🔍 DEBUG: Identified effect: {effect_name}")
            
            print(f"🔍 DEBUG: Final identified effects: {identified_effects}")
            return identified_effects
            
        except Exception as e:
            print(f"🔍 DEBUG: Error identifying effects: {e}")
            return []
    
    def load_effect_by_name(self, effect_name):
        """Load an effect by name."""
        print(f"🔍 DEBUG: Starting load_effect_by_name: {effect_name}")
        
        try:
            # Map effect names to effect types
            effect_type_mapping = {
                'Compressor': 0x01,
                'EQ': 0x02,
                'Mono Delay': 0x0D,
                'Stereo Delay': 0x0E,
                'Tape Echo': 0x0F,
                'Chorus': 0x03,
                'Flanger': 0x04,
                'Phaser': 0x05,
                'Overdrive': 0x06,
                'Distortion': 0x07,
                'Fuzz': 0x08,
                'Reverb': 0x09,
                'Gate': 0x0A,
                'Limiter': 0x0B
            }
            
            if effect_name in effect_type_mapping:
                effect_type = effect_type_mapping[effect_name]
                print(f"🔍 DEBUG: Effect type for {effect_name}: {effect_type}")
                
                # Load the effect widget
                success = self.load_effect_widget_by_type(effect_type)
                if success:
                    print(f"🔍 DEBUG: Successfully loaded effect widget for {effect_name}")
                    return True
                else:
                    print(f"🔍 DEBUG: Failed to load effect widget for {effect_name}")
                    return False
            else:
                print(f"🔍 DEBUG: Unknown effect name: {effect_name}")
                return False
                
        except Exception as e:
            print(f"🔍 DEBUG: Error loading effect by name: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_effect_widget_by_type(self, effect_type):
        """Load effect widget by type number."""
        print(f"🔍 DEBUG: Starting load_effect_widget_by_type: {effect_type}")
        
        try:
            # Get effect widget from registry
            if hasattr(self, 'effect_registry'):
                effect_class = self.effect_registry.get_effect_class(effect_type)
                if effect_class:
                    # Create and load the effect widget
                    self.current_effect_widget = effect_class(self.effects_frame)
                    self.current_effect_type = effect_type
                    
                    # Update UI
                    if hasattr(self, 'current_effect_var'):
                        effect_name = self.effect_registry.get_effect_name(effect_type)
                        self.current_effect_var.set(f"Loaded: {effect_name}")
                    
                    print(f"🔍 DEBUG: Successfully loaded effect widget type {effect_type}")
                    return True
                else:
                    print(f"🔍 DEBUG: Effect class not found for type {effect_type}")
                    return False
            else:
                print("🔍 DEBUG: Effect registry not available")
                return False
                
        except Exception as e:
            print(f"🔍 DEBUG: Error loading effect widget by type: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def send_patch_to_magicstomp(self):
        """Send current patch to Magicstomp device."""
        print("🔍 DEBUG: Starting send_patch_to_magicstomp()")
        
        if not self.current_patch:
            self.log_status("⚠️ No patch to send")
            print("🔍 DEBUG: No current patch to send")
            return
        
        try:
            self.log_status("📤 Sending patch to Magicstomp...")
            print("🔍 DEBUG: Starting patch send process...")
            print(f"🔍 DEBUG: Current patch: {self.current_patch}")
            
            # Import the adapter
            from adapter_magicstomp import MagicstompAdapter
            adapter = MagicstompAdapter()
            
            # List available MIDI ports first
            print("🔍 DEBUG: Listing MIDI ports...")
            adapter.list_midi_ports()
            
            # Convert patch to SysEx
            print("🔍 DEBUG: Converting patch to SysEx...")
            syx_data = adapter.json_to_syx(self.current_patch, patch_number=0)
            print(f"🔍 DEBUG: SysEx data length: {len(syx_data)} bytes")
            print(f"🔍 DEBUG: SysEx header: {syx_data[:10]}...")
            
            # Get selected MIDI port from settings
            midi_output = self.midi_output_var.get() if hasattr(self, 'midi_output_var') else None
            if not midi_output:
                self.log_status("⚠️ Please select MIDI output device in Settings tab")
                print("🔍 DEBUG: No MIDI output device selected")
                return
            
            # Send to device
            print(f"🔍 DEBUG: Sending to MIDI port: {midi_output}")
            adapter.send_syx_to_device(syx_data, midi_output)
            
            self.log_status("✅ Patch sent to Magicstomp successfully!")
            print("🔍 DEBUG: Patch sent successfully")
            
        except Exception as e:
            self.log_status(f"❌ Error sending patch: {e}")
            print(f"🔍 DEBUG: Error sending patch: {e}")
            import traceback
            traceback.print_exc()
    
    def refresh_audio_devices(self):
        """Refresh audio device list."""
        try:
            import sounddevice as sd
            
            # Get input devices
            input_devices = []
            output_devices = []
            
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                device_name = f"{device['name']} (ID: {i})"
                if device['max_input_channels'] > 0:
                    input_devices.append(device_name)
                if device['max_output_channels'] > 0:
                    output_devices.append(device_name)
            
            # Update comboboxes
            self.audio_input_combo['values'] = input_devices
            self.audio_output_combo['values'] = output_devices
            
            # Set default selections
            if input_devices and not self.audio_input_var.get():
                self.audio_input_var.set(input_devices[0])
            if output_devices and not self.audio_output_var.get():
                self.audio_output_var.set(output_devices[0])
            
            self.log_status(f"🔄 Found {len(input_devices)} input, {len(output_devices)} output audio devices")
            
        except ImportError:
            self.log_status("⚠️ sounddevice not available - using default audio")
            self.audio_input_combo['values'] = ["Default Input"]
            self.audio_output_combo['values'] = ["Default Output"]
            self.audio_input_var.set("Default Input")
            self.audio_output_var.set("Default Output")
        except Exception as e:
            self.log_status(f"❌ Error refreshing audio devices: {e}")
    
    def refresh_midi_devices(self):
        """Refresh MIDI device list."""
        try:
            import mido
            
            # Get MIDI devices
            input_names = mido.get_input_names()
            output_names = mido.get_output_names()
            
            # Update comboboxes
            self.midi_input_combo['values'] = input_names
            self.midi_output_combo['values'] = output_names
            
            # Set default selections
            if input_names and not self.midi_input_var.get():
                self.midi_input_var.set(input_names[0])
            if output_names and not self.midi_output_var.get():
                self.midi_output_var.set(output_names[0])
            
            self.log_status(f"🔄 Found {len(input_names)} MIDI input, {len(output_names)} MIDI output devices")
            
        except ImportError:
            self.log_status("⚠️ mido not available - using default MIDI")
            self.midi_input_combo['values'] = ["Default MIDI Input"]
            self.midi_output_combo['values'] = ["Default MIDI Output"]
            self.midi_input_var.set("Default MIDI Input")
            self.midi_output_var.set("Default MIDI Output")
        except Exception as e:
            self.log_status(f"❌ Error refreshing MIDI devices: {e}")
    
    def update_midi_channels(self, channel):
        """Update selected MIDI channels."""
        self.midi_channels = []
        for ch, var in self.midi_channel_vars.items():
            if var.get():
                self.midi_channels.append(ch)
        
        self.log_status(f"🎹 MIDI channels updated: {self.midi_channels}")
    
    def test_audio_setup(self):
        """Test the audio setup."""
        self.log_status("🎵 Testing audio setup...")
        
        try:
            import sounddevice as sd
            import numpy as np
            
            # Get settings
            sample_rate = int(self.sample_rate_var.get())
            buffer_size = int(self.buffer_size_var.get())
            
            # Create test tone
            duration = 1.0  # 1 second test
            frequency = 440  # A4 note
            t = np.linspace(0, duration, int(sample_rate * duration))
            test_tone = np.sin(2 * np.pi * frequency * t) * 0.1  # Low volume
            
            self.audio_test_status.config(text="Playing test tone...")
            
            # Play test tone
            sd.play(test_tone, samplerate=sample_rate, blocksize=buffer_size)
            sd.wait()  # Wait until finished
            
            self.audio_test_status.config(text="Test completed - check audio output")
            self.log_status("✅ Audio test completed")
            
        except ImportError:
            self.log_status("⚠️ sounddevice not available for testing")
            self.audio_test_status.config(text="sounddevice not available")
        except Exception as e:
            self.log_status(f"❌ Audio test failed: {e}")
            self.audio_test_status.config(text=f"Test failed: {e}")
    
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
        self.update_status_info()
        
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
                self.root.after(0, self.update_status_info)
        
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
            self.update_status_info()
            self.log_status("✅ Monitoring active")
        except Exception as e:
            self.log_status(f"❌ Error: {e}")
    
    def stop_live_monitoring(self):
        """Stop live monitoring."""
        try:
            self.is_live_monitoring = False
            self.monitor_btn.config(text="🎤 Start Monitoring")
            self.update_status_info()
            self.log_status("⏹️ Monitoring stopped")
        except Exception as e:
            self.log_status(f"❌ Error: {e}")
    
    def quick_analyze(self):
        """Quick analyze action."""
        self.log_status("⚡ Quick analyze...")
        self.analyze_current_parameters()
    
    def quick_generate(self):
        """Quick generate action."""
        self.log_status("⚡ Quick generate...")
        self.generate_target_parameters()
    
    def quick_apply(self):
        """Quick apply action."""
        self.log_status("⚡ Quick apply...")
        self.apply_changes()
    
    def clear_logs(self):
        """Clear status logs."""
        self.status_text.delete(1.0, tk.END)
    
    def log_status(self, message: str):
        """Log status message."""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Check if status_text is available
        if hasattr(self, 'status_text') and self.status_text:
            try:
                self.status_text.insert(tk.END, log_message)
                self.status_text.see(tk.END)
            except:
                # Fallback to console if GUI not ready
                print(log_message.strip())
        else:
            # Fallback to console if status_text not available
            print(log_message.strip())
    
    def on_closing(self):
        """Handle window closing."""
        try:
            # Stop all active processes
            if self.is_live_monitoring:
                self.stop_live_monitoring()
            if self.is_live_di_capturing:
                self.stop_live_di_capture()
            
            # Ensure audio stream is stopped
            self.stop_audio_capture()
            
            # Save settings before closing
            self.save_settings()
            
            self.log_status("👋 Application closing - settings saved")
            
        except Exception as e:
            print(f"Error during closing: {e}")
        finally:
            self.root.destroy()
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()


def main():
    """Main function."""
    app = SplitVerticalGUI()
    app.run()


if __name__ == "__main__":
    main()
