#!/usr/bin/env python3
"""
Large Fonts GUI Launcher for Magicstomp HIL System
=================================================

Launcher optimized for large fonts and better readability.
Perfect for users who need bigger text without changing window size.
"""

import sys
from pathlib import Path

# Add gui directory to path
sys.path.insert(0, str(Path(__file__).parent / "gui"))

try:
    from main_window import main
    
    if __name__ == "__main__":
        print("🎸 Starting Magicstomp HIL GUI (Large Fonts)...")
        print("🔤 Font sizes optimized for readability:")
        print("   - Title: 32px bold")
        print("   - Sections: 20px bold") 
        print("   - Info text: 16px")
        print("   - Buttons: 16px-18px bold")
        print("   - Graph titles: 20px")
        print("📏 Window size: 1400x900 (compact but readable)")
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
