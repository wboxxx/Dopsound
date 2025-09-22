#!/usr/bin/env python3
"""
Test direct des paramètres d'effets
==================================

Test direct des paramètres d'effets pour l'optimisation.
On va tester les paramètres les plus audibles.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_direct_effect_params():
    """Test direct des paramètres d'effets."""
    print("🎸 Test Direct Paramètres d'Effets")
    print("=" * 40)
    print("Test des paramètres qui devraient avoir un effet audible")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons les paramètres d'effets directement...")
    print("Vous êtes sur le patch U01 - quel effet est activé?")
    
    # Test des paramètres les plus audibles d'après MagicstompFrenzy
    test_params = [
        # Delay Level (offset 78) - très audible
        (78, "Delay Level", "Niveau du delay - devrait être très audible"),
        
        # Gain (offset 30) - très audible  
        (30, "Gain", "Gain de l'amplificateur - très audible"),
        
        # Master (offset 31) - très audible
        (31, "Master", "Volume maître - très audible"),
        
        # Delay HPF (offset 82) - audible
        (82, "Delay HPF", "Filtre passe-haut du delay"),
        
        # Delay LPF (offset 83) - audible
        (83, "Delay LPF", "Filtre passe-bas du delay"),
        
        # Compressor Threshold (offset 52) - audible
        (52, "Compressor Threshold", "Seuil de compression"),
    ]
    
    for i, (offset, name, description) in enumerate(test_params):
        print(f"\n--- Test {i+1}/6: {name} ---")
        print(f"Offset: {offset} | Description: {description}")
        
        # Test avec une valeur moyenne
        test_value = 64
        success = ms.tweak_parameter(offset, test_value)
        
        print(f"📤 Message envoyé: {name} = {test_value}")
        print("🎸 Jouez de la guitare et écoutez...")
        print("   Y a-t-il un changement audible?")
        print("   Tapez 'O' si oui, 'N' si non")
        
        response = input("Changement audible? (O/N): ").strip().upper()
        
        if response == 'O':
            print(f"🎉 SUCCESS! {name} a un effet audible!")
            print(f"Offset {offset} contrôle bien {name}")
            return offset, name
        else:
            print(f"❌ Pas d'effet audible avec {name}")
        
        time.sleep(2)
    
    print("\n❌ Aucun paramètre n'a produit d'effet audible")
    print("Peut-être que les offsets ne correspondent pas au patch U01")
    return None, None

def test_patch_type():
    """Test pour identifier le type de patch."""
    print("\n🔍 Identification du type de patch...")
    print("Quel effet est activé sur votre patch U01?")
    print("Options possibles:")
    print("- Amp Simulator")
    print("- Delay") 
    print("- Reverb")
    print("- Chorus/Flanger")
    print("- Distortion")
    print("- Autre?")
    
    patch_type = input("Type d'effet sur U01: ").strip()
    print(f"Patch type: {patch_type}")
    return patch_type

def main():
    """Test des paramètres d'effets."""
    print("🎸 Test Paramètres d'Effets - Optimisation")
    print("=" * 50)
    
    # Identifier le type de patch
    patch_type = test_patch_type()
    
    # Tester les paramètres
    working_offset, working_name = test_direct_effect_params()
    
    if working_offset:
        print(f"\n🎉 SUCCESS! On peut contrôler {working_name}")
        print(f"Offset {working_offset} fonctionne pour l'optimisation!")
    else:
        print("\n❌ Aucun paramètre trouvé")
        print("Il faut peut-être tester d'autres offsets ou types d'effets")

if __name__ == "__main__":
    main()


