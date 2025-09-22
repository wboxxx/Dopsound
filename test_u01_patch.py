#!/usr/bin/env python3
"""
Test du patch U01
================

Test spécifique avec le patch U01 affiché à l'écran du Magicstomp.
"""

import time
import mido
from realtime_magicstomp import RealtimeMagicstomp


def test_u01_patch():
    """Test du patch U01 actuellement affiché."""
    print("🎸 Test du patch U01")
    print("=" * 50)
    print("IMPORTANT: Assurez-vous que U01 est affiché à l'écran de votre Magicstomp!")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("🧪 Test des paramètres d'amplificateur sur U01...")
    print("Vous devriez entendre des changements sur le patch U01 actuel.")
    print()
    
    # Test 1: Amp Level (devrait changer le volume)
    print("🔊 Test 1: Amp Level (Volume)")
    print("  - Réglage à 30 (faible)")
    rt.tweak_parameter(9, 30, immediate=True)  # Amp Level
    time.sleep(1)
    
    print("  - Réglage à 100 (fort)")
    rt.tweak_parameter(9, 100, immediate=True)
    time.sleep(1)
    
    print("  - Retour à 64 (normal)")
    rt.tweak_parameter(9, 64, immediate=True)
    time.sleep(1)
    
    response = input("\nAvez-vous entendu des changements de volume ? (o/n): ").strip().lower()
    volume_works = response in ['o', 'oui', 'y', 'yes']
    
    # Test 2: Amp Gain (devrait changer la saturation)
    print("\n🔥 Test 2: Amp Gain (Saturation)")
    print("  - Réglage à 20 (clean)")
    rt.tweak_parameter(10, 20, immediate=True)  # Amp Gain
    time.sleep(1)
    
    print("  - Réglage à 100 (saturé)")
    rt.tweak_parameter(10, 100, immediate=True)
    time.sleep(1)
    
    print("  - Retour à 60 (normal)")
    rt.tweak_parameter(10, 60, immediate=True)
    time.sleep(1)
    
    response = input("\nAvez-vous entendu des changements de saturation ? (o/n): ").strip().lower()
    gain_works = response in ['o', 'oui', 'y', 'yes']
    
    # Test 3: Treble (devrait changer les aigus)
    print("\n🎛️ Test 3: Treble (Aigus)")
    print("  - Réglage à 10 (grave)")
    rt.tweak_parameter(11, 10, immediate=True)  # Treble
    time.sleep(1)
    
    print("  - Réglage à 120 (aigu)")
    rt.tweak_parameter(11, 120, immediate=True)
    time.sleep(1)
    
    print("  - Retour à 64 (normal)")
    rt.tweak_parameter(11, 64, immediate=True)
    time.sleep(1)
    
    response = input("\nAvez-vous entendu des changements d'aigus ? (o/n): ").strip().lower()
    treble_works = response in ['o', 'oui', 'y', 'yes']
    
    rt.stop()
    
    print("\n📊 RÉSULTATS:")
    print(f"  Volume (Amp Level): {'✅' if volume_works else '❌'}")
    print(f"  Saturation (Amp Gain): {'✅' if gain_works else '❌'}")
    print(f"  Aigus (Treble): {'✅' if treble_works else '❌'}")
    
    if any([volume_works, gain_works, treble_works]):
        print(f"\n🎉 SUCCÈS! Le système fonctionne sur U01!")
        print(f"Vous pouvez maintenant utiliser l'optimisation temps réel.")
        return True
    else:
        print(f"\n❌ PROBLÈME: Aucun paramètre ne fonctionne sur U01")
        print(f"Vérifiez la configuration MIDI de votre Magicstomp.")
        return False


def test_u01_with_different_channels():
    """Test U01 sur différents canaux MIDI."""
    print("\n📡 Test U01 sur différents canaux MIDI")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    print("Test de l'Amp Level sur différents canaux...")
    print("Pour chaque canal, vous devriez entendre un changement de volume.")
    print()
    
    working_channels = []
    
    for channel in range(16):
        print(f"🔍 Test canal {channel + 1}: ", end="", flush=True)
        
        # Test rapide de l'Amp Level
        rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=30))
        time.sleep(0.3)
        rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=100))
        time.sleep(0.3)
        rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=64))
        time.sleep(0.3)
        
        response = input(f"Canal {channel + 1}: Changement de volume ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            working_channels.append(channel + 1)
            print(f"  ✅ Canal {channel + 1} fonctionne!")
        else:
            print(f"  ❌ Canal {channel + 1} ne fonctionne pas")
    
    rt.stop()
    
    if working_channels:
        print(f"\n🎉 CANAUX FONCTIONNELS: {working_channels}")
        return working_channels[0]
    else:
        print(f"\n❌ Aucun canal ne fonctionne")
        return None


def main():
    """Fonction principale."""
    print("🎸 Test du patch U01")
    print("=" * 60)
    print("Test spécifique avec le patch U01 affiché à l'écran.")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Connectez votre guitare")
    print("3. Réglez le volume à un niveau audible")
    print("4. Jouez quelques notes pour tester")
    print()
    
    input("Appuyez sur Entrée quand U01 est affiché et que vous êtes prêt...")
    
    try:
        # Test principal
        success = test_u01_patch()
        
        if not success:
            print(f"\n🔧 Le test principal a échoué, testons les canaux MIDI...")
            working_channel = test_u01_with_different_channels()
            
            if working_channel:
                print(f"\n✅ Canal {working_channel} fonctionne!")
                print(f"Nous pouvons maintenant configurer le système pour ce canal.")
            else:
                print(f"\n❌ Problème de configuration MIDI du Magicstomp")
                print(f"Vérifiez les paramètres MIDI sur votre Magicstomp.")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()


