#!/usr/bin/env python3
"""
Test amélioré avec retry et commentaires
========================================

Test avec option retry et commentaires pour les changements.
"""

import time
from realtime_magicstomp import RealtimeMagicstomp


def test_improved():
    """Test amélioré avec retry et commentaires."""
    print("🎸 Test amélioré avec retry et commentaires")
    print("=" * 60)
    print("Options disponibles:")
    print("  N = Non Discernable Effect (pas d'effet)")
    print("  C = Changement (effet audible/changement visible)")
    print("  R = Reset (remise à zéro)")
    print("  r = Retry (retest du même paramètre)")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("Pendant le test:")
    print("1. Jouez votre guitare ET regardez l'écran")
    print("2. Répondez avec une lettre: N, C, R, ou r")
    print("3. Si changement (C), vous pourrez ajouter un commentaire")
    print()
    
    input("Appuyez sur Entrée pour commencer...")
    
    # Test des paramètres
    test_params = [
        (9, 30, "Amp Level 30"),
        (9, 64, "Amp Level 64"),
        (9, 100, "Amp Level 100"),
        (2, 0, "Control1 OFF"),
        (2, 1, "Control1 ON"),
        (4, 0, "Control2 OFF"),
        (4, 1, "Control2 ON"),
        (6, 0, "Control3 OFF"),
        (6, 1, "Control3 ON"),
    ]
    
    results = []
    
    for offset, value, description in test_params:
        while True:  # Boucle pour retry
            print(f"\n🧪 Test: {description}")
            print(f"  Offset: {offset}, Valeur: {value}")
            
            # Applique la valeur
            rt.tweak_parameter(offset, value, immediate=True)
            time.sleep(1)
            
            print("  Jouez votre guitare et regardez l'écran...")
            response = input(f"  {description}: N/C/R/r ? ").strip().upper()
            
            if response == "R":  # Retry
                print(f"  🔄 Retry de {description}...")
                continue  # Recommence le test
            elif response == "N":
                results.append((description, "N", "❌ Pas d'effet", ""))
                print(f"  ❌ {description}: Pas d'effet")
                break  # Sort de la boucle retry
            elif response == "C":
                # Demande un commentaire pour les changements
                comment = input(f"  💬 Commentaire pour {description}: ").strip()
                results.append((description, "C", "✅ Changement", comment))
                print(f"  ✅ {description}: Changement - {comment}")
                break  # Sort de la boucle retry
            elif response == "R":
                results.append((description, "R", "🔄 Reset", ""))
                print(f"  🔄 {description}: Reset à zéro")
                break  # Sort de la boucle retry
            else:
                print(f"  ❓ Réponse invalide. Options: N, C, R, r")
                continue  # Recommence le test
    
    rt.stop()
    
    print(f"\n📊 RÉSULTATS:")
    print("=" * 60)
    
    nde_count = 0
    change_count = 0
    reset_count = 0
    total_count = len(results)
    
    for description, result, display, comment in results:
        if comment:
            print(f"  {display} - {description}: {comment}")
        else:
            print(f"  {display} - {description}")
        
        if result == "N":
            nde_count += 1
        elif result == "C":
            change_count += 1
        elif result == "R":
            reset_count += 1
    
    print(f"\n📈 STATISTIQUES:")
    print(f"  Total des tests: {total_count}")
    print(f"  N (pas d'effet): {nde_count}")
    print(f"  Changements: {change_count}")
    print(f"  Resets: {reset_count}")
    
    print(f"\n📊 POURCENTAGES:")
    print(f"  N: {(nde_count/total_count)*100:.1f}%")
    print(f"  Changements: {(change_count/total_count)*100:.1f}%")
    print(f"  Resets: {(reset_count/total_count)*100:.1f}%")
    
    print(f"\n💬 COMMENTAIRES:")
    print("=" * 60)
    for description, result, display, comment in results:
        if result == "C" and comment:
            print(f"  ✅ {description}: {comment}")
    
    if change_count > 0:
        print(f"\n🎉 SUCCÈS! {change_count} changement(s) détecté(s)!")
        print(f"Le système fonctionne partiellement")
        return True
    elif reset_count > 0:
        print(f"\n⚠️ PROBLÈME! {reset_count} reset(s) détecté(s)")
        print(f"Le checksum ou le format pose problème")
        return False
    else:
        print(f"\n❌ Aucun effet détecté")
        print(f"Le système ne fonctionne pas")
        return False


def main():
    """Fonction principale."""
    print("🎸 Test amélioré avec retry et commentaires")
    print("=" * 70)
    print("Test avec option retry et commentaires pour les changements")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Connectez votre guitare")
    print("3. Réglez le volume à un niveau audible")
    print("4. Préparez-vous à jouer et observer")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        success = test_improved()
        
        if success:
            print(f"\n🎉🎉 SYSTÈME FONCTIONNEL!")
            print(f"Des changements sont détectés!")
            print(f"Votre système de modification temps réel fonctionne!")
        else:
            print(f"\n❌ Le système ne fonctionne pas correctement")
            print(f"Vérifiez la configuration MIDI de votre Magicstomp")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
