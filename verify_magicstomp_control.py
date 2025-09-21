#!/usr/bin/env python3
"""
Vérification du contrôle Magicstomp
==================================

Test complet pour vérifier que les messages sysex modifient vraiment
les paramètres du Magicstomp.
"""

import time
import numpy as np
from realtime_magicstomp import RealtimeMagicstomp


def test_audible_parameter_changes():
    """
    Test des modifications audibles des paramètres.
    
    Cette fonction teste des paramètres qui devraient produire
    des changements audibles évidents.
    """
    print("🎸 Test des modifications audibles des paramètres")
    print("=" * 50)
    print("IMPORTANT: Ayez votre guitare branchée et écoutez les changements!")
    print()
    
    with RealtimeMagicstomp() as rt:
        # Test 1: Amp Level (devrait changer le volume)
        print("🔊 Test 1: Amp Level (volume)")
        print("  - Réglage à 30 (faible)")
        rt.tweak_parameter(9, 30, immediate=True)  # Amp Level
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        print("  - Réglage à 90 (fort)")
        rt.tweak_parameter(9, 90, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        print("  - Retour à 64 (normal)")
        rt.tweak_parameter(9, 64, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le retour...")
        
        # Test 2: Amp Gain (devrait changer la saturation)
        print("\n🔥 Test 2: Amp Gain (saturation)")
        print("  - Réglage à 20 (clean)")
        rt.tweak_parameter(10, 20, immediate=True)  # Amp Gain
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        print("  - Réglage à 100 (saturé)")
        rt.tweak_parameter(10, 100, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        print("  - Retour à 60 (normal)")
        rt.tweak_parameter(10, 60, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le retour...")
        
        # Test 3: EQ (devrait changer le timbre)
        print("\n🎛️ Test 3: Treble (aigus)")
        print("  - Réglage à 10 (grave)")
        rt.tweak_parameter(11, 10, immediate=True)  # Treble
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        print("  - Réglage à 120 (aigu)")
        rt.tweak_parameter(11, 120, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        print("  - Retour à 64 (normal)")
        rt.tweak_parameter(11, 64, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le retour...")
        
        print("\n✅ Test des modifications audibles terminé!")


def test_parameter_response():
    """
    Test de la réactivité des paramètres.
    
    Teste si les paramètres répondent rapidement aux changements.
    """
    print("\n⚡ Test de réactivité des paramètres")
    print("=" * 50)
    
    with RealtimeMagicstomp() as rt:
        print("Test de modulation rapide de l'Amp Level...")
        
        # Modulation rapide pour tester la réactivité
        for i in range(5):
            # Valeur basse
            rt.tweak_parameter(9, 30, immediate=True)
            time.sleep(0.2)
            
            # Valeur haute
            rt.tweak_parameter(9, 100, immediate=True)
            time.sleep(0.2)
        
        # Retour à la normale
        rt.tweak_parameter(9, 64, immediate=True)
        print("✅ Test de réactivité terminé")


def test_multiple_parameters():
    """
    Test de modification simultanée de plusieurs paramètres.
    """
    print("\n🎛️ Test de modification multiple")
    print("=" * 50)
    
    with RealtimeMagicstomp() as rt:
        print("Modification de plusieurs paramètres simultanément...")
        
        # Configuration 1: Clean
        print("  Configuration 1: Clean (Level: 50, Gain: 30, Treble: 80)")
        rt.tweak_multiple_parameters({9: 50, 10: 30, 11: 80}, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        # Configuration 2: Crunch
        print("  Configuration 2: Crunch (Level: 70, Gain: 80, Treble: 60)")
        rt.tweak_multiple_parameters({9: 70, 10: 80, 11: 60}, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        # Configuration 3: High Gain
        print("  Configuration 3: High Gain (Level: 90, Gain: 110, Treble: 40)")
        rt.tweak_multiple_parameters({9: 90, 10: 110, 11: 40}, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le changement...")
        
        # Retour à la normale
        print("  Retour à la normale (Level: 64, Gain: 60, Treble: 64)")
        rt.tweak_multiple_parameters({9: 64, 10: 60, 11: 64}, immediate=True)
        input("  Appuyez sur Entrée quand vous entendez le retour...")
        
        print("✅ Test de modification multiple terminé")


def test_parameter_bounds():
    """
    Test des limites des paramètres.
    """
    print("\n📊 Test des limites des paramètres")
    print("=" * 50)
    
    with RealtimeMagicstomp() as rt:
        print("Test des valeurs limites...")
        
        # Test valeurs extrêmes
        print("  - Valeur minimale (0)")
        rt.tweak_parameter(9, 0, immediate=True)  # Amp Level à 0
        input("  Appuyez sur Entrée...")
        
        print("  - Valeur maximale (127)")
        rt.tweak_parameter(9, 127, immediate=True)  # Amp Level à 127
        input("  Appuyez sur Entrée...")
        
        # Test valeur invalide (devrait être ignorée ou clampée)
        print("  - Valeur invalide (150) - devrait être clampée à 127")
        rt.tweak_parameter(9, 150, immediate=True)
        input("  Appuyez sur Entrée...")
        
        # Retour à la normale
        rt.tweak_parameter(9, 64, immediate=True)
        print("✅ Test des limites terminé")


def interactive_parameter_control():
    """
    Contrôle interactif des paramètres.
    """
    print("\n🎮 Contrôle interactif des paramètres")
    print("=" * 50)
    print("Contrôlez manuellement les paramètres!")
    print("Commandes:")
    print("  l[value] = Amp Level (ex: l80)")
    print("  g[value] = Amp Gain (ex: g70)")
    print("  t[value] = Treble (ex: t60)")
    print("  m[value] = Middle (ex: m50)")
    print("  b[value] = Bass (ex: b40)")
    print("  q = Quitter")
    print()
    
    with RealtimeMagicstomp() as rt:
        while True:
            try:
                cmd = input("Commande (l/g/t/m/b[value] ou q): ").strip().lower()
                
                if cmd == 'q':
                    break
                elif cmd.startswith('l') and len(cmd) > 1:
                    value = int(cmd[1:])
                    rt.tweak_parameter(9, value, immediate=True)  # Amp Level
                    print(f"  Amp Level réglé à {value}")
                elif cmd.startswith('g') and len(cmd) > 1:
                    value = int(cmd[1:])
                    rt.tweak_parameter(10, value, immediate=True)  # Amp Gain
                    print(f"  Amp Gain réglé à {value}")
                elif cmd.startswith('t') and len(cmd) > 1:
                    value = int(cmd[1:])
                    rt.tweak_parameter(11, value, immediate=True)  # Treble
                    print(f"  Treble réglé à {value}")
                elif cmd.startswith('m') and len(cmd) > 1:
                    value = int(cmd[1:])
                    rt.tweak_parameter(12, value, immediate=True)  # Middle
                    print(f"  Middle réglé à {value}")
                elif cmd.startswith('b') and len(cmd) > 1:
                    value = int(cmd[1:])
                    rt.tweak_parameter(13, value, immediate=True)  # Bass
                    print(f"  Bass réglé à {value}")
                else:
                    print("  Commande invalide")
                    
            except (ValueError, KeyboardInterrupt):
                print("  Commande invalide ou interruption")
                break
    
    print("✅ Contrôle interactif terminé")


def main():
    """Fonction principale."""
    print("🎸 Vérification du contrôle Magicstomp")
    print("=" * 60)
    print("Ce script va tester si les messages sysex modifient vraiment")
    print("les paramètres de votre Magicstomp.")
    print()
    print("PRÉPARATION:")
    print("1. Connectez votre guitare au Magicstomp")
    print("2. Réglez le volume du Magicstomp à un niveau audible")
    print("3. Jouez quelques notes pour tester")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        # Tests automatiques
        test_audible_parameter_changes()
        test_parameter_response()
        test_multiple_parameters()
        test_parameter_bounds()
        
        # Test interactif
        interactive_parameter_control()
        
        print("\n🎉 Tous les tests terminés!")
        print("\nRÉSULTATS:")
        print("Si vous avez entendu des changements lors des tests,")
        print("alors le système fonctionne correctement! 🎸")
        print()
        print("Si vous n'avez rien entendu, il y a peut-être:")
        print("- Un problème de configuration du Magicstomp")
        print("- Un problème avec le format des messages sysex")
        print("- Un problème de patch actuel sur le Magicstomp")
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrompus par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")


if __name__ == "__main__":
    main()
