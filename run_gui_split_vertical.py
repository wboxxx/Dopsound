#!/usr/bin/env python3
"""
Split Vertical GUI Launcher with Impact Visualization
====================================================

Version avec split vertical permanent :
- 80% gauche : Interface principale avec onglets
- 20% droite : Status/Logs toujours visible
"""

import sys
from pathlib import Path

# Add gui directory to path
sys.path.insert(0, str(Path(__file__).parent / "gui"))

try:
    from split_vertical_window import main
    
    if __name__ == "__main__":
        print("🎸 Starting Split Vertical Magicstomp HIL GUI...")
        print("🔤 Split vertical layout:")
        print("   - 80% gauche : Interface principale avec onglets")
        print("   - 20% droite : Status/Logs toujours visible")
        print("   - Font sizes: 10-14px (compact)")
        print("   - Window size: 1400x900 (optimized)")
        print("🎯 Impact visualization for parameter changes")
        print("📈 Before/after comparison charts")
        print("🎛️ Magicstomp effect widgets integration")
        print("📊 Status panel always visible for real-time feedback")
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
