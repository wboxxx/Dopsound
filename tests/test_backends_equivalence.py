#!/usr/bin/env python3
"""
Test Backend Equivalence
=======================

Tests to ensure both backends return similar results for the same input.
Uses synthetic test signals to validate feature extraction consistency.
"""

import os
import sys
import unittest
import numpy as np
import tempfile
import soundfile as sf

# Add parent directory to path for imports
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analyzers.factory import get_available_backends, get_analyzer


class TestBackendEquivalence(unittest.TestCase):
    """Test that backends produce equivalent results."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_rate = 44100
        self.duration = 2.0
        self.tolerance = 0.1  # 10% relative tolerance
        
        # Check available backends
        self.backends = get_available_backends()
        
        # Create analyzers for available backends
        self.analyzers = {}
        
        if self.backends['librosa']:
            self.analyzers['librosa'] = get_analyzer('librosa', self.sample_rate)
        
        if self.backends['essentia']:
            self.analyzers['essentia'] = get_analyzer('essentia', self.sample_rate)
        
        # Skip tests if no backends available
        if not self.analyzers:
            self.skipTest("No backends available")
    
    def create_test_signal(self, signal_type='sine', frequency=440.0, 
                          add_noise=False, add_delay=False, add_modulation=False):
        """
        Create a test audio signal.
        
        Args:
            signal_type: Type of signal ('sine', 'impulse', 'chord')
            frequency: Fundamental frequency
            add_noise: Add white noise
            add_delay: Add delay effect
            add_modulation: Add amplitude modulation
            
        Returns:
            Tuple of (audio_data, file_path)
        """
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
        
        if signal_type == 'sine':
            # Pure sine wave
            signal = np.sin(2 * np.pi * frequency * t)
            
        elif signal_type == 'impulse':
            # Impulse train
            signal = np.zeros_like(t)
            impulse_times = np.arange(0, self.duration, 1.0/frequency)
            for impulse_time in impulse_times:
                idx = int(impulse_time * self.sample_rate)
                if idx < len(signal):
                    signal[idx] = 1.0
            
        elif signal_type == 'chord':
            # Chord with harmonics
            signal = (np.sin(2 * np.pi * frequency * t) +
                    0.5 * np.sin(2 * np.pi * frequency * 2 * t) +
                    0.3 * np.sin(2 * np.pi * frequency * 3 * t))
        
        else:
            raise ValueError(f"Unknown signal type: {signal_type}")
        
        # Add effects
        if add_delay:
            delay_samples = int(0.1 * self.sample_rate)  # 100ms delay
            delayed = np.zeros_like(signal)
            delayed[delay_samples:] = signal[:-delay_samples] * 0.3
            signal += delayed
        
        if add_modulation:
            # Add tremolo (amplitude modulation)
            tremolo_rate = 5.0  # Hz
            tremolo = 1.0 + 0.3 * np.sin(2 * np.pi * tremolo_rate * t)
            signal *= tremolo
        
        if add_noise:
            # Add white noise
            noise = np.random.randn(len(signal)) * 0.1
            signal += noise
        
        # Normalize
        signal = signal / np.max(np.abs(signal)) * 0.7
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            sf.write(f.name, signal, self.sample_rate)
            return signal, f.name
    
    def tearDown(self):
        """Clean up test files."""
        # Clean up temporary files if they exist
        pass
    
    def test_spectral_centroid_equivalence(self):
        """Test spectral centroid calculation equivalence."""
        if len(self.analyzers) < 2:
            self.skipTest("Need at least 2 backends for comparison")
        
        # Create test signal
        _, file_path = self.create_test_signal('sine', 440.0)
        
        try:
            results = {}
            for backend_name, analyzer in self.analyzers.items():
                y, sr = analyzer.load_audio(file_path)
                centroid = analyzer.spectral_centroid_mean(y, sr)
                results[backend_name] = centroid
                
                # Basic sanity check
                self.assertGreater(centroid, 0, f"{backend_name}: centroid should be positive")
                self.assertLess(centroid, sr/2, f"{backend_name}: centroid should be below Nyquist")
            
            # Compare results between backends
            backend_names = list(results.keys())
            for i in range(len(backend_names)):
                for j in range(i + 1, len(backend_names)):
                    backend1, backend2 = backend_names[i], backend_names[j]
                    centroid1, centroid2 = results[backend1], results[backend2]
                    
                    # Relative tolerance check
                    relative_diff = abs(centroid1 - centroid2) / max(centroid1, centroid2)
                    self.assertLess(relative_diff, self.tolerance,
                                  f"Spectral centroid mismatch: {backend1}={centroid1:.1f}Hz, "
                                  f"{backend2}={centroid2:.1f}Hz, diff={relative_diff:.3f}")
        
        finally:
            os.unlink(file_path)
    
    def test_spectral_tilt_equivalence(self):
        """Test spectral tilt calculation equivalence."""
        if len(self.analyzers) < 2:
            self.skipTest("Need at least 2 backends for comparison")
        
        # Create test signal with harmonics
        _, file_path = self.create_test_signal('chord', 220.0)
        
        try:
            results = {}
            for backend_name, analyzer in self.analyzers.items():
                y, sr = analyzer.load_audio(file_path)
                tilt = analyzer.spectral_tilt_db(y, sr)
                results[backend_name] = tilt
                
                # Basic sanity check
                self.assertIsInstance(tilt, (int, float), f"{backend_name}: tilt should be numeric")
            
            # Compare results between backends
            backend_names = list(results.keys())
            for i in range(len(backend_names)):
                for j in range(i + 1, len(backend_names)):
                    backend1, backend2 = backend_names[i], backend_names[j]
                    tilt1, tilt2 = results[backend1], results[backend2]
                    
                    # Absolute tolerance for spectral tilt (in dB)
                    abs_diff = abs(tilt1 - tilt2)
                    self.assertLess(abs_diff, 3.0,  # 3 dB tolerance
                                  f"Spectral tilt mismatch: {backend1}={tilt1:.1f}dB, "
                                  f"{backend2}={tilt2:.1f}dB, diff={abs_diff:.1f}dB")
        
        finally:
            os.unlink(file_path)
    
    def test_thd_proxy_equivalence(self):
        """Test THD proxy calculation equivalence."""
        if len(self.analyzers) < 2:
            self.skipTest("Need at least 2 backends for comparison")
        
        # Create test signal with harmonics
        _, file_path = self.create_test_signal('chord', 440.0)
        
        try:
            results = {}
            for backend_name, analyzer in self.analyzers.items():
                y, sr = analyzer.load_audio(file_path)
                thd = analyzer.thd_proxy(y, sr)
                results[backend_name] = thd
                
                # Basic sanity check
                self.assertGreaterEqual(thd, 0, f"{backend_name}: THD should be non-negative")
                self.assertIsInstance(thd, (int, float), f"{backend_name}: THD should be numeric")
            
            # Compare results between backends
            backend_names = list(results.keys())
            for i in range(len(backend_names)):
                for j in range(i + 1, len(backend_names)):
                    backend1, backend2 = backend_names[i], backend_names[j]
                    thd1, thd2 = results[backend1], results[backend2]
                    
                    # Relative tolerance check (higher tolerance for THD)
                    if max(thd1, thd2) > 0.01:  # Only compare if significant distortion
                        relative_diff = abs(thd1 - thd2) / max(thd1, thd2)
                        self.assertLess(relative_diff, 0.5,  # 50% tolerance for THD
                                      f"THD mismatch: {backend1}={thd1:.3f}, "
                                      f"{backend2}={thd2:.3f}, diff={relative_diff:.3f}")
        
        finally:
            os.unlink(file_path)
    
    def test_delay_detection_equivalence(self):
        """Test delay detection equivalence."""
        if len(self.analyzers) < 2:
            self.skipTest("Need at least 2 backends for comparison")
        
        # Create test signal with delay
        _, file_path = self.create_test_signal('impulse', 2.0, add_delay=True)
        
        try:
            results = {}
            for backend_name, analyzer in self.analyzers.items():
                y, sr = analyzer.load_audio(file_path)
                delay_ms, feedback = analyzer.onset_delay_ms(y, sr)
                results[backend_name] = (delay_ms, feedback)
                
                # Basic sanity check
                self.assertGreaterEqual(delay_ms, 0, f"{backend_name}: delay should be non-negative")
                self.assertGreaterEqual(feedback, 0, f"{backend_name}: feedback should be non-negative")
            
            # Compare results between backends
            backend_names = list(results.keys())
            for i in range(len(backend_names)):
                for j in range(i + 1, len(backend_names)):
                    backend1, backend2 = backend_names[i], backend_names[j]
                    delay1, feedback1 = results[backend1]
                    delay2, feedback2 = results[backend2]
                    
                    # Delay time comparison (should be close to 100ms)
                    delay_diff = abs(delay1 - delay2)
                    self.assertLess(delay_diff, 50,  # 50ms tolerance
                                  f"Delay mismatch: {backend1}={delay1:.0f}ms, "
                                  f"{backend2}={delay2:.0f}ms, diff={delay_diff:.0f}ms")
                    
                    # Feedback comparison
                    feedback_diff = abs(feedback1 - feedback2)
                    self.assertLess(feedback_diff, 0.3,  # 30% tolerance
                                  f"Feedback mismatch: {backend1}={feedback1:.2f}, "
                                  f"{backend2}={feedback2:.2f}, diff={feedback_diff:.2f}")
        
        finally:
            os.unlink(file_path)
    
    def test_lfo_detection_equivalence(self):
        """Test LFO detection equivalence."""
        if len(self.analyzers) < 2:
            self.skipTest("Need at least 2 backends for comparison")
        
        # Create test signal with modulation
        _, file_path = self.create_test_signal('sine', 440.0, add_modulation=True)
        
        try:
            results = {}
            for backend_name, analyzer in self.analyzers.items():
                y, sr = analyzer.load_audio(file_path)
                lfo_rate, lfo_strength = analyzer.lfo_rate_hz(y, sr)
                results[backend_name] = (lfo_rate, lfo_strength)
                
                # Basic sanity check
                if lfo_rate is not None:
                    self.assertGreater(lfo_rate, 0, f"{backend_name}: LFO rate should be positive")
                    self.assertLess(lfo_rate, 20, f"{backend_name}: LFO rate should be reasonable")
                self.assertGreaterEqual(lfo_strength, 0, f"{backend_name}: LFO strength should be non-negative")
            
            # Compare results between backends
            backend_names = list(results.keys())
            for i in range(len(backend_names)):
                for j in range(i + 1, len(backend_names)):
                    backend1, backend2 = backend_names[i], backend_names[j]
                    rate1, strength1 = results[backend1]
                    rate2, strength2 = results[backend2]
                    
                    # Compare LFO rates if both detected
                    if rate1 is not None and rate2 is not None:
                        rate_diff = abs(rate1 - rate2)
                        self.assertLess(rate_diff, 2.0,  # 2 Hz tolerance
                                      f"LFO rate mismatch: {backend1}={rate1:.1f}Hz, "
                                      f"{backend2}={rate2:.1f}Hz, diff={rate_diff:.1f}Hz")
                    
                    # Compare LFO strengths
                    strength_diff = abs(strength1 - strength2)
                    self.assertLess(strength_diff, 0.5,  # 50% tolerance
                                  f"LFO strength mismatch: {backend1}={strength1:.2f}, "
                                  f"{backend2}={strength2:.2f}, diff={strength_diff:.2f}")
        
        finally:
            os.unlink(file_path)


class TestBackendConsistency(unittest.TestCase):
    """Test individual backend consistency."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_rate = 44100
        self.backends = get_available_backends()
        
        # Create analyzers for available backends
        self.analyzers = {}
        if self.backends['librosa']:
            self.analyzers['librosa'] = get_analyzer('librosa', self.sample_rate)
        if self.backends['essentia']:
            self.analyzers['essentia'] = get_analyzer('essentia', self.sample_rate)
    
    def test_backend_consistency(self):
        """Test that each backend produces consistent results."""
        for backend_name, analyzer in self.analyzers.items():
            with self.subTest(backend=backend_name):
                # Create simple test signal
                t = np.linspace(0, 1.0, self.sample_rate)
                signal = np.sin(2 * np.pi * 440 * t)
                
                # Test multiple times
                results = []
                for _ in range(3):
                    centroid = analyzer.spectral_centroid_mean(signal, self.sample_rate)
                    results.append(centroid)
                
                # Results should be consistent
                for result in results[1:]:
                    self.assertAlmostEqual(result, results[0], places=1,
                                         msg=f"{backend_name}: inconsistent results")


if __name__ == '__main__':
    unittest.main()
