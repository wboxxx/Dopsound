#!/usr/bin/env python3
"""
Test simple du FLDP (Flanger Depth)
===================================

Test direct du paramètre flanger depth.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_flanger_depth():
    """Test du paramètre FLDP."""
    print("🎸 Test FLDP (Flanger Depth)")
    print("=" * 40)
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nTestons le paramètre FLDP (Flanger Depth)...")
    print("Votre potentiomètre 3 est assigné à FLDP")
    
    # Test avec des valeurs progressives
    test_values = [0, 32, 64, 96, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/5: FLDP = {value}")
        
        # Essayer de modifier directement le paramètre FLDP
        # D'après le mapping MagicstompFrenzy:
        # - Offset 53 = Flanger Depth dans AmpMultiFlangeKnobParameters
        # L'offset 53 > 32 donc c'est automatiquement la section effet
        success = ms.tweak_parameter(53, value)
        
        print(f"📤 Message envoyé: FLDP (offset 53) = {value}")
        print("👂 Écoutez le changement de profondeur du flanger...")
        print("   Tapez 'C' si vous entendez un changement")
        print("   Tapez 'N' si aucun changement audible")
        
        response = input("Votre réponse (C/N): ").strip().upper()
        
        if response == 'C':
            print(f"🎉 SUCCESS! FLDP {value} a un effet audible!")
            print("Le paramètre FLDP est bien contrôlé!")
            return True
        else:
            print("❌ Pas d'effet audible avec cette valeur")
        
        time.sleep(1)
    
    print("\n❌ Aucune valeur n'a produit d'effet audible")
    print("Peut-être que l'effet flanger n'est pas activé")
    return False

def main():
    """Test du paramètre FLDP."""
    test_flanger_depth()

if __name__ == "__main__":
    main()
