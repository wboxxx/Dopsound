#!/usr/bin/env python3
"""
Test des 3 potentiomètres
=========================

Test simple pour faire bouger les 3 potentiomètres du Magicstomp.
"""

import time
from realtime_magicstomp import RealtimeMagicstomp


def test_3_potentiometers():
    """Test des 3 potentiomètres."""
    print("🎸 Test des 3 potentiomètres")
    print("=" * 50)
    print("Test simple pour faire bouger les 3 potentiomètres")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("Pendant le test:")
    print("1. Regardez l'écran de votre Magicstomp")
    print("2. Observez si les potentiomètres bougent")
    print("3. Répondez: o (potentiomètre bouge) ou n (pas de mouvement)")
    print()
    
    input("Appuyez sur Entrée pour commencer...")
    
    # Test des 3 potentiomètres
    pot_tests = [
        (2, 0, "Potentiomètre 1 (gauche) - OFF"),
        (2, 1, "Potentiomètre 1 (gauche) - ON"),
        (4, 0, "Potentiomètre 2 (milieu) - OFF"),
        (4, 1, "Potentiomètre 2 (milieu) - ON"),
        (6, 0, "Potentiomètre 3 (droite) - OFF"),
        (6, 1, "Potentiomètre 3 (droite) - ON"),
    ]
    
    results = []
    
    for offset, value, description in pot_tests:
        print(f"\n🧪 Test: {description}")
        
        # Applique la valeur
        rt.tweak_parameter(offset, value, immediate=True)
        time.sleep(1)
        
        print("  Regardez l'écran de votre Magicstomp...")
        response = input(f"  {description}: Potentiomètre bouge ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            results.append((description, "✅ POTENTIOMÈTRE BOUGE"))
            print(f"  ✅ {description}: POTENTIOMÈTRE BOUGE")
        else:
            results.append((description, "❌ PAS DE MOUVEMENT"))
            print(f"  ❌ {description}: PAS DE MOUVEMENT")
    
    rt.stop()
    
    print(f"\n📊 RÉSULTATS:")
    print("=" * 50)
    
    moving_count = 0
    total_count = len(results)
    
    for description, result in results:
        print(f"  {result} - {description}")
        if "POTENTIOMÈTRE BOUGE" in result:
            moving_count += 1
    
    print(f"\n📈 STATISTIQUES:")
    print(f"  Total des tests: {total_count}")
    print(f"  Potentiomètres qui bougent: {moving_count}")
    print(f"  Pas de mouvement: {total_count - moving_count}")
    print(f"  Taux de succès: {(moving_count/total_count)*100:.1f}%")
    
    if moving_count > 0:
        print(f"\n🎉 SUCCÈS! Au moins {moving_count} potentiomètre(s) bouge(nt)!")
        return True
    else:
        print(f"\n❌ Aucun potentiomètre ne bouge")
        return False


def main():
    """Fonction principale."""
    print("🎸 Test des 3 potentiomètres")
    print("=" * 60)
    print("Test simple pour faire bouger les 3 potentiomètres du Magicstomp")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Regardez l'écran pendant les tests")
    print("3. Observez si les potentiomètres bougent")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        success = test_3_potentiometers()
        
        if success:
            print(f"\n🎉🎉 SYSTÈME FONCTIONNEL!")
            print(f"Les potentiomètres bougent!")
            print(f"Votre système de modification temps réel fonctionne!")
        else:
            print(f"\n❌ Les potentiomètres ne bougent pas")
            print(f"Vérifiez la configuration MIDI de votre Magicstomp")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()


