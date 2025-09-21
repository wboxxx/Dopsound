#!/usr/bin/env python3
"""
Test des vrais paramètres d'effets Magicstomp
============================================

Basé sur le mapping étendu de MagicstompFrenzy.
Test des paramètres qui ont un effet audible direct.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_delay_level():
    """Test du niveau du delay (paramètre le plus audible)."""
    print("🎸 Test Delay Level (offset 78 = 0x4E)")
    print("=" * 50)
    
    ms = RealtimeMagicstomp()
    if not ms._initialize_midi():
        return
    
    print("Testons le Delay Level avec différentes valeurs...")
    
    # Test avec des valeurs progressives
    test_values = [0, 32, 64, 96, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/5: Delay Level = {value}")
        print("Envoyez la commande...")
        
        # Envoyer la commande (section effet = 1)
        success = ms.tweak_parameter(78, value, section=1)
        
        if success:
            print(f"✅ Message envoyé: Offset 78, Valeur {value}")
            print("👂 Écoutez le changement de niveau du delay...")
            print("   Tapez 'C' si vous entendez un changement")
            print("   Tapez 'N' si aucun changement audible")
            
            response = input("Votre réponse (C/N): ").strip().upper()
            
            if response == 'C':
                print(f"🎉 SUCCESS! Delay Level {value} a un effet audible!")
                return True
            else:
                print("❌ Pas d'effet audible avec cette valeur")
        else:
            print("❌ Échec d'envoi du message")
        
        time.sleep(1)
    
    return False

def test_gain_master():
    """Test du gain et master (très audibles)."""
    print("\n🎸 Test Gain & Master")
    print("=" * 50)
    
    ms = RealtimeMagicstomp()
    if not ms._initialize_midi():
        return
    
    # Test Gain (offset 30 = 0x1E)
    print("\n1. Test Gain (offset 30):")
    test_values = [64, 96, 32]  # Valeurs moyennes pour éviter saturation
    
    for value in test_values:
        print(f"   Gain = {value}")
        success = ms.tweak_parameter(30, value, section=1)
        if success:
            print(f"   ✅ Gain {value} envoyé - Écoutez le changement de gain")
            response = input("   Changement audible? (C/N): ").strip().upper()
            if response == 'C':
                print(f"   🎉 Gain {value} a un effet audible!")
                break
        time.sleep(1)
    
    # Test Master (offset 31 = 0x1F)  
    print("\n2. Test Master (offset 31):")
    for value in test_values:
        print(f"   Master = {value}")
        success = ms.tweak_parameter(31, value, section=1)
        if success:
            print(f"   ✅ Master {value} envoyé - Écoutez le changement de volume")
            response = input("   Changement audible? (C/N): ").strip().upper()
            if response == 'C':
                print(f"   🎉 Master {value} a un effet audible!")
                break
        time.sleep(1)

def test_delay_filters():
    """Test des filtres du delay (HPF/LPF)."""
    print("\n🎸 Test Delay Filters")
    print("=" * 50)
    
    ms = RealtimeMagicstomp()
    if not ms._initialize_midi():
        return
    
    # Test Delay HPF (offset 82 = 0x52)
    print("\n1. Test Delay HPF (offset 82):")
    test_values = [0, 64, 127]  # Différentes fréquences de coupure
    
    for value in test_values:
        print(f"   Delay HPF = {value}")
        success = ms.tweak_parameter(82, value, section=1)
        if success:
            print(f"   ✅ Delay HPF {value} envoyé - Écoutez le changement de filtrage")
            response = input("   Changement audible? (C/N): ").strip().upper()
            if response == 'C':
                print(f"   🎉 Delay HPF {value} a un effet audible!")
                break
        time.sleep(1)
    
    # Test Delay LPF (offset 83 = 0x53)
    print("\n2. Test Delay LPF (offset 83):")
    for value in test_values:
        print(f"   Delay LPF = {value}")
        success = ms.tweak_parameter(83, value, section=1)
        if success:
            print(f"   ✅ Delay LPF {value} envoyé - Écoutez le changement de filtrage")
            response = input("   Changement audible? (C/N): ").strip().upper()
            if response == 'C':
                print(f"   🎉 Delay LPF {value} a un effet audible!")
                break
        time.sleep(1)

def test_compressor():
    """Test des paramètres de compression."""
    print("\n🎸 Test Compressor")
    print("=" * 50)
    
    ms = RealtimeMagicstomp()
    if not ms._initialize_midi():
        return
    
    # Test Compressor Threshold (offset 52 = 0x34)
    print("\n1. Test Compressor Threshold (offset 52):")
    test_values = [0, 32, 64, 96, 127]
    
    for value in test_values:
        print(f"   Compressor Threshold = {value}")
        success = ms.tweak_parameter(52, value, section=1)
        if success:
            print(f"   ✅ Compressor Threshold {value} envoyé")
            response = input("   Changement audible? (C/N): ").strip().upper()
            if response == 'C':
                print(f"   🎉 Compressor Threshold {value} a un effet audible!")
                break
        time.sleep(1)

def main():
    """Menu principal de test."""
    print("🎸 Test des Vrais Paramètres d'Effets Magicstomp")
    print("=" * 60)
    print("Basé sur le mapping étendu de MagicstompFrenzy")
    print("Test des paramètres qui devraient avoir un effet audible direct")
    print()
    
    while True:
        print("\nChoisissez un test:")
        print("1. Delay Level (le plus audible)")
        print("2. Gain & Master (volume)")
        print("3. Delay Filters (HPF/LPF)")
        print("4. Compressor Threshold")
        print("5. Quitter")
        
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == '1':
            test_delay_level()
        elif choice == '2':
            test_gain_master()
        elif choice == '3':
            test_delay_filters()
        elif choice == '4':
            test_compressor()
        elif choice == '5':
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()
