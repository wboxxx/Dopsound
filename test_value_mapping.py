#!/usr/bin/env python3
"""
Test de correspondance des valeurs
=================================

Test pour comprendre la correspondance entre nos valeurs et l'affichage.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_value_mapping():
    """Test de correspondance des valeurs."""
    print("🎸 Test Correspondance des Valeurs")
    print("=" * 40)
    print("Test pour comprendre l'affichage sur le Magicstomp")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons différentes valeurs et voyons ce qui s'affiche...")
    
    # Test avec des valeurs simples
    test_values = [0, 1, 10, 32, 64, 100, 127]
    
    for value in test_values:
        print(f"\nTest: Valeur envoyée = {value}")
        
        # Modifier le potentiomètre 3
        success = ms.tweak_parameter(6, value)
        
        print(f"📤 Message envoyé: Potentiomètre 3 = {value}")
        print("👀 Regardez l'écran du Magicstomp...")
        print("   Que voyez-vous s'afficher?")
        
        response = input("Affichage sur l'écran: ").strip()
        
        if response:
            print(f"📝 Valeur {value} → Affichage: {response}")
        else:
            print("❌ Pas de réponse")
        
        time.sleep(1)
    
    print("\n✅ Test terminé")
    print("Résumé de la correspondance:")

def main():
    """Test de correspondance."""
    test_value_mapping()

if __name__ == "__main__":
    main()


