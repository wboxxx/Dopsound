#!/usr/bin/env python3
"""
Test final d'optimisation temps réel
====================================

Le système fonctionne ! Testons maintenant l'optimisation complète.
"""

import time
import numpy as np
from realtime_magicstomp import RealtimeMagicstomp


def test_optimization_loop():
    """Test d'une boucle d'optimisation simple."""
    print("🎸 Test d'optimisation temps réel")
    print("=" * 50)
    print("Le système fonctionne ! Testons l'optimisation...")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("🧪 Test 1: Variation d'Amp Level")
    print("Optimisation simple: trouver le meilleur Amp Level")
    
    # Test avec différentes valeurs d'Amp Level
    amp_levels = [20, 40, 60, 80, 100]
    
    print("\nValeurs à tester:")
    for i, level in enumerate(amp_levels):
        print(f"  {i+1}. Amp Level: {level}")
    
    print("\nPendant le test:")
    print("1. Jouez votre guitare")
    print("2. Écoutez le son pour chaque valeur")
    print("3. Notez laquelle sonne le mieux")
    
    input("\nAppuyez sur Entrée pour commencer...")
    
    best_level = None
    best_score = 0
    
    for i, level in enumerate(amp_levels):
        print(f"\n🧪 Test {i+1}/5: Amp Level = {level}")
        
        # Applique la valeur
        rt.tweak_parameter(9, level, immediate=True)  # Amp Level
        time.sleep(0.5)
        
        print("  Jouez votre guitare et évaluez le son...")
        score = input(f"  Score (0-10): ").strip()
        
        try:
            score = float(score)
            if score > best_score:
                best_score = score
                best_level = level
                print(f"  ✅ Nouveau meilleur: {level} (score: {score})")
            else:
                print(f"  Score: {score}")
        except:
            print(f"  Score invalide, ignoré")
    
    print(f"\n🏆 RÉSULTAT:")
    print(f"Meilleur Amp Level: {best_level}")
    print(f"Meilleur score: {best_score}")
    
    # Applique le meilleur résultat
    if best_level is not None:
        print(f"\n✅ Application du meilleur résultat...")
        rt.tweak_parameter(9, best_level, immediate=True)
        time.sleep(0.5)
        print(f"Amp Level réglé à {best_level}")
    
    rt.stop()
    
    return best_level, best_score


def test_multiple_parameters():
    """Test d'optimisation de plusieurs paramètres."""
    print(f"\n🎛️ Test d'optimisation multi-paramètres")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    # Paramètres à optimiser
    parameters = [
        (9, "Amp Level", [30, 50, 70, 90]),
        (2, "Control1", [0, 1]),
        (4, "Control2", [0, 1]),
    ]
    
    print("Paramètres à optimiser:")
    for offset, name, values in parameters:
        print(f"  - {name}: {values}")
    
    print("\nPendant le test:")
    print("1. Nous testerons chaque combinaison")
    print("2. Jouez votre guitare pour chaque test")
    print("3. Évaluez le son global")
    
    input("\nAppuyez sur Entrée pour commencer...")
    
    best_combination = None
    best_score = 0
    test_count = 0
    
    # Test toutes les combinaisons
    for amp_level in parameters[0][2]:
        for control1 in parameters[1][2]:
            for control2 in parameters[2][2]:
                test_count += 1
                
                print(f"\n🧪 Test {test_count}: Amp={amp_level}, C1={control1}, C2={control2}")
                
                # Applique la combinaison
                rt.tweak_parameter(9, amp_level, immediate=True)
                rt.tweak_parameter(2, control1, immediate=True)
                rt.tweak_parameter(4, control2, immediate=True)
                time.sleep(0.5)
                
                print("  Jouez votre guitare et évaluez le son...")
                score = input(f"  Score (0-10): ").strip()
                
                try:
                    score = float(score)
                    if score > best_score:
                        best_score = score
                        best_combination = (amp_level, control1, control2)
                        print(f"  ✅ Nouveau meilleur: {best_combination} (score: {score})")
                    else:
                        print(f"  Score: {score}")
                except:
                    print(f"  Score invalide, ignoré")
    
    print(f"\n🏆 RÉSULTAT:")
    print(f"Meilleure combinaison: {best_combination}")
    print(f"Meilleur score: {best_score}")
    
    # Applique le meilleur résultat
    if best_combination is not None:
        print(f"\n✅ Application du meilleur résultat...")
        amp_level, control1, control2 = best_combination
        rt.tweak_parameter(9, amp_level, immediate=True)
        rt.tweak_parameter(2, control1, immediate=True)
        rt.tweak_parameter(4, control2, immediate=True)
        time.sleep(0.5)
        print(f"Paramètres appliqués: Amp={amp_level}, C1={control1}, C2={control2}")
    
    rt.stop()
    
    return best_combination, best_score


def main():
    """Fonction principale."""
    print("🎸 Test final d'optimisation temps réel")
    print("=" * 60)
    print("Le système de modification temps réel fonctionne !")
    print("Testons maintenant l'optimisation complète...")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Connectez votre guitare")
    print("3. Réglez le volume à un niveau audible")
    print("4. Préparez-vous à jouer et évaluer le son")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        # Test 1: Optimisation simple
        print("\n" + "="*60)
        best_level, best_score = test_optimization_loop()
        
        if best_level is not None:
            print(f"\n🎉 SUCCÈS! Optimisation simple fonctionne!")
            
            # Test 2: Optimisation multi-paramètres
            print("\n" + "="*60)
            best_combination, best_score = test_multiple_parameters()
            
            if best_combination is not None:
                print(f"\n🎉🎉 SUCCÈS! Optimisation multi-paramètres fonctionne!")
                
                print(f"\n🏆 SYSTÈME COMPLET FONCTIONNEL!")
                print(f"Votre système d'optimisation temps réel est opérationnel!")
                print(f"Vous pouvez maintenant:")
                print(f"1. Modifier les paramètres en temps réel")
                print(f"2. Optimiser automatiquement")
                print(f"3. Intégrer dans vos boucles de rétroaction")
                
                return True
        
        print(f"\n⚠️ Tests d'optimisation terminés")
        print(f"Le système de modification fonctionne, mais l'optimisation a besoin d'ajustements")
        return False
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return False
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False


if __name__ == "__main__":
    main()
