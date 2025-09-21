#!/usr/bin/env python3
"""
Perceptual Loss Functions
========================

Implements perceptual loss functions for audio comparison:
- Log-mel spectrogram L2 loss (weighted 0.6)
- MFCC L2 loss (weighted 0.4)

Used to compare target audio with Magicstomp processed audio
in Hardware-in-the-Loop optimization.
"""

import numpy as np
import librosa
import logging
from typing import Tuple, Optional
from scipy import signal


class PerceptualLoss:
    """
    Perceptual loss calculator for audio comparison.
    
    Combines log-mel spectrogram and MFCC features to compute
    perceptually meaningful distance between audio signals.
    """
    
    def __init__(self, sample_rate: int = 44100, 
                 n_mels: int = 64, n_mfcc: int = 20,
                 fmax: int = 8000):
        """
        Initialize perceptual loss calculator.
        
        Args:
            sample_rate: Audio sample rate
            n_mels: Number of mel frequency bins
            n_mfcc: Number of MFCC coefficients
            fmax: Maximum frequency for mel spectrogram
        """
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_mfcc = n_mfcc
        self.fmax = fmax
        
        # Loss weights
        self.mel_weight = 0.6
        self.mfcc_weight = 0.4
        
        self.logger = logging.getLogger(__name__)
        
        # Pre-compute mel filter bank
        self.mel_basis = librosa.filters.mel(
            sr=sample_rate,
            n_fft=2048,
            n_mels=n_mels,
            fmax=fmax
        )
    
    def extract_features(self, audio: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract log-mel and MFCC features from audio.
        
        Args:
            audio: Input audio signal
            
        Returns:
            Tuple of (log_mel, mfcc) features
        """
        # Ensure mono
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        # Compute STFT
        stft = librosa.stft(audio, n_fft=2048, hop_length=512)
        magnitude = np.abs(stft)
        
        # Log-mel spectrogram
        mel_spec = np.dot(self.mel_basis, magnitude)
        log_mel = np.log(mel_spec + 1e-10)  # Add small epsilon for numerical stability
        
        # MFCC
        mfcc = librosa.feature.mfcc(
            S=mel_spec,
            n_mfcc=self.n_mfcc,
            sr=self.sample_rate
        )
        
        return log_mel, mfcc
    
    def compute_loss(self, target_audio: np.ndarray, 
                    processed_audio: np.ndarray,
                    align_signals: bool = True) -> float:
        """
        Compute perceptual loss between target and processed audio.
        
        Args:
            target_audio: Target (reference) audio signal
            processed_audio: Processed (Magicstomp) audio signal
            align_signals: Whether to align signals before comparison
            
        Returns:
            Perceptual loss value (lower is better)
        """
        # Align signals if requested
        if align_signals:
            target_audio, processed_audio = self._align_signals(target_audio, processed_audio)
        
        # Extract features
        target_log_mel, target_mfcc = self.extract_features(target_audio)
        processed_log_mel, processed_mfcc = self.extract_features(processed_audio)
        
        # Compute L2 losses
        mel_loss = self._compute_l2_loss(target_log_mel, processed_log_mel)
        mfcc_loss = self._compute_l2_loss(target_mfcc, processed_mfcc)
        
        # Weighted combination
        total_loss = self.mel_weight * mel_loss + self.mfcc_weight * mfcc_loss
        
        self.logger.debug(f"Loss components: mel={mel_loss:.6f}, mfcc={mfcc_loss:.6f}, total={total_loss:.6f}")
        
        return total_loss
    
    def _compute_l2_loss(self, target: np.ndarray, processed: np.ndarray) -> float:
        """
        Compute L2 loss between feature matrices.
        
        Args:
            target: Target features
            processed: Processed features
            
        Returns:
            L2 loss value
        """
        # Ensure same dimensions
        min_frames = min(target.shape[1], processed.shape[1])
        target = target[:, :min_frames]
        processed = processed[:, :min_frames]
        
        # Compute L2 loss
        diff = target - processed
        l2_loss = np.mean(diff ** 2)
        
        return float(l2_loss)
    
    def _align_signals(self, target: np.ndarray, processed: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Align two audio signals using cross-correlation.
        
        Args:
            target: Target audio signal
            processed: Processed audio signal
            
        Returns:
            Tuple of aligned signals
        """
        # Ensure same length
        min_length = min(len(target), len(processed))
        target = target[:min_length]
        processed = processed[:min_length]
        
        # Cross-correlation
        correlation = signal.correlate(processed, target, mode='full')
        
        # Find best alignment
        best_lag = np.argmax(np.abs(correlation)) - (len(processed) - 1)
        
        # Apply alignment
        if best_lag > 0:
            # Processed is delayed, trim target
            target = target[best_lag:]
            processed = processed[:len(target)]
        elif best_lag < 0:
            # Target is delayed, trim processed
            processed = processed[-best_lag:]
            target = target[:len(processed)]
        
        return target, processed
    
    def compute_detailed_loss(self, target_audio: np.ndarray,
                            processed_audio: np.ndarray) -> dict:
        """
        Compute detailed loss breakdown for analysis.
        
        Args:
            target_audio: Target audio signal
            processed_audio: Processed audio signal
            
        Returns:
            Dictionary with detailed loss components
        """
        # Align signals
        target_aligned, processed_aligned = self._align_signals(target_audio, processed_audio)
        
        # Extract features
        target_log_mel, target_mfcc = self.extract_features(target_aligned)
        processed_log_mel, processed_mfcc = self.extract_features(processed_aligned)
        
        # Compute individual losses
        mel_loss = self._compute_l2_loss(target_log_mel, processed_log_mel)
        mfcc_loss = self._compute_l2_loss(target_mfcc, processed_mfcc)
        
        # Weighted total
        total_loss = self.mel_weight * mel_loss + self.mfcc_weight * mfcc_loss
        
        return {
            'total_loss': total_loss,
            'mel_loss': mel_loss,
            'mfcc_loss': mfcc_loss,
            'mel_weight': self.mel_weight,
            'mfcc_weight': self.mfcc_weight,
            'target_length': len(target_aligned),
            'processed_length': len(processed_aligned),
            'alignment_applied': True
        }


class SpectralLoss:
    """
    Additional spectral loss functions for audio comparison.
    
    Provides alternative loss functions that might be useful
    for specific optimization scenarios.
    """
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize spectral loss calculator.
        
        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        self.logger = logging.getLogger(__name__)
    
    def compute_spectral_centroid_loss(self, target: np.ndarray, processed: np.ndarray) -> float:
        """
        Compute loss based on spectral centroid difference.
        
        Args:
            target: Target audio signal
            processed: Processed audio signal
            
        Returns:
            Spectral centroid loss
        """
        target_centroid = librosa.feature.spectral_centroid(y=target, sr=self.sample_rate)
        processed_centroid = librosa.feature.spectral_centroid(y=processed, sr=self.sample_rate)
        
        centroid_diff = np.mean(np.abs(target_centroid - processed_centroid))
        normalized_loss = centroid_diff / self.sample_rate  # Normalize by Nyquist
        
        return float(normalized_loss)
    
    def compute_spectral_rolloff_loss(self, target: np.ndarray, processed: np.ndarray) -> float:
        """
        Compute loss based on spectral rolloff difference.
        
        Args:
            target: Target audio signal
            processed: Processed audio signal
            
        Returns:
            Spectral rolloff loss
        """
        target_rolloff = librosa.feature.spectral_rolloff(y=target, sr=self.sample_rate)
        processed_rolloff = librosa.feature.spectral_rolloff(y=processed, sr=self.sample_rate)
        
        rolloff_diff = np.mean(np.abs(target_rolloff - processed_rolloff))
        normalized_loss = rolloff_diff / self.sample_rate  # Normalize by Nyquist
        
        return float(normalized_loss)
    
    def compute_zero_crossing_loss(self, target: np.ndarray, processed: np.ndarray) -> float:
        """
        Compute loss based on zero crossing rate difference.
        
        Args:
            target: Target audio signal
            processed: Processed audio signal
            
        Returns:
            Zero crossing rate loss
        """
        target_zcr = librosa.feature.zero_crossing_rate(target)
        processed_zcr = librosa.feature.zero_crossing_rate(processed)
        
        zcr_diff = np.mean(np.abs(target_zcr - processed_zcr))
        
        return float(zcr_diff)


def demo_loss_calculation():
    """Demo function to test loss calculation."""
    import soundfile as sf
    
    # Create synthetic test signals
    sample_rate = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Target signal (clean sine wave)
    target = np.sin(2 * np.pi * 440 * t)
    
    # Processed signal (slightly distorted)
    processed = np.tanh(target * 1.5) * 0.8
    
    # Compute loss
    loss_calculator = PerceptualLoss(sample_rate)
    loss = loss_calculator.compute_loss(target, processed)
    
    print(f"Perceptual loss: {loss:.6f}")
    
    # Detailed breakdown
    details = loss_calculator.compute_detailed_loss(target, processed)
    print(f"Detailed loss: {details}")


if __name__ == "__main__":
    demo_loss_calculation()
