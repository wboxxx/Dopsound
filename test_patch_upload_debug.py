#!/usr/bin/env python3
"""
Test de debug pour l'upload de patch
====================================

Compare le format temps réel (qui marche) vs patch upload (qui ne marche pas)
"""

import json
from adapter_magicstomp import MagicstompAdapter
from realtime_magicstomp import RealtimeMagicstomp

def test_patch_upload_debug():
    """Debug de l'upload de patch."""
    print("🔍 Debug de l'upload de patch")
    print("=" * 50)
    
    # Test 1: Format temps réel (qui marche)
    print("\n🧪 Test 1: Format temps réel (qui marche)")
    try:
        rt = RealtimeMagicstomp(auto_detect=True)
        if rt.output_port:
            print("✅ RealtimeMagicstomp connecté")
            print("📤 Test message temps réel...")
            rt.tweak_parameter(6, 5, immediate=True)
            print("✅ Message temps réel envoyé")
        else:
            print("❌ Pas de connexion RealtimeMagicstomp")
    except Exception as e:
        print(f"❌ Erreur RealtimeMagicstomp: {e}")
    
    # Test 2: Format patch upload (qui ne marche pas)
    print("\n🧪 Test 2: Format patch upload (qui ne marche pas)")
    try:
        adapter = MagicstompAdapter()
        
        # Patch simple pour test
        test_patch = {
            "meta": {"name": "Test Patch"},
            "compressor": {"enabled": True, "threshold": 0.5, "ratio": 2.0, "attack": 10.0, "release": 100.0, "makeup_gain": 3.0},
            "eq": {"enabled": True, "low_gain": 0.0, "mid_gain": 2.0, "high_gain": 0.0, "low_freq": 100.0, "mid_freq": 1000.0, "high_freq": 5000.0},
            "delay": {"enabled": True, "time": 300, "feedback": 0.3, "mix": 0.2, "low_cut": 100.0, "high_cut": 8000.0}
        }
        
        print("🔄 Conversion patch vers SysEx...")
        syx_data = adapter.json_to_syx(test_patch)
        
        print(f"📊 Taille du message SysEx: {len(syx_data)} bytes")
        print(f"📊 Header: {syx_data[:10]}")
        
        # Vérifier les bytes invalides
        invalid_bytes = []
        for i, byte in enumerate(syx_data):
            if byte > 127:
                invalid_bytes.append((i, byte))
        
        if invalid_bytes:
            print(f"❌ Bytes invalides trouvés: {invalid_bytes[:5]}...")
            print("💡 Les bytes > 127 causent des erreurs MIDI")
        else:
            print("✅ Tous les bytes sont valides (<= 127)")
        
        # Test d'envoi
        print("📤 Test d'envoi du patch...")
        if hasattr(adapter, 'realtime_magicstomp') and adapter.realtime_magicstomp.output_port:
            adapter.send_to_device(syx_data)
            print("✅ Patch envoyé")
        else:
            print("❌ Pas de connexion pour envoyer le patch")
            
    except Exception as e:
        print(f"❌ Erreur patch upload: {e}")
        import traceback
        traceback.print_exc()

def compare_headers():
    """Compare les headers temps réel vs patch upload."""
    print("\n🔍 Comparaison des headers")
    print("=" * 30)
    
    # Header temps réel (qui marche)
    rt_header = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42]
    print(f"⏰ Header temps réel: {[hex(x) for x in rt_header]}")
    
    # Header patch upload (qui ne marche pas)
    patch_header = [0xF0, 0x43, 0x00, 0x2D, 0x40, 0x00]
    print(f"📦 Header patch upload: {[hex(x) for x in patch_header]}")
    
    print("\n💡 Différences:")
    print("- Temps réel: 43 7D 40 55 42 (6 bytes)")
    print("- Patch upload: 43 00 2D 40 00 (6 bytes)")
    print("- Le patch upload utilise un format différent et plus complexe")

def main():
    """Lance les tests de debug."""
    print("🎸 Debug de l'upload de patch Magicstomp")
    print("=" * 50)
    
    compare_headers()
    test_patch_upload_debug()
    
    print("\n💡 Conclusion:")
    print("- Les messages temps réel marchent (format simple)")
    print("- Les uploads de patch échouent (format complexe avec bytes > 127)")
    print("- Il faut soit corriger le format patch, soit utiliser le temps réel")

if __name__ == "__main__":
    main()
