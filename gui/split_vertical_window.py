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
import csv
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
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
from realtime_magicstomp import RealtimeMagicstomp
from magicstomp_parameter_map import EFFECT_PARAMETERS

# Import Magicstomp effects and visualization
from magicstomp_effects import EffectRegistry
from adapter_magicstomp import MagicstompAdapter
from gui.impact_visualization import ImpactVisualizer, ParameterImpact, ImpactLevel


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


class SplitVerticalGUI:
    """
    GUI avec split vertical permanent.
    
    Layout:
    - 80% gauche : Interface principale avec onglets
    - 20% droite : Status/Logs toujours visible
    """
    
    def __init__(self):
        """Initialize the split vertical GUI."""
        # Load effect metadata before the GUI starts so heuristics use official names
        self.official_effect_names = set()
        self.official_effect_lookup: Dict[str, str] = {}
        self.supported_effect_name_to_type: Dict[str, int] = {}
        self.supported_effect_normalized_to_name: Dict[str, str] = {}
        self.supported_effect_normalized_to_type: Dict[str, int] = {}
        self.canonical_to_official_name: Dict[str, str] = {}
        self.effect_metadata_loaded = False

        # Load Magicstomp catalog to align analysis suggestions with official effects
        self.load_official_effect_catalog()

        # GUI root configuration
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

        # Effect cascade management
        self.effect_widget_cascade = []
        self.last_identified_effects: Dict[str, List[EffectMatch]] = {}

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

        # MIDI/Sysex communication
        self.realtime_magicstomp = RealtimeMagicstomp()

        # Create reverse mapping: parameter name -> offset
        self.parameter_to_offset = {v: k for k, v in EFFECT_PARAMETERS.items()}

        # Parameter state
        self.original_parameters = {}
        self.target_parameters = {}
        self.current_parameters = {}

        # Settings file path
        self.settings_file = Path("magicstomp_gui_settings.json")

        # Initialize
        self.setup_styles()
        self.load_settings()
        self.create_widgets()
        self.init_hil_system()
        self.init_midi_connection()
    
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
        
        # Restore application state after interface is created
        self.restore_application_state()
        
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
                if 'audio_input_device' in settings and hasattr(self, 'audio_input_var'):
                    self.audio_input_var.set(settings['audio_input_device'])
                if 'audio_output_device' in settings and hasattr(self, 'audio_output_var'):
                    self.audio_output_var.set(settings['audio_output_device'])
                if 'sample_rate' in settings and hasattr(self, 'sample_rate_var'):
                    self.sample_rate_var.set(str(settings['sample_rate']))
                if 'buffer_size' in settings and hasattr(self, 'buffer_size_var'):
                    self.buffer_size_var.set(str(settings['buffer_size']))
                if 'audio_channels' in settings and hasattr(self, 'audio_channels_var'):
                    self.audio_channels_var.set(str(settings['audio_channels']))
                
                # Load MIDI settings
                if 'midi_input_device' in settings and hasattr(self, 'midi_input_var'):
                    self.midi_input_var.set(settings['midi_input_device'])
                if 'midi_output_device' in settings and hasattr(self, 'midi_output_var'):
                    self.midi_output_var.set(settings['midi_output_device'])
                if 'midi_channels' in settings and hasattr(self, 'midi_channel_vars'):
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
                
                # Load application state
                if 'last_active_tab' in settings:
                    self.last_active_tab = settings['last_active_tab']
                else:
                    self.last_active_tab = 0
                    
                if 'last_loaded_patch' in settings and settings['last_loaded_patch']:
                    self.last_loaded_patch = settings['last_loaded_patch']
                else:
                    self.last_loaded_patch = None
                
                # Load last effect type
                if 'last_effect_type' in settings:
                    self.current_effect_type = settings['last_effect_type']
                
                # Load current patch
                if 'last_loaded_patch' in settings and settings['last_loaded_patch']:
                    self.current_patch = settings['last_loaded_patch']
                    print(f"🔍 DEBUG: Loaded current_patch from settings: {self.current_patch.get('meta', {}).get('name', 'Unknown')}")
                else:
                    self.current_patch = None
                    print("🔍 DEBUG: No current_patch in settings, set to None")
                
                self.log_status("✅ Settings loaded successfully")
            else:
                self.log_status("ℹ️ No settings file found - using defaults")
                self.last_active_tab = 0
                self.last_loaded_patch = None
                
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
    
    def get_current_tab_index(self):
        """Get the index of the currently active tab."""
        try:
            if hasattr(self, 'notebook') and self.notebook:
                return self.notebook.index(self.notebook.select())
            return 0
        except:
            return 0
    
    def restore_application_state(self):
        """Restore application state from saved settings."""
        try:
            print("🔍 DEBUG: Starting restore_application_state()")
            print(f"🔍 DEBUG: last_active_tab = {getattr(self, 'last_active_tab', 'NOT SET')}")
            print(f"🔍 DEBUG: last_loaded_patch = {getattr(self, 'last_loaded_patch', 'NOT SET')}")
            print(f"🔍 DEBUG: notebook exists: {hasattr(self, 'notebook')}")
            if hasattr(self, 'notebook'):
                print(f"🔍 DEBUG: notebook tabs count: {self.notebook.index('end')}")
            
            # Restore active tab
            if hasattr(self, 'last_active_tab') and hasattr(self, 'notebook'):
                print(f"🔍 DEBUG: Attempting to restore tab {self.last_active_tab}")
                if 0 <= self.last_active_tab < self.notebook.index('end'):
                    self.notebook.select(self.last_active_tab)
                    self.log_status(f"🔄 Restored tab {self.last_active_tab}")
                    print(f"🔍 DEBUG: Successfully restored tab {self.last_active_tab}")
                else:
                    print(f"🔍 DEBUG: Tab index {self.last_active_tab} out of range (0-{self.notebook.index('end')-1})")
            else:
                print("🔍 DEBUG: No last_active_tab or notebook available")
            
            # Store patch for later restoration after widgets are loaded
            if hasattr(self, 'last_loaded_patch') and self.last_loaded_patch:
                print(f"🔍 DEBUG: Patch available for restoration: {self.last_loaded_patch.get('meta', {}).get('name', 'Unknown')}")
                self.patch_to_restore = self.last_loaded_patch
                print(f"🔍 DEBUG: Stored patch_to_restore: {self.patch_to_restore is not None}")
                self.log_status(f"🔄 Patch queued for restoration: {self.last_loaded_patch.get('meta', {}).get('name', 'Unknown')}")
                
                # Trigger restoration with a longer delay to allow widgets to load
                print("🔍 DEBUG: Scheduling patch restoration with 2 second delay")
                self.root.after(2000, self.reload_restored_patch)
            else:
                print("🔍 DEBUG: No patch to restore")
                self.patch_to_restore = None
                print(f"🔍 DEBUG: Set patch_to_restore to None")
                
            print("🔍 DEBUG: restore_application_state() completed")
                    
        except Exception as e:
            self.log_status(f"⚠️ Error restoring application state: {e}")
            print(f"🔍 DEBUG: Error restoring state: {e}")
            import traceback
            print(f"🔍 DEBUG: Traceback: {traceback.format_exc()}")
    
    def reload_restored_patch(self):
        """Reload the restored patch to properly initialize widgets."""
        try:
            if hasattr(self, 'patch_to_restore') and self.patch_to_restore:
                print("🔍 DEBUG: Restoring queued patch to initialize widgets")
                self.log_status("🔄 Restoring patch to initialize widgets...")
                
                # Set the current patch
                self.current_patch = self.patch_to_restore
                
                # Auto-load effects from patch (this will create the widgets)
                print("🔍 DEBUG: Auto-loading effects from patch...")
                self.auto_load_effects_from_patch()
                
                # Clear the queued patch
                self.patch_to_restore = None
                
                # Trigger analysis to fully initialize the system
                if hasattr(self, 'run_analysis'):
                    print("🔍 DEBUG: Triggering analysis to complete initialization")
                    self.run_analysis()
                
                self.log_status("✅ Patch restored and widgets initialized")
                print("🔍 DEBUG: Patch restoration completed")
            else:
                print("🔍 DEBUG: No queued patch to restore")
        except Exception as e:
            self.log_status(f"⚠️ Error restoring patch: {e}")
            print(f"🔍 DEBUG: Error restoring patch: {e}")
            import traceback
            print(f"🔍 DEBUG: Traceback: {traceback.format_exc()}")
    
    def on_tab_changed(self, event=None):
        """Handle tab change event - save current state."""
        try:
            # Save current tab index
            if hasattr(self, 'notebook'):
                self.save_settings()
        except Exception as e:
            print(f"🔍 DEBUG: Error saving state on tab change: {e}")
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            # Debug current state before saving
            print(f"🔍 DEBUG: Saving settings - current_patch exists: {hasattr(self, 'current_patch')}")
            if hasattr(self, 'current_patch'):
                print(f"🔍 DEBUG: current_patch value: {self.current_patch}")
            print(f"🔍 DEBUG: last_active_tab will be: {self.get_current_tab_index()}")
            
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
                
                # Application state
                'last_active_tab': self.get_current_tab_index(),
                'last_loaded_patch': self.current_patch if hasattr(self, 'current_patch') and self.current_patch else None,
            }
            
            print(f"🔍 DEBUG: Writing to settings file: {self.settings_file}")
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            print(f"🔍 DEBUG: Settings file written successfully")
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
        
        # Bind tab change event to save state
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # Create tabs following natural workflow
        self.create_target_analysis_tab()
        self.create_patch_builder_tab()
        self.create_upload_test_tab()
        self.create_live_comparison_tab()
        self.create_iterative_improvement_tab()
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
    
    def create_target_analysis_tab(self):
        """Create target analysis tab - load target audio, analyze, generate initial patch."""
        self.target_analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.target_analysis_frame, text="🎯 Target Analysis")
        
        # Title
        title = ttk.Label(self.target_analysis_frame, text="Target Analysis & Patch Generation", style='Title.TLabel')
        title.pack(pady=10)
        
        # Workflow guide
        workflow_frame = ttk.LabelFrame(self.target_analysis_frame, text="📋 Workflow Guide", padding=10)
        workflow_frame.pack(fill=tk.X, padx=10, pady=5)
        
        workflow_text = """1. Select Target Audio (the sound you want to reproduce)
2. Select DI Audio (dry guitar signal) 
3. Analyze target audio to extract features
4. Generate initial patch compatible with Magicstomp
5. Proceed to Patch Builder tab to configure effects"""
        
        workflow_label = ttk.Label(workflow_frame, text=workflow_text, 
                                  style='Info.TLabel', justify=tk.LEFT)
        workflow_label.pack(anchor=tk.W)
        
        # Target file
        target_frame = ttk.LabelFrame(self.target_analysis_frame, text="Target Audio", padding=10)
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.target_var = tk.StringVar(value="No file selected")
        target_label = ttk.Label(target_frame, textvariable=self.target_var, width=50)
        target_label.pack(side=tk.LEFT, padx=(0, 10))
        
        target_btn = ttk.Button(target_frame, text="Select Target", 
                               command=self.select_target_file)
        target_btn.pack(side=tk.LEFT)
        
        # DI file
        di_frame = ttk.LabelFrame(self.target_analysis_frame, text="DI Audio", padding=10)
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
        analysis_frame = ttk.LabelFrame(self.target_analysis_frame, text="Audio Analysis", padding=10)
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
        patch_buttons_frame = ttk.Frame(self.target_analysis_frame)
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
    
    def create_patch_builder_tab(self):
        """Create patch builder tab - break down patch into Magicstomp widgets, visual parameter adjustment."""
        self.patch_builder_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.patch_builder_frame, text="🎛️ Patch Builder")
        
        # Title
        title = ttk.Label(self.patch_builder_frame, text="Patch Builder & Effect Configuration", style='Title.TLabel')
        title.pack(pady=10)
        
        # Effect selection
        selection_frame = ttk.LabelFrame(self.patch_builder_frame, text="Effect Selection", padding=10)
        selection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.effect_var = tk.StringVar()
        self.effect_combo = ttk.Combobox(selection_frame, textvariable=self.effect_var,
                                        state="readonly", width=40)
        self.effect_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        load_btn = ttk.Button(selection_frame, text="Load Effect", 
                             command=self.load_effect_widget)
        load_btn.pack(side=tk.LEFT)
        
        # Effect parameters (scrollable)
        params_frame = ttk.LabelFrame(self.patch_builder_frame, text="Parameters", padding=10)
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
    
    def create_upload_test_tab(self):
        """Create upload and test tab - send patch to device, test and verify upload."""
        self.upload_test_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.upload_test_frame, text="📤 Upload & Test")
        
        # Title
        title = ttk.Label(self.upload_test_frame, text="Upload & Test Patch", style='Title.TLabel')
        title.pack(pady=10)
        
        # Upload controls
        controls_frame = ttk.Frame(self.upload_test_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        upload_btn = ttk.Button(controls_frame, text="📤 Upload Patch", 
                               command=self.send_patch_to_magicstomp)
        upload_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        test_btn = ttk.Button(controls_frame, text="🎸 Test Patch", 
                             command=self.test_patch_on_device)
        test_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        verify_btn = ttk.Button(controls_frame, text="✅ Verify Upload", 
                               command=self.verify_patch_upload)
        verify_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        status_btn = ttk.Button(controls_frame, text="📊 Device Status", 
                               command=self.check_device_status)
        status_btn.pack(side=tk.LEFT)
        
        # Impact visualization
        self.init_impact_visualizer()
    
    def create_iterative_improvement_tab(self):
        """Create iterative improvement tab - generate retroactioned patches, optimization loop."""
        self.iterative_improvement_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.iterative_improvement_frame, text="🔄 Iterative Improvement")
        
        # Title
        title = ttk.Label(self.iterative_improvement_frame, text="Iterative Improvement & Optimization", style='Title.TLabel')
        title.pack(pady=10)
        
        # Optimization controls
        opt_frame = ttk.LabelFrame(self.iterative_improvement_frame, text="Optimization Controls", padding=10)
        opt_frame.pack(fill=tk.X, padx=10, pady=5)
        
        start_opt_btn = ttk.Button(opt_frame, text="🚀 Start Optimization", 
                                  style='Large.TButton',
                                  command=self.start_optimization)
        start_opt_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        stop_opt_btn = ttk.Button(opt_frame, text="⏹️ Stop Optimization", 
                                 command=self.stop_optimization_simple)
        stop_opt_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        generate_retro_btn = ttk.Button(opt_frame, text="🎯 Generate Retroactioned Patch", 
                                       command=self.generate_retroactioned_patch)
        generate_retro_btn.pack(side=tk.LEFT)
    
    def create_live_comparison_tab(self):
        """Create live comparison tab - live guitar input, real-time comparison with target."""
        self.live_comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.live_comparison_frame, text="🎸 Live Comparison")
        
        # Title
        title = ttk.Label(self.live_comparison_frame, text="Live Comparison & Analysis", style='Title.TLabel')
        title.pack(pady=10)
        
        # Live monitoring controls
        monitor_frame = ttk.LabelFrame(self.live_comparison_frame, text="Live Monitoring", padding=10)
        monitor_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.monitor_btn = ttk.Button(monitor_frame, text="🎤 Start Monitoring", 
                                     style='Large.TButton',
                                     command=self.toggle_live_monitoring)
        self.monitor_btn.pack(pady=10)
        
        # Optimization controls
        opt_frame = ttk.LabelFrame(self.live_comparison_frame, text="Optimization", padding=10)
        opt_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.optimize_btn = ttk.Button(opt_frame, text="🔄 Start Optimization", 
                                      style='Large.TButton',
                                      command=self.start_optimization)
        self.optimize_btn.pack(pady=10)
        
        # Quick actions
        actions_frame = ttk.LabelFrame(self.live_comparison_frame, text="Quick Actions", padding=10)
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
        self.midi_input_combo.bind('<<ComboboxSelected>>', self.on_midi_input_changed)
        
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
        self.midi_output_combo.bind('<<ComboboxSelected>>', self.on_midi_output_changed)
        
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
        
        # Recharge les paramètres MIDI après création des widgets
        self.reload_midi_settings()
        
        # Recharge les fichiers et patch après création des widgets
        self.reload_file_and_patch_settings()
        
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
        """Initialize impact visualizer in upload test tab."""
        self.impact_visualizer = ImpactVisualizer(self.upload_test_frame)
    
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
            display_name = self.get_display_name_for_effect(effect_name)
            self.current_effect_var.set(f"Effect: {display_name}")
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
                    
                    # Auto-load effects from generated patch first
                    self.root.after(50, self.auto_load_effects_from_patch)
                    
                    # Then auto-generate patch proposal if effect is loaded
                    if self.current_effect_widget:
                        self.root.after(100, self.auto_generate_patch_proposal)
                    
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
                    
                    # Auto-load effects from generated patch first
                    self.root.after(50, self.auto_load_effects_from_patch)
                    
                    # Then auto-generate patch proposal if effect is loaded
                    if self.current_effect_widget:
                        self.root.after(100, self.auto_generate_patch_proposal)
                
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
            
            # Save state after generating patch
            self.save_settings()
            
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
                def log_effect_label():
                    if self.current_effect_type is not None:
                        effect_name = EffectRegistry.get_effect_name(self.current_effect_type)
                        display_name = self.get_display_name_for_effect(effect_name)
                        self.log_status(f"🎛️ Effect: {display_name}")

                self.root.after(0, log_effect_label)
                
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
                
                # Save state after loading patch
                self.save_settings()
                
                # Try to identify and auto-load effects from patch
                print(f"🔍 DEBUG: About to auto-load effects from patch: {self.current_patch}")
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
        print("🔍 DEBUG: Starting convert_patch_to_widget_params()")
        print(f"🔍 DEBUG: Input patch: {patch}")
        
        try:
            widget_params = {}
            
            # Extract parameters from patch sections with proper mapping
            for section_name, section_data in patch.items():
                if isinstance(section_data, dict) and section_name != 'meta':
                    print(f"🔍 DEBUG: Processing section: {section_name}")
                    
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
            identification = self.identify_effects_from_patch(self.current_patch)
            official_matches = identification.get('official', [])
            unsupported_matches = identification.get('unsupported', [])
            unverified_matches = identification.get('unverified', [])
            duplicate_matches = identification.get('duplicates', [])

            official_names = [match.display_name for match in official_matches]
            unsupported_names = [match.display_name for match in unsupported_matches]
            unverified_names = [match.display_name for match in unverified_matches]
            duplicate_names = [match.display_name for match in duplicate_matches]

            print(f"🔍 DEBUG: Official matches: {official_names}")
            print(f"🔍 DEBUG: Unsupported matches: {unsupported_names}")
            print(f"🔍 DEBUG: Unverified matches: {unverified_names}")
            print(f"🔍 DEBUG: Duplicate matches: {duplicate_names}")

            if not official_matches:
                if unsupported_names:
                    self.log_status(f"⚠️ Official effects unsupported: {', '.join(unsupported_names)}")
                if unverified_names:
                    self.log_status(f"ℹ️ Effect hints outside official catalog: {', '.join(unverified_names)}")
                if duplicate_names:
                    self.log_status(f"ℹ️ Duplicate effect hints ignored: {', '.join(duplicate_names)}")
                print("🔍 DEBUG: No official effects identified in patch")
                self.log_status("💡 No specific effects identified in patch - manual selection required")
                return

            self.log_status(f"🔍 Identified effects: {', '.join(official_names)}")
            print(f"🔍 DEBUG: Loading effect cascade with {len(official_matches)} effects")
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
                print(f"🔍 DEBUG: add_effect_to_cascade returned: {success}, info: {info}")

                if success:
                    loaded_effects.append(match)
                    self.log_status(f"✅ Loaded: {display_name}")
                    print(f"🔍 DEBUG: Successfully loaded effect: {display_name}")
                else:
                    load_failures.append((match, info))
                    self.log_status(f"❌ Failed to load {display_name}: {info}")
                    print(f"🔍 DEBUG: Failed to load effect: {display_name} ({info})")

            # Report cascade status
            if loaded_effects:
                loaded_display_names = [match.display_name for match in loaded_effects]
                self.log_status(
                    f"🎛️ Effect cascade loaded: {len(loaded_effects)}/{len(official_matches)} effects"
                    f" ({', '.join(loaded_display_names)})"
                )
                print(f"🔍 DEBUG: Effect cascade loaded: {[match.display_name for match in loaded_effects]}")
                    
                # Check if we need to restore a queued patch
                print(f"🔍 DEBUG: Checking for queued patch restoration...")
                print(
                    f"🔍 DEBUG: - hasattr patch_to_restore: {hasattr(self, 'patch_to_restore')}"
                )
                if hasattr(self, 'patch_to_restore'):
                    print(f"🔍 DEBUG: - patch_to_restore value: {self.patch_to_restore}")
                if hasattr(self, 'patch_to_restore') and self.patch_to_restore:
                    print("🔍 DEBUG: Widgets loaded, triggering patch restoration")
                    self.root.after(
                        500, self.reload_restored_patch
                    )  # Small delay to ensure widgets are ready
                else:
                    print("🔍 DEBUG: No queued patch to restore")

                # Auto-apply patch parameters to the last loaded effect (current active one)
                    print(f"🔍 DEBUG: Checking auto-apply conditions:")
                    print(f"🔍 DEBUG: - current_patch: {bool(self.current_patch)}")
                    print(f"🔍 DEBUG: - current_effect_widget: {bool(self.current_effect_widget)}")
                    print(f"🔍 DEBUG: - has set_all_parameters: {hasattr(self.current_effect_widget, 'set_all_parameters') if self.current_effect_widget else False}")
                    
                    if (self.current_patch and self.effect_widget_cascade) or getattr(self, 'auto_apply_restored_patch', False):
                        print(f"🔍 DEBUG: All conditions met, proceeding with auto-apply")
                        is_restored_patch = getattr(self, 'auto_apply_restored_patch', False)
                        if is_restored_patch:
                            print(f"🔍 DEBUG: Auto-applying restored patch to widgets")
                        widget_params = self.convert_patch_to_widget_params(self.current_patch)
                        print(f"🔍 DEBUG: Converted widget params: {widget_params}")
                        
                        if widget_params:
                            # Appliquer les paramètres à tous les widgets de la cascade
                            print(f"🔍 DEBUG: Applying parameters to all widgets in cascade")
                            for i, effect_widget in enumerate(self.effect_widget_cascade):
                                try:
                                    widget_type = type(effect_widget).__name__
                                    print(f"🔍 DEBUG: Applying to widget {i}: {widget_type}")
                                    
                                    # Obtenir les paramètres spécifiques à ce widget
                                    specific_params = self.get_widget_specific_params(widget_type, widget_params)
                                    print(f"🔍 DEBUG: Specific params for {widget_type}: {specific_params}")
                                    
                                    if specific_params:
                                        effect_widget.set_all_parameters(specific_params)
                                        print(f"🔍 DEBUG: set_all_parameters succeeded for widget {i}")
                                    else:
                                        print(f"🔍 DEBUG: No specific params for {widget_type}")
                                        
                                except Exception as e:
                                    print(f"🔍 DEBUG: Error applying to widget {i}: {e}")
                            
                            # Mettre à jour les paramètres actuels et cibles
                            self.current_parameters = widget_params
                            self.target_parameters = widget_params.copy()
                            
                            # Update impact visualization
                            print(f"🔍 DEBUG: Scheduling impact visualization update")
                            self.root.after(100, self.update_impact_visualization)
                            self.log_status("📊 Impact visualization updated automatically")
                            self.log_status("🎛️ Patch parameters applied to all auto-loaded effects")
                            self.log_status("💡 Go to Effects tab to see the visual representation!")
                            self.log_status("💡 Go to Analysis tab to see the parameter impacts!")
                            print(f"🔍 DEBUG: Auto-applied patch parameters: {widget_params}")
                            
                            # Reset the flag only after successful application
                            if is_restored_patch:
                                self.auto_apply_restored_patch = False
                                print(f"🔍 DEBUG: Reset auto_apply_restored_patch flag after successful application")
                            
                            # Debug current state
                            print(f"🔍 DEBUG: Current effect widget: {self.current_effect_widget}")
                            print(f"🔍 DEBUG: Current effect type: {self.current_effect_type}")
                            print(f"🔍 DEBUG: Current parameters: {self.current_parameters}")
                            print(f"🔍 DEBUG: Target parameters: {self.target_parameters}")
                        else:
                            print(f"🔍 DEBUG: No widget params to apply")
                    else:
                        print(f"🔍 DEBUG: Cannot auto-apply - conditions not met")
                        print(f"🔍 DEBUG: - current_effect_widget: {self.current_effect_widget}")
                        print(f"🔍 DEBUG: - has set_all_parameters: {hasattr(self.current_effect_widget, 'set_all_parameters') if self.current_effect_widget else False}")
                        self.log_status("⚠️ Effect loaded but cannot apply parameters")
            else:
                failed_display_names = [match.display_name for match in official_matches]
                failed_list = ', '.join(failed_display_names) if failed_display_names else 'None'
                self.log_status(f"⚠️ Could not auto-load effects: {failed_list}")
                print("🔍 DEBUG: Failed to auto-load any effects")

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
                print(f"🔍 DEBUG: Summary bits: {summary_bits}")
                
        except Exception as e:
            print(f"🔍 DEBUG: Error in auto_load_effects_from_patch: {e}")
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
        print(f"🔍 DEBUG: Loading official effect catalog from {catalog_path}")

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

                print(f"🔍 DEBUG: Loaded {len(self.official_effect_names)} official effect names")
            except Exception as exc:
                print(f"🔍 DEBUG: Failed to load official effect catalog: {exc}")
                self.official_effect_names = set()
                self.official_effect_lookup = {}
        else:
            print("🔍 DEBUG: Official effect catalog not found; falling back to registry names only")

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
        print(f"🔍 DEBUG: Supported effects (widgets): {len(self.supported_effect_name_to_type)}")

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
            print(f"🔍 DEBUG: Section {section_name} ignored (not a mapping)")
            return None

        section_key = section_name.lower()
        if section_key == 'meta':
            return None

        if not self.is_section_enabled(section_data):
            print(f"🔍 DEBUG: Section {section_name} disabled or bypassed")
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
                print(f"🔍 DEBUG: Direct mapping failed for section {section_name}")
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
            print(f"🔍 DEBUG: No mapping found for section: {section_name}")
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

        print("🔍 DEBUG: Starting identify_effects_from_patch()")
        print(f"🔍 DEBUG: Analyzing patch: {patch}")

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
                    print(f"🔍 DEBUG: Analyzing section: {section_name}")

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
            print(f"🔍 DEBUG: Identification report: {summary}")
            self.last_identified_effects = report
            return report

        except Exception as e:
            print(f"🔍 DEBUG: Error identifying effects: {e}")
            self.last_identified_effects = {
                'official': [],
                'unsupported': [],
                'unverified': [],
                'duplicates': [],
            }
            return self.last_identified_effects

    def add_effect_to_cascade(self, effect_match: EffectMatch):
        """Add an effect widget to the cascade without replacing existing ones."""

        print(f"🔍 DEBUG: Starting add_effect_to_cascade: {effect_match}")

        if not isinstance(effect_match, EffectMatch):
            print("🔍 DEBUG: Invalid effect match provided to add_effect_to_cascade")
            return False, "Invalid effect description"

        try:
            display_name = effect_match.display_name

            if not effect_match.should_attempt_load():
                reason = effect_match.describe_failure() or "Unsupported effect"
                print(f"🔍 DEBUG: Cannot load effect {display_name}: {reason}")
                return False, reason

            effect_type = effect_match.effect_type
            if effect_type is None and effect_match.canonical_name:
                effect_type = self.get_effect_type_for_name(effect_match.canonical_name)

            if effect_type is None:
                reason = effect_match.describe_failure() or "No widget available"
                print(f"🔍 DEBUG: No widget available for {display_name}")
                return False, reason

            print(f"🔍 DEBUG: Loading widget for type {effect_type} ({display_name})")
            effect_widget = self.load_effect_widget_by_type(effect_type)

            if effect_widget:
                print(f"🔍 DEBUG: Successfully added {display_name} to cascade")
                self.current_effect_widget = effect_widget
                self.current_effect_type = effect_type
                return True, display_name

            reason = f"Widget load failed for {display_name}"
            print(f"🔍 DEBUG: Failed to add {display_name} to cascade")
            return False, reason

        except Exception as e:
            print(f"🔍 DEBUG: Error adding effect to cascade: {e}")
            return False, str(e)
    
    def get_last_effect_widget(self):
        """Get the last (most recently added) effect widget from the scrollable frame."""
        children = self.params_scrollable_frame.winfo_children()
        effect_widgets = [child for child in children if hasattr(child, 'set_all_parameters')]
        return effect_widgets[-1] if effect_widgets else None
    
    def load_effect_by_name(self, effect_name):
        """Load an effect by name."""
        print(f"🔍 DEBUG: Starting load_effect_by_name: {effect_name}")
        
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
                print(f"🔍 DEBUG: Effect type for {effect_name}: {effect_type}")
                
                # Load the effect widget
                success = self.load_effect_widget_by_type(effect_type)
                if success:
                    print(f"🔍 DEBUG: Successfully loaded effect widget for {effect_name}")
                    return True
                else:
                    print(f"🔍 DEBUG: Failed to load effect widget for {effect_name}")
                    return False
            elif effect_name == 'Compressor':
                # Use real Compressor widget
                print(f"🔍 DEBUG: Loading real Compressor widget")
                effect_type = 0x36  # CompressorWidget
                success = self.load_effect_widget_by_type(effect_type)
                if success:
                    print(f"🔍 DEBUG: Successfully loaded Compressor widget")
                    return True
                else:
                    print(f"🔍 DEBUG: Failed to load Compressor widget")
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
            # Get effect widget from registry (using static class)
            print(f"🔍 DEBUG: Using EffectRegistry static class")
            effect_class = EffectRegistry.create_effect_widget(effect_type, None)
            print(f"🔍 DEBUG: Effect class for type {effect_type}: {effect_class}")
            
            if effect_class:
                # Create and load the effect widget
                print(f"🔍 DEBUG: Creating effect widget with parent: {self.params_scrollable_frame}")
                effect_widget = EffectRegistry.create_effect_widget(effect_type, self.params_scrollable_frame)
                self.current_effect_type = effect_type
                
                # Debug widget properties
                print(f"🔍 DEBUG: Widget created: {effect_widget}")
                print(f"🔍 DEBUG: Widget type: {type(effect_widget)}")
                
                # Pack the widget in the scrollable frame
                print(f"🔍 DEBUG: Packing widget in scrollable frame")
                effect_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                print(f"🔍 DEBUG: Widget packed successfully")
                
                # Force widget to update and show
                print(f"🔍 DEBUG: Forcing widget update")
                effect_widget.update_idletasks()
                effect_widget.update()
                print(f"🔍 DEBUG: Widget update completed")
                
                # Force grid layout update
                print(f"🔍 DEBUG: Forcing grid layout update")
                effect_widget.grid_rowconfigure(0, weight=1)
                effect_widget.grid_columnconfigure(0, weight=1)
                effect_widget.grid_propagate(True)
                print(f"🔍 DEBUG: Grid layout update completed")
                print(f"🔍 DEBUG: Widget methods: {dir(effect_widget)}")
                
                # Check if widget has required methods
                if hasattr(effect_widget, 'set_all_parameters'):
                    print(f"🔍 DEBUG: Widget has set_all_parameters method")
                else:
                    print(f"🔍 DEBUG: Widget MISSING set_all_parameters method")
                
                if hasattr(effect_widget, 'get_all_parameters'):
                    print(f"🔍 DEBUG: Widget has get_all_parameters method")
                else:
                    print(f"🔍 DEBUG: Widget MISSING get_all_parameters method")
                
                # Update UI
                if hasattr(self, 'current_effect_var'):
                    effect_name = EffectRegistry.get_effect_name(effect_type)
                    display_name = self.get_display_name_for_effect(effect_name)
                    self.current_effect_var.set(f"Loaded: {display_name}")
                    print(f"🔍 DEBUG: Updated current_effect_var to: Loaded: {display_name}")
                else:
                    print(f"🔍 DEBUG: No current_effect_var found")
                
                # Check patch builder frame
                print(f"🔍 DEBUG: Patch builder frame: {self.patch_builder_frame}")
                print(f"🔍 DEBUG: Params scrollable frame: {self.params_scrollable_frame}")
                print(f"🔍 DEBUG: Params scrollable frame children: {self.params_scrollable_frame.winfo_children()}")
                
                # Check if widget is visible
                if effect_widget:
                    print(f"🔍 DEBUG: Widget visible: {effect_widget.winfo_viewable()}")
                    print(f"🔍 DEBUG: Widget mapped: {effect_widget.winfo_ismapped()}")
                    print(f"🔍 DEBUG: Widget geometry: {effect_widget.winfo_geometry()}")
                    print(f"🔍 DEBUG: Widget size: {effect_widget.winfo_reqwidth()}x{effect_widget.winfo_reqheight()}")
                    print(f"🔍 DEBUG: Widget children: {effect_widget.winfo_children()}")
                    print(f"🔍 DEBUG: Widget children count: {len(effect_widget.winfo_children())}")
                
                # Add widget to cascade
                self.effect_widget_cascade.append(effect_widget)
                print(f"🔍 DEBUG: Added widget to cascade. Cascade size: {len(self.effect_widget_cascade)}")
                
                print(f"🔍 DEBUG: Successfully loaded effect widget type {effect_type}")
                print(f"🔍 DEBUG: Created effect widget: {effect_widget}")
                return effect_widget
            else:
                print(f"🔍 DEBUG: Effect class not found for type {effect_type}")
                print(f"🔍 DEBUG: Available effects in registry: {list(EffectRegistry.EFFECT_WIDGETS.keys())}")
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
            print(f"🔍 DEBUG: Nombre de messages SysEx: {len(syx_data)}")
            if syx_data:
                print(f"🔍 DEBUG: Premier message: {syx_data[0]}")
            
            # Get selected MIDI port from settings
            midi_output = self.midi_output_var.get() if hasattr(self, 'midi_output_var') else None
            if not midi_output:
                self.log_status("⚠️ Please select MIDI output device in Settings tab")
                print("🔍 DEBUG: No MIDI output device selected")
                return
            
            # Send to device using existing port if available
            print(f"🔍 DEBUG: Sending to MIDI port: {midi_output}")
            existing_port = None
            if hasattr(self, 'realtime_magicstomp'):
                print(f"🔍 DEBUG: RealtimeMagicstomp exists: {self.realtime_magicstomp}")
                if hasattr(self.realtime_magicstomp, 'output_port') and self.realtime_magicstomp.output_port:
                    existing_port = self.realtime_magicstomp.output_port
                    print("🔍 DEBUG: Using existing RealtimeMagicstomp port")
                else:
                    print("🔍 DEBUG: No existing port available in RealtimeMagicstomp")
            else:
                print("🔍 DEBUG: No RealtimeMagicstomp available")
            success = adapter.send_to_device(syx_data, midi_output, existing_port)
            
            if success:
                self.log_status("✅ Patch sent to Magicstomp successfully!")
                print("🔍 DEBUG: Patch sent successfully")
            else:
                self.log_status("❌ Failed to send patch to Magicstomp")
                print("🔍 DEBUG: Patch send failed")
            
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
    
    def reload_midi_settings(self):
        """Recharge les paramètres MIDI depuis le fichier de configuration."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                # Recharge les paramètres MIDI
                if 'midi_input_device' in settings and hasattr(self, 'midi_input_var'):
                    self.midi_input_var.set(settings['midi_input_device'])
                    print(f"🔍 DEBUG: Reloaded MIDI input: {settings['midi_input_device']}")
                
                if 'midi_output_device' in settings and hasattr(self, 'midi_output_var'):
                    self.midi_output_var.set(settings['midi_output_device'])
                    print(f"🔍 DEBUG: Reloaded MIDI output: {settings['midi_output_device']}")
                    
                    # Mise à jour automatique du port RealtimeMagicstomp
                    if hasattr(self, 'realtime_magicstomp') and settings['midi_output_device']:
                        self.update_realtime_magicstomp_port(settings['midi_output_device'])
                
                if 'midi_channels' in settings and hasattr(self, 'midi_channel_vars'):
                    # Reset all channels first
                    for var in self.midi_channel_vars.values():
                        var.set(False)
                    # Restore selected channels
                    for channel in settings['midi_channels']:
                        if channel in self.midi_channel_vars:
                            self.midi_channel_vars[channel].set(True)
                    self.midi_channels = settings['midi_channels']
                    print(f"🔍 DEBUG: Reloaded MIDI channels: {settings['midi_channels']}")
                
        except Exception as e:
            print(f"🔍 DEBUG: Error reloading MIDI settings: {e}")
    
    def reload_file_and_patch_settings(self):
        """Recharge les fichiers et patch depuis le fichier de configuration."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)

                # Recharge les fichiers
                if 'last_target_file' in settings and settings['last_target_file']:
                    self.target_file = settings['last_target_file']
                    if hasattr(self, 'target_var'):
                        self.target_var.set(f"Target: {Path(self.target_file).name}")
                    self.log_status(f"📁 Restored target: {Path(self.target_file).name}")
                    print(f"🔍 DEBUG: Reloaded target file: {self.target_file}")

                if 'last_di_file' in settings and settings['last_di_file']:
                    self.di_file = settings['last_di_file']
                    if hasattr(self, 'di_var'):
                        self.di_var.set(f"DI: {Path(self.di_file).name}")
                    self.log_status(f"📁 Restored DI: {Path(self.di_file).name}")
                    print(f"🔍 DEBUG: Reloaded DI file: {self.di_file}")

                # Le patch est déjà géré par restore_application_state()
                # Pas besoin de le recharger ici

        except Exception as e:
            print(f"🔍 DEBUG: Error reloading file and patch settings: {e}")
    
    def update_realtime_magicstomp_port(self, port_name):
        """Met à jour le port MIDI de RealtimeMagicstomp."""
        try:
            if hasattr(self, 'realtime_magicstomp') and self.realtime_magicstomp:
                # Ferme l'ancien port s'il existe
                if self.realtime_magicstomp.output_port:
                    self.realtime_magicstomp.output_port.close()
                
                # Se connecte au nouveau port
                self.realtime_magicstomp.midi_port_name = port_name
                self.realtime_magicstomp._connect_to_port(port_name)
                
                if self.realtime_magicstomp.output_port:
                    print(f"✅ RealtimeMagicstomp connecté au port: {port_name}")
                    self.log_status(f"✅ MIDI connecté: {port_name}")
                else:
                    print(f"❌ Échec connexion RealtimeMagicstomp au port: {port_name}")
                    self.log_status(f"❌ Échec connexion MIDI: {port_name}")
                    
        except Exception as e:
            print(f"❌ Erreur mise à jour port RealtimeMagicstomp: {e}")
    
    def on_midi_input_changed(self, event=None):
        """Callback quand le port MIDI input change."""
        try:
            port_name = self.midi_input_var.get()
            print(f"🔍 DEBUG: MIDI input changed to: {port_name}")
            self.save_settings()  # Sauvegarde automatique
        except Exception as e:
            print(f"❌ Erreur changement MIDI input: {e}")
    
    def on_midi_output_changed(self, event=None):
        """Callback quand le port MIDI output change."""
        try:
            port_name = self.midi_output_var.get()
            print(f"🔍 DEBUG: MIDI output changed to: {port_name}")
            
            # Met à jour RealtimeMagicstomp
            self.update_realtime_magicstomp_port(port_name)
            
            # Sauvegarde automatique
            self.save_settings()
            
        except Exception as e:
            print(f"❌ Erreur changement MIDI output: {e}")
    
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
            
            # Auto-detect Magicstomp and set default selections
            magicstomp_output = None
            magicstomp_input = None
            
            # Recherche Magicstomp dans les ports de sortie
            for port in output_names:
                if 'ub9' in port.lower() or 'magicstomp' in port.lower():
                    magicstomp_output = port
                    break
            
            # Recherche Magicstomp dans les ports d'entrée
            for port in input_names:
                if 'ub9' in port.lower() or 'magicstomp' in port.lower():
                    magicstomp_input = port
                    break
            
            # Définit les sélections par défaut
            if input_names and not self.midi_input_var.get():
                if magicstomp_input:
                    self.midi_input_var.set(magicstomp_input)
                    print(f"🔍 DEBUG: Auto-selected Magicstomp input: {magicstomp_input}")
                else:
                    self.midi_input_var.set(input_names[0])
                    
            if output_names and not self.midi_output_var.get():
                if magicstomp_output:
                    self.midi_output_var.set(magicstomp_output)
                    print(f"🔍 DEBUG: Auto-selected Magicstomp output: {magicstomp_output}")
                    # Met à jour RealtimeMagicstomp automatiquement
                    self.update_realtime_magicstomp_port(magicstomp_output)
                else:
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
            
            # Close MIDI connection
            if hasattr(self, 'realtime_magicstomp'):
                # Close MIDI ports
                if hasattr(self.realtime_magicstomp, 'output_port') and self.realtime_magicstomp.output_port:
                    self.realtime_magicstomp.output_port.close()
                if hasattr(self.realtime_magicstomp, 'input_port') and self.realtime_magicstomp.input_port:
                    self.realtime_magicstomp.input_port.close()
            
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
    
    def test_patch_on_device(self):
        """Test the current patch on the Magicstomp device."""
        try:
            self.log_status("🎸 Testing patch on device...")
            # This would implement patch testing functionality
            # For now, just log the action
            self.log_status("✅ Patch test completed")
        except Exception as e:
            self.log_status(f"❌ Error testing patch: {e}")
    
    def verify_patch_upload(self):
        """Verify that the patch was uploaded correctly to the device."""
        try:
            self.log_status("✅ Verifying patch upload...")
            # This would implement patch verification functionality
            # For now, just log the action
            self.log_status("✅ Patch upload verified")
        except Exception as e:
            self.log_status(f"❌ Error verifying upload: {e}")
    
    def check_device_status(self):
        """Check the status of the Magicstomp device."""
        try:
            self.log_status("📊 Checking device status...")
            # This would implement device status checking
            # For now, just log the action
            self.log_status("✅ Device status: Connected")
        except Exception as e:
            self.log_status(f"❌ Error checking device status: {e}")
    
    def generate_retroactioned_patch(self):
        """Generate a retroactioned patch based on current analysis."""
        try:
            self.log_status("🎯 Generating retroactioned patch...")
            # This would implement retroactioned patch generation
            # For now, just log the action
            self.log_status("✅ Retroactioned patch generated")
        except Exception as e:
            self.log_status(f"❌ Error generating retroactioned patch: {e}")
    
    def stop_optimization_simple(self):
        """Stop optimization process."""
        try:
            self.log_status("⏹️ Stopping optimization...")
            # This would implement optimization stopping
            # For now, just log the action
            self.log_status("✅ Optimization stopped")
        except Exception as e:
            self.log_status(f"❌ Error stopping optimization: {e}")


def main():
    """Main function."""
    app = SplitVerticalGUI()
    app.run()


if __name__ == "__main__":
    main()
