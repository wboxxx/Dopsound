#!/usr/bin/env python3
"""
Debug de la connexion Magicstomp
===============================

Diagnostique pourquoi les messages sysex ne modifient pas les paramètres.
"""

import time
import mido
from realtime_magicstomp import RealtimeMagicstomp


def test_different_sysex_formats():
    """Test différents formats de messages sysex."""
    print("🔬 Test de différents formats sysex")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    # Test 1: Format actuel
    print("Test 1: Format actuel (basé sur MagicstompFrenzy)")
    rt.tweak_parameter(9, 64, immediate=True)
    time.sleep(1)
    
    # Test 2: Format alternatif (peut-être que le Magicstomp attend un format différent)
    print("\nTest 2: Format alternatif - sans header spécifique")
    try:
        # Message sysex simple
        simple_message = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42, 0x20, 0x00, 0x09, 0x40, 0x69, 0xF7]
        rt.output_port.send(mido.Message('sysex', data=simple_message[1:-1]))
        print("Message simple envoyé")
        time.sleep(1)
    except Exception as e:
        print(f"Erreur: {e}")
    
    # Test 3: Format avec device ID différent
    print("\nTest 3: Format avec device ID 0x00")
    try:
        # Peut-être que le device ID doit être 0x00 au lieu de 0x40
        alt_message = [0xF0, 0x43, 0x7D, 0x00, 0x55, 0x42, 0x20, 0x00, 0x09, 0x40, 0x29, 0xF7]
        rt.output_port.send(mido.Message('sysex', data=alt_message[1:-1]))
        print("Message avec device ID 0x00 envoyé")
        time.sleep(1)
    except Exception as e:
        print(f"Erreur: {e}")
    
    # Test 4: Format avec checksum différent
    print("\nTest 4: Format avec checksum sur 8 bits")
    try:
        # Peut-être que le checksum doit être sur 8 bits
        alt_message = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42, 0x20, 0x00, 0x09, 0x40, 0x69, 0xF7]
        rt.output_port.send(mido.Message('sysex', data=alt_message[1:-1]))
        print("Message avec checksum 8 bits envoyé")
        time.sleep(1)
    except Exception as e:
        print(f"Erreur: {e}")
    
    rt.stop()


def test_magicstomp_modes():
    """Test différents modes du Magicstomp."""
    print("\n🎛️ Test des modes Magicstomp")
    print("=" * 50)
    
    print("IMPORTANT: Vérifiez le mode de votre Magicstomp!")
    print()
    print("Le Magicstomp peut être dans différents modes:")
    print("1. Mode Performance - Les paramètres peuvent être verrouillés")
    print("2. Mode Edit - Les paramètres peuvent être modifiés")
    print("3. Mode MIDI - Doit être activé pour recevoir les messages")
    print()
    print("Vérifiez aussi:")
    print("- Le patch actuel est-il un patch utilisateur (U01-U99) ?")
    print("- Le Magicstomp est-il configuré pour recevoir MIDI ?")
    print("- Y a-t-il un verrouillage des paramètres ?")
    
    input("\nAppuyez sur Entrée quand vous avez vérifié...")
    
    rt = RealtimeMagicstomp()
    
    # Test avec un patch utilisateur (peut-être que ça ne marche qu'avec les patches utilisateur)
    print("\nTest avec sélection de patch utilisateur...")
    
    # Envoie un Program Change pour sélectionner un patch utilisateur
    try:
        rt.output_port.send(mido.Message('program_change', channel=0, program=0))  # Patch U01
        print("Program Change vers U01 envoyé")
        time.sleep(0.5)
        
        # Maintenant teste les paramètres
        rt.tweak_parameter(9, 30, immediate=True)
        print("Paramètre envoyé sur patch U01")
        time.sleep(1)
        
        rt.tweak_parameter(9, 100, immediate=True)
        print("Paramètre envoyé sur patch U01")
        time.sleep(1)
        
    except Exception as e:
        print(f"Erreur: {e}")
    
    rt.stop()


