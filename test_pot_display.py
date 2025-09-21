#!/usr/bin/env python3
"""
Test de l'affichage des potentiomètres
=====================================

Test pour comprendre ce qui s'affiche sur le Magicstomp.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_pot_display():
    """Test de l'affichage des potentiomètres."""
    print("🎸 Test Affichage Potentiomètres")
    print("=" * 40)
    print("Test pour comprendre l'affichage sur le Magicstomp")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons différentes valeurs pour le potentiomètre 3...")
    print("Dites-moi ce que vous voyez sur l'écran du Magicstomp")
    
    # Test avec des valeurs progressives
    test_values = [0, 32, 64, 96, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/5: Potentiomètre 3 = {value}")
        
        # Modifier le potentiomètre 3
        success = ms.tweak_parameter(6, value)
        
        print(f"📤 Message envoyé: Potentiomètre 3 = {value}")
        print("👀 Regardez l'écran du Magicstomp...")
        print("   Que voyez-vous? Décrivez ce qui s'affiche")
        
        response = input("Description de l'écran: ").strip()
        
        if response:
            print(f"📝 Valeur {value}: {response}")
        else:
            print("❌ Pas de description")
        
        time.sleep(2)
    
    print("\n✅ Test terminé")
    print("Résumé de ce qui s'affiche sur le Magicstomp:")

def main():
    """Test de l'affichage."""
    test_pot_display()

if __name__ == "__main__":
    main()
