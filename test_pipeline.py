#!/usr/bin/env python3
"""
Test du pipeline complet avec signal audio réaliste
==================================================

Crée un signal audio plus complexe simulant une vraie guitare électrique
avec plusieurs effets et teste le pipeline complet.
"""

import numpy as np
import soundfile as sf
import sys
from pathlib import Path

# Ajoute le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from cli.analyze2stomp import MagicstompCLI


def create_realistic_guitar_signal():
    """Crée un signal de guitare électrique réaliste avec effets."""
    print("🎸 Création d'un signal de guitare réaliste...")
    
    sample_rate = 44100
    duration = 4.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Note fondamentale (E2 = 82.4 Hz)
    fundamental = 82.4
    signal = np.zeros_like(t)
    
    # Génère une séquence d'accords
    chords = [
        [82.4, 103.8, 123.5],  # E
        [73.4, 92.5, 110.0],   # D
        [87.3, 110.0, 130.8],  # F#
        [98.0, 123.5, 146.8],  # G
    ]
    
    chord_duration = duration / len(chords)
    
    for i, chord in enumerate(chords):
        start_time = i * chord_duration
        end_time = (i + 1) * chord_duration
        chord_mask = (t >= start_time) & (t < end_time)
        
        # Enveloppe ADSR pour chaque accord
        chord_t = t[chord_mask] - start_time
        attack = 0.1
        decay = 0.2
        sustain_level = 0.6
        release = 0.3
        
        envelope = np.ones_like(chord_t)
        
        # Attack
        attack_mask = chord_t < attack
        envelope[attack_mask] = chord_t[attack_mask] / attack
        
        # Decay
        decay_mask = (chord_t >= attack) & (chord_t < attack + decay)
        envelope[decay_mask] = 1.0 - (1.0 - sustain_level) * (chord_t[decay_mask] - attack) / decay
        
        # Sustain
        sustain_mask = (chord_t >= attack + decay) & (chord_t < chord_duration - release)
        envelope[sustain_mask] = sustain_level
        
        # Release
        release_mask = chord_t >= chord_duration - release
        envelope[release_mask] = sustain_level * (chord_duration - chord_t[release_mask]) / release
        
        # Génère les notes de l'accord
        for freq in chord:
            # Signal avec harmoniques (simule une guitare électrique)
            note = (np.sin(2 * np.pi * freq * chord_t) +
                   0.5 * np.sin(2 * np.pi * freq * 2 * chord_t) +
                   0.3 * np.sin(2 * np.pi * freq * 3 * chord_t) +
                   0.2 * np.sin(2 * np.pi * freq * 4 * chord_t) +
                   0.1 * np.sin(2 * np.pi * freq * 5 * chord_t))
            
            # Applique l'enveloppe
            note *= envelope
            
            # Ajoute une légère distorsion (simule l'ampli)
            note = np.tanh(note * 2.0) * 0.8
            
            signal[chord_mask] += note / len(chord)
    
    # Normalise
    signal = signal / np.max(np.abs(signal)) * 0.7
    
    # Ajoute du delay
    print("   Ajout du delay...")
    delay_time = 0.4  # 400ms
    delay_samples = int(delay_time * sample_rate)
    delayed_signal = np.zeros_like(signal)
    delayed_signal[delay_samples:] = signal[:-delay_samples] * 0.3
    
    # Ajoute du feedback
    feedback_delay = int(0.8 * sample_rate)
    if feedback_delay < len(signal):
        delayed_signal[feedback_delay:] += signal[:-feedback_delay] * 0.15
    
    signal += delayed_signal
    
    # Ajoute de la reverb (simulation simple)
    print("   Ajout de la reverb...")
    reverb_impulse_length = int(1.5 * sample_rate)
    reverb_impulse = np.exp(-np.linspace(0, 5, reverb_impulse_length))
    reverb_impulse *= np.random.randn(reverb_impulse_length) * 0.1
    
    # Convolution simple (approximation)
    reverb_signal = np.convolve(signal, reverb_impulse, mode='same')
    signal = signal + reverb_signal * 0.15
    
    # Ajoute de la modulation (chorus)
    print("   Ajout de la modulation...")
    lfo_rate = 0.8  # Hz
    lfo_depth = 0.01  # 10ms de modulation
    
    modulated_signal = np.zeros_like(signal)
    for i in range(len(signal)):
        # LFO pour la modulation
        lfo = lfo_depth * np.sin(2 * np.pi * lfo_rate * i / sample_rate)
        delay_samples = int(lfo * sample_rate)
        
        if i + delay_samples < len(signal) and i + delay_samples >= 0:
            modulated_signal[i] = signal[i + delay_samples]
        else:
            modulated_signal[i] = signal[i]
    
    signal = 0.7 * signal + 0.3 * modulated_signal
    
    # Normalise final
    signal = signal / np.max(np.abs(signal)) * 0.8
    
    # Sauvegarde
    filename = "realistic_guitar.wav"
    sf.write(filename, signal, sample_rate)
    print(f"✅ Signal de guitare réaliste créé: {filename}")
    
    return filename


