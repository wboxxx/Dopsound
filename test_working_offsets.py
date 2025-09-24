#!/usr/bin/env python3
"""
Test avec les offsets qui marchaient hier
========================================

Retour aux offsets de contrôle qui fonctionnaient :
- Control1 = offset 2
- Control2 = offset 4  
- Control3 = offset 6
"""

import time
from realtime_magicstomp import RealtimeMagicstomp

def test_working_offsets():
    """Test avec les offsets qui marchaient hier."""
    print("🧪 Test avec les offsets qui marchaient hier")
    print("=" * 50)
    
    try:
        rt = RealtimeMagicstomp(auto_detect=True)
        
        if not rt.output_port:
            print("❌ Pas de connexion MIDI")
            return False
        
        print(f"✅ Connecté au Magicstomp: {rt.midi_port_name}")
        print("📺 Regardez l'écran du Magicstomp pendant le test")
        
        # Test 1: Control3 (offset 6) - celui qui marchait hier
        print("\n🧪 Test 1: Control3 (offset 6)")
        print("Hier ça marchait et on voyait des changements sur l'écran")
        
        values = [0, 1, 2, 10, 20]
        for value in values:
            print(f"📤 Envoi Control3 = {value}")
            rt.tweak_parameter(6, value, immediate=True)
            time.sleep(2)
        
        # Test 2: Control1 (offset 2) - aussi testé hier
        print("\n🧪 Test 2: Control1 (offset 2)")
        
        values = [0, 1, 2, 5, 10]
        for value in values:
            print(f"📤 Envoi Control1 = {value}")
            rt.tweak_parameter(2, value, immediate=True)
            time.sleep(2)
        
        # Test 3: Control2 (offset 4) - pour compléter
        print("\n🧪 Test 3: Control2 (offset 4)")
        
        values = [0, 1, 2, 5, 10]
        for value in values:
            print(f"📤 Envoi Control2 = {value}")
            rt.tweak_parameter(4, value, immediate=True)
            time.sleep(2)
        
        print("\n✅ Test terminé !")
        print("💡 Si vous avez vu des changements sur l'écran du Magicstomp, ces offsets marchent encore !")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    finally:
        if 'rt' in locals():
            rt.stop()

def main():
    """Lance le test avec les offsets qui marchaient."""
    print("🎸 Test avec les offsets qui marchaient hier")
    print("=" * 50)
    print("On retourne aux offsets de contrôle (2, 4, 6) qui fonctionnaient")
    print("Regardez l'écran du Magicstomp pour voir les changements")
    print()
    
    input("Appuyez sur Entrée pour commencer le test...")
    
    success = test_working_offsets()
    
    if success:
        print("\n🎉 Test réussi ! Ces offsets marchent encore.")
        print("💡 Le problème est qu'on utilise maintenant de mauvais offsets.")
    else:
        print("\n❌ Test échoué. Vérifiez la connexion MIDI.")

if __name__ == "__main__":
    main()
