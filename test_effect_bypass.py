#!/usr/bin/env python3
"""
Test de bypass des effets
========================

D'après l'analyse de MagicstompFrenzy, les paramètres Control1, Control2, Control3
peuvent contrôler l'état des effets. Testons si les effets doivent être OFF.
"""

import time
import mido
from realtime_magicstomp import RealtimeMagicstomp


def test_effect_bypass():
    """Test si les effets doivent être désactivés."""
    print("🎸 Test de bypass des effets")
    print("=" * 50)
    print("D'après MagicstompFrenzy, les paramètres Control1, Control2, Control3")
    print("peuvent contrôler l'état des effets.")
    print()
    print("IMPORTANT: Assurez-vous que U01 est affiché à l'écran de votre Magicstomp!")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("🧪 Test 1: Paramètres d'amplificateur avec effets ON")
    print("(État actuel de votre patch)")
    
    # Test des paramètres d'amplificateur
    print("  - Amp Level: 30 (faible)")
    rt.tweak_parameter(9, 30, immediate=True)  # Amp Level
    time.sleep(1)
    
    print("  - Amp Level: 100 (fort)")
    rt.tweak_parameter(9, 100, immediate=True)
    time.sleep(1)
    
    print("  - Amp Level: 64 (normal)")
    rt.tweak_parameter(9, 64, immediate=True)
    time.sleep(1)
    
    response = input("\nAvec effets ON: Avez-vous entendu des changements d'Amp Level ? (o/n): ").strip().lower()
    effects_on_works = response in ['o', 'oui', 'y', 'yes']
    
    print(f"\n🧪 Test 2: Désactivation des effets (Control1 = 0)")
    
    # Désactive les effets via Control1 (offset 2)
    print("  - Désactivation des effets (Control1 = 0)")
    rt.tweak_parameter(2, 0, immediate=True)  # Control1 = 0 (effets OFF)
    time.sleep(0.5)
    
    print("  - Amp Level: 30 (faible)")
    rt.tweak_parameter(9, 30, immediate=True)  # Amp Level
    time.sleep(1)
    
    print("  - Amp Level: 100 (fort)")
    rt.tweak_parameter(9, 100, immediate=True)
    time.sleep(1)
    
    print("  - Amp Level: 64 (normal)")
    rt.tweak_parameter(9, 64, immediate=True)
    time.sleep(1)
    
    response = input("\nAvec effets OFF: Avez-vous entendu des changements d'Amp Level ? (o/n): ").strip().lower()
    effects_off_works = response in ['o', 'oui', 'y', 'yes']
    
    print(f"\n🧪 Test 3: Réactivation des effets (Control1 = 1)")
    
    # Réactive les effets
    print("  - Réactivation des effets (Control1 = 1)")
    rt.tweak_parameter(2, 1, immediate=True)  # Control1 = 1 (effets ON)
    time.sleep(0.5)
    
    print("  - Amp Level: 30 (faible)")
    rt.tweak_parameter(9, 30, immediate=True)  # Amp Level
    time.sleep(1)
    
    print("  - Amp Level: 100 (fort)")
    rt.tweak_parameter(9, 100, immediate=True)
    time.sleep(1)
    
    print("  - Amp Level: 64 (normal)")
    rt.tweak_parameter(9, 64, immediate=True)
    time.sleep(1)
    
    response = input("\nAvec effets ON (retour): Avez-vous entendu des changements d'Amp Level ? (o/n): ").strip().lower()
    effects_on_again_works = response in ['o', 'oui', 'y', 'yes']
    
    rt.stop()
    
    print(f"\n📊 RÉSULTATS:")
    print(f"  Effets ON (initial): {'✅' if effects_on_works else '❌'}")
    print(f"  Effets OFF (Control1=0): {'✅' if effects_off_works else '❌'}")
    print(f"  Effets ON (retour): {'✅' if effects_on_again_works else '❌'}")
    
    if effects_off_works and not effects_on_works:
        print(f"\n🎉 SUCCÈS! Les effets doivent être OFF pour les modifications temps réel!")
        return True, "effects_off"
    elif effects_on_works:
        print(f"\n🎉 SUCCÈS! Les modifications fonctionnent avec les effets ON!")
        return True, "effects_on"
    else:
        print(f"\n❌ Les modifications ne fonctionnent ni avec les effets ON ni OFF")
        return False, "neither"


def test_different_control_values():
    """Test différentes valeurs de contrôle."""
    print(f"\n🎛️ Test de différentes valeurs de contrôle")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    print("Test de différentes valeurs pour Control1, Control2, Control3...")
    
    control_tests = [
        (2, 0, "Control1 = 0"),
        (2, 1, "Control1 = 1"),
        (4, 0, "Control2 = 0"),
        (4, 1, "Control2 = 1"),
        (6, 0, "Control3 = 0"),
        (6, 1, "Control3 = 1"),
    ]
    
    working_combinations = []
    
    for offset, value, description in control_tests:
        print(f"\n🧪 Test: {description}")
        
        # Applique la valeur de contrôle
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(0.5)
        
        # Test rapide de l'Amp Level
        rt.tweak_parameter(9, 30, immediate=True)
        time.sleep(0.5)
        rt.tweak_parameter(9, 100, immediate=True)
        time.sleep(0.5)
        rt.tweak_parameter(9, 64, immediate=True)
        time.sleep(0.5)
        
        response = input(f"{description}: Changement d'Amp Level audible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            working_combinations.append((offset, value, description))
            print(f"  ✅ {description} fonctionne!")
        else:
            print(f"  ❌ {description} ne fonctionne pas")
    
    rt.stop()
    
    if working_combinations:
        print(f"\n🎉 COMBINAISONS FONCTIONNELLES:")
        for offset, value, description in working_combinations:
            print(f"  ✅ {description}")
        return working_combinations[0]  # Retourne la première qui fonctionne
    else:
        print(f"\n❌ Aucune combinaison ne fonctionne")
        return None


def main():
    """Fonction principale."""
    print("🎸 Test de bypass des effets")
    print("=" * 60)
    print("Test si les effets doivent être désactivés pour les modifications temps réel.")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Connectez votre guitare")
    print("3. Réglez le volume à un niveau audible")
    print("4. Jouez quelques notes pour tester")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        # Test principal
        success, mode = test_effect_bypass()
        
        if success:
            print(f"\n🎉 SYSTÈME FONCTIONNEL!")
            print(f"Mode: {mode}")
            
            if mode == "effects_off":
                print(f"\n💡 SOLUTION:")
                print(f"Les effets doivent être OFF (Control1 = 0) pour les modifications temps réel.")
                print(f"Vous pouvez maintenant utiliser l'optimisation avec les effets désactivés.")
            elif mode == "effects_on":
                print(f"\n💡 SOLUTION:")
                print(f"Les modifications fonctionnent avec les effets ON.")
                print(f"Vous pouvez utiliser l'optimisation normalement.")
        else:
            print(f"\n🔧 Test des différentes valeurs de contrôle...")
            working_combination = test_different_control_values()
            
            if working_combination:
                offset, value, description = working_combination
                print(f"\n🎉 SOLUTION TROUVÉE:")
                print(f"Utilisez {description} pour activer les modifications temps réel.")
                print(f"Offset: {offset}, Valeur: {value}")
            else:
                print(f"\n❌ Aucune configuration ne fonctionne")
                print(f"Vérifiez la configuration MIDI de votre Magicstomp.")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
