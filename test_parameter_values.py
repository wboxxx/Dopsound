#!/usr/bin/env python3
"""
Test des valeurs de paramètres
==============================

Si les paramètres se remettent à zéro, le problème peut être:
1. Checksum incorrect
2. Format de données incorrect
3. Valeurs hors plage
"""

import time
import mido
from realtime_magicstomp import RealtimeMagicstomp


def test_checksum_calculation():
    """Test si le checksum est correct."""
    print("🧮 Test du calcul de checksum")
    print("=" * 50)
    
    # Test avec des valeurs connues
    test_cases = [
        (9, 30, "Amp Level 30"),
        (9, 64, "Amp Level 64"), 
        (9, 100, "Amp Level 100"),
        (2, 0, "Control1 OFF"),
        (2, 1, "Control1 ON"),
    ]
    
    rt = RealtimeMagicstomp()
    
    for offset, value, description in test_cases:
        print(f"\n🧪 Test: {description}")
        print(f"  Offset: {offset}, Valeur: {value}")
        
        # Test direct avec notre méthode
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(1)
        
        response = input(f"  {description}: Paramètre visible à l'écran ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print(f"  ✅ {description} fonctionne!")
        else:
            print(f"  ❌ {description} ne fonctionne pas")
    
    rt.stop()


def test_sysex_format():
    """Test du format SysEx directement."""
    print(f"\n📤 Test du format SysEx direct")
    print("=" * 50)
    
    try:
        port = mido.open_output('2- Yamaha UB9-1 5')
        
        print("Test 1: Amp Level avec checksum manuel")
        
        # Format: F0 43 7D 40 55 42 20 00 09 [data] [checksum] F7
        # Calculons le checksum manuellement
        
        # Test avec valeur 64 (0x40)
        data = [0x20, 0x00, 0x09, 0x40]  # Section, offset, data
        checksum = 0x80 - (sum(data) & 0x7F)
        checksum = checksum & 0x7F
        
        sysex_data = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42] + data + [checksum, 0xF7]
        
        print(f"  SysEx: {[hex(x) for x in sysex_data]}")
        port.send(mido.Message('sysex', data=sysex_data))
        time.sleep(1)
        
        response = input("  Amp Level 64: Paramètre visible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print("  ✅ Format SysEx correct!")
        else:
            print("  ❌ Format SysEx incorrect")
            
        # Test avec valeur 100 (0x64)
        data = [0x20, 0x00, 0x09, 0x64]  # Section, offset, data
        checksum = 0x80 - (sum(data) & 0x7F)
        checksum = checksum & 0x7F
        
        sysex_data = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42] + data + [checksum, 0xF7]
        
        print(f"  SysEx: {[hex(x) for x in sysex_data]}")
        port.send(mido.Message('sysex', data=sysex_data))
        time.sleep(1)
        
        response = input("  Amp Level 100: Paramètre visible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print("  ✅ Format SysEx correct!")
        else:
            print("  ❌ Format SysEx incorrect")
            
        port.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_parameter_ranges():
    """Test des plages de paramètres."""
    print(f"\n📊 Test des plages de paramètres")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    # Test avec des valeurs dans différentes plages
    test_values = [
        (9, 0, "Amp Level 0 (min)"),
        (9, 32, "Amp Level 32 (1/4)"),
        (9, 64, "Amp Level 64 (1/2)"),
        (9, 96, "Amp Level 96 (3/4)"),
        (9, 127, "Amp Level 127 (max)"),
    ]
    
    for offset, value, description in test_values:
        print(f"\n🧪 Test: {description}")
        
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(1)
        
        response = input(f"  {description}: Paramètre visible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print(f"  ✅ {description} fonctionne!")
        else:
            print(f"  ❌ {description} ne fonctionne pas")
    
    rt.stop()


def test_different_parameters():
    """Test de différents paramètres."""
    print(f"\n🎛️ Test de différents paramètres")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    # Test de différents offsets
    test_params = [
        (2, 0, "Control1 OFF"),
        (2, 1, "Control1 ON"),
        (4, 0, "Control2 OFF"),
        (4, 1, "Control2 ON"),
        (6, 0, "Control3 OFF"),
        (6, 1, "Control3 ON"),
        (9, 64, "Amp Level 64"),
        (10, 64, "Amp Type 64"),
        (11, 64, "Speaker Sim 64"),
    ]
    
    for offset, value, description in test_params:
        print(f"\n🧪 Test: {description}")
        
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(1)
        
        response = input(f"  {description}: Paramètre visible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print(f"  ✅ {description} fonctionne!")
        else:
            print(f"  ❌ {description} ne fonctionne pas")
    
    rt.stop()


def main():
    """Fonction principale."""
    print("🎸 Test des valeurs de paramètres")
    print("=" * 60)
    print("Vous avez vu les paramètres se faire resetter - la communication fonctionne!")
    print("Testons maintenant pourquoi ils se remettent à zéro...")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Regardez l'écran pendant les tests")
    print("3. Notez si les paramètres changent ou se remettent à zéro")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        # Test 1: Calcul de checksum
        print("\n" + "="*60)
        test_checksum_calculation()
        
        # Test 2: Format SysEx
        print("\n" + "="*60)
        test_sysex_format()
        
        # Test 3: Plages de paramètres
        print("\n" + "="*60)
        test_parameter_ranges()
        
        # Test 4: Différents paramètres
        print("\n" + "="*60)
        test_different_parameters()
        
        print(f"\n📊 ANALYSE:")
        print(f"Si les paramètres se remettent à zéro, le problème est probablement:")
        print(f"1. Checksum incorrect")
        print(f"2. Format de données incorrect")
        print(f"3. Valeurs hors plage autorisée")
        print(f"4. Offset incorrect")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
