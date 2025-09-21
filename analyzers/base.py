#!/usr/bin/env python3
"""
Base Audio Analyzer Interface
============================

Defines the abstract interface for audio analysis backends.
All concrete implementations must provide these methods with consistent
numeric ranges and semantics.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any
import logging


class AudioAnalyzer(ABC):
    """
    Abstract base class for audio analysis backends.
    
    All methods must return consistent numeric ranges across implementations.
    Methods should not raise exceptions for impossible features - instead
    return sensible defaults and log warnings.
    """
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the analyzer.
        
        Args:
            sample_rate: Target sample rate for analysis
        """
        self.sample_rate = sample_rate
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def load_audio(self, path: str, sr: Optional[int] = None) -> Tuple[Any, int]:
        """
        Load audio file and return normalized mono signal.
        
        Args:
            path: Path to audio file
            sr: Target sample rate (defaults to self.sample_rate)
            
        Returns:
            Tuple of (audio_data, actual_sample_rate)
            
        Note:
            Audio should be normalized to [-1, 1] range, mono.
        """
        pass
    
    @abstractmethod
    def spectral_tilt_db(self, y: Any, sr: int) -> float:
        """
        Calculate spectral tilt in dB (brightness indicator).
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Spectral tilt in dB (positive = bright, negative = dark)
            
        Heuristic:
            High-frequency vs low-frequency energy ratio.
            Used for amplifier model selection.
        """
        pass
    
    @abstractmethod
    def spectral_centroid_mean(self, y: Any, sr: int) -> float:
        """
        Calculate mean spectral centroid in Hz.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Mean spectral centroid in Hz
            
        Heuristic:
            "Center of mass" of the spectrum.
            Used for EQ settings (treble/bass balance).
        """
        pass
    
    @abstractmethod
    def thd_proxy(self, y: Any, sr: int) -> float:
        """
        Calculate Total Harmonic Distortion proxy.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            THD proxy (0.0 = clean, 1.0+ = highly distorted)
            
        Heuristic:
            Ratio of harmonic energy to fundamental energy.
            Used for drive/gain settings.
        """
        pass
    
    @abstractmethod
    def onset_delay_ms(self, y: Any, sr: int) -> Tuple[float, float]:
        """
        Detect delay time and feedback from onset autocorrelation.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (delay_time_ms, feedback_estimate)
            
        Heuristic:
            Autocorrelation of onset envelope to find periodic repetitions.
            Used for delay effect detection and parameter mapping.
        """
        pass
    
    @abstractmethod
    def reverb_estimate(self, y: Any, sr: int) -> Tuple[float, float]:
        """
        Estimate reverb decay time and mix level.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (decay_time_seconds, mix_level)
            
        Heuristic:
            Analysis of reverberation tail and spectral density.
            Used for reverb effect detection and parameter mapping.
        """
        pass
    
    @abstractmethod
    def lfo_rate_hz(self, y: Any, sr: int) -> Tuple[Optional[float], float]:
        """
        Detect LFO rate and strength from amplitude modulation.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tuple of (lfo_rate_hz, modulation_strength)
            lfo_rate_hz is None if no significant modulation detected
            
        Heuristic:
            FFT of amplitude envelope in 0.2-6 Hz band.
            Used for chorus/phaser/tremolo detection.
        """
        pass
    
    @abstractmethod
    def tempo_bpm(self, y: Any, sr: int) -> Optional[float]:
        """
        Estimate tempo in beats per minute.
        
        Args:
            y: Audio signal
            sr: Sample rate
            
        Returns:
            Tempo in BPM, or None if tempo cannot be determined
            
        Heuristic:
            Rhythm extraction from onset patterns.
            Used for tempo-synced effects (delay, modulation).
        """
        pass
    
    def analyze(self, path: str) -> Dict[str, Any]:
        """
        Perform complete audio analysis.
        
        Args:
            path: Path to audio file
            
        Returns:
            Dictionary containing all extracted features
            
        Note:
            This is a convenience method that calls all individual
            feature extraction methods and combines results.
        """
        self.logger.info(f"Analyzing audio: {path}")
        
        # Load audio
        y, sr = self.load_audio(path)
        
        # Extract features
        features = {
            'spectral_tilt_db': self.spectral_tilt_db(y, sr),
            'spectral_centroid_mean': self.spectral_centroid_mean(y, sr),
            'thd_proxy': self.thd_proxy(y, sr),
            'onset_delay_ms': self.onset_delay_ms(y, sr),
            'reverb_estimate': self.reverb_estimate(y, sr),
            'lfo_rate_hz': self.lfo_rate_hz(y, sr),
            'tempo_bpm': self.tempo_bpm(y, sr),
            'sample_rate': sr,
            'duration_s': len(y) / sr if hasattr(y, '__len__') else 0
        }
        
        self.logger.info("Analysis complete")
        return features
    
    def get_backend_name(self) -> str:
        """
        Return the name of this backend implementation.
        
        Returns:
            Backend name string
        """
        return self.__class__.__name__.replace('Analyzer', '').lower()
