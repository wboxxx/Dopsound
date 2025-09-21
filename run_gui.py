#!/usr/bin/env python3
"""
GUI Launcher for Magicstomp HIL System
=====================================

Simple launcher script for the graphical interface.
"""

import sys
from pathlib import Path

# Add gui directory to path
sys.path.insert(0, str(Path(__file__).parent / "gui"))

try:
    from main_window import main
    
    if __name__ == "__main__":
        print("🎸 Starting Magicstomp HIL GUI...")
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
