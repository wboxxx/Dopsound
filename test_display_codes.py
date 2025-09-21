#!/usr/bin/env python3
"""
Test des codes d'affichage Magicstomp
====================================

Test pour comprendre les codes d'affichage comme @ et les icônes de potentiomètres.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_display_codes():
    """Test des codes d'affichage."""
    print("🎸 Test Codes d'Affichage Magicstomp")
    print("=" * 45)
    print("Test pour comprendre l'affichage sur le Magicstomp")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons différentes valeurs et observons l'affichage...")
    print("Vous avez vu: @ + deux petits icônes de potentiomètres")
    
    # Test avec des valeurs simples
    test_values = [0, 1, 2, 10, 32, 64, 100, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/8: Valeur = {value}")
        
        # Modifier le potentiomètre 3
        success = ms.tweak_parameter(6, value)
        
        print(f"📤 Message envoyé: Potentiomètre 3 = {value}")
        print("👀 Regardez l'écran du Magicstomp...")
        print("   Décrivez exactement ce que vous voyez:")
        print("   - Des lettres? Des chiffres? Des symboles?")
        print("   - Combien de potentiomètres?")
        print("   - Quelle valeur affichée?")
        
        response = input("Description de l'écran: ").strip()
        
        if response:
            print(f"📝 Valeur {value} → {response}")
        else:
            print("❌ Pas de description")
        
        time.sleep(2)
    
    print("\n✅ Test terminé")
    print("\nRésumé des observations:")
    print("- Le @ semble être un code d'affichage spécifique")
    print("- Les icônes de potentiomètres indiquent l'état des contrôles")
    print("- Il faut comprendre la correspondance valeur → affichage")

def main():
    """Test des codes d'affichage."""
    test_display_codes()

if __name__ == "__main__":
    main()
