#!/usr/bin/env python3
"""
GUI Demonstration Script
=======================

Demonstrates the complete GUI workflow with synthetic data.
Shows all features without requiring real hardware.
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
import numpy as np
import soundfile as sf
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from demo_hil import HILDemo


class GUIDemo:
    """
    GUI Demonstration class.
    
    Shows complete workflow with synthetic data.
    """
    
    def __init__(self, gui_app):
        """Initialize GUI demo."""
        self.gui_app = gui_app
        self.demo = HILDemo()
        
    def run_complete_demo(self):
        """Run complete GUI demonstration."""
        def demo_worker():
            try:
                # Step 1: Create demo files
                self.gui_app.root.after(0, lambda: self.gui_app.update_status("Creating demo files..."))
                
                self.demo.create_test_signals(duration=2.0)
                
                # Save demo files
                target_file = "demo_target.wav"
                di_file = "demo_di.wav"
                
                sf.write(target_file, self.demo.target_audio, 44100)
                sf.write(di_file, self.demo.di_signal, 44100)
                
                # Step 2: Simulate file selection
                self.gui_app.root.after(0, lambda: self.simulate_file_selection(target_file, di_file))
                
                # Step 3: Simulate analysis
                time.sleep(1)
                self.gui_app.root.after(0, lambda: self.simulate_analysis())
                
                # Step 4: Simulate calibration
                time.sleep(1)
                self.gui_app.root.after(0, lambda: self.simulate_calibration())
                
                # Step 5: Simulate optimization
                time.sleep(1)
                self.gui_app.root.after(0, lambda: self.simulate_optimization())
                
                self.gui_app.root.after(0, lambda: self.gui_app.update_status("Demo complete!"))
                
            except Exception as e:
                self.gui_app.root.after(0, lambda: self.gui_app.update_status(f"Demo error: {e}"))
    
    def simulate_file_selection(self, target_file, di_file):
        """Simulate file selection."""
        self.gui_app.target_file = target_file
        self.gui_app.di_file = di_file
        
        self.gui_app.target_file_var.set("demo_target.wav")
        self.gui_app.di_file_var.set("demo_di.wav")
        
        self.gui_app.update_status("Demo files selected")
    
    def simulate_analysis(self):
        """Simulate analysis process."""
        self.gui_app.update_status("Analyzing demo audio...")
        
        # Create a demo patch
        demo_patch = {
            "amp": {
                "model": "TWEED_BASSMAN",
                "gain": 0.6,
                "bass": 1.0,
                "mid": 0.4,
                "treble": 0.8,
                "presence": 0.7,
                "cab": "4x10_TWEED"
            },
            "booster": {
                "type": "DISTORTION",
                "level": 0.4
            },
            "delay": {
                "enabled": True,
                "mix": 0.25,
                "feedback": 0.35,
                "time_ms": 300
            },
            "reverb": {
                "enabled": True,
                "mix": 0.2,
                "decay_s": 1.5
            },
            "mod": {
                "enabled": True,
                "type": "CHORUS",
                "rate_hz": 0.8,
                "depth": 0.6,
                "mix": 0.3
            }
        }
        
        self.gui_app.current_patch = demo_patch
        self.gui_app.display_patch()
        self.gui_app.update_status("Demo patch generated")
    
    def simulate_calibration(self):
        """Simulate calibration process."""
        self.gui_app.update_status("Calibrating demo system...")
        
        # Simulate calibration results
        self.gui_app.calibration_status_var.set("Demo calibrated - Latency: 12.5ms")
        
        # Display demo audio
        self.gui_app.display_audio_waveforms()
        
        self.gui_app.update_status("Demo calibration complete")
    
    def simulate_optimization(self):
        """Simulate optimization process."""
        self.gui_app.update_status("Starting demo optimization...")
        
        # Simulate optimization progress
        for i in range(101):
            self.gui_app.root.after(i * 50, lambda i=i: self.update_progress(i))
        
        # Simulate final results
        self.gui_app.root.after(5000, lambda: self.show_final_results())
    
    def update_progress(self, progress):
        """Update optimization progress."""
        self.gui_app.progress_var.set(progress)
        self.gui_app.progress_label_var.set(f"Demo optimization... {progress}%")
        
        # Simulate loss improvement
        if progress > 0:
            initial_loss = 4.5
            current_loss = initial_loss * (1 - progress / 200)  # Simulate improvement
            improvement = initial_loss - current_loss
            
            self.gui_app.initial_loss_var.set(f"{initial_loss:.4f}")
            self.gui_app.current_loss_var.set(f"{current_loss:.4f}")
            self.gui_app.improvement_var.set(f"{improvement:.4f}")
    
    def show_final_results(self):
        """Show final optimization results."""
        self.gui_app.update_status("Demo optimization complete!")
        
        result_text = "🎸 Demo Complete!\n\n"
        result_text += "This demonstration showed:\n"
        result_text += "✅ File selection workflow\n"
        result_text += "✅ Patch generation and display\n"
        result_text += "✅ Audio visualization\n"
        result_text += "✅ Optimization progress tracking\n"
        result_text += "✅ Real-time loss monitoring\n\n"
        result_text += "Ready for real hardware testing!"
        
        messagebox.showinfo("Demo Complete", result_text)


def add_demo_button(gui_app):
    """Add demo button to GUI."""
    # Add demo button to file selection section
    demo_button = tk.Button(gui_app.file_frame,
                           text="🎬 Run Complete Demo",
                           command=lambda: GUIDemo(gui_app).run_complete_demo(),
                           bg='#3498db',
                           fg='white',
                           font=('Arial', 10, 'bold'))
    demo_button.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')


def main():
    """Main entry point for GUI demo."""
    try:
        # Import and run GUI with demo button
        from gui.main_window import MagicstompHILGUI
        
        app = MagicstompHILGUI()
        add_demo_button(app)
        
        print("🎬 Starting GUI Demo...")
        print("Click 'Run Complete Demo' to see the full workflow!")
        
        app.run()
        
    except Exception as e:
        print(f"❌ Demo Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
