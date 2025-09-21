#!/usr/bin/env python3
"""
Test direct du paramètre FLDP (Flanger Depth)
==============================================

Test direct du paramètre flanger depth sans passer par les potentiomètres.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_flanger_depth_direct():
    """Test direct du paramètre FLDP."""
    print("🎸 Test Direct FLDP (Flanger Depth)")
    print("=" * 50)
    print("Test du paramètre flanger depth directement")
    
    ms = RealtimeMagicstomp()
    if not ms._initialize_midi():
        return
    
    print("\nTestons différentes valeurs pour FLDP...")
    print("(Le paramètre FLDP devrait être dans la section effet)")
    
    # Test avec des valeurs progressives
    test_values = [0, 32, 64, 96, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/5: FLDP = {value}")
        
        # Essayer de modifier directement le paramètre FLDP
        # FLDP pourrait être dans la section effet (section=1)
        # On va tester plusieurs offsets possibles pour FLDP
        
        # Offset 53 = Flanger Depth dans AmpMultiFlangeKnobParameters
        success = ms.tweak_parameter(53, value, section=1)
        
        if success:
            print(f"✅ Message envoyé: FLDP (offset 53) = {value}")
            print("👂 Écoutez le changement de profondeur du flanger...")
            print("   Tapez 'C' si vous entendez un changement")
            print("   Tapez 'N' si aucun changement audible")
            print("   Tapez 'r' pour refaire ce test")
            
            response = input("Votre réponse (C/N/r): ").strip().upper()
            
            if response == 'C':
                print(f"🎉 SUCCESS! FLDP {value} a un effet audible!")
                print("Le paramètre FLDP est bien contrôlé!")
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
    print("Peut-être que l'effet flanger n'est pas activé ou l'offset est incorrect")
    return False

def test_flanger_other_offsets():
    """Test d'autres offsets possibles pour FLDP."""
    print("\n🔍 Test d'autres offsets possibles pour FLDP...")
    
    ms = RealtimeMagicstomp()
    if not ms._initialize_midi():
        return
    
    # D'après le mapping MagicstompFrenzy, FLDP pourrait être à différents offsets
    possible_offsets = [
        (53, "Flanger Depth (AmpMultiFlange)"),
        (54, "Flanger Feedback (AmpMultiFlange)"), 
        (55, "Flanger Level (AmpMultiFlange)"),
        (9, "Flanger Depth (FlangeKnobParameters)"),
        (10, "Flanger Feedback (FlangeKnobParameters)")
    ]
    
    for offset, description in possible_offsets:
        print(f"\nTest offset {offset}: {description}")
        print("Valeur test: 64")
        
        success = ms.tweak_parameter(offset, 64, section=1)
        
        if success:
            print(f"✅ Message envoyé: Offset {offset} = 64")
            response = input("Changement audible? (C/N): ").strip().upper()
            if response == 'C':
                print(f"🎉 SUCCESS! Offset {offset} contrôle bien le flanger!")
                return offset
            else:
                print("❌ Pas d'effet audible")
        else:
            print("❌ Échec d'envoi du message")
        
        time.sleep(1)
    
    return None

def main():
    """Test du paramètre FLDP."""
    print("🎸 Test FLDP (Flanger Depth) - Paramètre Direct")
    print("=" * 50)
    
    # Test direct
    if test_flanger_depth_direct():
        return
    
    # Test d'autres offsets
    working_offset = test_flanger_other_offsets()
    if working_offset:
        print(f"\n🎉 Offset {working_offset} fonctionne pour FLDP!")
    else:
        print("\n❌ Aucun offset trouvé pour FLDP")

if __name__ == "__main__":
    main()
