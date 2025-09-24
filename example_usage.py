#!/usr/bin/env python3
"""
Exemple d'usage du pipeline Audio → Magicstomp
=============================================

Script de démonstration montrant comment utiliser les modules
individuellement ou via la CLI.
"""

import sys
from pathlib import Path

# Ajoute le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from analyze2json import AudioAnalyzer
from adapter_magicstomp import MagicstompAdapter


def demo_analysis():
    """Démonstration de l'analyse audio."""
    print("🎵 Démonstration - Analyse audio")
    print("=" * 40)
    
    # Crée un signal de test (sine wave avec harmoniques)
    import numpy as np
    
    # Génère un signal de test simulant une guitare avec effets
    sample_rate = 44100
    duration = 3.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Signal de base (note fondamentale)
    fundamental = 220  # A3
    signal = np.sin(2 * np.pi * fundamental * t)
    
    # Ajoute des harmoniques (simule une guitare)
    signal += 0.3 * np.sin(2 * np.pi * fundamental * 2 * t)
    signal += 0.2 * np.sin(2 * np.pi * fundamental * 3 * t)
    signal += 0.1 * np.sin(2 * np.pi * fundamental * 4 * t)
    
    # Ajoute un delay simple (simulation)
    delay_samples = int(0.3 * sample_rate)  # 300ms delay
    delayed_signal = np.zeros_like(signal)
    delayed_signal[delay_samples:] = signal[:-delay_samples] * 0.3
    signal += delayed_signal
    
    # Normalise
    signal = signal / np.max(np.abs(signal)) * 0.7
    
    # Sauvegarde le signal de test
    import soundfile as sf
    test_file = "test_guitar.wav"
    sf.write(test_file, signal, sample_rate)
    print(f"✅ Signal de test créé: {test_file}")
    
    # Analyse le signal
    analyzer = AudioAnalyzer()
    patch = analyzer.analyze(test_file)
    
    # Affiche le résultat
    print("\n📋 Patch généré:")
    import json
    print(json.dumps(patch, indent=2, ensure_ascii=False))
    
    return patch


def demo_conversion(patch):
    """Démonstration de la conversion vers SysEx."""
    print("\n🔄 Démonstration - Conversion SysEx")
    print("=" * 40)
    
    # Convertit vers SysEx
    adapter = MagicstompAdapter()
    syx_messages = adapter.json_to_syx(patch, patch_number=1)

    print(f"✅ {len(syx_messages)} message(s) SysEx généré(s)")
    if syx_messages:
        print(f"   Premier message: {syx_messages[0]}")

    # Sauvegarde le fichier SysEx
    syx_file = "test_patch.syx"
    adapter.save_to_file(syx_messages, syx_file)
    print(f"✅ Fichier SysEx sauvegardé: {syx_file}")
    
    # Affiche les ports MIDI disponibles
    print("\n🔌 Ports MIDI disponibles:")
    adapter.list_midi_ports()

    return syx_messages


def demo_cli():
    """Démonstration de l'usage CLI."""
    print("\n💻 Démonstration - Interface CLI")
    print("=" * 40)
    
    print("Commandes CLI disponibles:")
    print("  python cli/analyze2stomp.py test_guitar.wav --json-only --verbose")
    print("  python cli/analyze2stomp.py test_guitar.wav --syx test.syx")
    print("  python cli/analyze2stomp.py test_guitar.wav --send --patch 5")
    print("  python cli/analyze2stomp.py --list-ports")


def cleanup():
    """Nettoie les fichiers de test."""
    test_files = ["test_guitar.wav", "test_patch.syx"]
    for file in test_files:
        if Path(file).exists():
            Path(file).unlink()
            print(f"🗑️  Supprimé: {file}")


def main():
    """Point d'entrée principal de la démonstration."""
    print("🚀 Démonstration Pipeline Audio → Magicstomp")
    print("=" * 50)
    
    try:
        # Démonstration 1: Analyse audio
        patch = demo_analysis()
        
        # Démonstration 2: Conversion SysEx
    syx_data = demo_conversion(patch)
        
        # Démonstration 3: Usage CLI
        demo_cli()
        
        print("\n✅ Démonstration terminée avec succès!")
        print("\n📝 Prochaines étapes:")
        print("   1. Testez avec vos propres fichiers audio")
        print("   2. Connectez votre Magicstomp via USB-MIDI")
        print("   3. Utilisez --send pour envoyer directement")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Nettoie les fichiers de test
        cleanup()


if __name__ == "__main__":
    main()