def test_pipeline():
    """Teste le pipeline complet."""
    print("🚀 Test du pipeline complet")
    print("=" * 50)
    
    # Crée le signal de test
    audio_file = create_realistic_guitar_signal()
    
    # Teste la CLI
    print("\n🧪 Test de la CLI...")
    
    cli = MagicstompCLI()
    
    # Test 1: Analyse JSON seulement
    print("\n1️⃣ Test analyse JSON...")
    patch = cli.analyze_audio(audio_file, verbose=True)
    
    # Sauvegarde JSON
    json_file = "test_patch.json"
    cli.save_json(patch, json_file, verbose=True)
    
    # Test 2: Conversion SysEx
    print("\n2️⃣ Test conversion SysEx...")
    syx_data = cli.convert_to_syx(patch, patch_number=2, verbose=True)
    
    # Sauvegarde SysEx
    syx_file = "test_patch.syx"
    cli.save_syx(syx_data, syx_file, verbose=True)
    
    # Test 3: Pipeline complet via CLI
    print("\n3️⃣ Test pipeline CLI complet...")
    success = cli.run_pipeline(
        audio_file=audio_file,
        json_output="cli_test.json",
        syx_output="cli_test.syx",
        patch_number=3,
        verbose=True
    )
    
    if success:
        print("\n✅ Tous les tests ont réussi!")
        print("\n📁 Fichiers générés:")
        for file in ["realistic_guitar.wav", "test_patch.json", "test_patch.syx", 
                     "cli_test.json", "cli_test.syx"]:
            if Path(file).exists():
                size = Path(file).stat().st_size
                print(f"   📄 {file} ({size} bytes)")
    else:
        print("\n❌ Certains tests ont échoué")
    
    return success


def cleanup_test_files():
    """Nettoie les fichiers de test."""
    test_files = [
        "realistic_guitar.wav",
        "test_patch.json", 
        "test_patch.syx",
        "cli_test.json",
        "cli_test.syx"
    ]
    
    cleaned = []
    for file in test_files:
        if Path(file).exists():
            Path(file).unlink()
            cleaned.append(file)
    
    if cleaned:
        print(f"\n🗑️  Fichiers nettoyés: {', '.join(cleaned)}")


def main():
    """Point d'entrée principal."""
    try:
        success = test_pipeline()
        
        if success:
            print("\n🎉 Pipeline testé avec succès!")
            print("\n📋 Prochaines étapes:")
            print("   1. Testez avec vos propres fichiers audio")
            print("   2. Connectez votre Magicstomp")
            print("   3. Utilisez: python cli/analyze2stomp.py your_audio.wav --send")
        else:
            print("\n⚠️  Tests partiellement réussis")
            
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Demande si on doit nettoyer
        try:
            response = input("\n🧹 Nettoyer les fichiers de test? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                cleanup_test_files()
        except KeyboardInterrupt:
            print("\n👋 Au revoir!")


if __name__ == "__main__":
    main()
