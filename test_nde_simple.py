#!/usr/bin/env python3
"""
Test NDE (Non Discernable Effect) simple
========================================

Test simple: entendez-vous un effet ou pas ?
"""

import time
from realtime_magicstomp import RealtimeMagicstomp


def test_nde_simple():
    """Test NDE simple."""
    print("🎸 Test NDE (Non Discernable Effect)")
    print("=" * 50)
    print("Test simple: entendez-vous un effet ou pas ?")
    print()
    
    rt = RealtimeMagicstomp()
    
    # Test avec des paramètres qui devraient avoir un effet audible
    test_params = [
        (9, 30, "Amp Level 30 (faible)"),
        (9, 100, "Amp Level 100 (fort)"),
        (9, 64, "Amp Level 64 (normal)"),
        (2, 0, "Control1 OFF"),
        (2, 1, "Control1 ON"),
        (4, 0, "Control2 OFF"),
        (4, 1, "Control2 ON"),
    ]
    
    print("Pendant le test:")
    print("1. Jouez votre guitare")
    print("2. Répondez simplement: o (effet audible) ou n (pas d'effet)")
    print()
    
    input("Appuyez sur Entrée pour commencer...")
    
    results = []
    
    for offset, value, description in test_params:
        print(f"\n🧪 Test: {description}")
        
        # Applique la valeur
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(0.5)
        
        print("  Jouez votre guitare...")
        response = input(f"  Effet audible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            results.append((description, "✅ EFFET AUDIBLE"))
            print(f"  ✅ {description}: EFFET AUDIBLE")
        else:
            results.append((description, "❌ PAS D'EFFET"))
            print(f"  ❌ {description}: PAS D'EFFET")
    
    rt.stop()
    
    print(f"\n📊 RÉSULTATS:")
    print("=" * 50)
    
    audible_count = 0
    total_count = len(results)
    
    for description, result in results:
        print(f"  {result} - {description}")
        if "EFFET AUDIBLE" in result:
            audible_count += 1
    
    print(f"\n📈 STATISTIQUES:")
    print(f"  Total des tests: {total_count}")
    print(f"  Effets audibles: {audible_count}")
    print(f"  Pas d'effet: {total_count - audible_count}")
    print(f"  Taux de succès: {(audible_count/total_count)*100:.1f}%")
    
    if audible_count > 0:
        print(f"\n🎉 SUCCÈS! Le système fonctionne!")
        print(f"Vous pouvez entendre {audible_count}/{total_count} modifications")
        return True
    else:
        print(f"\n❌ PROBLÈME! Aucun effet audible")
        print(f"Le système ne fonctionne pas comme attendu")
        return False


def main():
    """Fonction principale."""
    print("🎸 Test NDE (Non Discernable Effect)")
    print("=" * 60)
    print("Test simple: entendez-vous un effet ou pas ?")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Connectez votre guitare")
    print("3. Réglez le volume à un niveau audible")
    print("4. Préparez-vous à jouer et écouter")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        success = test_nde_simple()
        
        if success:
            print(f"\n🎉🎉 SYSTÈME FONCTIONNEL!")
            print(f"Votre système de modification temps réel fonctionne!")
            print(f"Vous pouvez maintenant:")
            print(f"1. Modifier les paramètres en temps réel")
            print(f"2. Entendre les changements")
            print(f"3. Utiliser pour l'optimisation")
        else:
            print(f"\n❌ Le système ne fonctionne pas")
            print(f"Vérifiez la configuration MIDI de votre Magicstomp")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
