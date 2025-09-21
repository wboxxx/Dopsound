#!/usr/bin/env python3
"""
Tabbed Compact GUI Launcher with Impact Visualization
====================================================

Version ultra-compacte avec layout en onglets pour maximiser l'espace.
Optimisée pour les écrans de résolution standard.
"""

import sys
from pathlib import Path

# Add gui directory to path
sys.path.insert(0, str(Path(__file__).parent / "gui"))

try:
    from tabbed_compact_window import main
    
    if __name__ == "__main__":
        print("🎸 Starting Tabbed Compact Magicstomp HIL GUI...")
        print("🔤 Ultra-compact design with tabs:")
        print("   - Tabbed interface for maximum space efficiency")
        print("   - Font sizes: 10-14px (standard)")
        print("   - Window size: 1200x800 (fits most screens)")
        print("   - Organized in logical tabs")
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
