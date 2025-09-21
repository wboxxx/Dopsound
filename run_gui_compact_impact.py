#!/usr/bin/env python3
"""
Compact GUI Launcher with Impact Visualization
=============================================

Version compacte optimisée pour les résolutions standard.
Interface adaptative qui s'ajuste à la taille de l'écran.
"""

import sys
from pathlib import Path

# Add gui directory to path
sys.path.insert(0, str(Path(__file__).parent / "gui"))

try:
    from compact_main_window import main
    
    if __name__ == "__main__":
        print("🎸 Starting Compact Magicstomp HIL GUI with Impact Visualization...")
        print("🔤 Font sizes optimized for standard screens:")
        print("   - Title: 24px bold")
        print("   - Sections: 16px bold") 
        print("   - Info text: 12px")
        print("   - Buttons: 12px-14px")
        print("   - Graph titles: 16px")
        print("📊 Adaptive layout for better screen fit")
        print("📏 Window size: 1400x900 (compact and efficient)")
        print("🎯 Impact visualization for parameter changes")
        print("📈 Before/after comparison charts")
        print("🎛️ Magicstomp effect widgets integration")
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