def test_midi_channels():
    """Test différents canaux MIDI."""
    print("\n📡 Test des canaux MIDI")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    print("Test sur différents canaux MIDI...")
    
    for channel in range(16):
        print(f"Test canal {channel + 1}...")
        
        # Envoie un message de contrôle sur ce canal
        try:
            rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=64))  # Volume
            time.sleep(0.2)
        except Exception as e:
            print(f"Erreur canal {channel + 1}: {e}")
    
    rt.stop()


def test_bulk_dump_request():
    """Test d'une requête de dump pour voir si le Magicstomp répond."""
    print("\n📥 Test de requête de dump")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    print("Envoi d'une requête de dump de patch...")
    
    # Format de requête de dump selon MagicstompFrenzy
    dump_request = [0xF0, 0x43, 0x7D, 0x50, 0x55, 0x42, 0x30, 0x01, 0xF7]
    
    try:
        rt.output_port.send(mido.Message('sysex', data=dump_request[1:-1]))
        print("Requête de dump envoyée")
        print("Le Magicstomp devrait répondre avec le patch actuel...")
        
        # Écoute les réponses pendant 2 secondes
        time.sleep(2)
        
    except Exception as e:
        print(f"Erreur: {e}")
    
    rt.stop()


def test_simple_cc_messages():
    """Test de messages Control Change simples."""
    print("\n🎚️ Test de messages Control Change")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    print("Test de messages CC simples...")
    print("(Ces messages devraient fonctionner sur la plupart des appareils MIDI)")
    
    # Test CC 7 (Volume)
    print("Test CC 7 (Volume) - canal 0...")
    for value in [30, 64, 100, 64]:
        try:
            rt.output_port.send(mido.Message('control_change', channel=0, control=7, value=value))
            print(f"  CC 7 = {value}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Erreur: {e}")
    
    # Test CC 11 (Expression)
    print("\nTest CC 11 (Expression) - canal 0...")
    for value in [30, 64, 100, 64]:
        try:
            rt.output_port.send(mido.Message('control_change', channel=0, control=11, value=value))
            print(f"  CC 11 = {value}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Erreur: {e}")
    
    rt.stop()


def main():
    """Fonction principale de debug."""
    print("🐛 Debug de la connexion Magicstomp")
    print("=" * 60)
    print("Diagnostic pourquoi les messages sysex ne modifient pas les paramètres")
    print()
    
    try:
        test_different_sysex_formats()
        test_magicstomp_modes()
        test_midi_channels()
        test_bulk_dump_request()
        test_simple_cc_messages()
        
        print("\n🔍 DIAGNOSTIC TERMINÉ")
        print("=" * 60)
        print("Si aucun test n'a fonctionné, vérifiez:")
        print()
        print("1. 🎛️ MODE MAGICSTOMP:")
        print("   - Le Magicstomp est-il en mode Edit ?")
        print("   - Le patch est-il un patch utilisateur (U01-U99) ?")
        print("   - Les paramètres ne sont-ils pas verrouillés ?")
        print()
        print("2. 📡 CONFIGURATION MIDI:")
        print("   - Le MIDI est-il activé sur le Magicstomp ?")
        print("   - Le canal MIDI est-il correct ?")
        print("   - Y a-t-il des filtres MIDI actifs ?")
        print()
        print("3. 🔌 CONNEXION:")
        print("   - Le câble USB est-il bien branché ?")
        print("   - Le driver Yamaha est-il installé ?")
        print("   - Le port MIDI est-il le bon ?")
        print()
        print("4. 📋 DOCUMENTATION:")
        print("   - Consultez le manuel du Magicstomp pour la configuration MIDI")
        print("   - Vérifiez si des paramètres spéciaux sont requis")
        print()
        print("💡 ASTUCE: Essayez d'abord les messages CC simples (CC 7, CC 11)")
        print("   Si ça marche, le problème est dans le format sysex.")
        print("   Si ça ne marche pas, le problème est dans la configuration MIDI.")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du diagnostic: {e}")


if __name__ == "__main__":
    main()
