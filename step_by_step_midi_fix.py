#!/usr/bin/env python3
"""
Correction étape par étape du MIDI Magicstomp
============================================

Procédure systématique pour résoudre les problèmes MIDI.
"""

import time
import mido
from realtime_magicstomp import RealtimeMagicstomp


def step_1_identify_midi_channel():
    """Étape 1: Identifier le canal MIDI correct."""
    print("🎯 ÉTAPE 1: Identifier le canal MIDI correct")
    print("=" * 60)
    print("Le Magicstomp affiche des erreurs MIDI, c'est bon signe!")
    print("Il reçoit les messages mais ils ne sont pas sur le bon canal.")
    print()
    print("Sur votre Magicstomp, regardez:")
    print("- L'écran affiche-t-il des erreurs MIDI ?")
    print("- Y a-t-il un indicateur de canal MIDI ?")
    print()
    
    rt = RealtimeMagicstomp()
    
    print("Test systématique des canaux MIDI...")
    print("Pour chaque canal, vous devriez voir:")
    print("- Soit une erreur MIDI (mauvais canal)")
    print("- Soit un changement de paramètre (bon canal)")
    print()
    
    working_channels = []
    
    for channel in range(16):
        print(f"\n🔍 Test canal {channel + 1}:")
        print("  Envoi CC 7 (Volume) = 30...")
        
        try:
            rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=30))
            time.sleep(1)
            
            print("  Envoi CC 7 (Volume) = 100...")
            rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=100))
            time.sleep(1)
            
            print("  Retour à CC 7 (Volume) = 64...")
            rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=64))
            time.sleep(1)
            
            # Demande à l'utilisateur avec retry
            while True:
                response = input(f"  Canal {channel + 1}: Avez-vous entendu des changements de volume ? (o/n/r pour retry/q pour quitter): ").strip().lower()
                
                if response in ['o', 'oui', 'y', 'yes']:
                    working_channels.append(channel + 1)
                    print(f"  ✅ Canal {channel + 1} fonctionne!")
                    break
                elif response in ['r', 'retry', 'retest']:
                    print(f"  🔄 Retest du canal {channel + 1}...")
                    # Retest rapide
                    rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=30))
                    time.sleep(0.5)
                    rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=100))
                    time.sleep(0.5)
                    rt.output_port.send(mido.Message('control_change', channel=channel, control=7, value=64))
                    time.sleep(0.5)
                    continue
                elif response in ['q', 'quit', 'quitter']:
                    print(f"  ⏭️ Passage au canal suivant...")
                    break
                elif response in ['n', 'non', 'no']:
                    print(f"  ❌ Canal {channel + 1} ne fonctionne pas")
                    break
                else:
                    print(f"  ❓ Réponse invalide. Utilisez: o/n/r/q")
                
        except Exception as e:
            print(f"  ❌ Erreur canal {channel + 1}: {e}")
    
    rt.stop()
    
    if working_channels:
        print(f"\n🎉 CANAUX FONCTIONNELS TROUVÉS: {working_channels}")
        return working_channels[0]  # Retourne le premier canal qui fonctionne
    else:
        print("\n❌ Aucun canal ne fonctionne")
        return None


