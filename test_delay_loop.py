#!/usr/bin/env python3
"""
Test simple: afficher Delay sur les potentiomètres en boucle
===========================================================

Test simple pour voir si on peut afficher "Delay" sur les potentiomètres.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_delay_loop():
    """Test d'affichage de Delay en boucle."""
    print("🎸 Test Simple: Delay sur les potentiomètres")
    print("=" * 45)
    print("Affichage de Delay sur pot 1, 2, 3 en boucle")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons d'afficher Delay sur les potentiomètres...")
    print("Regardez l'écran du Magicstomp")
    
    # Boucle infinie
    loop_count = 0
    while True:
        loop_count += 1
        print(f"\n--- Boucle {loop_count} ---")
        
        # Potentiomètre 1 (Control1 = offset 2)
        print("📤 Potentiomètre 1 → Delay")
        ms.tweak_parameter(2, 0)  # Valeur 0 pour Delay
        time.sleep(2)
        
        # Potentiomètre 2 (Control2 = offset 4)  
        print("📤 Potentiomètre 2 → Delay")
        ms.tweak_parameter(4, 0)  # Valeur 0 pour Delay
        time.sleep(2)
        
        # Potentiomètre 3 (Control3 = offset 6)
        print("📤 Potentiomètre 3 → Delay") 
        ms.tweak_parameter(6, 0)  # Valeur 0 pour Delay
        time.sleep(2)
        
        print("🔄 Boucle terminée - redémarrage...")
        time.sleep(1)

def main():
    """Test en boucle."""
    test_delay_loop()

if __name__ == "__main__":
    main()


