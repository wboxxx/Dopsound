#!/usr/bin/env python3
"""
Librosa Audio Analyzer Backend
==============================

Pure Python implementation using librosa for audio analysis.
Adapts the existing analysis logic from analyze2json.py to fit the
new interface.
"""

import librosa
import numpy as np
from scipy import signal
from scipy.stats import kurtosis
from typing import Tuple, Optional, Any
import logging

from .base import AudioAnalyzer


class LibrosaAnalyzer(AudioAnalyzer):
    """
    Librosa-based audio analyzer implementation.
    
    Uses librosa for spectral analysis, onset detection, and feature extraction.
    This is the pure Python backend that should always be available.
    """
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize Librosa analyzer.
        
        Args:
            sample_rate: Target sample rate for analysis
        """
        super().__init__(sample_rate)
        self.logger.info("Initialized Librosa backend")
    
    def load_audio(self, path: str, sr: Optional[int] = None) -> Tuple[np.ndarray, int]:
        """
        Load audio file using librosa.
        
        Args:
            path: Path to audio file
            sr: Target sample rate (defaults to self.sample_rate)
            
        Returns:
            Tuple of (audio_data, actual_sample_rate)
        """
        if sr is None:
            sr = self.sample_rate
            
        # Load audio and normalize
        y, actual_sr = librosa.load(path, sr=sr, mono=True)
        
        # Normalization RMS
        rms = np.sqrt(np.mean(y**2))
        if rms > 0:
            y = y / rms * 0.7  # Normalize to 70% for safety
        
        self.logger.debug(f"Loaded audio: {len(y)} samples, {actual_sr}Hz, RMS={rms:.3f}")
        return y, actual_sr
    
    def spectral_tilt_db(self, y: np.ndarray, sr: int) -> float:
        """
        Calculate spectral tilt using high/low frequency energy ratio.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Spectral tilt in dB
        """
        # Compute STFT
        stft = librosa.stft(y)
        magnitude = np.abs(stft)
        
        # Frequency bins
        freqs = librosa.fft_frequencies(sr=sr)
        
        # Define frequency bands
        low_freq_mask = freqs < 1000
        high_freq_mask = freqs > 4000
        
        # Calculate energy in each band
        low_energy = np.sum(magnitude[low_freq_mask, :])
        high_energy = np.sum(magnitude[high_freq_mask, :])
        
        # Avoid division by zero
        if low_energy == 0:
            return 0.0
        
        # Convert to dB
        tilt_db = 20 * np.log10((high_energy + 1e-10) / (low_energy + 1e-10))
        
        self.logger.debug(f"Spectral tilt: {tilt_db:.2f} dB")
        return float(tilt_db)
    
    def spectral_centroid_mean(self, y: np.ndarray, sr: int) -> float:
        """
        Calculate mean spectral centroid.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Mean spectral centroid in Hz
        """
        # Compute spectral centroid
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        mean_centroid = np.mean(centroid)
        
        self.logger.debug(f"Spectral centroid: {mean_centroid:.1f} Hz")
        return float(mean_centroid)
    
    def thd_proxy(self, y: np.ndarray, sr: int) -> float:
        """
        Calculate THD proxy using harmonic analysis.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            THD proxy (0.0 = clean, 1.0+ = distorted)
        """
        # FFT analysis
        fft = np.fft.fft(y)
        freqs = np.fft.fftfreq(len(fft), 1/sr)
        
        # Find fundamental frequency
        magnitude = np.abs(fft)
        fundamental_idx = np.argmax(magnitude[1:len(magnitude)//2]) + 1
        fundamental_freq = freqs[fundamental_idx]
        
        if fundamental_freq <= 0:
            return 0.0
        
        # Calculate harmonic energy
        harmonic_energy = 0
        fundamental_energy = magnitude[fundamental_idx]
        
        # Sum harmonics 2-8
        for harmonic in range(2, 9):
            harmonic_idx = int(fundamental_idx * harmonic)
            if harmonic_idx < len(magnitude):
                harmonic_energy += magnitude[harmonic_idx]
        
        # Calculate THD proxy
        if fundamental_energy > 0:
            thd_proxy = harmonic_energy / fundamental_energy
        else:
            thd_proxy = 0.0
        
        # Also consider clipping as distortion indicator
        clipped_samples = np.sum(np.abs(y) > 0.95)
        clipping_ratio = clipped_samples / len(y)
        
        # Combine THD and clipping
        total_distortion = thd_proxy + clipping_ratio * 2.0
        
        self.logger.debug(f"THD proxy: {thd_proxy:.3f}, clipping: {clipping_ratio:.3f}, total: {total_distortion:.3f}")
        return float(total_distortion)
    
    def onset_delay_ms(self, y: np.ndarray, sr: int) -> Tuple[float, float]:
        """
        Detect delay using onset envelope autocorrelation.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (delay_time_ms, feedback_estimate)
        """
        # Compute onset strength
        onset_strength = librosa.onset.onset_strength(y=y, sr=sr)
        
        # Autocorrelation of onset envelope
        autocorr = np.correlate(onset_strength, onset_strength, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Normalize
        if np.max(autocorr) > 0:
            autocorr = autocorr / np.max(autocorr)
        
        # Search for peaks after minimum delay (10ms)
        min_delay_samples = int(0.01 * sr)
        search_window = autocorr[min_delay_samples:min(len(autocorr), int(2.0 * sr))]
        
        # Find peaks
        peaks, properties = signal.find_peaks(search_window, height=0.3, distance=100)
        
        if len(peaks) > 0:
            # Take strongest peak
            best_peak_idx = peaks[np.argmax(search_window[peaks])]
            delay_samples = best_peak_idx + min_delay_samples
            delay_time_ms = delay_samples * 1000 / sr
            
            # Estimate feedback from peak amplitude
            feedback = min(0.8, search_window[best_peak_idx] * 1.5)
            
            self.logger.debug(f"Delay detected: {delay_time_ms:.0f}ms, feedback: {feedback:.2f}")
            return float(delay_time_ms), float(feedback)
        else:
            self.logger.debug("No delay detected")
            return 0.0, 0.0
    
    def reverb_estimate(self, y: np.ndarray, sr: int) -> Tuple[float, float]:
        """
        Estimate reverb using decay analysis and spectral density.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (decay_time_seconds, mix_level)
        """
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
        
        # Spectral analysis for reverb coloration
        stft = librosa.stft(y)
        magnitude = np.abs(stft)
        
        # High frequency energy ratio
        freqs = librosa.fft_frequencies(sr=sr)
        high_freq_mask = freqs > 3000
        high_freq_energy = np.mean(magnitude[high_freq_mask, :])
        total_energy = np.mean(magnitude)
        
        if total_energy > 0:
            high_freq_ratio = high_freq_energy / total_energy
        else:
            high_freq_ratio = 0
        
        # Detect reverb presence
        has_reverb = decay_time_s > 0.8 and high_freq_ratio > 0.1
        
        if has_reverb:
            # Estimate mix level
            mix = min(0.3, high_freq_ratio * 2.0)
            
            self.logger.debug(f"Reverb detected: decay={decay_time_s:.1f}s, mix={mix:.2f}")
            return float(decay_time_s), float(mix)
        else:
            self.logger.debug("No reverb detected")
            return 0.0, 0.0
    
    def lfo_rate_hz(self, y: np.ndarray, sr: int) -> Tuple[Optional[float], float]:
        """
        Detect LFO rate from amplitude modulation.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (lfo_rate_hz, modulation_strength)
        """
        # Amplitude envelope
        envelope = np.abs(y)
        
        # Downsample envelope to ~40 Hz for LFO analysis
        downsample_factor = max(1, sr // 40)
        downsampled_envelope = envelope[::downsample_factor]
        
        # Low-pass filter to isolate modulation
        nyquist = sr / downsample_factor / 2
        low_freq = 8 / nyquist  # 8 Hz cutoff
        if low_freq < 1.0:
            b, a = signal.butter(4, low_freq, btype='low')
            filtered_envelope = signal.filtfilt(b, a, downsampled_envelope)
        else:
            filtered_envelope = downsampled_envelope
        
        # FFT of modulation
        mod_fft = np.fft.fft(filtered_envelope)
        freqs = np.fft.fftfreq(len(mod_fft), downsample_factor/sr)
        
        # Search in LFO band (0.2-6 Hz)
        lfo_mask = (freqs >= 0.2) & (freqs <= 6.0)
        mod_spectrum = np.abs(mod_fft[lfo_mask])
        mod_freqs = freqs[lfo_mask]
        
        if len(mod_spectrum) > 0:
            # Find strongest modulation
            peak_idx = np.argmax(mod_spectrum)
            lfo_rate = mod_freqs[peak_idx]
            modulation_strength = mod_spectrum[peak_idx] / np.sum(mod_spectrum)
            
            # Threshold for significance
            if modulation_strength > 0.1 and lfo_rate > 0.2:
                self.logger.debug(f"LFO detected: {lfo_rate:.2f}Hz, strength: {modulation_strength:.2f}")
                return float(lfo_rate), float(modulation_strength)
        
        self.logger.debug("No LFO detected")
        return None, 0.0
    
    def tempo_bpm(self, y: np.ndarray, sr: int) -> Optional[float]:
        """
        Estimate tempo using librosa's tempo detection.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tempo in BPM, or None if cannot be determined
        """
        try:
            # Use librosa's tempo detection
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            if tempo > 0:
                self.logger.debug(f"Tempo detected: {tempo:.1f} BPM")
                return float(tempo)
            else:
                self.logger.debug("No tempo detected")
                return None
                
        except Exception as e:
            self.logger.warning(f"Tempo detection failed: {e}")
            return None
