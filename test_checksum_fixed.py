#!/usr/bin/env python3
"""
Test avec checksum corrigé
===========================

Testons si le checksum corrigé résout le problème de reset.
"""

import time
from realtime_magicstomp import RealtimeMagicstomp


def test_checksum_fixed():
    """Test avec checksum corrigé."""
    print("🎸 Test avec checksum corrigé")
    print("=" * 50)
    print("Le checksum a été corrigé pour correspondre à MagicstompFrenzy")
    print("Testons si les paramètres ne se remettent plus à zéro...")
    print()
    
    rt = RealtimeMagicstomp()
    
    # Test avec des paramètres qui devraient avoir un effet
    test_params = [
        (9, 30, "Amp Level 30"),
        (9, 64, "Amp Level 64"),
        (9, 100, "Amp Level 100"),
        (2, 0, "Control1 OFF"),
        (2, 1, "Control1 ON"),
        (4, 0, "Control2 OFF"),
        (4, 1, "Control2 ON"),
    ]
    
    print("Pendant le test:")
    print("1. Regardez l'écran de votre Magicstomp")
    print("2. Notez si les paramètres changent ou se remettent à zéro")
    print("3. Répondez: o (paramètre visible) ou n (reset à zéro)")
    print()
    
    input("Appuyez sur Entrée pour commencer...")
    
    results = []
    
    for offset, value, description in test_params:
        print(f"\n🧪 Test: {description}")
        print(f"  Offset: {offset}, Valeur: {value}")
        
        # Applique la valeur
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(1)
        
        print("  Regardez l'écran de votre Magicstomp...")
        response = input(f"  {description}: Paramètre visible (pas de reset) ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            results.append((description, "✅ PARAMÈTRE VISIBLE"))
            print(f"  ✅ {description}: PARAMÈTRE VISIBLE")
        else:
            results.append((description, "❌ RESET À ZÉRO"))
            print(f"  ❌ {description}: RESET À ZÉRO")
    
    rt.stop()
    
    print(f"\n📊 RÉSULTATS:")
    print("=" * 50)
    
    visible_count = 0
    reset_count = 0
    total_count = len(results)
    
    for description, result in results:
        print(f"  {result} - {description}")
        if "PARAMÈTRE VISIBLE" in result:
            visible_count += 1
        else:
            reset_count += 1
    
    print(f"\n📈 STATISTIQUES:")
    print(f"  Total des tests: {total_count}")
    print(f"  Paramètres visibles: {visible_count}")
    print(f"  Resets à zéro: {reset_count}")
    print(f"  Taux de succès: {(visible_count/total_count)*100:.1f}%")
    
    if reset_count == 0:
        print(f"\n🎉 SUCCÈS! Le checksum corrigé fonctionne!")
        print(f"Aucun reset à zéro - tous les paramètres sont visibles")
        return True
    elif visible_count > reset_count:
        print(f"\n✅ AMÉLIORATION! Moins de resets qu'avant")
        print(f"Le checksum corrigé améliore la situation")
        return True
    else:
        print(f"\n❌ PROBLÈME PERSISTANT!")
        print(f"Le checksum n'était pas le seul problème")
        return False


def main():
    """Fonction principale."""
    print("🎸 Test avec checksum corrigé")
    print("=" * 60)
    print("Le checksum a été corrigé pour correspondre à MagicstompFrenzy:")
    print("Ancien: checksum ^= byte (XOR)")
    print("Nouveau: checksum += byte puis (-checksum) & 0x7F")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Regardez l'écran pendant les tests")
    print("3. Notez si les paramètres changent ou se remettent à zéro")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        success = test_checksum_fixed()
        
        if success:
            print(f"\n🎉🎉 SYSTÈME FONCTIONNEL!")
            print(f"Le checksum corrigé résout le problème!")
            print(f"Votre système de modification temps réel fonctionne maintenant!")
        else:
            print(f"\n❌ Le problème persiste")
            print(f"Il y a d'autres problèmes à résoudre...")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
