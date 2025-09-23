#!/usr/bin/env python3
"""
Test simple de bouton pour vérifier la communication
====================================================

Test direct et simple pour voir si on peut modifier un paramètre
sur le patch courant du Magicstomp.
"""

import time
from realtime_magicstomp import RealtimeMagicstomp

def test_simple_parameter_change():
    """Test simple de changement de paramètre."""
    print("🧪 Test simple de changement de paramètre")
    print("=" * 50)
    
    try:
        # Initialise avec auto-détection
        rt = RealtimeMagicstomp(auto_detect=True)
        
        if not rt.output_port:
            print("❌ Pas de connexion MIDI")
            return False
        
        print(f"✅ Connecté au Magicstomp: {rt.midi_port_name}")
        print("📺 Regardez l'écran du Magicstomp pendant le test")
        
        # Test 1: Delay Level (DLVL) - offset 67
        print("\n🧪 Test 1: Delay Level (DLVL)")
        print("Vous devriez voir 'DLVL' ou 'Delay Level' sur l'écran")
        
        values = [30, 60, 90]
        for value in values:
            print(f"📤 Envoi DLVL = {value}")
            rt.tweak_parameter(67, value, immediate=True)
            time.sleep(2)
        
        # Test 2: Delay High Pass Filter (DHPF) - offset 71  
        print("\n🧪 Test 2: Delay High Pass Filter (DHPF)")
        print("Vous devriez voir 'DHPF' ou 'HPF' sur l'écran")
        
        values = [20, 50, 80]
        for value in values:
            print(f"📤 Envoi DHPF = {value}")
            rt.tweak_parameter(71, value, immediate=True)
            time.sleep(2)
        
        # Test 3: Flanger Depth - offset 53
        print("\n🧪 Test 3: Flanger Depth")
        print("Vous devriez voir 'FLDP' ou 'Flanger Depth' sur l'écran")
        
        values = [10, 40, 70]
        for value in values:
            print(f"📤 Envoi Flanger Depth = {value}")
            rt.tweak_parameter(53, value, immediate=True)
            time.sleep(2)
        
        print("\n✅ Test terminé !")
        print("💡 Si vous avez vu des changements sur l'écran du Magicstomp, la communication fonctionne !")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    finally:
        if 'rt' in locals():
            rt.stop()

def main():
    """Lance le test simple."""
    print("🎸 Test Simple de Communication Magicstomp")
    print("=" * 50)
    print("Ce test va modifier des paramètres sur le patch courant")
    print("Regardez l'écran du Magicstomp pour voir les changements")
    print()
    
    input("Appuyez sur Entrée pour commencer le test...")
    
    success = test_simple_parameter_change()
    
    if success:
        print("\n🎉 Test réussi ! La communication fonctionne.")
    else:
        print("\n❌ Test échoué. Vérifiez la connexion MIDI.")

if __name__ == "__main__":
    main()
