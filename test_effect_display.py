#!/usr/bin/env python3
"""
Test affichage des effets sur Magicstomp
=======================================

Test pour voir si on peut modifier l'affichage des valeurs d'effets.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_effect_display():
    """Test de l'affichage des effets."""
    print("🎸 Test Affichage des Effets Magicstomp")
    print("=" * 45)
    print("Test pour voir l'affichage des valeurs d'effets")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons les paramètres d'effets...")
    print("Regardez juste l'affichage sur le Magicstomp")
    
    # Test des paramètres les plus importants
    test_params = [
        (30, "Gain"),
        (31, "Master"), 
        (78, "Delay Level"),
        (82, "Delay HPF"),
        (83, "Delay LPF"),
        (53, "Flanger Depth"),
    ]
    
    for i, (offset, name) in enumerate(test_params):
        print(f"\n--- Test {i+1}/6: {name} ---")
        print(f"Offset: {offset}")
        
        # Test avec différentes valeurs
        test_values = [0, 32, 64, 96, 127]
        
        for value in test_values:
            success = ms.tweak_parameter(offset, value)
            
            print(f"📤 {name} = {value}")
            print("👀 Regardez l'écran du Magicstomp...")
            print("   Que voyez-vous affiché?")
            
            response = input("Affichage: ").strip()
            
            if response:
                print(f"📝 {name} {value} → {response}")
                
                # Si on voit un changement, c'est bon
                if response != "rien" and response != "":
                    print(f"🎉 SUCCESS! {name} change l'affichage!")
                    break
            else:
                print("❌ Pas de réponse")
            
            time.sleep(1)
        
        print()
    
    print("✅ Test terminé")

def main():
    """Test de l'affichage des effets."""
    test_effect_display()

if __name__ == "__main__":
    main()
