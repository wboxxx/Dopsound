#!/usr/bin/env python3
"""
Test d'upload de patch
======================

Test simple pour vérifier que l'upload de patch fonctionne avec les corrections.
"""

import time
from patch_to_realtime_converter import PatchToRealtimeConverter

def test_patch_upload():
    """Test d'upload de patch avec les nouvelles valeurs."""
    print("🎸 Test d'upload de patch")
    print("=" * 50)
    
    # Patch de test avec les mêmes valeurs que la GUI
    test_patch = {
        "meta": {"name": "Test Patch Upload"},
        "compressor": {"enabled": True, "threshold": 0.7217913070078934, "ratio": 2.0, "makeup_gain": 3.608956535039467},
        "eq": {"enabled": True, "low_gain": 0.0, "mid_gain": 2.0, "high_gain": 0.0},
        "delay": {"enabled": True, "time": 500, "feedback": 0.3, "mix": 0.2}
    }
    
    print("📊 Patch de test:")
    print(f"  - Compressor: threshold={test_patch['compressor']['threshold']:.2f}, ratio={test_patch['compressor']['ratio']}")
    print(f"  - EQ: mid_gain={test_patch['eq']['mid_gain']}")
    print(f"  - Delay: time={test_patch['delay']['time']}, feedback={test_patch['delay']['feedback']}")
    print()
    
    # Créer le convertisseur
    converter = PatchToRealtimeConverter()
    
    if not converter.realtime_magicstomp or not converter.realtime_magicstomp.output_port:
        print("❌ Pas de connexion MIDI")
        return False
    
    print("✅ Connexion MIDI établie")
    print()
    
    # Convertir le patch en messages
    messages = converter.patch_to_realtime_messages(test_patch)
    print(f"📤 Messages générés: {len(messages)}")
    
    for offset, value, description in messages:
        print(f"  - {description}: offset {offset} = {value}")
    
    print()
    print("🎯 Envoi des messages...")
    print("Regardez l'écran de votre Magicstomp pendant l'envoi...")
    print()
    
    # Appliquer le patch
    success = converter.apply_patch_realtime(test_patch, delay=1.0)
    
    if success:
        print("✅ Patch envoyé avec succès!")
        print("Vérifiez si les potentiomètres bougent sur le Magicstomp")
        return True
    else:
        print("❌ Échec de l'envoi du patch")
        return False

def main():
    """Fonction principale."""
    print("🎸 Test d'upload de patch")
    print("=" * 60)
    print("Test pour vérifier que l'upload de patch fonctionne")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que votre Magicstomp est allumé")
    print("2. Regardez l'écran pendant le test")
    print("3. Observez si les potentiomètres bougent")
    print()
    
    input("Appuyez sur Entrée pour commencer...")
    
    try:
        success = test_patch_upload()
        
        if success:
            print("\n🎉 SUCCÈS!")
            print("L'upload de patch fonctionne!")
        else:
            print("\n❌ ÉCHEC")
            print("L'upload de patch ne fonctionne pas")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    main()
