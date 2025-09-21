#!/usr/bin/env python3
"""
Essentia Audio Analyzer Backend
===============================

C++ core implementation using Essentia for high-performance audio analysis.
Provides the same interface as LibrosaAnalyzer but with optimized algorithms.
"""

import numpy as np
from typing import Tuple, Optional, Any
import logging

from .base import AudioAnalyzer

# Try to import Essentia, mark as unavailable if import fails
try:
    import essentia
    import essentia.standard as es
    # Test if Essentia is actually functional
    _ = essentia.__version__
    ESSENTIA_AVAILABLE = True
except (ImportError, AttributeError, Exception):
    ESSENTIA_AVAILABLE = False
    es = None


class EssentiaAnalyzer(AudioAnalyzer):
    """
    Essentia-based audio analyzer implementation.
    
    Uses Essentia's C++ algorithms for high-performance audio analysis.
    Falls back gracefully if Essentia is not available.
    """
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize Essentia analyzer.
        
        Args:
            sample_rate: Target sample rate for analysis
        """
        super().__init__(sample_rate)
        
        if not ESSENTIA_AVAILABLE:
            self.logger.warning("Essentia not available - backend will not function properly")
            return
        
        self.logger.info("Initialized Essentia backend")
        
        # Initialize Essentia algorithms
        self.mono_loader = es.MonoLoader(sampleRate=sample_rate, normalize=True)
        self.spectrum = es.Spectrum()
        self.centroid = es.Centroid()
        self.spectral_peaks = es.SpectralPeaks()
        self.onset_detection = es.OnsetDetection()
        self.onsets = es.Onsets()
        self.rhythm_extractor = es.RhythmExtractor2013()
        
        # Window and hop sizes
        self.frame_size = 2048
        self.hop_size = 512
        self.windowing = es.Windowing(type='hann')
    
    def load_audio(self, path: str, sr: Optional[int] = None) -> Tuple[np.ndarray, int]:
        """
        Load audio file using Essentia's MonoLoader.
        
        Args:
            path: Path to audio file
            sr: Target sample rate (defaults to self.sample_rate)
            
        Returns:
            Tuple of (audio_data, actual_sample_rate)
        """
        if not ESSENTIA_AVAILABLE:
            raise RuntimeError("Essentia not available")
        
        if sr is not None and sr != self.sample_rate:
            # Create loader with custom sample rate
            loader = es.MonoLoader(filename=path, sampleRate=sr, normalize=True)
            audio = loader()
            actual_sr = sr
        else:
            # Use default sample rate
            self.mono_loader.parameter('filename').setValue(path)
            audio = self.mono_loader()
            actual_sr = self.sample_rate
        
        # Convert to numpy array
        audio_array = np.array(audio)
        
        self.logger.debug(f"Loaded audio: {len(audio_array)} samples, {actual_sr}Hz")
        return audio_array, actual_sr
    
    def spectral_tilt_db(self, y: np.ndarray, sr: int) -> float:
        """
        Calculate spectral tilt using Essentia's spectral analysis.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Spectral tilt in dB
        """
        if not ESSENTIA_AVAILABLE:
            self.logger.warning("Essentia not available - returning default spectral tilt")
            return 0.0
        
        try:
            # Convert to Essentia vector
            audio_vector = essentia.array(y)
            
            # Compute spectrum
            spectrum = self.spectrum(audio_vector)
            
            # Define frequency bins
            freqs = np.linspace(0, sr/2, len(spectrum))
            
            # Calculate energy in frequency bands
            low_mask = freqs < 1000
            high_mask = freqs > 4000
            
            low_energy = np.sum(spectrum[low_mask])
            high_energy = np.sum(spectrum[high_mask])
            
            # Convert to dB
            if low_energy > 0:
                tilt_db = 20 * np.log10((high_energy + 1e-10) / (low_energy + 1e-10))
            else:
                tilt_db = 0.0
            
            self.logger.debug(f"Spectral tilt: {tilt_db:.2f} dB")
            return float(tilt_db)
            
        except Exception as e:
            self.logger.warning(f"Spectral tilt calculation failed: {e}")
            return 0.0
    
    def spectral_centroid_mean(self, y: np.ndarray, sr: int) -> float:
        """
        Calculate mean spectral centroid using Essentia.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Mean spectral centroid in Hz
        """
        if not ESSENTIA_AVAILABLE:
            self.logger.warning("Essentia not available - returning default centroid")
            return 2000.0
        
        try:
            # Convert to Essentia vector
            audio_vector = essentia.array(y)
            
            # Compute spectrum
            spectrum = self.spectrum(audio_vector)
            
            # Calculate centroid
            centroid = self.centroid(spectrum)
            
            self.logger.debug(f"Spectral centroid: {centroid:.1f} Hz")
            return float(centroid)
            
        except Exception as e:
            self.logger.warning(f"Spectral centroid calculation failed: {e}")
            return 2000.0
    
    def thd_proxy(self, y: np.ndarray, sr: int) -> float:
        """
        Calculate THD proxy using Essentia's spectral peak analysis.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            THD proxy (0.0 = clean, 1.0+ = distorted)
        """
        if not ESSENTIA_AVAILABLE:
            self.logger.warning("Essentia not available - returning default THD")
            return 0.0
        
        try:
            # Convert to Essentia vector
            audio_vector = essentia.array(y)
            
            # Compute spectrum and peaks
            spectrum = self.spectrum(audio_vector)
            freqs, magnitudes = self.spectral_peaks(spectrum)
            
            if len(freqs) == 0:
                return 0.0
            
            # Find fundamental (strongest peak)
            fundamental_idx = np.argmax(magnitudes)
            fundamental_freq = freqs[fundamental_idx]
            fundamental_mag = magnitudes[fundamental_idx]
            
            # Calculate harmonic energy
            harmonic_energy = 0
            tolerance = 0.05  # 5% frequency tolerance
            
            for harmonic in range(2, 9):
                target_freq = fundamental_freq * harmonic
                
                # Find closest peak to harmonic frequency
                for i, freq in enumerate(freqs):
                    if abs(freq - target_freq) / target_freq < tolerance:
                        harmonic_energy += magnitudes[i]
                        break
            
            # Calculate THD proxy
            if fundamental_mag > 0:
                thd_proxy = harmonic_energy / fundamental_mag
            else:
                thd_proxy = 0.0
            
            # Also consider clipping
            clipped_samples = np.sum(np.abs(y) > 0.95)
            clipping_ratio = clipped_samples / len(y)
            
            total_distortion = thd_proxy + clipping_ratio * 2.0
            
            self.logger.debug(f"THD proxy: {thd_proxy:.3f}, clipping: {clipping_ratio:.3f}, total: {total_distortion:.3f}")
            return float(total_distortion)
            
        except Exception as e:
            self.logger.warning(f"THD calculation failed: {e}")
            return 0.0
    
    def onset_delay_ms(self, y: np.ndarray, sr: int) -> Tuple[float, float]:
        """
        Detect delay using Essentia's onset detection and autocorrelation.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (delay_time_ms, feedback_estimate)
        """
        if not ESSENTIA_AVAILABLE:
            self.logger.warning("Essentia not available - returning default delay")
            return 0.0, 0.0
        
        try:
            # Convert to Essentia vector
            audio_vector = essentia.array(y)
            
            # Frame the audio
            frames = []
            for i in range(0, len(audio_vector) - self.frame_size, self.hop_size):
                frame = audio_vector[i:i + self.frame_size]
                windowed_frame = self.windowing(frame)
                frames.append(windowed_frame)
            
            if not frames:
                return 0.0, 0.0
            
            # Compute onset strength for each frame
            onset_strengths = []
            for frame in frames:
                spectrum = self.spectrum(frame)
                onset_strength = self.onset_detection(spectrum)
                onset_strengths.append(onset_strength)
            
            onset_envelope = np.array(onset_strengths)
            
            # Autocorrelation
            autocorr = np.correlate(onset_envelope, onset_envelope, mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            
            # Normalize
            if np.max(autocorr) > 0:
                autocorr = autocorr / np.max(autocorr)
            
            # Search for delay peaks
            min_delay_frames = int(0.01 * sr / self.hop_size)  # 10ms minimum
            max_delay_frames = int(2.0 * sr / self.hop_size)   # 2s maximum
            
            search_window = autocorr[min_delay_frames:min(len(autocorr), max_delay_frames)]
            
            # Find peaks
            from scipy import signal
            peaks, properties = signal.find_peaks(search_window, height=0.3, distance=10)
            
            if len(peaks) > 0:
                # Take strongest peak
                best_peak_idx = peaks[np.argmax(search_window[peaks])]
                delay_frames = best_peak_idx + min_delay_frames
                delay_time_ms = delay_frames * self.hop_size * 1000 / sr
                
                # Estimate feedback
                feedback = min(0.8, search_window[best_peak_idx] * 1.5)
                
                self.logger.debug(f"Delay detected: {delay_time_ms:.0f}ms, feedback: {feedback:.2f}")
                return float(delay_time_ms), float(feedback)
            else:
                self.logger.debug("No delay detected")
                return 0.0, 0.0
                
        except Exception as e:
            self.logger.warning(f"Delay detection failed: {e}")
            return 0.0, 0.0
    
    def reverb_estimate(self, y: np.ndarray, sr: int) -> Tuple[float, float]:
        """
        Estimate reverb using Essentia's spectral analysis.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (decay_time_seconds, mix_level)
        """
        if not ESSENTIA_AVAILABLE:
            self.logger.warning("Essentia not available - returning default reverb")
            return 0.0, 0.0
        
        try:
            # Convert to Essentia vector
            audio_vector = essentia.array(y)
            
            # Analyze decay envelope
            envelope = np.abs(y)
            max_envelope = np.max(envelope)
            threshold = max_envelope * 0.1
            
            # Find decay time
            above_threshold = envelope > threshold
            if np.any(above_threshold):
                last_above = np.where(above_threshold)[0][-1]
                decay_time_s = last_above / sr
            else:
                decay_time_s = 0.5
            
            # Spectral analysis for reverb detection
            spectrum = self.spectrum(audio_vector)
            freqs = np.linspace(0, sr/2, len(spectrum))
            
            # High frequency energy ratio
            high_freq_mask = freqs > 3000
            high_freq_energy = np.sum(spectrum[high_freq_mask])
            total_energy = np.sum(spectrum)
            
            if total_energy > 0:
                high_freq_ratio = high_freq_energy / total_energy
            else:
                high_freq_ratio = 0
            
            # Detect reverb
            has_reverb = decay_time_s > 0.8 and high_freq_ratio > 0.1
            
            if has_reverb:
                mix = min(0.3, high_freq_ratio * 2.0)
                self.logger.debug(f"Reverb detected: decay={decay_time_s:.1f}s, mix={mix:.2f}")
                return float(decay_time_s), float(mix)
            else:
                self.logger.debug("No reverb detected")
                return 0.0, 0.0
                
        except Exception as e:
            self.logger.warning(f"Reverb estimation failed: {e}")
            return 0.0, 0.0
    
    def lfo_rate_hz(self, y: np.ndarray, sr: int) -> Tuple[Optional[float], float]:
        """
        Detect LFO rate using Essentia's envelope analysis.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (lfo_rate_hz, modulation_strength)
        """
        if not ESSENTIA_AVAILABLE:
            self.logger.warning("Essentia not available - returning default LFO")
            return None, 0.0
        
        try:
            # Convert to Essentia vector
            audio_vector = essentia.array(y)
            
            # Downsample for LFO analysis
            downsample_factor = max(1, sr // 40)
            downsampled_audio = audio_vector[::downsample_factor]
            
            # Compute envelope
            envelope = np.abs(downsampled_audio)
            
            # Low-pass filter for modulation
            from scipy import signal
            nyquist = sr / downsample_factor / 2
            low_freq = 8 / nyquist
            if low_freq < 1.0:
                b, a = signal.butter(4, low_freq, btype='low')
                filtered_envelope = signal.filtfilt(b, a, envelope)
            else:
                filtered_envelope = envelope
            
            # FFT analysis
            mod_fft = np.fft.fft(filtered_envelope)
            freqs = np.fft.fftfreq(len(mod_fft), downsample_factor/sr)
            
            # Search in LFO band
            lfo_mask = (freqs >= 0.2) & (freqs <= 6.0)
            mod_spectrum = np.abs(mod_fft[lfo_mask])
            mod_freqs = freqs[lfo_mask]
            
            if len(mod_spectrum) > 0:
                peak_idx = np.argmax(mod_spectrum)
                lfo_rate = mod_freqs[peak_idx]
                modulation_strength = mod_spectrum[peak_idx] / np.sum(mod_spectrum)
                
                if modulation_strength > 0.1 and lfo_rate > 0.2:
                    self.logger.debug(f"LFO detected: {lfo_rate:.2f}Hz, strength: {modulation_strength:.2f}")
                    return float(lfo_rate), float(modulation_strength)
            
            self.logger.debug("No LFO detected")
            return None, 0.0
            
        except Exception as e:
            self.logger.warning(f"LFO detection failed: {e}")
            return None, 0.0
    
    def tempo_bpm(self, y: np.ndarray, sr: int) -> Optional[float]:
        """
        Estimate tempo using Essentia's RhythmExtractor2013.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tempo in BPM, or None if cannot be determined
        """
        if not ESSENTIA_AVAILABLE:
            self.logger.warning("Essentia not available - returning default tempo")
            return None
        
        try:
            # Convert to Essentia vector
            audio_vector = essentia.array(y)
            
            # Extract tempo using Essentia's rhythm extractor
            bpm, beats, beats_confidence, _, beats_intervals = self.rhythm_extractor(audio_vector)
            
            if bpm > 0:
                self.logger.debug(f"Tempo detected: {bpm:.1f} BPM")
                return float(bpm)
            else:
                self.logger.debug("No tempo detected")
                return None
                
        except Exception as e:
            self.logger.warning(f"Tempo detection failed: {e}")
            return None
