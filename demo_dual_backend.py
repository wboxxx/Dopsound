#!/usr/bin/env python3
"""
Démonstration du système dual backend
====================================

Script de démonstration pour montrer les fonctionnalités du système
dual backend (Essentia + librosa) avec sélection runtime.
"""

import sys
import numpy as np
import soundfile as sf
import tempfile
import os
from pathlib import Path

# Ajoute le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from analyzers.factory import get_analyzer, get_available_backends
from auto_tone_match_magicstomp import AutoToneMatcher


def create_demo_audio():
    """Crée un fichier audio de démonstration."""
    print("🎵 Création d'un fichier audio de démonstration...")
    
    sample_rate = 44100
    duration = 3.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Crée un signal complexe avec plusieurs effets
    # Note fondamentale
    fundamental = 220  # A3
    signal = np.sin(2 * np.pi * fundamental * t)
    
    # Ajoute des harmoniques (simule une guitare électrique)
    signal += 0.5 * np.sin(2 * np.pi * fundamental * 2 * t)
    signal += 0.3 * np.sin(2 * np.pi * fundamental * 3 * t)
    signal += 0.2 * np.sin(2 * np.pi * fundamental * 4 * t)
    
    # Ajoute de la distortion (saturation)
    signal = np.tanh(signal * 2.5) * 0.8
    
    # Ajoute du delay
    delay_time = 0.4  # 400ms
    delay_samples = int(delay_time * sample_rate)
    delayed_signal = np.zeros_like(signal)
    delayed_signal[delay_samples:] = signal[:-delay_samples] * 0.3
    signal += delayed_signal
    
    # Ajoute de la modulation (tremolo)
    tremolo_rate = 4.0  # Hz
    tremolo = 1.0 + 0.4 * np.sin(2 * np.pi * tremolo_rate * t)
    signal *= tremolo
    
    # Normalise
    signal = signal / np.max(np.abs(signal)) * 0.7
    
    # Sauvegarde
    filename = "demo_guitar.wav"
    sf.write(filename, signal, sample_rate)
    print(f"✅ Fichier de démonstration créé: {filename}")
    
    return filename


def demo_backend_selection():
    """Démonstration de la sélection de backend."""
    print("\n🔧 Démonstration de la sélection de backend")
    print("=" * 50)
    
    # Vérifie les backends disponibles
    backends = get_available_backends()
    print("Backends disponibles:")
    for name, available in backends.items():
        status = "✅ Disponible" if available else "❌ Non disponible"
        print(f"  {name}: {status}")
    
    # Test de sélection automatique
    print("\n🤖 Test de sélection automatique...")
    try:
        analyzer = get_analyzer('auto')
        print(f"✅ Backend auto-sélectionné: {analyzer.get_backend_name()}")
    except Exception as e:
        print(f"❌ Erreur lors de la sélection auto: {e}")
    
    # Test de sélection manuelle
    for backend_name in ['librosa', 'essentia']:
        if backends[backend_name]:
            print(f"\n🎯 Test de sélection manuelle: {backend_name}")
            try:
                analyzer = get_analyzer(backend_name)
                print(f"✅ Backend {backend_name} créé avec succès")
            except Exception as e:
                print(f"❌ Erreur avec {backend_name}: {e}")
        else:
            print(f"\n⏭️  Backend {backend_name} non disponible - ignoré")


