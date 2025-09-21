#!/usr/bin/env python3
"""
Test du canal OMNI (canal 0)
===========================

D'après MagicstompFrenzy, le canal par défaut est OMNI (0).
"""

import time
import mido
from realtime_magicstomp import RealtimeMagicstomp


def test_omni_channel():
    """Test du canal OMNI (0) comme MagicstompFrenzy."""
    print("🎸 Test du canal OMNI (canal 0)")
    print("=" * 50)
    print("D'après MagicstompFrenzy, le canal par défaut est OMNI (0)")
    print("Testons d'abord le canal 0...")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("🧪 Test CC 7 (Volume) sur canal 0 (OMNI)...")
    
    # Test canal 0 (OMNI)
    print("  Canal 0 (OMNI): Volume faible")
    rt.output_port.send(mido.Message('control_change', channel=0, control=7, value=30))
    time.sleep(1)
    
    print("  Canal 0 (OMNI): Volume fort")
    rt.output_port.send(mido.Message('control_change', channel=0, control=7, value=100))
    time.sleep(1)
    
    print("  Canal 0 (OMNI): Volume normal")
    rt.output_port.send(mido.Message('control_change', channel=0, control=7, value=64))
    time.sleep(1)
    
    response = input("\nCanal 0 (OMNI): Avez-vous entendu des changements de volume ? (o/n): ").strip().lower()
    
    if response in ['o', 'oui', 'y', 'yes']:
        print("🎉 SUCCÈS! Le canal 0 (OMNI) fonctionne!")
        rt.stop()
        return 0
    
    print("❌ Canal 0 (OMNI) ne fonctionne pas")
    
    # Si OMNI ne fonctionne pas, testons les canaux 1-16
    print("\n🔍 Canal OMNI ne fonctionne pas, testons les canaux 1-16...")
    
    for channel in range(1, 17):  # Canaux 1-16
        print(f"  Canal {channel}: Volume faible")
        rt.output_port.send(mido.Message('control_change', channel=channel-1, control=7, value=30))
        time.sleep(0.5)
        
        print(f"  Canal {channel}: Volume fort")
        rt.output_port.send(mido.Message('control_change', channel=channel-1, control=7, value=100))
        time.sleep(0.5)
        
        print(f"  Canal {channel}: Volume normal")
        rt.output_port.send(mido.Message('control_change', channel=channel-1, control=7, value=64))
        time.sleep(0.5)
        
        response = input(f"Canal {channel}: Changement de volume ? (o/n/q pour quitter): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print(f"🎉 SUCCÈS! Le canal {channel} fonctionne!")
            rt.stop()
            return channel
        elif response in ['q', 'quit', 'quitter']:
            print("⏭️ Test interrompu")
            break
    
    rt.stop()
    print("❌ Aucun canal ne fonctionne")
    return None


def test_sysex_with_working_channel(channel):
    """Test du format sysex avec le canal qui fonctionne."""
    print(f"\n🎯 Test du format sysex avec le canal {channel}")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    print("IMPORTANT: Assurez-vous que U01 est affiché à l'écran de votre Magicstomp!")
    print()
    
    # Test sysex (ne dépend pas du canal MIDI)
    print("🧪 Test format sysex - Amp Level")
    print("  - Réglage à 30 (faible)")
    rt.tweak_parameter(9, 30, immediate=True)  # Amp Level
    time.sleep(1)
    
    print("  - Réglage à 100 (fort)")
    rt.tweak_parameter(9, 100, immediate=True)
    time.sleep(1)
    
    print("  - Retour à 64 (normal)")
    rt.tweak_parameter(9, 64, immediate=True)
    time.sleep(1)
    
    response = input("\nFormat sysex: Avez-vous entendu des changements d'Amp Level ? (o/n): ").strip().lower()
    
    rt.stop()
    
    if response in ['o', 'oui', 'y', 'yes']:
        print("🎉 SUCCÈS! Le format sysex fonctionne!")
        return True
    else:
        print("❌ Le format sysex ne fonctionne pas")
        return False


def main():
    """Fonction principale."""
    print("🎸 Test du canal OMNI et sysex")
    print("=" * 60)
    print("Basé sur l'analyse de MagicstompFrenzy:")
    print("- Canal par défaut: OMNI (0)")
    print("- Si OMNI ne fonctionne pas, tester les canaux 1-16")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        # Test du canal MIDI
        working_channel = test_omni_channel()
        
        if working_channel is not None:
            print(f"\n✅ Canal MIDI fonctionnel trouvé: {working_channel}")
            
            # Test du format sysex
            sysex_works = test_sysex_with_working_channel(working_channel)
            
            if sysex_works:
                print(f"\n🎉 SYSTÈME COMPLET FONCTIONNEL!")
                print(f"Canal MIDI: {working_channel}")
                print(f"Format sysex: ✅")
                print(f"Vous pouvez maintenant utiliser l'optimisation temps réel!")
            else:
                print(f"\n🔧 Canal MIDI OK, mais format sysex à corriger")
                print(f"Canal MIDI: {working_channel}")
                print(f"Format sysex: ❌")
        else:
            print(f"\n❌ Problème de configuration MIDI du Magicstomp")
            print(f"Vérifiez les paramètres MIDI sur votre Magicstomp.")
            print(f"Essayez de configurer le canal sur OMNI (0) ou canal 1")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
