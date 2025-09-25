"""Setup and UI helpers for the split vertical GUI."""

from __future__ import annotations

import json
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from magicstomp_effects import EffectRegistry

from gui.impact_visualization import ImpactVisualizer


class SplitVerticalGUISetupMixin:
    """Setup and UI helpers for the split vertical GUI."""

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
                    from debug_logger import debug_logger
debug_logger.log(f"🔍 DEBUG: Loaded current_patch from settings: {self.current_patch.get('meta', {}).get('name', 'Unknown')}")
                else:
                    self.current_patch = None
debug_logger.log(f"🔍 DEBUG: No current_patch in settings, set to None")
                
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
            
debug_logger.log(f"🔍 DEBUG: Saved file selections - Target: {self.target_file}, DI: {self.di_file}")
            
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error saving file selections: {e}")
    
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
debug_logger.log(f"🔍 DEBUG: Starting restore_application_state()")
debug_logger.log(f"🔍 DEBUG: last_active_tab = {getattr(self, 'last_active_tab', 'NOT SET')}")
debug_logger.log(f"🔍 DEBUG: last_loaded_patch = {getattr(self, 'last_loaded_patch', 'NOT SET')}")
debug_logger.log(f"🔍 DEBUG: notebook exists: {hasattr(self, 'notebook')}")
            if hasattr(self, 'notebook'):
debug_logger.log(f"🔍 DEBUG: notebook tabs count: {self.notebook.index('end')}")
            
            # Restore active tab
            if hasattr(self, 'last_active_tab') and hasattr(self, 'notebook'):
debug_logger.log(f"🔍 DEBUG: Attempting to restore tab {self.last_active_tab}")
                if 0 <= self.last_active_tab < self.notebook.index('end'):
                    self.notebook.select(self.last_active_tab)
                    self.log_status(f"🔄 Restored tab {self.last_active_tab}")
debug_logger.log(f"🔍 DEBUG: Successfully restored tab {self.last_active_tab}")
                else:
debug_logger.log(f"🔍 DEBUG: Tab index {self.last_active_tab} out of range (0-{self.notebook.index('end')-1})")
            else:
debug_logger.log(f"🔍 DEBUG: No last_active_tab or notebook available")
            
            # Store patch for later restoration after widgets are loaded
            if hasattr(self, 'last_loaded_patch') and self.last_loaded_patch:
debug_logger.log(f"🔍 DEBUG: Patch available for restoration: {self.last_loaded_patch.get('meta', {}).get('name', 'Unknown')}")
                self.patch_to_restore = self.last_loaded_patch
debug_logger.log(f"🔍 DEBUG: Stored patch_to_restore: {self.patch_to_restore is not None}")
                self.log_status(f"🔄 Patch queued for restoration: {self.last_loaded_patch.get('meta', {}).get('name', 'Unknown')}")
                
                # Trigger restoration with a longer delay to allow widgets to load
debug_logger.log(f"🔍 DEBUG: Scheduling patch restoration with 2 second delay")
                self.root.after(2000, self.reload_restored_patch)
            else:
debug_logger.log(f"🔍 DEBUG: No patch to restore")
                self.patch_to_restore = None
debug_logger.log(f"🔍 DEBUG: Set patch_to_restore to None")
                
debug_logger.log(f"🔍 DEBUG: restore_application_state() completed")
                    
        except Exception as e:
            self.log_status(f"⚠️ Error restoring application state: {e}")
debug_logger.log(f"🔍 DEBUG: Error restoring state: {e}")
            import traceback
debug_logger.log(f"🔍 DEBUG: Traceback: {traceback.format_exc()}")
    
    def reload_restored_patch(self):
        """Reload the restored patch to properly initialize widgets."""
        try:
            if hasattr(self, 'patch_to_restore') and self.patch_to_restore:
debug_logger.log(f"🔍 DEBUG: Restoring queued patch to initialize widgets")
                self.log_status("🔄 Restoring patch to initialize widgets...")
                
                # Set the current patch
                self.current_patch = self.patch_to_restore
                
                # Auto-load effects from patch (this will create the widgets)
debug_logger.log(f"🔍 DEBUG: Auto-loading effects from patch...")
                self.auto_load_effects_from_patch()
                
                # Apply patch parameters to widgets after a short delay
                self.root.after(500, self.apply_patch_parameters_to_widgets)
                
                # Clear the queued patch
                self.patch_to_restore = None
                
                # Trigger analysis to fully initialize the system
                if hasattr(self, 'run_analysis'):
debug_logger.log(f"🔍 DEBUG: Triggering analysis to complete initialization")
                    self.run_analysis()
                
                self.log_status("✅ Patch restored and widgets initialized")
debug_logger.log(f"🔍 DEBUG: Patch restoration completed")
            else:
debug_logger.log(f"🔍 DEBUG: No queued patch to restore")
                # If no patch to restore, try to download from Magicstomp
                if hasattr(self, 'download_current_patch'):
debug_logger.log(f"🔍 DEBUG: No patch to restore, attempting to download from Magicstomp")
                    self.log_status("🔄 No saved patch, downloading from Magicstomp...")
                    self.root.after(1000, self.download_current_patch)
        except Exception as e:
            self.log_status(f"⚠️ Error restoring patch: {e}")
debug_logger.log(f"🔍 DEBUG: Error restoring patch: {e}")
            import traceback
debug_logger.log(f"🔍 DEBUG: Traceback: {traceback.format_exc()}")
    
    def on_tab_changed(self, event=None):
        """Handle tab change event - save current state."""
        try:
            # Save current tab index
            if hasattr(self, 'notebook'):
                self.save_settings()
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error saving state on tab change: {e}")
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            # Debug current state before saving
debug_logger.log(f"🔍 DEBUG: Saving settings - current_patch exists: {hasattr(self, 'current_patch')}")
            if hasattr(self, 'current_patch'):
debug_logger.log(f"🔍 DEBUG: current_patch value: {self.current_patch}")
debug_logger.log(f"🔍 DEBUG: last_active_tab will be: {self.get_current_tab_index()}")
            
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
            
debug_logger.log(f"🔍 DEBUG: Writing to settings file: {self.settings_file}")
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
debug_logger.log(f"🔍 DEBUG: Settings file written successfully")
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
        
        download_btn = ttk.Button(selection_frame, text="📥 Download Current",
                                 command=self.download_current_patch)
        download_btn.pack(side=tk.LEFT, padx=(10, 0))
        
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
    