def demo_feature_extraction():
    """Démonstration de l'extraction de features."""
    print("\n🔍 Démonstration de l'extraction de features")
    print("=" * 50)
    
    # Crée un fichier audio de test
    audio_file = create_demo_audio()
    
    try:
        # Test avec différents backends
        backends = get_available_backends()
        
        for backend_name, available in backends.items():
            if not available:
                continue
                
            print(f"\n🎵 Analyse avec backend {backend_name}:")
            print("-" * 30)
            
            try:
                # Crée l'analyzer
                analyzer = get_analyzer(backend_name)
                
                # Charge l'audio
                y, sr = analyzer.load_audio(audio_file)
                print(f"  Audio chargé: {len(y)} échantillons, {sr}Hz")
                
                # Extrait les features
                features = analyzer.analyze(audio_file)
                
                # Affiche les résultats
                print(f"  Spectral tilt: {features['spectral_tilt_db']:.1f} dB")
                print(f"  Spectral centroid: {features['spectral_centroid_mean']:.0f} Hz")
                print(f"  THD proxy: {features['thd_proxy']:.3f}")
                
                delay_ms, feedback = features['onset_delay_ms']
                if delay_ms > 10:
                    print(f"  Delay détecté: {delay_ms:.0f}ms, feedback: {feedback:.2f}")
                else:
                    print("  Pas de delay détecté")
                
                decay_s, mix = features['reverb_estimate']
                if decay_s > 0.8:
                    print(f"  Reverb détectée: {decay_s:.1f}s, mix: {mix:.2f}")
                else:
                    print("  Pas de reverb détectée")
                
                lfo_rate, lfo_strength = features['lfo_rate_hz']
                if lfo_rate is not None:
                    print(f"  LFO détecté: {lfo_rate:.2f}Hz, force: {lfo_strength:.2f}")
                else:
                    print("  Pas de LFO détecté")
                
                tempo = features['tempo_bpm']
                if tempo is not None:
                    print(f"  Tempo: {tempo:.1f} BPM")
                else:
                    print("  Tempo non détecté")
                
            except Exception as e:
                print(f"  ❌ Erreur avec {backend_name}: {e}")
    
    finally:
        # Nettoie le fichier de démonstration
        if os.path.exists(audio_file):
            os.unlink(audio_file)
            print(f"\n🗑️  Fichier de démonstration nettoyé: {audio_file}")


def demo_pipeline_complet():
    """Démonstration du pipeline complet."""
    print("\n🚀 Démonstration du pipeline complet")
    print("=" * 50)
    
    # Crée un fichier audio de test
    audio_file = create_demo_audio()
    
    try:
        # Test avec différents backends
        backends = get_available_backends()
        
        for backend_name, available in backends.items():
            if not available:
                continue
                
            print(f"\n🎸 Pipeline complet avec backend {backend_name}:")
            print("-" * 40)
            
            try:
                # Crée le tone matcher
                tone_matcher = AutoToneMatcher(backend_name)
                
                # Analyse l'audio
                features = tone_matcher.analyze_audio(audio_file, verbose=False)
                
                # Mappe vers patch
                patch = tone_matcher.map_to_patch()
                
                # Affiche le patch
                print(f"  Amplificateur: {patch['amp']['model']}")
                print(f"  Gain: {patch['amp']['gain']:.2f}")
                print(f"  EQ: B={patch['amp']['bass']:.2f} M={patch['amp']['mid']:.2f} T={patch['amp']['treble']:.2f}")
                print(f"  Booster: {patch['booster']['type']}")
                
                if patch['delay']['enabled']:
                    print(f"  Delay: {patch['delay']['time_ms']:.0f}ms")
                
                if patch['reverb']['enabled']:
                    print(f"  Reverb: {patch['reverb']['type']}")
                
                if patch['mod']['enabled']:
                    print(f"  Modulation: {patch['mod']['type']}")
                
                print(f"  Backend utilisé: {patch['meta']['backend']}")
                
            except Exception as e:
                print(f"  ❌ Erreur avec {backend_name}: {e}")
    
    finally:
        # Nettoie le fichier de démonstration
        if os.path.exists(audio_file):
            os.unlink(audio_file)
            print(f"\n🗑️  Fichier de démonstration nettoyé: {audio_file}")


def main():
    """Point d'entrée principal de la démonstration."""
    print("🎸 Démonstration du système dual backend")
    print("=" * 60)
    
    try:
        # Démonstration 1: Sélection de backend
        demo_backend_selection()
        
        # Démonstration 2: Extraction de features
        demo_feature_extraction()
        
        # Démonstration 3: Pipeline complet
        demo_pipeline_complet()
        
        print("\n✅ Démonstration terminée avec succès!")
        print("\n📋 Prochaines étapes:")
        print("   1. Installez Essentia pour de meilleures performances")
        print("   2. Testez avec vos propres fichiers audio")
        print("   3. Utilisez: python auto_tone_match_magicstomp.py your_audio.wav --backend auto")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
