#!/usr/bin/env python3
"""
HIL (Hardware-in-the-Loop) Demonstration
=======================================

Demonstrates the complete HIL tone matching system with simulated hardware.
Shows the workflow from audio analysis to parameter optimization.

This demo uses synthetic audio signals to simulate the HIL process
without requiring actual Magicstomp hardware.
"""

import numpy as np
import soundfile as sf
import logging
import time
from pathlib import Path

# Import HIL components
from hil.io import AudioDeviceManager
from optimize.loss import PerceptualLoss
from optimize.search import CoordinateSearchOptimizer, ParameterSpace
from optimize.constraints import MagicstompConstraints, ParameterValidator
from analyzers.factory import get_analyzer


class SimulatedMagicstomp:
    """
    Simulated Magicstomp for demonstration purposes.
    
    Applies audio processing effects based on parameter settings
    to simulate the behavior of real Magicstomp hardware.
    """
    
    def __init__(self, sample_rate: int = 44100):
        """Initialize simulated Magicstomp."""
        self.sample_rate = sample_rate
        self.current_params = {}
        self.logger = logging.getLogger(__name__)
    
    def set_parameters(self, params: dict) -> None:
        """Set Magicstomp parameters."""
        self.current_params = params.copy()
        self.logger.debug(f"Magicstomp parameters set: {params}")
    
    def process_audio(self, input_audio: np.ndarray) -> np.ndarray:
        """
        Process audio through simulated Magicstomp.
        
        Args:
            input_audio: Input audio signal
            
        Returns:
            Processed audio signal
        """
        output_audio = input_audio.copy()
        
        # Apply gain
        if 'gain' in self.current_params:
            gain = self.current_params['gain']
            output_audio = output_audio * (0.5 + gain * 0.5)  # 0.5x to 1.0x
        
        # Apply treble boost/cut
        if 'treble' in self.current_params:
            treble = self.current_params['treble']
            # Simple high-pass filter simulation
            from scipy import signal
            if treble > 0.5:
                # Treble boost
                b, a = signal.butter(2, 2000 / (self.sample_rate / 2), btype='high')
                treble_signal = signal.filtfilt(b, a, output_audio)
                output_audio = output_audio + treble_signal * (treble - 0.5) * 0.3
            else:
                # Treble cut
                b, a = signal.butter(2, 2000 / (self.sample_rate / 2), btype='low')
                output_audio = signal.filtfilt(b, a, output_audio)
        
        # Apply delay
        if 'delay_mix' in self.current_params and self.current_params['delay_mix'] > 0:
            delay_mix = self.current_params['delay_mix']
            delay_time_ms = self.current_params.get('delay_time_ms', 300)
            feedback = self.current_params.get('delay_feedback', 0.3)
            
            delay_samples = int(delay_time_ms * self.sample_rate / 1000)
            
            # Simple delay implementation
            delayed_signal = np.zeros_like(output_audio)
            if delay_samples < len(output_audio):
                delayed_signal[delay_samples:] = output_audio[:-delay_samples] * feedback
            
            output_audio = output_audio * (1 - delay_mix) + delayed_signal * delay_mix
        
        # Apply reverb (simple)
        if 'reverb_mix' in self.current_params and self.current_params['reverb_mix'] > 0:
            reverb_mix = self.current_params['reverb_mix']
            decay_s = self.current_params.get('reverb_decay_s', 1.5)
            
            # Simple reverb simulation using multiple delays
            reverb_signal = np.zeros_like(output_audio)
            delays = [37, 59, 83, 127, 149]  # Prime numbers for delay times
            
            for delay_samples in delays:
                if delay_samples < len(output_audio):
                    decay = np.exp(-delay_samples / (decay_s * self.sample_rate))
                    delayed = np.zeros_like(output_audio)
                    delayed[delay_samples:] = output_audio[:-delay_samples] * decay
                    reverb_signal += delayed
            
            reverb_signal /= len(delays)
            output_audio = output_audio * (1 - reverb_mix) + reverb_signal * reverb_mix
        
        # Apply modulation (chorus/phaser)
        if 'mod_mix' in self.current_params and self.current_params['mod_mix'] > 0:
            mod_mix = self.current_params['mod_mix']
            mod_depth = self.current_params.get('mod_depth', 0.35)
            mod_rate_hz = self.current_params.get('mod_rate_hz', 0.8)
            
            # Simple chorus effect
            t = np.linspace(0, len(output_audio) / self.sample_rate, len(output_audio))
            lfo = np.sin(2 * np.pi * mod_rate_hz * t) * mod_depth * 0.01  # 10ms max delay
            
            # Apply variable delay (simplified)
            mod_signal = np.zeros_like(output_audio)
            for i in range(len(output_audio)):
                delay_samples = int(lfo[i] * self.sample_rate)
                if i + delay_samples < len(output_audio):
                    mod_signal[i] = output_audio[i + delay_samples]
            
            output_audio = output_audio * (1 - mod_mix) + mod_signal * mod_mix
        
        # Apply presence
        if 'presence' in self.current_params:
            presence = self.current_params['presence']
            if presence > 0.5:
                # Presence boost (2-4 kHz)
                from scipy import signal
                b, a = signal.butter(2, [2000, 4000], btype='band', fs=self.sample_rate)
                presence_signal = signal.filtfilt(b, a, output_audio)
                output_audio = output_audio + presence_signal * (presence - 0.5) * 0.2
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(output_audio))
        if max_val > 0:
            output_audio = output_audio / max_val * 0.9
        
        return output_audio


