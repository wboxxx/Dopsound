#!/usr/bin/env python3
"""
Test simple du potentiomètre 3
==============================

Test si on arrive à faire bouger le potentiomètre 3 sur l'écran du Magicstomp.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_pot3_movement():
    """Test du mouvement du potentiomètre 3."""
    print("🎸 Test Potentiomètre 3 - Mouvement Visuel")
    print("=" * 50)
    print("Test si le potentiomètre 3 bouge sur l'écran du Magicstomp")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons le potentiomètre 3 avec différentes valeurs...")
    print("Regardez l'écran du Magicstomp - le potentiomètre 3 devrait changer")
    
    # Test avec des valeurs progressives
    test_values = [0, 32, 64, 96, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/5: Potentiomètre 3 = {value}")
        
        # Modifier le potentiomètre 3 directement
        # Control3 = offset 6 dans la section commune
        success = ms.tweak_parameter(6, value)
        
        print(f"📤 Message envoyé: Potentiomètre 3 = {value}")
        print("👀 Regardez l'écran du Magicstomp...")
        print("   Le potentiomètre 3 a-t-il changé?")
        print("   Tapez 'O' si oui, 'N' si non")
        
        response = input("Le potentiomètre 3 a bougé? (O/N): ").strip().upper()
        
        if response == 'O':
            print(f"🎉 SUCCESS! Le potentiomètre 3 bouge avec la valeur {value}!")
            print("On peut contrôler le potentiomètre 3!")
            return True
        else:
            print("❌ Le potentiomètre 3 n'a pas bougé")
        
        time.sleep(2)  # Attendre un peu entre les tests
    
    print("\n❌ Le potentiomètre 3 n'a pas bougé avec aucune valeur")
    print("Il y a peut-être un problème avec l'offset ou la méthode")
    return False

def main():
    """Test du potentiomètre 3."""
    test_pot3_movement()

if __name__ == "__main__":
    main()


