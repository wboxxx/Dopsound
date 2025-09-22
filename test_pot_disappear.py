#!/usr/bin/env python3
"""
Test de disparition des potentiomètres
=====================================

Test pour comprendre pourquoi les potentiomètres disparaissent.
"""

import time
from realtime_magicstomp import RealtimeMagicstomp


def test_pot_disappear():
    """Test de disparition des potentiomètres."""
    print("🎸 Test de disparition des potentiomètres")
    print("=" * 60)
    print("Test pour comprendre pourquoi les potentiomètres disparaissent")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("Pendant le test:")
    print("1. Regardez l'écran de votre Magicstomp")
    print("2. Observez si les potentiomètres:")
    print("   - Disparaissent complètement")
    print("   - Se mettent à null/zéro")
    print("   - Changent de valeur")
    print("3. Répondez: D (disparaît), N (null), C (changement), R (reset)")
    print()
    
    input("Appuyez sur Entrée pour commencer...")
    
    # Test spécifique pour comprendre les effets
    test_sequence = [
        (2, 0, "Control1 OFF - Potentiomètre 1"),
        (2, 1, "Control1 ON - Potentiomètre 1"),
        (4, 0, "Control2 OFF - Potentiomètre 2"),
        (4, 1, "Control2 ON - Potentiomètre 2"),
        (6, 0, "Control3 OFF - Potentiomètre 3"),
        (6, 1, "Control3 ON - Potentiomètre 3"),
    ]
    
    results = []
    
    for offset, value, description in test_sequence:
        print(f"\n🧪 Test: {description}")
        print(f"  Offset: {offset}, Valeur: {value}")
        
        # Applique la valeur
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(1)
        
        print("  Regardez l'écran de votre Magicstomp...")
        response = input(f"  {description}: D/N/C/R ? ").strip().upper()
        
        if response == "D":
            results.append((description, "D", "👻 DISPARAÎT"))
            print(f"  👻 {description}: DISPARAÎT")
        elif response == "N":
            results.append((description, "N", "🔢 NULL"))
            print(f"  🔢 {description}: NULL")
        elif response == "C":
            results.append((description, "C", "✅ CHANGEMENT"))
            print(f"  ✅ {description}: CHANGEMENT")
        elif response == "R":
            results.append((description, "R", "🔄 RESET"))
            print(f"  🔄 {description}: RESET")
        else:
            results.append((description, "?", "❓ INVALIDE"))
            print(f"  ❓ {description}: RÉPONSE INVALIDE")
    
    rt.stop()
    
    print(f"\n📊 RÉSULTATS:")
    print("=" * 60)
    
    disappear_count = 0
    null_count = 0
    change_count = 0
    reset_count = 0
    invalid_count = 0
    total_count = len(results)
    
    for description, result, display in results:
        print(f"  {display} - {description}")
        if result == "D":
            disappear_count += 1
        elif result == "N":
            null_count += 1
        elif result == "C":
            change_count += 1
        elif result == "R":
            reset_count += 1
        else:
            invalid_count += 1
    
    print(f"\n📈 STATISTIQUES:")
    print(f"  Total des tests: {total_count}")
    print(f"  Disparaissent: {disappear_count}")
    print(f"  Null: {null_count}")
    print(f"  Changements: {change_count}")
    print(f"  Resets: {reset_count}")
    print(f"  Réponses invalides: {invalid_count}")
    
    print(f"\n📊 POURCENTAGES:")
    print(f"  Disparaissent: {(disappear_count/total_count)*100:.1f}%")
    print(f"  Null: {(null_count/total_count)*100:.1f}%")
    print(f"  Changements: {(change_count/total_count)*100:.1f}%")
    print(f"  Resets: {(reset_count/total_count)*100:.1f}%")
    
    print(f"\n🔍 ANALYSE:")
    if disappear_count > 0:
        print(f"  👻 {disappear_count} potentiomètre(s) disparaissent")
        print(f"     → Valeur 1 désactive probablement le potentiomètre")
    
    if null_count > 0:
        print(f"  🔢 {null_count} potentiomètre(s) se mettent à null")
        print(f"     → Valeur 0 remet probablement à zéro")
    
    if change_count > 0:
        print(f"  ✅ {change_count} changement(s) détecté(s)")
        print(f"     → Le système fonctionne partiellement")
    
    return change_count > 0 or disappear_count > 0 or null_count > 0


def main():
    """Fonction principale."""
    print("🎸 Test de disparition des potentiomètres")
    print("=" * 70)
    print("Test pour comprendre pourquoi les potentiomètres disparaissent")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Regardez l'écran pendant les tests")
    print("3. Observez si les potentiomètres disparaissent ou changent")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        success = test_pot_disappear()
        
        if success:
            print(f"\n🎉🎉 SYSTÈME FONCTIONNEL!")
            print(f"Les potentiomètres réagissent aux commandes!")
            print(f"Votre système de modification temps réel fonctionne!")
        else:
            print(f"\n❌ Les potentiomètres ne réagissent pas")
            print(f"Vérifiez la configuration MIDI de votre Magicstomp")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()


