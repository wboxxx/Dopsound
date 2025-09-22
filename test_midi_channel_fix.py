#!/usr/bin/env python3
"""
Test de correction du canal MIDI
================================

D'après MagicstompFrenzy:
- Canal par défaut: 0 (OMNI)
- Notre code envoie sur canal 1
- Il faut envoyer sur canal 0 !
"""

import time
import mido
from realtime_magicstomp import RealtimeMagicstomp


def test_channel_0():
    """Test avec canal MIDI 0 (OMNI)."""
    print("🎸 Test avec canal MIDI 0 (OMNI)")
    print("=" * 50)
    print("D'après MagicstompFrenzy, le canal par défaut est 0 (OMNI)")
    print("Notre code envoie sur canal 1, testons canal 0!")
    print()
    print("IMPORTANT: Assurez-vous que U01 est affiché à l'écran de votre Magicstomp!")
    print()
    
    # Test direct avec mido
    print("🧪 Test direct avec canal 0...")
    
    try:
        port = mido.open_output('2- Yamaha UB9-1 5')
        
        print("  - Test CC 7 (Volume) sur canal 0")
        port.send(mido.Message('control_change', channel=0, control=7, value=30))
        time.sleep(1)
        port.send(mido.Message('control_change', channel=0, control=7, value=100))
        time.sleep(1)
        port.send(mido.Message('control_change', channel=0, control=7, value=64))
        time.sleep(1)
        
        response = input("Canal 0 CC 7: Changement de volume audible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print("  ✅ Canal 0 fonctionne!")
            port.close()
            return True
        else:
            print("  ❌ Canal 0 ne fonctionne pas")
            
        print("  - Test CC 11 (Expression) sur canal 0")
        port.send(mido.Message('control_change', channel=0, control=11, value=30))
        time.sleep(1)
        port.send(mido.Message('control_change', channel=0, control=11, value=100))
        time.sleep(1)
        port.send(mido.Message('control_change', channel=0, control=11, value=64))
        time.sleep(1)
        
        response = input("Canal 0 CC 11: Changement d'expression audible ? (o/n): ").strip().lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print("  ✅ Canal 0 fonctionne avec CC 11!")
            port.close()
            return True
        else:
            print("  ❌ Canal 0 ne fonctionne pas avec CC 11")
            
        port.close()
        return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_sysex_with_channel_0():
    """Test SysEx avec canal 0."""
    print(f"\n🎛️ Test SysEx avec canal 0")
    print("=" * 50)
    
    # Modifions temporairement le code pour utiliser canal 0
    print("Modification temporaire pour canal 0...")
    
    rt = RealtimeMagicstomp()
    
    # Test avec canal 0 (modification temporaire)
    print("🧪 Test SysEx Amp Level avec canal 0...")
    
    try:
        # Envoi direct avec canal 0
        port = mido.open_output('2- Yamaha UB9-1 5')
        
        # SysEx pour Amp Level (offset 9) avec canal 0
        # Format: F0 43 7D 40 55 42 20 00 09 [data] F7
        sysex_data = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42, 0x20, 0x00, 0x09, 30, 0xF7]
        port.send(mido.Message('sysex', data=sysex_data))
        time.sleep(1)
        
        sysex_data = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42, 0x20, 0x00, 0x09, 100, 0xF7]
        port.send(mido.Message('sysex', data=sysex_data))
        time.sleep(1)
        
        sysex_data = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42, 0x20, 0x00, 0x09, 64, 0xF7]
        port.send(mido.Message('sysex', data=sysex_data))
        time.sleep(1)
        
        response = input("SysEx canal 0: Changement d'Amp Level audible ? (o/n): ").strip().lower()
        
        port.close()
        
        if response in ['o', 'oui', 'y', 'yes']:
            print("  ✅ SysEx avec canal 0 fonctionne!")
            return True
        else:
            print("  ❌ SysEx avec canal 0 ne fonctionne pas")
            return False
            
    except Exception as e:
        print(f"❌ Erreur SysEx: {e}")
        return False


def fix_realtime_magicstomp():
    """Corrige le code pour utiliser canal 0."""
    print(f"\n🔧 Correction du code pour canal 0")
    print("=" * 50)
    
    # Lisons le fichier actuel
    with open('realtime_magicstomp.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplaçons channel=1 par channel=0
    if 'channel=1' in content:
        content = content.replace('channel=1', 'channel=0')
        print("✅ Canal MIDI corrigé: 1 → 0")
        
        # Sauvegardons
        with open('realtime_magicstomp.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fichier sauvegardé")
        return True
    else:
        print("⚠️ Canal 1 non trouvé dans le code")
        return False


def test_fixed_code():
    """Test avec le code corrigé."""
    print(f"\n🧪 Test avec le code corrigé")
    print("=" * 50)
    
    rt = RealtimeMagicstomp()
    
    print("Test des paramètres d'amplificateur avec canal 0...")
    
    # Test des paramètres d'amplificateur
    print("  - Amp Level: 30 (faible)")
    rt.tweak_parameter(9, 30, immediate=True)  # Amp Level
    time.sleep(1)
    
    print("  - Amp Level: 100 (fort)")
    rt.tweak_parameter(9, 100, immediate=True)
    time.sleep(1)
    
    print("  - Amp Level: 64 (normal)")
    rt.tweak_parameter(9, 64, immediate=True)
    time.sleep(1)
    
    response = input("Code corrigé: Changement d'Amp Level audible ? (o/n): ").strip().lower()
    
    rt.stop()
    
    if response in ['o', 'oui', 'y', 'yes']:
        print("  ✅ Code corrigé fonctionne!")
        return True
    else:
        print("  ❌ Code corrigé ne fonctionne pas")
        return False


def main():
    """Fonction principale."""
    print("🎸 Test de correction du canal MIDI")
    print("=" * 60)
    print("D'après MagicstompFrenzy, le canal par défaut est 0 (OMNI)")
    print("Notre code envoie sur canal 1 - c'est probablement le problème!")
    print()
    print("PRÉPARATION:")
    print("1. Assurez-vous que U01 est affiché à l'écran de votre Magicstomp")
    print("2. Connectez votre guitare")
    print("3. Réglez le volume à un niveau audible")
    print("4. Jouez quelques notes pour tester")
    print()
    
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    try:
        # Test 1: Canal 0 direct
        print("\n" + "="*60)
        success_cc = test_channel_0()
        
        if success_cc:
            print(f"\n🎉 SUCCÈS! Canal 0 fonctionne!")
            
            # Test 2: SysEx avec canal 0
            print("\n" + "="*60)
            success_sysex = test_sysex_with_channel_0()
            
            if success_sysex:
                print(f"\n🎉 SUCCÈS! SysEx avec canal 0 fonctionne!")
                
                # Test 3: Corriger le code
                print("\n" + "="*60)
                fix_success = fix_realtime_magicstomp()
                
                if fix_success:
                    # Test 4: Code corrigé
                    print("\n" + "="*60)
                    final_success = test_fixed_code()
                    
                    if final_success:
                        print(f"\n🎉🎉🎉 PROBLÈME RÉSOLU!")
                        print(f"Le canal MIDI était le problème!")
                        print(f"Votre système de modification temps réel fonctionne maintenant!")
                        return True
        
        print(f"\n❌ Le canal 0 ne résout pas le problème")
        print(f"Le problème est ailleurs...")
        return False
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return False
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False


if __name__ == "__main__":
    main()


