#!/usr/bin/env python3
"""
Test rapide de confirmation MIDI
===============================

Test simple pour confirmer si le problème est la configuration MIDI.
"""

import time
import mido
from realtime_magicstomp import RealtimeMagicstomp


def test_all_channels_quick():
    """Test rapide de tous les canaux."""
    print("🎯 Test rapide de tous les canaux MIDI")
    print("=" * 50)
    print("Ce test va envoyer un message CC 7 sur chaque canal.")
    print("Écoutez attentivement - vous devriez entendre UN changement de volume.")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("Test en cours...")
    
    for channel in range(16):
        print(f"Canal {channel + 1}: ", end="", flush=True)
        
        # Volume faible
        rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=30))
        time.sleep(0.3)
        
        # Volume fort
        rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=100))
        time.sleep(0.3)
        
        # Retour normal
        rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=64))
        time.sleep(0.3)
        
        print("✅")
    
    rt.stop()
    
    print("\n🎉 Test terminé!")
    print("\nRÉSULTATS:")
    print("- Avez-vous entendu UN changement de volume ?")
    print("- Sur quel canal (1-16) ?")
    print()
    print("Si vous n'avez rien entendu, le problème est la configuration MIDI du Magicstomp.")


def test_program_change_quick():
    """Test rapide des Program Change."""
    print("\n🎵 Test rapide des Program Change")
    print("=" * 50)
    print("Ce test va envoyer des Program Change sur tous les canaux.")
    print("Regardez l'écran du Magicstomp - il devrait changer de patch UNE fois.")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("Test en cours...")
    
    for channel in range(16):
        print(f"Canal {channel + 1}: ", end="", flush=True)
        
        # Change vers patch U10
        rt.output_port.send(mido.Message('program_change', channel=channel, program=9))
        time.sleep(0.5)
        
        # Retour vers patch U01
        rt.output_port.send(mido.Message('program_change', channel=channel, program=0))
        time.sleep(0.5)
        
        print("✅")
    
    rt.stop()
    
    print("\n🎉 Test terminé!")
    print("\nRÉSULTATS:")
    print("- L'écran du Magicstomp a-t-il changé de patch ?")
    print("- Sur quel canal (1-16) ?")
    print()
    print("Si l'écran n'a pas changé, le problème est la configuration MIDI du Magicstomp.")


def main():
    """Fonction principale."""
    print("🎸 Test rapide de confirmation MIDI")
    print("=" * 60)
    print("Tests rapides pour confirmer le problème de configuration MIDI.")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        test_all_channels_quick()
        
        input("\nAppuyez sur Entrée pour continuer avec les Program Change...")
        test_program_change_quick()
        
        print("\n🔍 DIAGNOSTIC FINAL:")
        print("=" * 60)
        print("Basé sur vos réponses:")
        print()
        print("Si vous avez entendu/vu des changements:")
        print("  → Le MIDI fonctionne, on peut continuer avec les tests sysex")
        print()
        print("Si vous n'avez rien entendu/vu:")
        print("  → Problème de configuration MIDI du Magicstomp")
        print("  → Vérifiez les paramètres MIDI sur votre Magicstomp")
        print("  → Consultez le manuel pour activer la réception MIDI")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
