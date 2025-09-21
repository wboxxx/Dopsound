#!/usr/bin/env python3
"""
Enhanced GUI Launcher with Impact Visualization
==============================================

Launcher that integrates the Magicstomp effects widgets with impact visualization
into the existing HIL GUI system. Provides complete workflow with visual feedback.
"""

import sys
from pathlib import Path

# Add gui directory to path
sys.path.insert(0, str(Path(__file__).parent / "gui"))

try:
    from enhanced_main_window import main
    
    if __name__ == "__main__":
        print("🎸 Starting Enhanced Magicstomp HIL GUI with Impact Visualization...")
        print("🔤 Font sizes optimized for ULTIMATE readability:")
        print("   - Title: 56px bold (GIGANTIC!)")
        print("   - Sections: 32px bold") 
        print("   - Info text: 24px")
        print("   - Buttons: 24px-28px bold")
        print("   - Graph titles: 36px")
        print("📊 Graph size: 14x10 (HUGE for better visibility)")
        print("📏 Window size: 1800x1200 (spacious for massive fonts)")
        print("🎯 NEW: Impact visualization for parameter changes")
        print("📈 NEW: Before/after comparison charts")
        print("🎛️ NEW: Magicstomp effect widgets integration")
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