class HILDemo:
    """
    Hardware-in-the-Loop demonstration system.
    
    Shows the complete HIL workflow using simulated hardware.
    """
    
    def __init__(self, sample_rate: int = 44100):
        """Initialize HIL demo."""
        self.sample_rate = sample_rate
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.magicstomp = SimulatedMagicstomp(sample_rate)
        self.loss_calculator = PerceptualLoss(sample_rate)
        self.parameter_space = ParameterSpace()
        self.constraints = MagicstompConstraints()
        self.validator = ParameterValidator()
        
        # State
        self.target_audio = None
        self.di_signal = None
        self.current_patch = None
    
    def create_test_signals(self, duration: float = 3.0) -> None:
        """
        Create synthetic test signals for demonstration.
        
        Args:
            duration: Duration of test signals in seconds
        """
        self.logger.info("Creating synthetic test signals...")
        
        # Generate time vector
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Create target signal (complex guitar-like sound)
        # Fundamental + harmonics + some noise
        fundamental = 220  # A3
        target = np.zeros_like(t)
        
        # Add fundamental and harmonics
        for harmonic in range(1, 6):
            freq = fundamental * harmonic
            amplitude = 1.0 / harmonic  # Decreasing amplitude
            target += amplitude * np.sin(2 * np.pi * freq * t)
        
        # Add some attack transients
        attack_samples = int(0.01 * self.sample_rate)  # 10ms
        target[:attack_samples] *= np.linspace(0, 1, attack_samples)
        
        # Add slight noise
        noise = np.random.normal(0, 0.05, len(target))
        target += noise
        
        # Normalize
        target = target / np.max(np.abs(target)) * 0.8
        
        # Create DI signal (cleaner version)
        di = np.zeros_like(t)
        for harmonic in range(1, 4):  # Fewer harmonics for DI
            freq = fundamental * harmonic
            amplitude = 1.0 / harmonic
            di += amplitude * np.sin(2 * np.pi * freq * t)
        
        # Add attack
        di[:attack_samples] *= np.linspace(0, 1, attack_samples)
        
        # Normalize
        di = di / np.max(np.abs(di)) * 0.7
        
        self.target_audio = target
        self.di_signal = di
        
        self.logger.info(f"Test signals created: {len(target)} samples, {duration:.1f}s")
    
    def analyze_target(self) -> dict:
        """
        Analyze target audio to generate initial patch.
        
        Returns:
            Initial patch configuration
        """
        self.logger.info("Analyzing target audio...")
        
        # Simple analysis-based patch generation
        # In real implementation, this would use the full analyzer pipeline
        
        # Analyze spectral content
        target_centroid = self._compute_spectral_centroid(self.target_audio)
        target_energy = np.mean(self.target_audio ** 2)
        
        # Generate initial patch based on analysis
        patch = {
            'gain': min(0.7, 0.3 + target_energy * 0.5),  # More energy = more gain
            'treble': min(0.8, 0.4 + (target_centroid - 1000) / 2000),  # Higher centroid = more treble
            'presence': 0.5,  # Default
            'delay_mix': 0.2,  # Default
            'delay_feedback': 0.3,  # Default
            'delay_time_ms': 300,  # Default
            'reverb_mix': 0.15,  # Default
            'reverb_decay_s': 1.5,  # Default
            'mod_depth': 0.35,  # Default
            'mod_rate_hz': 0.8,  # Default
            'mod_mix': 0.18  # Default
        }
        
        # Validate patch
        is_valid, errors = self.validator.validate_patch(patch)
        if not is_valid:
            self.logger.warning(f"Patch validation errors: {errors}")
            # Apply fixes
            suggestions = self.validator.suggest_fixes(patch)
            for param, value in suggestions.items():
                patch[param] = value
        
        self.current_patch = patch
        
        self.logger.info("Target analysis complete")
        return patch
    
    def _compute_spectral_centroid(self, audio: np.ndarray) -> float:
        """Compute spectral centroid of audio signal."""
        from scipy.fft import fft, fftfreq
        
        # Compute FFT
        fft_data = fft(audio)
        freqs = fftfreq(len(audio), 1/self.sample_rate)
        
        # Only use positive frequencies
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = np.abs(fft_data[:len(fft_data)//2])
        
        # Compute centroid
        if np.sum(positive_fft) > 0:
            centroid = np.sum(positive_freqs * positive_fft) / np.sum(positive_fft)
        else:
            centroid = 1000  # Default
        
        return centroid
    
    def simulate_hil_optimization(self, max_iterations: int = 10) -> dict:
        """
        Simulate Hardware-in-the-Loop optimization.
        
        Args:
            max_iterations: Maximum optimization iterations
            
        Returns:
            Optimization results
        """
        self.logger.info("Starting simulated HIL optimization...")
        
        # Initialize parameter space
        for param_name, value in self.current_patch.items():
            constraint = self.constraints.get_constraint(param_name)
            if constraint:
                self.parameter_space.set_parameter_value(param_name, value)
        
        # Create loss function
        def loss_function(params: dict) -> float:
            # Set Magicstomp parameters
            self.magicstomp.set_parameters(params)
            
            # Process DI signal through simulated Magicstomp
            processed_audio = self.magicstomp.process_audio(self.di_signal)
            
            # Compute perceptual loss
            loss = self.loss_calculator.compute_loss(self.target_audio, processed_audio)
            
            self.logger.debug(f"Parameters: {params} -> Loss: {loss:.6f}")
            
            return loss
        
        # Run optimization
        optimizer = CoordinateSearchOptimizer(
            self.parameter_space,
            loss_function,
            max_iterations=max_iterations
        )
        
        results = optimizer.optimize()
        
        # Update current patch with best parameters
        if results['success']:
            self.current_patch.update(results['best_parameters'])
        
        self.logger.info("Simulated HIL optimization complete")
        return results
    
    def save_results(self, output_dir: str = "out") -> dict:
        """
        Save demonstration results.
        
        Args:
            output_dir: Output directory
            
        Returns:
            Dictionary of saved file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        saved_files = {}
        
        # Save audio signals
        target_file = output_path / "demo_target.wav"
        sf.write(target_file, self.target_audio, self.sample_rate)
        saved_files['target'] = str(target_file)
        
        di_file = output_path / "demo_di.wav"
        sf.write(di_file, self.di_signal, self.sample_rate)
        saved_files['di'] = str(di_file)
        
        # Process DI through optimized Magicstomp
        self.magicstomp.set_parameters(self.current_patch)
        processed_audio = self.magicstomp.process_audio(self.di_signal)
        
        processed_file = output_path / "demo_processed.wav"
        sf.write(processed_file, processed_audio, self.sample_rate)
        saved_files['processed'] = str(processed_file)
        
        # Save patch configuration
        import json
        patch_file = output_path / "demo_patch.json"
        with open(patch_file, 'w') as f:
            json.dump(self.current_patch, f, indent=2)
        saved_files['patch'] = str(patch_file)
        
        self.logger.info("Demo results saved:")
        for file_type, file_path in saved_files.items():
            self.logger.info(f"  {file_type}: {file_path}")
        
        return saved_files
    
    def run_complete_demo(self, duration: float = 3.0, 
                         max_iterations: int = 10) -> dict:
        """
        Run complete HIL demonstration.
        
        Args:
            duration: Duration of test signals
            max_iterations: Maximum optimization iterations
            
        Returns:
            Demonstration results
        """
        self.logger.info("Starting complete HIL demonstration...")
        
        # Step 1: Create test signals
        self.create_test_signals(duration)
        
        # Step 2: Analyze target
        initial_patch = self.analyze_target()
        self.logger.info(f"Initial patch: {initial_patch}")
        
        # Step 3: Simulate HIL optimization
        optimization_results = self.simulate_hil_optimization(max_iterations)
        
        # Step 4: Save results
        saved_files = self.save_results()
        
        # Summary
        self.logger.info("HIL demonstration complete!")
        self.logger.info(f"Initial loss: {optimization_results['initial_loss']:.6f}")
        self.logger.info(f"Final loss: {optimization_results['final_loss']:.6f}")
        self.logger.info(f"Improvement: {optimization_results['improvement']:.6f}")
        
        return {
            'initial_patch': initial_patch,
            'optimization_results': optimization_results,
            'saved_files': saved_files
        }


def main():
    """Main entry point for HIL demo."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        # Create and run HIL demo
        demo = HILDemo()
        results = demo.run_complete_demo(duration=2.0, max_iterations=8)
        
        logger.info("Demo completed successfully!")
        
        # Print summary
        print("\n" + "="*50)
        print("HIL DEMONSTRATION SUMMARY")
        print("="*50)
        print(f"Initial Loss: {results['optimization_results']['initial_loss']:.6f}")
        print(f"Final Loss: {results['optimization_results']['final_loss']:.6f}")
        print(f"Improvement: {results['optimization_results']['improvement']:.6f}")
        print(f"Iterations: {results['optimization_results']['iterations']}")
        print("\nSaved Files:")
        for file_type, file_path in results['saved_files'].items():
            print(f"  {file_type}: {file_path}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
