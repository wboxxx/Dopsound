#!/usr/bin/env python3
"""
Test filtre passe-haut sur potentiomètre 3
==========================================

Test pour mettre le filtre passe-haut sur le potentiomètre 3 et le régler à 50%.
"""

import time
from realtime_magicstomp import RealtimeMagicstomp


def test_highpass_filter():
    """Test filtre passe-haut sur potentiomètre 3."""
    print("🎸 Test filtre passe-haut sur potentiomètre 3")
    print("=" * 60)
    print("Objectif: Mettre le filtre passe-haut sur le potentiomètre 3 et le régler à 50%")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("Pendant le test:")
    print("1. Regardez l'écran de votre Magicstomp")
    print("2. Observez si le potentiomètre 3 affiche le filtre passe-haut")
    print("3. Répondez: N (pas d'effet), C (changement), R (reset)")
    print()
    
    input("Appuyez sur Entrée pour commencer...")
    
    # Test 1: Activer le filtre passe-haut sur le potentiomètre 3
    print("\n🧪 Test 1: Activer le filtre passe-haut sur le potentiomètre 3")
    print("  Offset: 6, Valeur: 0 (Control3 OFF)")
    
    rt.tweak_parameter(6, 0, immediate=True)  # Control3 OFF
    time.sleep(1)
    
    print("  Regardez l'écran de votre Magicstomp...")
    response1 = input("  Control3 OFF: N/C/R ? ").strip().upper()
    
    if response1 == "C":
        print("  ✅ Control3 OFF: Changement détecté")
        
        # Test 2: Régler le filtre passe-haut à 50%
        print("\n🧪 Test 2: Régler le filtre passe-haut à 50%")
        print("  Offset: 6, Valeur: 64 (50% de 127)")
        
        rt.tweak_parameter(6, 64, immediate=True)  # 50% du filtre
        time.sleep(1)
        
        print("  Regardez l'écran de votre Magicstomp...")
        response2 = input("  Filtre passe-haut 50%: N/C/R ? ").strip().upper()
        
        if response2 == "C":
            print("  ✅ Filtre passe-haut 50%: Changement détecté")
            
            # Test 3: Vérifier que le potentiomètre 3 affiche bien le filtre
            print("\n🧪 Test 3: Vérification du potentiomètre 3")
            print("  Le potentiomètre 3 affiche-t-il le filtre passe-haut ?")
            
            comment = input("  💬 Commentaire sur l'affichage du potentiomètre 3: ").strip()
            
            print(f"\n🎉 SUCCÈS!")
            print(f"Filtre passe-haut configuré sur le potentiomètre 3")
            print(f"Commentaire: {comment}")
            
            rt.stop()
            return True
            
        else:
            print(f"  ❌ Filtre passe-haut 50%: {response2}")
            
    else:
        print(f"  ❌ Control3 OFF: {response1}")
    
    rt.stop()
    return False


def test_different_filter_values():
    """Test différentes valeurs du filtre passe-haut."""
    print(f"\n🎛️ Test différentes valeurs du filtre passe-haut")
    print("=" * 60)
    
    rt = RealtimeMagicstomp()
    
    # Valeurs à tester
    filter_values = [
        (0, "0% (minimum)"),
        (32, "25%"),
        (64, "50%"),
        (96, "75%"),
        (127, "100% (maximum)"),
    ]
    
    print("Test de différentes valeurs du filtre passe-haut...")
    print("Répondez: N (pas d'effet), C (changement), R (reset)")
    print()
    
    results = []
    
    for value, description in filter_values:
        print(f"\n🧪 Test: {description}")
        print(f"  Offset: 6, Valeur: {value}")
        
        rt.tweak_parameter(6, value, immediate=True)
        time.sleep(1)
        
        print("  Regardez l'écran de votre Magicstomp...")
        response = input(f"  {description}: N/C/R ? ").strip().upper()
        
        if response == "C":
            results.append((description, "✅ Changement"))
            print(f"  ✅ {description}: Changement détecté")
        elif response == "R":
            results.append((description, "🔄 Reset"))
            print(f"  🔄 {description}: Reset détecté")
        else:
            results.append((description, "❌ Pas d'effet"))
            print(f"  ❌ {description}: Pas d'effet")
    
    rt.stop()
    
    print(f"\n📊 RÉSULTATS:")
    print("=" * 60)
    
    for description, result in results:
        print(f"  {result} - {description}")
    
    change_count = sum(1 for _, result in results if "Changement" in result)
    
    if change_count > 0:
        print(f"\n🎉 SUCCÈS! {change_count} valeur(s) du filtre fonctionnent!")
        return True
    else:
        print(f"\n❌ Aucune valeur du filtre ne fonctionne")
        return False


def main():
    """Fonction principale."""
    print("🎸 Test filtre passe-haut sur potentiomètre 3")
    print("=" * 70)
    print("Objectif: Mettre le filtre passe-haut sur le potentiomètre 3 et le régler à 50%")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Regardez l'écran pendant les tests")
    print("3. Observez si le potentiomètre 3 affiche le filtre passe-haut")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        # Test principal
        success = test_highpass_filter()
        
        if success:
            print(f"\n🎉🎉 SUCCÈS!")
            print(f"Le filtre passe-haut est configuré sur le potentiomètre 3!")
            
            # Test des différentes valeurs
            print(f"\n" + "="*70)
            test_different_filter_values()
            
        else:
            print(f"\n❌ Le filtre passe-haut ne s'est pas configuré")
            print(f"Vérifiez la configuration MIDI de votre Magicstomp")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
