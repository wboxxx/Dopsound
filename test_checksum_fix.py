#!/usr/bin/env python3
"""
Test de la correction du checksum
=================================

Testons si la correction du checksum résout le problème.
"""

import time
from realtime_magicstomp import RealtimeMagicstomp


def test_checksum_fix():
    """Test de la correction du checksum."""
    print("🧮 Test de la correction du checksum")
    print("=" * 50)
    print("Testons si la correction du checksum 0 résout le problème...")
    print()
    
    rt = RealtimeMagicstomp()
    
    # Test des valeurs problématiques
    test_cases = [
        (9, 30, "Amp Level 30 (checksum normal)"),
        (9, 64, "Amp Level 64 (checksum était 0)"),
        (9, 100, "Amp Level 100 (checksum normal)"),
    ]
    
    for offset, value, description in test_cases:
        print(f"\n🧪 Test: {description}")
        
        # Affiche le message qui sera envoyé
        message = rt.create_parameter_message(offset, [value])
        checksum = message[-2]  # Avant-dernier byte
        
        print(f"  Message: {[hex(x) for x in message]}")
        print(f"  Checksum: {hex(checksum)} ({checksum})")
        
        # Envoie le message
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(1)
        
        response = input(f"  {description}: Paramètre visible à l'écran ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print(f"  ✅ {description} fonctionne!")
        else:
            print(f"  ❌ {description} ne fonctionne pas")
    
    rt.stop()


def test_audible_changes():
    """Test des changements audibles."""
    print(f"\n🔊 Test des changements audibles")
    print("=" * 50)
    print("Maintenant testons si les changements sont audibles...")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("🧪 Test: Amp Level avec guitare")
    print("  - Connectez votre guitare")
    print("  - Réglez le volume audible")
    print("  - Jouez quelques notes")
    
    input("  Appuyez sur Entrée quand vous êtes prêt...")
    
    # Test avec des valeurs très différentes
    test_values = [
        (20, "très faible"),
        (80, "fort"),
        (64, "normal"),
    ]
    
    for value, description in test_values:
        print(f"\n  - Amp Level = {value} ({description})")
        rt.tweak_parameter(9, value, immediate=True)
        time.sleep(0.5)
        
        print("  Jouez votre guitare...")
        response = input(f"  Son {description} audible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print(f"  ✅ Son {description} audible!")
        else:
            print(f"  ❌ Son {description} non audible")
    
    rt.stop()


def main():
    """Fonction principale."""
    print("🧮 Test de la correction du checksum")
    print("=" * 60)
    print("Le problème était probablement le checksum = 0 pour Amp Level 64")
    print("Testons si la correction résout le problème...")
    print()
    
    try:
        # Test 1: Correction du checksum
        print("=" * 60)
        test_checksum_fix()
        
        # Test 2: Changements audibles
        print("\n" + "=" * 60)
        test_audible_changes()
        
        print(f"\n📊 ANALYSE:")
        print(f"Si les paramètres fonctionnent maintenant, le problème était le checksum = 0")
        print(f"Si les paramètres ne fonctionnent toujours pas, le problème est ailleurs")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
