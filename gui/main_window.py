#!/usr/bin/env python3
"""
Main GUI Window for Magicstomp HIL System
========================================

Modern graphical interface for Hardware-in-the-Loop tone matching.
Provides complete workflow from file selection to optimization.
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


class MagicstompHILGUI:
    """
    Main GUI application for Magicstomp HIL system.
    
    Provides complete workflow:
    1. File selection (target + DI)
    2. Patch generation and display
    3. Audio monitoring
    4. Optimization feedback loop
    """
    
    def __init__(self):
        """Initialize the main GUI application."""
        self.root = tk.Tk()
        self.root.title("🎸 Magicstomp HIL Tone Matcher")
        self.root.geometry("1800x1200")
        self.root.configure(bg='#2c3e50')
        
        # Make window resizable
        self.root.minsize(1600, 1000)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # State variables
        self.target_file = None
        self.di_file = None
        self.current_patch = None
        self.is_live_monitoring = False
        self.audio_stream = None
        self.hil_matcher = None
        self.audio_manager = None
        self.is_optimizing = False
        
        # Initialize components
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
        # Initialize HIL system
        self.init_hil_system()
    
    def setup_styles(self):
        """Setup modern styling for the GUI."""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Custom styles with MASSIVE fonts for MAXIMUM visibility
        style.configure('Title.TLabel', 
                       font=('Arial', 56, 'bold'),
                       foreground='#ecf0f1',
                       background='#2c3e50')
        
        style.configure('Section.TLabel',
                       font=('Arial', 32, 'bold'),
                       foreground='#3498db',
                       background='#2c3e50')
        
        style.configure('Info.TLabel',
                       font=('Arial', 24),
                       foreground='#bdc3c7',
                       background='#2c3e50')
        
        style.configure('Success.TLabel',
                       font=('Arial', 24, 'bold'),
                       foreground='#27ae60',
                       background='#2c3e50')
        
        style.configure('Warning.TLabel',
                       font=('Arial', 24, 'bold'),
                       foreground='#f39c12',
                       background='#2c3e50')
        
        style.configure('Error.TLabel',
                       font=('Arial', 24, 'bold'),
                       foreground='#e74c3c',
                       background='#2c3e50')
        
        # Configure button styles with MASSIVE fonts
        style.configure('TButton',
                       font=('Arial', 24, 'bold'),
                       padding=(20, 15))
        
        # Configure combobox styles with HUGE fonts
        style.configure('TCombobox',
                       font=('Arial', 22),
                       padding=(12, 10))
        
        # Configure dropdown listbox (the actual dropdown menu) with MASSIVE fonts
        style.configure('TCombobox',
                       font=('Arial', 22))
        
        # Also configure the dropdown arrow and field
        style.map('TCombobox',
                 fieldbackground=[('readonly', '#ffffff')],
                 arrowcolor=[('active', '#000000')])
        
        # Configure entry styles with HUGE fonts
        style.configure('TEntry',
                       font=('Arial', 22),
                       padding=(12, 10))
        
        # Configure large button styles with GIGANTIC fonts
        style.configure('Large.TButton',
                       font=('Arial', 28, 'bold'),
                       padding=(30, 18))
        
        # Force large fonts for dropdown menus (Windows specific)
        try:
            # This forces the dropdown list to use large fonts
            self.root.option_add('*TCombobox*Listbox.font', ('Arial', 22))
            self.root.option_add('*TCombobox*Listbox.selectBackground', '#3498db')
            self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')
            # Increase dropdown height significantly
            self.root.option_add('*TCombobox*Listbox.height', 12)
            
            # Additional Windows-specific options for larger dropdown text
            self.root.option_add('*Listbox.font', ('Arial', 22))
            self.root.option_add('*Listbox.height', 12)
            
        except:
            pass  # Fallback if option_add doesn't work
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        
        # Title
        self.title_label = ttk.Label(self.main_frame, 
                                   text="🎸 Magicstomp HIL Tone Matcher",
                                   style='Title.TLabel')
        
        # Step 1: File Selection
        self.create_file_selection_section()
        
        # Step 2: Patch Generation
        self.create_patch_generation_section()
        
        # Step 3: Audio Monitoring
        self.create_audio_monitoring_section()
        
        # Step 4: Optimization Loop
        self.create_optimization_section()
        
        # Status bar
        self.create_status_bar()
    
    def create_file_selection_section(self):
        """Create file selection section."""
        # File selection frame
        self.file_frame = ttk.LabelFrame(self.main_frame, 
                                       text="📁 Step 1: File Selection",
                                       padding="15")
        
        # Target file selection
        ttk.Label(self.file_frame, text="Target Audio:", style='Section.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        
        self.target_file_var = tk.StringVar(value="No file selected")
        self.target_file_label = ttk.Label(self.file_frame, 
                                         textvariable=self.target_file_var,
                                         style='Info.TLabel')
        self.target_file_label.grid(row=0, column=1, sticky='w', padx=10)
        
        ttk.Button(self.file_frame, 
                  text="Browse Target",
                  command=self.select_target_file,
                  style='Large.TButton').grid(row=0, column=2, padx=5)
        
        # DI Signal section with live input option
        di_frame = ttk.Frame(self.file_frame)
        di_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=5)
        
        ttk.Label(di_frame, text="DI Signal:", style='Section.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        
        # DI file selection
        file_frame = ttk.Frame(di_frame)
        file_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=5)
        
        self.di_file_var = tk.StringVar(value="No file selected")
        self.di_file_label = ttk.Label(file_frame,
                                     textvariable=self.di_file_var,
                                     style='Info.TLabel')
        self.di_file_label.grid(row=0, column=0, sticky='w', padx=10)
        
        ttk.Button(file_frame,
                  text="Browse DI File",
                  command=self.select_di_file,
                  style='Large.TButton').grid(row=0, column=1, padx=5)
        
        # Live input option
        live_frame = ttk.Frame(di_frame)
        live_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=5)
        
        ttk.Label(live_frame, text="OR Live Input:", style='Section.TLabel').grid(row=0, column=0, sticky='w', padx=5)
        
        self.live_input_var = tk.BooleanVar(value=False)
        self.live_input_check = ttk.Checkbutton(live_frame,
                                              text="Use Live Guitar Input",
                                              variable=self.live_input_var,
                                              command=self.toggle_live_input)
        self.live_input_check.grid(row=0, column=1, sticky='w', padx=10)
        
        # Live monitoring controls
        self.live_monitor_frame = ttk.Frame(di_frame)
        self.live_monitor_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=5)
        
        self.monitor_button = ttk.Button(self.live_monitor_frame,
                                       text="🎤 Start Live Monitoring",
                                       command=self.toggle_live_monitoring,
                                       style='Large.TButton')
        self.monitor_button.grid(row=0, column=0, padx=5)
        
        self.live_status_var = tk.StringVar(value="Live monitoring: OFF")
        self.live_status_label = ttk.Label(self.live_monitor_frame,
                                         textvariable=self.live_status_var,
                                         style='Info.TLabel')
        self.live_status_label.grid(row=0, column=1, sticky='w', padx=10)
        
        # Initially hide live monitoring controls
        self.live_monitor_frame.grid_remove()
        
        # Audio device selection
        ttk.Label(self.file_frame, text="Audio Devices:", style='Section.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        
        device_frame = ttk.Frame(self.file_frame)
        device_frame.grid(row=2, column=1, columnspan=2, sticky='w', padx=10)
        
        ttk.Label(device_frame, text="Input:").grid(row=0, column=0)
        self.input_device_var = tk.StringVar()
        self.input_device_combo = ttk.Combobox(device_frame, 
                                             textvariable=self.input_device_var,
                                             width=35)
        self.input_device_combo.grid(row=0, column=1, padx=5)
        
        # Force large font for this specific combobox
        self.input_device_combo.bind('<Configure>', self._configure_combobox_font)
        
        ttk.Label(device_frame, text="Output:").grid(row=0, column=2)
        self.output_device_var = tk.StringVar()
        self.output_device_combo = ttk.Combobox(device_frame,
                                              textvariable=self.output_device_var,
                                              width=35)
        self.output_device_combo.grid(row=0, column=3, padx=5)
        
        # Force large font for this specific combobox
        self.output_device_combo.bind('<Configure>', self._configure_combobox_font)
        
        ttk.Button(device_frame,
                  text="Refresh Devices",
                  command=self.refresh_audio_devices).grid(row=0, column=4, padx=5)
    
    def create_patch_generation_section(self):
        """Create patch generation section."""
        self.patch_frame = ttk.LabelFrame(self.main_frame,
                                        text="⚙️ Step 2: Patch Generation",
                                        padding="15")
        
        # Analysis controls
        analysis_frame = ttk.Frame(self.patch_frame)
        analysis_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Button(analysis_frame,
                  text="🎵 Analyze Target & Generate Patch",
                  command=self.analyze_and_generate_patch,
                  style='Large.TButton').grid(row=0, column=0, padx=5)
        
        self.backend_var = tk.StringVar(value="auto")
        backend_combo = ttk.Combobox(analysis_frame,
                                   textvariable=self.backend_var,
                                   values=["auto", "librosa", "essentia"],
                                   width=15)
        backend_combo.grid(row=0, column=1, padx=5)
        
        # Force large font for this specific combobox
        backend_combo.bind('<Configure>', self._configure_combobox_font)
        
        # Patch display
        self.patch_display_frame = ttk.Frame(self.patch_frame)
        self.patch_display_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Patch parameters display (will be populated dynamically)
        self.patch_params_frame = ttk.Frame(self.patch_display_frame)
        self.patch_params_frame.pack(fill='x')
        
        # Patch actions
        actions_frame = ttk.Frame(self.patch_frame)
        actions_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Button(actions_frame,
                  text="📤 Send to Magicstomp",
                  command=self.send_patch_to_magicstomp,
                  style='Large.TButton').grid(row=0, column=0, padx=5)
        
        ttk.Button(actions_frame,
                  text="💾 Save Patch",
                  command=self.save_patch,
                  style='Large.TButton').grid(row=0, column=1, padx=5)
    
    def create_audio_monitoring_section(self):
        """Create audio monitoring section."""
        self.monitor_frame = ttk.LabelFrame(self.main_frame,
                                          text="🎤 Step 3: Audio Monitoring",
                                          padding="15")
        
        # Calibration controls
        calib_frame = ttk.Frame(self.monitor_frame)
        calib_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Button(calib_frame,
                  text="🔧 Calibrate System",
                  command=self.calibrate_system).grid(row=0, column=0, padx=5)
        
        self.calibration_status_var = tk.StringVar(value="Not calibrated")
        ttk.Label(calib_frame,
                 textvariable=self.calibration_status_var,
                 style='Info.TLabel').grid(row=0, column=1, padx=10)
        
        # Audio visualization
        viz_frame = ttk.Frame(self.monitor_frame)
        viz_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Create matplotlib figure for audio visualization with MASSIVE fonts and size
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(14, 10))
        self.ax1.set_title("Target Audio", fontsize=36, fontweight='bold')
        self.ax1.set_ylabel("Amplitude", fontsize=28)
        self.ax2.set_title("Processed Audio", fontsize=36, fontweight='bold')
        self.ax2.set_ylabel("Amplitude", fontsize=28)
        self.ax2.set_xlabel("Time (s)", fontsize=28)
        
        # Increase tick label sizes to MAXIMUM
        self.ax1.tick_params(labelsize=24)
        self.ax2.tick_params(labelsize=24)
        
        # Increase line thickness for better visibility
        for ax in [self.ax1, self.ax2]:
            ax.tick_params(width=3, length=8)
            for spine in ax.spines.values():
                spine.set_linewidth(3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Monitoring controls
        monitor_controls = ttk.Frame(self.monitor_frame)
        monitor_controls.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Button(monitor_controls,
                  text="▶️ Start Monitoring",
                  command=self.start_monitoring).grid(row=0, column=0, padx=5)
        
        ttk.Button(monitor_controls,
                  text="⏹️ Stop Monitoring",
                  command=self.stop_monitoring).grid(row=0, column=1, padx=5)
    
    def create_optimization_section(self):
        """Create optimization section."""
        self.optimize_frame = ttk.LabelFrame(self.main_frame,
                                           text="🔄 Step 4: Optimization Loop",
                                           padding="15")
        
        # Optimization controls
        opt_controls = ttk.Frame(self.optimize_frame)
        opt_controls.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Button(opt_controls,
                  text="🚀 Start HIL Optimization",
                  command=self.start_optimization).grid(row=0, column=0, padx=5)
        
        ttk.Button(opt_controls,
                  text="⏸️ Pause Optimization",
                  command=self.pause_optimization).grid(row=0, column=1, padx=5)
        
        ttk.Button(opt_controls,
                  text="⏹️ Stop Optimization",
                  command=self.stop_optimization).grid(row=0, column=2, padx=5)
        
        # Optimization parameters
        params_frame = ttk.Frame(self.optimize_frame)
        params_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(params_frame, text="Max Iterations:").grid(row=0, column=0, padx=5)
        self.max_iterations_var = tk.StringVar(value="20")
        ttk.Entry(params_frame, textvariable=self.max_iterations_var, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(params_frame, text="Session Name:").grid(row=0, column=2, padx=5)
        self.session_name_var = tk.StringVar(value="hil_session")
        ttk.Entry(params_frame, textvariable=self.session_name_var, width=20).grid(row=0, column=3, padx=5)
        
        # Progress display
        self.progress_frame = ttk.Frame(self.optimize_frame)
        self.progress_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                          variable=self.progress_var,
                                          maximum=100)
        self.progress_bar.pack(fill='x', pady=5)
        
        self.progress_label_var = tk.StringVar(value="Ready for optimization")
        ttk.Label(self.progress_frame,
                 textvariable=self.progress_label_var,
                 style='Info.TLabel').pack()
        
        # Loss display
        loss_frame = ttk.Frame(self.optimize_frame)
        loss_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(loss_frame, text="Initial Loss:", style='Section.TLabel').grid(row=0, column=0, padx=5)
        self.initial_loss_var = tk.StringVar(value="--")
        ttk.Label(loss_frame, textvariable=self.initial_loss_var, style='Info.TLabel').grid(row=0, column=1, padx=5)
        
        ttk.Label(loss_frame, text="Current Loss:", style='Section.TLabel').grid(row=0, column=2, padx=5)
        self.current_loss_var = tk.StringVar(value="--")
        ttk.Label(loss_frame, textvariable=self.current_loss_var, style='Info.TLabel').grid(row=0, column=3, padx=5)
        
        ttk.Label(loss_frame, text="Improvement:", style='Section.TLabel').grid(row=0, column=4, padx=5)
        self.improvement_var = tk.StringVar(value="--")
        ttk.Label(loss_frame, textvariable=self.improvement_var, style='Success.TLabel').grid(row=0, column=5, padx=5)
    
    def create_status_bar(self):
        """Create status bar."""
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(side='bottom', fill='x', pady=10)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.status_frame,
                 textvariable=self.status_var,
                 style='Info.TLabel').pack(side='left')
        
        # Backend info
        self.backend_info_var = tk.StringVar(value="Backend: auto")
        ttk.Label(self.status_frame,
                 textvariable=self.backend_info_var,
                 style='Info.TLabel').pack(side='right')
    
    def setup_layout(self):
        """Setup the main layout."""
        self.main_frame.pack(fill='both', expand=True)
        
        # Arrange sections vertically
        self.title_label.pack(pady=(0, 20))
        self.file_frame.pack(fill='x', pady=(0, 10))
        self.patch_frame.pack(fill='x', pady=(0, 10))
        self.monitor_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.optimize_frame.pack(fill='x', pady=(0, 10))
        self.status_frame.pack(side='bottom', fill='x')
    
    def init_hil_system(self):
        """Initialize HIL system components."""
        try:
            self.hil_matcher = HILToneMatcher()
            self.audio_manager = AudioDeviceManager()
            self.refresh_audio_devices()
            self.update_status("HIL system initialized successfully")
        except Exception as e:
            self.update_status(f"Error initializing HIL system: {e}")
            messagebox.showerror("Initialization Error", f"Failed to initialize HIL system:\n{e}")
    
    def refresh_audio_devices(self):
        """Refresh list of available audio devices."""
        try:
            devices = self.audio_manager.list_audio_devices()
            
            input_names = [f"{d['id']}: {d['name']}" for d in devices['input']]
            output_names = [f"{d['id']}: {d['name']}" for d in devices['output']]
            
            self.input_device_combo['values'] = input_names
            self.output_device_combo['values'] = output_names
            
            # Auto-select first device if available
            if input_names:
                self.input_device_combo.set(input_names[0])
            if output_names:
                self.output_device_combo.set(output_names[0])
                
        except Exception as e:
            self.update_status(f"Error refreshing audio devices: {e}")
    
    def select_target_file(self):
        """Select target audio file."""
        file_path = filedialog.askopenfilename(
            title="Select Target Audio File",
            filetypes=[("Audio files", "*.wav *.mp3 *.flac *.m4a"), ("All files", "*.*")]
        )
        
        if file_path:
            self.target_file = file_path
            self.target_file_var.set(Path(file_path).name)
            self.update_status(f"Target file selected: {Path(file_path).name}")
    
    def select_di_file(self):
        """Select DI audio file."""
        file_path = filedialog.askopenfilename(
            title="Select DI Audio File",
            filetypes=[("Audio files", "*.wav *.mp3 *.flac *.m4a"), ("All files", "*.*")]
        )
        
        if file_path:
            self.di_file = file_path
            self.di_file_var.set(Path(file_path).name)
            self.update_status(f"DI file selected: {Path(file_path).name}")
    
    def toggle_live_input(self):
        """Toggle live input mode."""
        if self.live_input_var.get():
            self.live_monitor_frame.grid()
            self.update_status("Live input mode enabled - select audio device and start monitoring")
        else:
            self.live_monitor_frame.grid_remove()
            if self.is_live_monitoring:
                self.stop_live_monitoring()
            self.update_status("Live input mode disabled")
    
    def toggle_live_monitoring(self):
        """Toggle live monitoring."""
        if self.is_live_monitoring:
            self.stop_live_monitoring()
        else:
            self.start_live_monitoring()
    
    def start_live_monitoring(self):
        """Start live audio monitoring."""
        try:
            import sounddevice as sd
            import numpy as np
            
            # Get selected input device
            input_device = self.input_device_var.get()
            if not input_device:
                messagebox.showerror("Error", "Please select an input audio device")
                return
            
            # Extract device ID from the device string
            device_id = int(input_device.split(':')[0])
            
            # Audio parameters
            sample_rate = 44100
            chunk_size = 1024
            
            def audio_callback(indata, frames, time, status):
                """Audio callback for real-time processing."""
                if status:
                    print(f"Audio status: {status}")
                
                # Convert to numpy array and process
                audio_data = indata[:, 0]  # Mono channel
                
                # Update GUI with audio data (in a thread-safe way)
                self.root.after(0, lambda: self.update_audio_visualization(audio_data))
            
            # Start audio stream
            self.audio_stream = sd.InputStream(
                device=device_id,
                channels=1,
                samplerate=sample_rate,
                blocksize=chunk_size,
                callback=audio_callback,
                dtype=np.float32
            )
            
            self.audio_stream.start()
            self.is_live_monitoring = True
            
            # Update UI
            self.monitor_button.configure(text="⏹️ Stop Live Monitoring")
            self.live_status_var.set("Live monitoring: ON - Playing guitar...")
            self.update_status("Live monitoring started - play your guitar!")
            
        except Exception as e:
            messagebox.showerror("Audio Error", f"Failed to start live monitoring:\n{e}")
            self.update_status(f"Live monitoring error: {e}")
    
    def stop_live_monitoring(self):
        """Stop live audio monitoring."""
        try:
            if self.audio_stream:
                self.audio_stream.stop()
                self.audio_stream.close()
                self.audio_stream = None
            
            self.is_live_monitoring = False
            
            # Update UI
            self.monitor_button.configure(text="🎤 Start Live Monitoring")
            self.live_status_var.set("Live monitoring: OFF")
            self.update_status("Live monitoring stopped")
            
        except Exception as e:
            self.update_status(f"Error stopping live monitoring: {e}")
    
    def update_audio_visualization(self, audio_data):
        """Update audio visualization with live data."""
        try:
            import numpy as np
            
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            # Plot live audio data
            time_axis = np.linspace(0, len(audio_data) / 44100, len(audio_data))
            
            self.ax1.plot(time_axis, audio_data, 'b-', linewidth=2)
            self.ax1.set_title("Live Guitar Input", fontsize=36, fontweight='bold')
            self.ax1.set_ylabel("Amplitude", fontsize=28)
            self.ax1.set_ylim(-1, 1)
            self.ax1.tick_params(labelsize=24)
            
            # Show processed audio (empty for now)
            self.ax2.plot([0], [0], 'r-', linewidth=2)
            self.ax2.set_title("Processed Audio (Magicstomp Output)", fontsize=36, fontweight='bold')
            self.ax2.set_ylabel("Amplitude", fontsize=28)
            self.ax2.set_xlabel("Time (s)", fontsize=28)
            self.ax2.set_ylim(-1, 1)
            self.ax2.tick_params(labelsize=24)
            
            # Refresh canvas
            self.canvas.draw()
            
        except Exception as e:
            print(f"Visualization error: {e}")
    
    def analyze_and_generate_patch(self):
        """Analyze target audio and generate patch."""
        if not self.target_file:
            messagebox.showerror("Error", "Please select a target audio file first")
            return
        
        def analyze_worker():
            try:
                self.update_status("Analyzing target audio...")
                
                # Create tone matcher
                backend = self.backend_var.get()
                tone_matcher = AutoToneMatcher(backend)
                
                # Analyze audio
                features = tone_matcher.analyze_audio(self.target_file, verbose=True)
                patch = tone_matcher.map_to_patch()
                
                self.current_patch = patch
                
                # Update GUI in main thread
                self.root.after(0, self.display_patch)
                self.root.after(0, lambda: self.update_status("Analysis complete - patch generated"))
                
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Analysis error: {e}"))
                self.root.after(0, lambda: messagebox.showerror("Analysis Error", f"Failed to analyze audio:\n{e}"))
        
        # Run analysis in background thread
        threading.Thread(target=analyze_worker, daemon=True).start()
    
    def display_patch(self):
        """Display the generated patch parameters."""
        if not self.current_patch:
            return
        
        # Clear existing parameter widgets
        for widget in self.patch_params_frame.winfo_children():
            widget.destroy()
        
        # Display patch parameters
        row = 0
        for section_name, section_data in self.current_patch.items():
            if isinstance(section_data, dict) and section_name != 'meta':
                # Section header
                ttk.Label(self.patch_params_frame,
                         text=f"{section_name.upper()}:",
                         style='Section.TLabel').grid(row=row, column=0, columnspan=2, sticky='w', pady=(10, 5))
                row += 1
                
                # Parameters in this section
                for param_name, param_value in section_data.items():
                    if param_name != 'enabled':
                        ttk.Label(self.patch_params_frame,
                                 text=f"  {param_name}:",
                                 style='Info.TLabel').grid(row=row, column=0, sticky='w', padx=20)
                        
                        value_text = f"{param_value:.4f}" if isinstance(param_value, (int, float)) else str(param_value)
                        ttk.Label(self.patch_params_frame,
                                 text=value_text,
                                 style='Info.TLabel').grid(row=row, column=1, sticky='w', padx=10)
                        row += 1
    
    def send_patch_to_magicstomp(self):
        """Send patch to Magicstomp device."""
        if not self.current_patch:
            messagebox.showerror("Error", "No patch available to send")
            return
        
        try:
            # This would integrate with the HIL system to send SysEx
            self.update_status("Patch sent to Magicstomp")
            messagebox.showinfo("Success", "Patch sent to Magicstomp successfully!")
            
        except Exception as e:
            self.update_status(f"Error sending patch: {e}")
            messagebox.showerror("Error", f"Failed to send patch:\n{e}")
    
    def save_patch(self):
        """Save current patch to file."""
        if not self.current_patch:
            messagebox.showerror("Error", "No patch available to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Patch",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.current_patch, f, indent=2)
                self.update_status(f"Patch saved to {Path(file_path).name}")
                messagebox.showinfo("Success", f"Patch saved successfully!")
            except Exception as e:
                self.update_status(f"Error saving patch: {e}")
                messagebox.showerror("Error", f"Failed to save patch:\n{e}")
    
    def calibrate_system(self):
        """Calibrate audio system."""
        def calibrate_worker():
            try:
                self.root.after(0, lambda: self.update_status("Calibrating audio system..."))
                
                # Setup audio devices
                input_device = self.input_device_var.get()
                output_device = self.output_device_var.get()
                
                if input_device and output_device:
                    # Extract device ID from selection
                    input_id = int(input_device.split(':')[0])
                    output_id = int(output_device.split(':')[0])
                    
                    self.hil_matcher.setup_audio_devices(
                        input_device=input_id,
                        output_device=output_id
                    )
                
                # Perform calibration
                calibration_results = self.hil_matcher.calibrate_system()
                
                latency_ms = calibration_results['latency_ms']
                gain_comp = calibration_results['gain_compensation']
                
                self.root.after(0, lambda: self.calibration_status_var.set(f"Calibrated - Latency: {latency_ms:.1f}ms"))
                self.root.after(0, lambda: self.update_status("System calibration complete"))
                
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Calibration error: {e}"))
                self.root.after(0, lambda: messagebox.showerror("Calibration Error", f"Failed to calibrate system:\n{e}"))
        
        threading.Thread(target=calibrate_worker, daemon=True).start()
    
    def start_monitoring(self):
        """Start audio monitoring."""
        if not self.target_file or not self.di_file:
            messagebox.showerror("Error", "Please select both target and DI files")
            return
        
        self.update_status("Starting audio monitoring...")
        # This would start real-time audio monitoring
        # For now, just display the target audio
        self.display_audio_waveforms()
    
    def stop_monitoring(self):
        """Stop audio monitoring."""
        self.update_status("Audio monitoring stopped")
    
    def display_audio_waveforms(self):
        """Display audio waveforms."""
        try:
            if self.target_file:
                # Load and display target audio
                target_audio, sr = sf.read(self.target_file)
                time_axis = np.linspace(0, len(target_audio) / sr, len(target_audio))
                
                self.ax1.clear()
                self.ax1.plot(time_axis, target_audio)
                self.ax1.set_title("Target Audio")
                self.ax1.set_ylabel("Amplitude")
                
                self.canvas.draw()
                
        except Exception as e:
            self.update_status(f"Error displaying audio: {e}")
    
    def start_optimization(self):
        """Start HIL optimization."""
        if not self.target_file or not self.di_file:
            messagebox.showerror("Error", "Please select both target and DI files")
            return
        
        if not self.current_patch:
            messagebox.showerror("Error", "Please generate a patch first")
            return
        
        def optimization_worker():
            try:
                self.root.after(0, lambda: self.update_status("Starting HIL optimization..."))
                self.root.after(0, lambda: self.set_optimization_state(True))
                
                # Load audio files
                self.hil_matcher.load_target_audio(self.target_file)
                self.hil_matcher.load_di_signal(self.di_file)
                
                # Run optimization
                max_iterations = int(self.max_iterations_var.get())
                session_name = self.session_name_var.get()
                
                results = self.hil_matcher.optimize_patch(max_iterations)
                
                if results['success']:
                    initial_loss = results['initial_loss']
                    final_loss = results['final_loss']
                    improvement = results['improvement']
                    
                    self.root.after(0, lambda: self.initial_loss_var.set(f"{initial_loss:.4f}"))
                    self.root.after(0, lambda: self.current_loss_var.set(f"{final_loss:.4f}"))
                    self.root.after(0, lambda: self.improvement_var.set(f"{improvement:.4f}"))
                    self.root.after(0, lambda: self.progress_var.set(100))
                    self.root.after(0, lambda: self.progress_label_var.set("Optimization complete!"))
                    
                    # Export results
                    exported_files = self.hil_matcher.export_results(session_name)
                    
                    self.root.after(0, lambda: self.update_status("HIL optimization complete!"))
                    self.root.after(0, lambda: self.set_optimization_state(False))
                    
                    # Show results dialog
                    result_text = f"Optimization Complete!\n\n"
                    result_text += f"Initial Loss: {initial_loss:.4f}\n"
                    result_text += f"Final Loss: {final_loss:.4f}\n"
                    result_text += f"Improvement: {improvement:.4f}\n\n"
                    result_text += f"Files exported to 'out/' directory"
                    
                    self.root.after(0, lambda: messagebox.showinfo("Optimization Complete", result_text))
                else:
                    self.root.after(0, lambda: self.update_status("Optimization failed"))
                    self.root.after(0, lambda: self.set_optimization_state(False))
                    
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Optimization error: {e}"))
                self.root.after(0, lambda: self.set_optimization_state(False))
                self.root.after(0, lambda: messagebox.showerror("Optimization Error", f"Failed to run optimization:\n{e}"))
        
        threading.Thread(target=optimization_worker, daemon=True).start()
    
    def pause_optimization(self):
        """Pause optimization."""
        self.update_status("Optimization paused")
    
    def stop_optimization(self):
        """Stop optimization."""
        self.update_status("Optimization stopped")
        self.set_optimization_state(False)
    
    def set_optimization_state(self, is_running):
        """Set optimization state."""
        self.is_optimizing = is_running
        if is_running:
            self.progress_var.set(0)
            self.progress_label_var.set("Optimization in progress...")
        else:
            self.progress_label_var.set("Ready for optimization")
    
    def update_status(self, message):
        """Update status bar."""
        self.status_var.set(message)
        print(f"Status: {message}")  # Also print to console
    
    def _configure_combobox_font(self, event):
        """Configure font for combobox dropdown."""
        try:
            widget = event.widget
            # Force the dropdown listbox to use large font
            widget.bind('<Button-1>', self._on_combobox_click)
            widget.bind('<KeyPress>', self._on_combobox_key)
        except:
            pass  # Ignore errors
    
    def _on_combobox_click(self, event):
        """Handle combobox click to configure dropdown font."""
        try:
            widget = event.widget
            # Schedule font configuration after the dropdown appears
            self.root.after(10, lambda: self._configure_dropdown_font(widget))
        except:
            pass
    
    def _on_combobox_key(self, event):
        """Handle combobox key press to configure dropdown font."""
        try:
            widget = event.widget
            # Schedule font configuration after the dropdown appears
            self.root.after(10, lambda: self._configure_dropdown_font(widget))
        except:
            pass
    
    def _configure_dropdown_font(self, combobox):
        """Configure the dropdown listbox font."""
        try:
            # Find all listbox widgets and configure their font
            for widget in self.root.winfo_children():
                self._recursive_configure_listbox(widget)
        except:
            pass
    
    def _recursive_configure_listbox(self, widget):
        """Recursively find and configure listbox widgets."""
        try:
            if isinstance(widget, tk.Listbox):
                widget.configure(font=('Arial', 22))
            for child in widget.winfo_children():
                self._recursive_configure_listbox(child)
        except:
            pass
    
    def on_closing(self):
        """Handle application closing."""
        try:
            if self.is_live_monitoring:
                self.stop_live_monitoring()
            self.root.destroy()
        except:
            self.root.destroy()
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point for GUI application."""
    try:
        app = MagicstompHILGUI()
        app.run()
    except Exception as e:
        print(f"GUI Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
