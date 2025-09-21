#!/usr/bin/env python3
"""
Large GUI Launcher for Magicstomp HIL System
===========================================

Launcher for the graphical interface with larger fonts and window size.
Optimized for better visibility and usability.
"""

import sys
from pathlib import Path

# Add gui directory to path
sys.path.insert(0, str(Path(__file__).parent / "gui"))

try:
    from main_window import main
    
    if __name__ == "__main__":
        print("🎸 Starting Magicstomp HIL GUI (Large Size)...")
        print("📏 Window size: 1600x1000")
        print("🔤 Font sizes: Enhanced for better visibility")
        main()
        
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
