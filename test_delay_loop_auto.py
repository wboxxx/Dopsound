#!/usr/bin/env python3
"""
Test automatique: Delay sur les potentiomètres
=============================================

Test automatique qui dit ce que vous devriez voir et loop tout seul.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_delay_loop_auto():
    """Test automatique d'affichage de Delay."""
    print("🎸 Test Automatique: Delay sur les potentiomètres")
    print("=" * 55)
    print("Test automatique - regardez l'écran du Magicstomp")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\n🔄 DÉMARRAGE DU TEST AUTOMATIQUE")
    print("=" * 40)
    print("Le test va boucler automatiquement")
    print("Regardez l'écran du Magicstomp pour voir les changements")
    print("\nAppuyez sur Ctrl+C pour arrêter")
    
    time.sleep(3)  # Pause pour lire les instructions
    
    # Boucle automatique
    loop_count = 0
    while True:
        loop_count += 1
        print(f"\n🔄 BOUCLE {loop_count}")
        print("-" * 20)
        
        # Potentiomètre 1 (Control1 = offset 2)
        print("📤 Envoi: Potentiomètre 1 → Delay")
        print("👀 VOUS DEVRIEZ VOIR: 'DLY' ou 'Delay' sur le potentiomètre 1")
        ms.tweak_parameter(2, 0)  # Valeur 0 pour Delay
        time.sleep(2)
        
        # Potentiomètre 2 (Control2 = offset 4)  
        print("📤 Envoi: Potentiomètre 2 → Delay")
        print("👀 VOUS DEVRIEZ VOIR: 'DLY' ou 'Delay' sur le potentiomètre 2")
        ms.tweak_parameter(4, 0)  # Valeur 0 pour Delay
        time.sleep(2)
        
        # Potentiomètre 3 (Control3 = offset 6)
        print("📤 Envoi: Potentiomètre 3 → Delay") 
        print("👀 VOUS DEVRIEZ VOIR: 'DLY' ou 'Delay' sur le potentiomètre 3")
        ms.tweak_parameter(6, 0)  # Valeur 0 pour Delay
        time.sleep(2)
        
        print("✅ Boucle terminée - redémarrage dans 1 seconde...")
        time.sleep(1)

def main():
    """Test automatique."""
    try:
        test_delay_loop_auto()
    except KeyboardInterrupt:
        print("\n\n🛑 Test arrêté par l'utilisateur")
        print("✅ Test terminé")

if __name__ == "__main__":
    main()


