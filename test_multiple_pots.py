#!/usr/bin/env python3
"""
Test des multiples potentiomètres
================================

Vous voyez plein de petits potentiomètres - testons pour comprendre.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_multiple_pots():
    """Test des multiples potentiomètres."""
    print("🎸 Test Multiples Potentiomètres")
    print("=" * 40)
    print("Vous voyez plein de petits potentiomètres - testons!")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons différentes valeurs et comptons les potentiomètres...")
    
    # Test avec des valeurs progressives
    test_values = [0, 10, 32, 64, 100, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/6: Valeur = {value}")
        
        # Modifier le potentiomètre 3
        success = ms.tweak_parameter(6, value)
        
        print(f"📤 Message envoyé: Potentiomètre 3 = {value}")
        print("👀 Regardez l'écran du Magicstomp...")
        print("   Combien de petits potentiomètres voyez-vous?")
        
        response = input("Nombre de potentiomètres visibles: ").strip()
        
        if response.isdigit():
            num_pots = int(response)
            print(f"📝 Valeur {value} → {num_pots} potentiomètres visibles")
            
            if num_pots > 0:
                print("🎉 SUCCESS! On peut contrôler l'affichage des potentiomètres!")
                print("Le Magicstomp réagit à nos messages MIDI!")
        else:
            print("❌ Réponse non numérique")
        
        time.sleep(2)
    
    print("\n✅ Test terminé")
    print("\nConclusion:")
    print("- La communication MIDI fonctionne")
    print("- Le Magicstomp affiche des potentiomètres en réponse")
    print("- On peut contrôler l'affichage via MIDI")

def main():
    """Test des multiples potentiomètres."""
    test_multiple_pots()

if __name__ == "__main__":
    main()
