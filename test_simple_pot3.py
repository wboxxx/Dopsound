#!/usr/bin/env python3
"""
Test simple du potentiomètre 3 assigné à FLDP
=============================================

Vous avez le potentiomètre 3 assigné à FLDP (Flanger Depth).
Testons de modifier sa valeur directement.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_pot3_flanger_depth():
    """Test du potentiomètre 3 assigné à FLDP."""
    print("🎸 Test Potentiomètre 3 - FLDP (Flanger Depth)")
    print("=" * 50)
    print("Votre potentiomètre 3 est assigné à FLDP")
    print("Testons de modifier sa valeur...")
    
    ms = RealtimeMagicstomp()
    if not ms._initialize_midi():
        return
    
    print("\nTestons différentes valeurs pour FLDP:")
    
    # Test avec des valeurs progressives
    test_values = [0, 32, 64, 96, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/5: FLDP = {value}")
        
        # Envoyer la valeur directement au potentiomètre 3
        # Le potentiomètre 3 est déjà assigné à FLDP, on modifie juste sa valeur
        success = ms.tweak_parameter(6, value, section=0)  # Control3 = offset 6, section commune
        
        if success:
            print(f"✅ Message envoyé: Potentiomètre 3 (FLDP) = {value}")
            print("👂 Écoutez le changement de profondeur du flanger...")
            print("   Tapez 'C' si vous entendez un changement")
            print("   Tapez 'N' si aucun changement audible")
            print("   Tapez 'r' pour refaire ce test")
            
            response = input("Votre réponse (C/N/r): ").strip().upper()
            
            if response == 'C':
                print(f"🎉 SUCCESS! FLDP {value} a un effet audible!")
                print("Le potentiomètre 3 contrôle bien la profondeur du flanger!")
                return True
            elif response == 'R':
                print("🔄 Retest de la même valeur...")
                i -= 1  # Refaire le même test
                continue
            else:
                print("❌ Pas d'effet audible avec cette valeur")
        else:
            print("❌ Échec d'envoi du message")
        
        time.sleep(1)
    
    print("\n❌ Aucune valeur n'a produit d'effet audible")
    print("Peut-être que l'effet flanger n'est pas activé ou configuré correctement")
    return False

def main():
    """Test simple du potentiomètre 3."""
    print("🎸 Test Simple - Potentiomètre 3 (FLDP)")
    print("=" * 40)
    
    test_pot3_flanger_depth()

if __name__ == "__main__":
    main()