def step_2_test_basic_cc(channel):
    """Étape 2: Tester les messages CC de base."""
    print(f"\n🎯 ÉTAPE 2: Tester les messages CC sur le canal {channel}")
    print("=" * 60)
    
    rt = RealtimeMagicstomp()
    
    print("Test des différents types de messages CC...")
    
    # Test CC 7 (Volume Master)
    print(f"\n🔊 Test CC 7 (Volume Master) - Canal {channel}")
    values = [20, 80, 20, 100, 20, 64]
    for i, value in enumerate(values):
        print(f"  {i+1}/6: Volume = {value}")
        rt.output_port.send(mido.Message('control_change', channel=channel-1, control=7, value=value))
        time.sleep(1)
    
    while True:
        response = input(f"\nCC 7 (Volume) sur canal {channel}: Avez-vous entendu des changements ? (o/n/r pour retry): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            cc7_works = True
            break
        elif response in ['r', 'retry', 'retest']:
            print(f"🔄 Retest CC 7 (Volume)...")
            values = [20, 100, 64]
            for value in values:
                print(f"  Volume = {value}")
                rt.output_port.send(mido.Message('control_change', channel=channel-1, control=7, value=value))
                time.sleep(1)
            continue
        elif response in ['n', 'non', 'no']:
            cc7_works = False
            break
        else:
            print("❓ Réponse invalide. Utilisez: o/n/r")
    
    # Test CC 11 (Expression)
    print(f"\n🎚️ Test CC 11 (Expression) - Canal {channel}")
    values = [20, 80, 20, 100, 20, 64]
    for i, value in enumerate(values):
        print(f"  {i+1}/6: Expression = {value}")
        rt.output_port.send(mido.Message('control_change', channel=channel-1, control=11, value=value))
        time.sleep(1)
    
    while True:
        response = input(f"\nCC 11 (Expression) sur canal {channel}: Avez-vous entendu des changements ? (o/n/r pour retry): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            cc11_works = True
            break
        elif response in ['r', 'retry', 'retest']:
            print(f"🔄 Retest CC 11 (Expression)...")
            values = [20, 100, 64]
            for value in values:
                print(f"  Expression = {value}")
                rt.output_port.send(mido.Message('control_change', channel=channel-1, control=11, value=value))
                time.sleep(1)
            continue
        elif response in ['n', 'non', 'no']:
            cc11_works = False
            break
        else:
            print("❓ Réponse invalide. Utilisez: o/n/r")
    
    # Test CC 1 (Modulation)
    print(f"\n🌀 Test CC 1 (Modulation) - Canal {channel}")
    values = [0, 64, 0, 127, 0, 64]
    for i, value in enumerate(values):
        print(f"  {i+1}/6: Modulation = {value}")
        rt.output_port.send(mido.Message('control_change', channel=channel-1, control=1, value=value))
        time.sleep(1)
    
    while True:
        response = input(f"\nCC 1 (Modulation) sur canal {channel}: Avez-vous entendu des changements ? (o/n/r pour retry): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            cc1_works = True
            break
        elif response in ['r', 'retry', 'retest']:
            print(f"🔄 Retest CC 1 (Modulation)...")
            values = [0, 127, 0, 64]
            for value in values:
                print(f"  Modulation = {value}")
                rt.output_port.send(mido.Message('control_change', channel=channel-1, control=1, value=value))
                time.sleep(1)
            continue
        elif response in ['n', 'non', 'no']:
            cc1_works = False
            break
        else:
            print("❓ Réponse invalide. Utilisez: o/n/r")
    
    rt.stop()
    
    print(f"\n📊 RÉSULTATS ÉTAPE 2:")
    print(f"  CC 7 (Volume): {'✅' if cc7_works else '❌'}")
    print(f"  CC 11 (Expression): {'✅' if cc11_works else '❌'}")
    print(f"  CC 1 (Modulation): {'✅' if cc1_works else '❌'}")
    
    return {
        'channel': channel,
        'cc7_works': cc7_works,
        'cc11_works': cc11_works,
        'cc1_works': cc1_works
    }


def step_3_test_program_change(channel):
    """Étape 3: Tester les Program Change."""
    print(f"\n🎯 ÉTAPE 3: Tester les Program Change sur le canal {channel}")
    print("=" * 60)
    print("Regardez l'écran de votre Magicstomp pendant ce test...")
    
    rt = RealtimeMagicstomp()
    
    print(f"\n🎵 Test Program Change - Canal {channel}")
    patches = [0, 5, 10, 15, 0]  # U01, U06, U11, U16, retour U01
    
    for patch in patches:
        print(f"  Sélection patch U{patch+1:02d}")
        rt.output_port.send(mido.Message('program_change', channel=channel-1, program=patch))
        time.sleep(2)
    
    rt.stop()
    
    while True:
        response = input(f"\nProgram Change sur canal {channel}: L'écran du Magicstomp a-t-il changé de patch ? (o/n/r pour retry): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            pc_works = True
            break
        elif response in ['r', 'retry', 'retest']:
            print(f"🔄 Retest Program Change...")
            patches = [0, 10, 0]  # U01, U11, retour U01
            for patch in patches:
                print(f"  Patch U{patch+1:02d}")
                rt.output_port.send(mido.Message('program_change', channel=channel-1, program=patch))
                time.sleep(2)
            continue
        elif response in ['n', 'non', 'no']:
            pc_works = False
            break
        else:
            print("❓ Réponse invalide. Utilisez: o/n/r")
    
    print(f"\n📊 RÉSULTAT ÉTAPE 3:")
    print(f"  Program Change: {'✅' if pc_works else '❌'}")
    
    return pc_works


def step_4_test_sysex_format(channel):
    """Étape 4: Tester le format sysex avec le bon canal."""
    print(f"\n🎯 ÉTAPE 4: Tester le format sysex sur le canal {channel}")
    print("=" * 60)
    
    rt = RealtimeMagicstomp()
    
    print("Test du format sysex avec le canal identifié...")
    print("IMPORTANT: Écoutez attentivement les changements!")
    
    # Test format actuel
    print(f"\n🧪 Test format actuel - Amp Level")
    rt.tweak_parameter(9, 30, immediate=True)  # Volume faible
    time.sleep(1)
    rt.tweak_parameter(9, 100, immediate=True)  # Volume fort
    time.sleep(1)
    rt.tweak_parameter(9, 64, immediate=True)   # Retour normal
    time.sleep(1)
    
    response = input(f"\nFormat sysex actuel: Avez-vous entendu des changements d'Amp Level ? (o/n): ").strip().lower()
    current_format_works = response in ['o', 'oui', 'y', 'yes']
    
    if not current_format_works:
        print(f"\n🔧 Le format actuel ne fonctionne pas, testons des alternatives...")
        
        # Test format alternatif 1: Device ID 0x00
        print(f"\n🧪 Test format alternatif 1 - Device ID 0x00")
        try:
            alt_message = [0xF0, 0x43, 0x7D, 0x00, 0x55, 0x42, 0x20, 0x00, 0x09, 0x40, 0x29, 0xF7]
            rt.output_port.send(mido.Message('sysex', data=alt_message[1:-1]))
            time.sleep(1)
            
            alt_message = [0xF0, 0x43, 0x7D, 0x00, 0x55, 0x42, 0x20, 0x00, 0x09, 0x64, 0x4D, 0xF7]
            rt.output_port.send(mido.Message('sysex', data=alt_message[1:-1]))
            time.sleep(1)
            
            response = input(f"Format alternatif 1: Avez-vous entendu des changements ? (o/n): ").strip().lower()
            alt1_works = response in ['o', 'oui', 'y', 'yes']
            
        except Exception as e:
            print(f"Erreur format alternatif 1: {e}")
            alt1_works = False
        
        # Test format alternatif 2: Header différent
        print(f"\n🧪 Test format alternatif 2 - Header différent")
        try:
            alt_message = [0xF0, 0x43, 0x7D, 0x30, 0x55, 0x42, 0x20, 0x00, 0x09, 0x40, 0x69, 0xF7]
            rt.output_port.send(mido.Message('sysex', data=alt_message[1:-1]))
            time.sleep(1)
            
            response = input(f"Format alternatif 2: Avez-vous entendu des changements ? (o/n): ").strip().lower()
            alt2_works = response in ['o', 'oui', 'y', 'yes']
            
        except Exception as e:
            print(f"Erreur format alternatif 2: {e}")
            alt2_works = False
        
        print(f"\n📊 RÉSULTATS FORMATS ALTERNATIFS:")
        print(f"  Format actuel: {'✅' if current_format_works else '❌'}")
        print(f"  Format alternatif 1: {'✅' if alt1_works else '❌'}")
        print(f"  Format alternatif 2: {'✅' if alt2_works else '❌'}")
        
        return {
            'current_works': current_format_works,
            'alt1_works': alt1_works,
            'alt2_works': alt2_works
        }
    
    rt.stop()
    
    return {'current_works': current_format_works}


def step_5_configure_magicstomp():
    """Étape 5: Configuration du Magicstomp."""
    print(f"\n🎯 ÉTAPE 5: Configuration du Magicstomp")
    print("=" * 60)
    print("Sur votre Magicstomp, vérifiez et configurez:")
    print()
    print("1. 🎛️ MODE:")
    print("   - Mode Edit (pas Performance)")
    print("   - Patch utilisateur (U01-U99)")
    print("   - Paramètres non verrouillés")
    print()
    print("2. 📡 MIDI:")
    print("   - MIDI activé")
    print("   - Canal MIDI correct")
    print("   - Pas de filtres MIDI")
    print()
    print("3. 🔌 CONNEXION:")
    print("   - Câble USB bien branché")
    print("   - Driver Yamaha installé")
    print()
    
    input("Appuyez sur Entrée quand vous avez vérifié la configuration...")


def main():
    """Procédure principale étape par étape."""
    print("🎸 Correction étape par étape du MIDI Magicstomp")
    print("=" * 70)
    print("Procédure systématique pour résoudre les problèmes MIDI.")
    print()
    print("OPTIONS DISPONIBLES:")
    print("- o/n: Oui/Non")
    print("- r: Retry (retest)")
    print("- q: Quitter l'étape actuelle")
    print("- s: Skip (passer l'étape)")
    print()
    
    try:
        # Étape 1: Identifier le canal MIDI (OBLIGATOIRE)
        print("🎯 ÉTAPE 1: Identifier le canal MIDI correct")
        print("⚠️ Cette étape est OBLIGATOIRE - elle ne peut pas être passée")
        working_channel = step_1_identify_midi_channel()
        
        if working_channel is None:
            print("\n❌ PROBLÈME: Aucun canal MIDI ne fonctionne")
            print("Vérifiez la configuration MIDI de votre Magicstomp.")
            return
        
        # Étape 2: Tester les messages CC
        print(f"\n🎯 ÉTAPE 2: Tester les messages CC sur le canal {working_channel}")
        skip = input("Voulez-vous passer cette étape ? (o/n): ").strip().lower() in ['o', 'oui', 'y', 'yes', 's', 'skip']
        
        if skip:
            print("⏭️ Étape 2 passée")
            cc_results = {'channel': working_channel, 'cc7_works': True, 'cc11_works': True, 'cc1_works': True}
        else:
            cc_results = step_2_test_basic_cc(working_channel)
        
        if not any([cc_results['cc7_works'], cc_results['cc11_works'], cc_results['cc1_works']]):
            print(f"\n❌ PROBLÈME: Aucun message CC ne fonctionne sur le canal {working_channel}")
            print("Vérifiez la configuration MIDI de votre Magicstomp.")
            return
        
        # Étape 3: Tester les Program Change
        print(f"\n🎯 ÉTAPE 3: Tester les Program Change sur le canal {working_channel}")
        skip = input("Voulez-vous passer cette étape ? (o/n): ").strip().lower() in ['o', 'oui', 'y', 'yes', 's', 'skip']
        
        if skip:
            print("⏭️ Étape 3 passée")
            pc_works = True
        else:
            pc_works = step_3_test_program_change(working_channel)
        
        # Étape 4: Tester le format sysex
        print(f"\n🎯 ÉTAPE 4: Tester le format sysex sur le canal {working_channel}")
        skip = input("Voulez-vous passer cette étape ? (o/n): ").strip().lower() in ['o', 'oui', 'y', 'yes', 's', 'skip']
        
        if skip:
            print("⏭️ Étape 4 passée")
            sysex_results = {'current_works': True}
        else:
            sysex_results = step_4_test_sysex_format(working_channel)
        
        # Étape 5: Configuration
        step_5_configure_magicstomp()
        
        # Résumé final
        print(f"\n🎉 DIAGNOSTIC TERMINÉ")
        print("=" * 70)
        print(f"Canal MIDI fonctionnel: {working_channel}")
        print(f"Messages CC: {'✅' if any([cc_results['cc7_works'], cc_results['cc11_works'], cc_results['cc1_works']]) else '❌'}")
        print(f"Program Change: {'✅' if pc_works else '❌'}")
        print(f"Format sysex: {'✅' if sysex_results.get('current_works') else '❌'}")
        
        if sysex_results.get('current_works'):
            print(f"\n✅ SUCCÈS: Le système fonctionne parfaitement!")
            print(f"Vous pouvez maintenant utiliser l'optimisation temps réel.")
        else:
            print(f"\n🔧 ACTION REQUISE:")
            print(f"Le format sysex doit être corrigé.")
            print(f"Basé sur les tests, nous devrons ajuster le format.")
        
    except KeyboardInterrupt:
        print("\n⚠️ Procédure interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de la procédure: {e}")


if __name__ == "__main__":
    main()
