#!/usr/bin/env python3
"""
Audio Analysis to Magicstomp JSON Converter
===========================================

Analyse un fichier audio et extrait des features guitare pour générer
un patch JSON compatible Magicstomp.

Usage:
    python analyze2json.py input.wav [--output output.json] [--verbose]

Fonctionnalités:
- Détection d'effets (delay, reverb, chorus, phaser, distortion)
- Mapping vers paramètres Magicstomp (amp, cab, drive, delay, reverb, mod)
- Export JSON neutre avec scores de confiance
"""

import librosa
import numpy as np
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from scipy import signal
from scipy.stats import kurtosis


class AudioAnalyzer:
    """Analyseur audio pour extraction de features guitare."""
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialise l'analyseur audio.
        
        Args:
            sample_rate: Fréquence d'échantillonnage cible
        """
        self.sample_rate = sample_rate
        self.features = {}
        self.confidence_scores = {}
    
    def load_audio(self, file_path: str) -> np.ndarray:
        """
        Charge un fichier audio.
        
        Args:
            file_path: Chemin vers le fichier audio
            
        Returns:
            Signal audio normalisé
        """
        print(f"🎵 Chargement de {file_path}...")
        
        try:
            # Charge l'audio et normalise
            y, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
            
            # Normalisation RMS
            rms = np.sqrt(np.mean(y**2))
            if rms > 0:
                y = y / rms * 0.7  # Normalise à 70% pour éviter la saturation
                
            print(f"✅ Audio chargé: {len(y)} échantillons, {sr}Hz, RMS={rms:.3f}")
            return y
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            sys.exit(1)
    
    def analyze_spectral_features(self, y: np.ndarray) -> Dict[str, float]:
        """
        Analyse les caractéristiques spectrales pour détecter les effets.
        
        Args:
            y: Signal audio
            
        Returns:
            Dictionnaire des features spectrales
        """
        print("🔍 Analyse des features spectrales...")
        
        # Spectrogramme
        stft = librosa.stft(y)
        magnitude = np.abs(stft)
        
        # Features spectrales de base
        spectral_centroid = librosa.feature.spectral_centroid(S=magnitude, sr=self.sample_rate)
        spectral_rolloff = librosa.feature.spectral_rolloff(S=magnitude, sr=self.sample_rate)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(S=magnitude, sr=self.sample_rate)
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
        
        # Moyennes temporelles
        features = {
            'spectral_centroid_mean': np.mean(spectral_centroid),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'spectral_bandwidth_mean': np.mean(spectral_bandwidth),
            'zcr_mean': np.mean(zero_crossing_rate),
            'spectral_centroid_std': np.std(spectral_centroid),
            'spectral_bandwidth_std': np.std(spectral_bandwidth)
        }
        
        print(f"   Centroid: {features['spectral_centroid_mean']:.1f}Hz")
        print(f"   Rolloff: {features['spectral_rolloff_mean']:.1f}Hz")
        print(f"   Bandwidth: {features['spectral_bandwidth_mean']:.1f}Hz")
        
        return features
    
    def detect_delay(self, y: np.ndarray) -> Tuple[bool, Dict[str, float]]:
        """
        Détecte la présence et les paramètres de delay.
        
        Heuristique: Auto-corrélation pour trouver des répétitions périodiques.
        
        Args:
            y: Signal audio
            
        Returns:
            Tuple (présence_delay, paramètres)
        """
        print("⏰ Détection du delay...")
        
        # Auto-corrélation
        autocorr = np.correlate(y, y, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Normalise
        autocorr = autocorr / np.max(autocorr)
        
        # Recherche des pics après le premier (delay)
        # Ignore les premiers 10ms (latence minimum)
        min_delay_samples = int(0.01 * self.sample_rate)
        search_window = autocorr[min_delay_samples:min(len(autocorr), int(2.0 * self.sample_rate))]
        
        # Détecte les pics significatifs
        peaks, properties = signal.find_peaks(search_window, height=0.3, distance=100)
        
        if len(peaks) > 0:
            # Prend le pic le plus fort
            best_peak_idx = peaks[np.argmax(search_window[peaks])]
            delay_time_ms = (best_peak_idx + min_delay_samples) * 1000 / self.sample_rate
            
            # Estime le feedback basé sur l'amplitude du pic
            feedback = min(0.8, search_window[best_peak_idx] * 1.5)
            
            # Estime le mix basé sur l'énergie relative
            mix = min(0.4, feedback * 0.6)
            
            confidence = min(0.95, search_window[best_peak_idx] * 1.2)
            
            print(f"   ✅ Delay détecté: {delay_time_ms:.0f}ms, feedback={feedback:.2f}, mix={mix:.2f}")
            print(f"   📊 Confiance: {confidence:.2f}")
            
            return True, {
                'time_ms': delay_time_ms,
                'feedback': feedback,
                'mix': mix,
                'confidence': confidence
            }
        else:
            print("   ❌ Aucun delay détecté")
            return False, {'confidence': 0.0}
    
    def detect_reverb(self, y: np.ndarray) -> Tuple[bool, Dict[str, float]]:
        """
        Détecte la présence et les paramètres de reverb.
        
        Heuristique: Analyse de la queue de réverbération et des caractéristiques spectrales.
        
        Args:
            y: Signal audio
            
        Returns:
            Tuple (présence_reverb, paramètres)
        """
        print("🏛️ Détection de la reverb...")
        
        # Analyse de la queue de réverbération
        # Trouve le point où l'enveloppe descend en dessous de 10% du max
        envelope = np.abs(y)
        max_envelope = np.max(envelope)
        threshold = max_envelope * 0.1
        
        # Trouve les points de croisement avec le seuil
        above_threshold = envelope > threshold
        if np.any(above_threshold):
            last_above = np.where(above_threshold)[0][-1]
            decay_time_s = last_above / self.sample_rate
        else:
            decay_time_s = 0.5  # Valeur par défaut
        
        # Analyse spectrale pour détecter la coloration
        stft = librosa.stft(y)
        magnitude = np.abs(stft)
        
        # Calcul de la densité spectrale dans les hautes fréquences
        freqs = librosa.fft_frequencies(sr=self.sample_rate)
        high_freq_mask = freqs > 3000
        high_freq_energy = np.mean(magnitude[high_freq_mask, :])
        total_energy = np.mean(magnitude)
        
        high_freq_ratio = high_freq_energy / (total_energy + 1e-8)
        
        # Détection basée sur la queue et la densité spectrale
        has_reverb = decay_time_s > 0.8 and high_freq_ratio > 0.1
        
        if has_reverb:
            # Estime le type de reverb basé sur la décroissance
            if decay_time_s > 2.0:
                reverb_type = "HALL"
                decay_s = min(3.0, decay_time_s)
            elif decay_time_s > 1.2:
                reverb_type = "PLATE"
                decay_s = min(2.0, decay_time_s)
            else:
                reverb_type = "ROOM"
                decay_s = min(1.5, decay_time_s)
            
            # Estime le mix basé sur l'énergie relative
            mix = min(0.3, high_freq_ratio * 2.0)
            
            confidence = min(0.9, (decay_time_s - 0.5) / 2.0 + high_freq_ratio)
            
            print(f"   ✅ Reverb détectée: {reverb_type}, decay={decay_s:.1f}s, mix={mix:.2f}")
            print(f"   📊 Confiance: {confidence:.2f}")
            
            return True, {
                'type': reverb_type,
                'decay_s': decay_s,
                'mix': mix,
                'confidence': confidence
            }
        else:
            print("   ❌ Aucune reverb détectée")
            return False, {'confidence': 0.0}
    
    def detect_modulation(self, y: np.ndarray) -> Tuple[bool, Dict[str, float]]:
        """
        Détecte les effets de modulation (chorus, phaser, tremolo).
        
        Heuristique: Analyse de la modulation d'amplitude et de phase.
        
        Args:
            y: Signal audio
            
        Returns:
            Tuple (présence_modulation, paramètres)
        """
        print("🌊 Détection de la modulation...")
        
        # Analyse de la modulation d'amplitude
        envelope = np.abs(y)
        
        # Filtre passe-bas pour isoler la modulation
        nyquist = self.sample_rate / 2
        low_freq = 20 / nyquist
        b, a = signal.butter(4, low_freq, btype='low')
        mod_envelope = signal.filtfilt(b, a, envelope)
        
        # Normalise
        mod_envelope = mod_envelope / (np.max(mod_envelope) + 1e-8)
        
        # Analyse spectrale de la modulation
        mod_fft = np.fft.fft(mod_envelope)
        freqs = np.fft.fftfreq(len(mod_fft), 1/self.sample_rate)
        
        # Recherche des pics dans la bande 0.5-8 Hz (modulation typique)
        freq_mask = (freqs >= 0.5) & (freqs <= 8.0)
        mod_spectrum = np.abs(mod_fft[freq_mask])
        mod_freqs = freqs[freq_mask]
        
        if len(mod_spectrum) > 0:
            # Trouve le pic principal
            peak_idx = np.argmax(mod_spectrum)
            mod_rate = mod_freqs[peak_idx]
            mod_strength = mod_spectrum[peak_idx] / np.sum(mod_spectrum)
            
            # Détection basée sur la force de la modulation
            has_modulation = mod_strength > 0.1 and mod_rate > 0.3
            
            if has_modulation:
                # Détermine le type basé sur la fréquence
                if mod_rate < 1.5:
                    mod_type = "CHORUS"
                elif mod_rate < 4.0:
                    mod_type = "PHASER"
                else:
                    mod_type = "TREMOLO"
                
                # Estime les paramètres
                depth = min(0.7, mod_strength * 3.0)
                mix = min(0.3, mod_strength * 2.0)
                
                confidence = min(0.85, mod_strength * 4.0)
                
                print(f"   ✅ Modulation détectée: {mod_type}, rate={mod_rate:.1f}Hz, depth={depth:.2f}")
                print(f"   📊 Confiance: {confidence:.2f}")
                
                return True, {
                    'type': mod_type,
                    'rate_hz': mod_rate,
                    'depth': depth,
                    'mix': mix,
                    'confidence': confidence
                }
        
        print("   ❌ Aucune modulation détectée")
        return False, {'confidence': 0.0}
    
    def detect_distortion(self, y: np.ndarray) -> Tuple[bool, Dict[str, float]]:
        """
        Détecte la présence de distortion/overdrive.
        
        Heuristique: Analyse de la distorsion harmonique et du clipping.
        
        Args:
            y: Signal audio
            
        Returns:
            Tuple (présence_distortion, paramètres)
        """
        print("🔥 Détection de la distortion...")
        
        # Analyse du clipping (saturation)
        clipped_samples = np.sum(np.abs(y) > 0.95)
        clipping_ratio = clipped_samples / len(y)
        
        # Analyse harmonique
        fft = np.fft.fft(y)
        freqs = np.fft.fftfreq(len(fft), 1/self.sample_rate)
        
        # Calcul de la distorsion harmonique (THD approximatif)
        fundamental_freq = freqs[np.argmax(np.abs(fft))]
        
        # Énergie dans les harmoniques vs fondamentale
        fundamental_idx = int(fundamental_freq * len(fft) / self.sample_rate)
        harmonic_energy = 0
        fundamental_energy = 0
        
        for harmonic in range(1, 8):  # Analyse jusqu'à la 7ème harmonique
            harmonic_idx = fundamental_idx * harmonic
            if harmonic_idx < len(fft):
                if harmonic == 1:
                    fundamental_energy = np.abs(fft[harmonic_idx])
                else:
                    harmonic_energy += np.abs(fft[harmonic_idx])
        
        if fundamental_energy > 0:
            thd_approx = harmonic_energy / fundamental_energy
        else:
            thd_approx = 0
        
        # Détection basée sur le clipping et les harmoniques
        has_distortion = clipping_ratio > 0.01 or thd_approx > 0.1
        
        if has_distortion:
            # Estime le gain basé sur le clipping
            if clipping_ratio > 0.05:
                drive_level = min(0.9, 0.3 + clipping_ratio * 10)
            else:
                drive_level = min(0.7, thd_approx * 3.0)
            
            confidence = min(0.9, (clipping_ratio * 20 + thd_approx * 2))
            
            print(f"   ✅ Distortion détectée: drive={drive_level:.2f}, THD≈{thd_approx:.3f}")
            print(f"   📊 Confiance: {confidence:.2f}")
            
            return True, {
                'drive_level': drive_level,
                'thd_approx': thd_approx,
                'confidence': confidence
            }
        else:
            print("   ❌ Aucune distortion détectée")
            return False, {'confidence': 0.0}
    
    def map_to_amp_settings(self, features: Dict[str, float], has_distortion: bool, 
                           distortion_params: Dict[str, float]) -> Dict[str, Any]:
        """
        Mappe les features audio vers les paramètres d'amplificateur.
        
        Args:
            features: Features spectrales extraites
            has_distortion: Présence de distortion détectée
            distortion_params: Paramètres de distortion
            
        Returns:
            Configuration d'amplificateur
        """
        print("🎸 Mapping vers paramètres amplificateur...")
        
        # Sélection du modèle d'amp basé sur les caractéristiques spectrales
        centroid = features.get('spectral_centroid_mean', 2000)
        bandwidth = features.get('spectral_bandwidth_mean', 1000)
        
        if centroid > 3000 and bandwidth > 1500:
            amp_model = "BRIT_TOP_BOOST"  # Bright, clair
        elif centroid < 2000 and bandwidth < 1000:
            amp_model = "TWEED_BASSMAN"   # Chaleureux, vintage
        else:
            amp_model = "JCM800"          # Équilibré, rock
        
        # Paramètres de tonalité basés sur le spectre
        treble = min(1.0, (centroid - 1000) / 3000)
        bass = min(1.0, (1500 - centroid) / 1000)
        mid = 0.5 + (bandwidth - 1000) / 2000
        mid = max(0.0, min(1.0, mid))
        
        # Presence basé sur les hautes fréquences
        presence = min(1.0, treble * 1.2)
        
        # Gain basé sur la distortion détectée
        if has_distortion:
            gain = distortion_params.get('drive_level', 0.3)
        else:
            # Gain basé sur l'énergie RMS
            rms_estimate = features.get('spectral_bandwidth_mean', 1000) / 2000
            gain = min(0.7, max(0.2, rms_estimate))
        
        # Sélection de cabine basée sur le modèle d'amp
        cab_mapping = {
            "BRIT_TOP_BOOST": "2x12_ALNICO",
            "TWEED_BASSMAN": "4x10_TWEED",
            "JCM800": "4x12_VINTAGE"
        }
        cab = cab_mapping.get(amp_model, "2x12_ALNICO")
        
        print(f"   Amp: {amp_model}, Gain: {gain:.2f}")
        print(f"   EQ: Bass={bass:.2f}, Mid={mid:.2f}, Treble={treble:.2f}, Presence={presence:.2f}")
        print(f"   Cab: {cab}")
        
        return {
            "model": amp_model,
            "gain": gain,
            "bass": bass,
            "mid": mid,
            "treble": treble,
            "presence": presence,
            "cab": cab
        }
    
    def map_to_booster(self, features: Dict[str, float], has_distortion: bool) -> Dict[str, Any]:
        """
        Mappe vers les paramètres de booster.
        
        Args:
            features: Features spectrales
            has_distortion: Présence de distortion
            
        Returns:
            Configuration de booster
        """
        centroid = features.get('spectral_centroid_mean', 2000)
        
        # Booster basé sur le besoin de clarté
        if centroid > 2500 and not has_distortion:
            booster_type = "TREBLE"
            level = 0.6
        elif centroid < 1500:
            booster_type = "TUBE_SCREAMER"
            level = 0.4
        else:
            booster_type = "CLEAN"
            level = 0.3
        
        return {
            "type": booster_type,
            "level": level
        }
    
    def analyze(self, file_path: str) -> Dict[str, Any]:
        """
        Analyse complète d'un fichier audio.
        
        Args:
            file_path: Chemin vers le fichier audio
            
        Returns:
            Dictionnaire contenant la configuration complète
        """
        print(f"🚀 Analyse audio de {file_path}")
        print("=" * 50)
        
        # Charge l'audio
        y = self.load_audio(file_path)
        
        # Analyse des features spectrales
        spectral_features = self.analyze_spectral_features(y)
        
        # Détection des effets
        has_delay, delay_params = self.detect_delay(y)
        has_reverb, reverb_params = self.detect_reverb(y)
        has_modulation, mod_params = self.detect_modulation(y)
        has_distortion, distortion_params = self.detect_distortion(y)
        
        # Mapping vers paramètres Magicstomp
        amp_config = self.map_to_amp_settings(spectral_features, has_distortion, distortion_params)
        booster_config = self.map_to_booster(spectral_features, has_distortion)
        
        # Construction du patch final
        patch = {
            "amp": amp_config,
            "booster": booster_config,
            "delay": {
                "enabled": has_delay,
                **delay_params
            },
            "reverb": {
                "enabled": has_reverb,
                **reverb_params
            },
            "mod": {
                "enabled": has_modulation,
                **mod_params
            }
        }
        
        # Calcul du score de confiance global
        confidence_scores = [
            delay_params.get('confidence', 0),
            reverb_params.get('confidence', 0),
            mod_params.get('confidence', 0),
            distortion_params.get('confidence', 0)
        ]
        global_confidence = np.mean([score for score in confidence_scores if score > 0])
        
        patch["meta"] = {
            "global_confidence": global_confidence,
            "analysis_version": "1.0",
            "input_file": Path(file_path).name
        }
        
        print("\n" + "=" * 50)
        print(f"✅ Analyse terminée - Confiance globale: {global_confidence:.2f}")
        
        return patch


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(
        description="Analyse audio et génère un patch JSON Magicstomp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python analyze2json.py guitar.wav
  python analyze2json.py guitar.wav --output my_patch.json --verbose
        """
    )
    
    parser.add_argument('input', help='Fichier audio à analyser')
    parser.add_argument('--output', '-o', help='Fichier JSON de sortie')
    parser.add_argument('--verbose', '-v', action='store_true', help='Mode verbeux')
    
    args = parser.parse_args()
    
    # Vérifie que le fichier d'entrée existe
    if not Path(args.input).exists():
        print(f"❌ Erreur: Le fichier {args.input} n'existe pas")
        sys.exit(1)
    
    # Analyse
    analyzer = AudioAnalyzer()
    patch = analyzer.analyze(args.input)
    
    # Détermine le fichier de sortie
    output_file = args.output
    if not output_file:
        input_path = Path(args.input)
        output_file = input_path.with_suffix('.json')
    
    # Sauvegarde
    print(f"\n💾 Sauvegarde vers {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(patch, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Patch sauvegardé: {output_file}")
    
    if args.verbose:
        print("\n📋 Configuration générée:")
        print(json.dumps(patch, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
