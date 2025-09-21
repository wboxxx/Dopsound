#!/usr/bin/env python3
"""
Fullscreen GUI Launcher for Magicstomp HIL System
================================================

Launcher for the graphical interface in fullscreen mode.
Maximum visibility and workspace utilization.
"""

import sys
import tkinter as tk
from pathlib import Path

# Add gui directory to path
sys.path.insert(0, str(Path(__file__).parent / "gui"))

try:
    from main_window import MagicstompHILGUI
    
    def launch_fullscreen():
        """Launch GUI in fullscreen mode."""
        app = MagicstompHILGUI()
        
        # Get screen dimensions
        screen_width = app.root.winfo_screenwidth()
        screen_height = app.root.winfo_screenheight()
        
        # Set fullscreen geometry
        app.root.geometry(f"{screen_width}x{screen_height}")
        app.root.state('zoomed')  # Maximize window on Windows
        
        print(f"🎸 Starting Magicstomp HIL GUI (Fullscreen)...")
        print(f"📏 Screen size: {screen_width}x{screen_height}")
        print("🔤 Font sizes: Enhanced for better visibility")
        print("💡 Press F11 to toggle fullscreen mode")
        
        app.run()
    
    if __name__ == "__main__":
        launch_fullscreen()
        
except ImportError as e:
    print(f"❌ Error importing GUI modules: {e}")
    print("Please install required dependencies:")
    print("pip install matplotlib sounddevice")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error starting GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
