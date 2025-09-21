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
        print("🎸 Starting Magicstomp HIL GUI (MASSIVE Fonts + Large Graphs)...")
        print("🔤 Font sizes optimized for ULTIMATE readability:")
        print("   - Title: 56px bold (GIGANTIC!)")
        print("   - Sections: 32px bold") 
        print("   - Info text: 24px")
        print("   - Buttons: 24px-28px bold")
        print("   - Graph titles: 36px")
        print("📊 Graph size: 14x10 (HUGE for better visibility)")
        print("📏 Window size: 1800x1200 (spacious for massive fonts)")
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
