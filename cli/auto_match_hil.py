#!/usr/bin/env python3
"""
Auto Match HIL (Hardware-in-the-Loop) CLI
========================================

Complete Hardware-in-the-Loop tone matching system for Yamaha Magicstomp.
Performs automatic optimization through real hardware feedback.

Usage:
    python cli/auto_match_hil.py target.wav --di-signal dry.wav --send-patch
    python cli/auto_match_hil.py target.wav --di-signal dry.wav --optimize --max-iterations 10
    python cli/auto_match_hil.py target.wav --di-signal dry.wav --calibrate --list-devices

Features:
- Real-time audio I/O with Magicstomp hardware
- Automatic calibration (latency + gain)
- Perceptual loss optimization (log-mel + MFCC)
- Coordinate search parameter tuning
- Complete patch export (JSON + SYX + WAV)
"""

import argparse
import sys
import logging
import time
import json
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyzers.factory import get_analyzer
from adapter_magicstomp import MagicstompAdapter
from hil.io import AudioDeviceManager, list_audio_devices
from optimize.loss import PerceptualLoss
from optimize.search import CoordinateSearchOptimizer, ParameterSpace
from auto_tone_match_magicstomp import AutoToneMatcher


class HILToneMatcher:
    """
    Hardware-in-the-Loop tone matching system.
    
    Orchestrates the complete HIL optimization pipeline:
    1. Analyze target audio
    2. Generate initial patch
    3. Calibrate audio system
    4. Optimize through hardware feedback
    5. Export results
    """
    
    def __init__(self, backend: str = 'auto', sample_rate: int = 44100):
        """
        Initialize HIL tone matcher.
        
        Args:
            backend: Audio analysis backend
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.audio_manager = AudioDeviceManager(sample_rate)
        self.magicstomp_adapter = MagicstompAdapter()
        self.loss_calculator = PerceptualLoss(sample_rate)
        self.parameter_space = ParameterSpace()
        
        # Tone matcher for initial analysis
        self.tone_matcher = AutoToneMatcher(backend, sample_rate)
        
        # State
        self.target_audio = None
        self.di_signal = None
        self.calibrated = False
        self.current_patch = None
        self.optimization_results = None
        
        # Output directory
        self.output_dir = Path("out")
        self.output_dir.mkdir(exist_ok=True)
    
    def setup_audio_devices(self, input_device: Optional[str] = None,
                          output_device: Optional[str] = None,
                          input_channels: List[int] = None,
                          output_channels: List[int] = None) -> bool:
        """
        Setup audio input/output devices.
        
        Args:
            input_device: Input device name or ID
            output_device: Output device name or ID
            input_channels: Input channels to use
            output_channels: Output channels to use
            
        Returns:
            True if devices set successfully
        """
        self.logger.info("Setting up audio devices...")
        
        # Set input device
        if input_device:
            if not self.audio_manager.set_input_device(device_name=input_device, channels=input_channels):
                self.logger.error(f"Failed to set input device: {input_device}")
                return False
        
        # Set output device
        if output_device:
            if not self.audio_manager.set_output_device(device_name=output_device, channels=output_channels):
                self.logger.error(f"Failed to set output device: {output_device}")
                return False
        
        self.logger.info("Audio devices configured successfully")
        return True
    
    def load_target_audio(self, target_path: str) -> None:
        """
        Load target audio for tone matching.
        
        Args:
            target_path: Path to target audio file
        """
        self.logger.info(f"Loading target audio: {target_path}")
        
        # Load using audio manager
        self.target_audio = self.audio_manager.load_di_signal(target_path)
        
        self.logger.info(f"Target audio loaded: {len(self.target_audio)} samples, {len(self.target_audio)/self.sample_rate:.2f}s")
    
    def load_di_signal(self, di_path: str) -> None:
        """
        Load DI (Direct Input) signal for re-amping.
        
        Args:
            di_path: Path to DI audio file
        """
        self.logger.info(f"Loading DI signal: {di_path}")
        
        # Load using audio manager
        self.di_signal = self.audio_manager.load_di_signal(di_path)
        
        self.logger.info(f"DI signal loaded: {len(self.di_signal)} samples, {len(self.di_signal)/self.sample_rate:.2f}s")
    
    def analyze_target(self, verbose: bool = False) -> Dict[str, Any]:
        """
        Analyze target audio and generate initial patch.
        
        Args:
            verbose: Enable verbose logging
            
        Returns:
            Initial patch configuration
        """
        if self.target_audio is None:
            raise RuntimeError("Target audio not loaded")
        
        self.logger.info("Analyzing target audio...")
        
        # Save target audio temporarily for analysis
        target_temp = self.output_dir / "target_temp.wav"
        self.audio_manager.save_recorded_signal(self.target_audio, str(target_temp))
        
        try:
            # Analyze using tone matcher
            features = self.tone_matcher.analyze_audio(str(target_temp), verbose)
            patch = self.tone_matcher.map_to_patch()
            
            self.current_patch = patch
            
            self.logger.info("Target analysis complete")
            return patch
            
        finally:
            # Cleanup temp file
            if target_temp.exists():
                target_temp.unlink()
    
    def calibrate_system(self, duration: float = 2.0) -> Dict[str, Any]:
        """
        Calibrate audio system for latency and gain.
        
        Args:
            duration: Calibration signal duration
            
        Returns:
            Calibration results
        """
        self.logger.info("Calibrating audio system...")
        
        if not self.audio_manager.input_device or not self.audio_manager.output_device:
            raise RuntimeError("Audio devices must be set before calibration")
        
        # Perform calibration
        calibration_data = self.audio_manager.calibrate_system(duration)
        
        # Save calibration data
        calibration_file = self.output_dir / "calibration.json"
        self.audio_manager.save_calibration(str(calibration_file))
        
        self.calibrated = True
        
        self.logger.info("System calibration complete")
        return calibration_data
    
    def send_patch_to_magicstomp(self, patch: Dict[str, Any], 
                                patch_number: int = 0,
                                midi_port: Optional[str] = None) -> bool:
        """
        Send patch to Magicstomp via SysEx.
        
        Args:
            patch: Patch configuration
            patch_number: Magicstomp patch number
            midi_port: MIDI port name
            
        Returns:
            True if patch sent successfully
        """
        self.logger.info(f"Sending patch to Magicstomp (patch #{patch_number})...")
        
        # Generate SysEx data
        syx_data = self.magicstomp_adapter.json_to_syx(patch, patch_number)
        
        # Send to device
        if midi_port:
            # Use specific port
            success = self.magicstomp_adapter.send_to_device(syx_data)
        else:
            # Auto-detect port
            success = self.magicstomp_adapter.send_to_device(syx_data)
        
        if success:
            self.logger.info("Patch sent successfully")
        else:
            self.logger.warning("Failed to send patch to Magicstomp")
        
        return success
    
    def capture_magicstomp_output(self, wait_time: float = 0.1) -> np.ndarray:
        """
        Capture audio output from Magicstomp.
        
        Args:
            wait_time: Wait time after sending patch before capture
            
        Returns:
            Captured audio signal
        """
        if self.di_signal is None:
            raise RuntimeError("DI signal not loaded")
        
        # Wait for patch to take effect
        if wait_time > 0:
            time.sleep(wait_time)
        
        # Play DI signal and record return
        captured_audio = self.audio_manager.play_and_record(self.di_signal)
        
        self.logger.debug(f"Captured {len(captured_audio)} samples from Magicstomp")
        
        return captured_audio
    
    def compute_loss(self, target_audio: np.ndarray, 
                    processed_audio: np.ndarray) -> float:
        """
        Compute perceptual loss between target and processed audio.
        
        Args:
            target_audio: Target audio signal
            processed_audio: Processed audio signal
            
        Returns:
            Perceptual loss value
        """
        return self.loss_calculator.compute_loss(target_audio, processed_audio)
    
    def create_loss_function(self) -> callable:
        """
        Create loss function for optimization.
        
        Returns:
            Loss function that takes parameter dict and returns loss
        """
        def loss_function(parameters: Dict[str, float]) -> float:
            # Update parameter space
            for name, value in parameters.items():
                self.parameter_space.set_parameter_value(name, value)
            
            # Generate patch with new parameters
            patch = self.current_patch.copy()
            self._update_patch_with_parameters(patch, parameters)
            
            # Send patch to Magicstomp
            if not self.send_patch_to_magicstomp(patch):
                return float('inf')  # High loss if patch send fails
            
            # Capture Magicstomp output
            captured_audio = self.capture_magicstomp_output()
            
            # Compute loss
            loss = self.compute_loss(self.target_audio, captured_audio)
            
            self.logger.debug(f"Parameters: {parameters} -> Loss: {loss:.6f}")
            
            return loss
        
        return loss_function
    
    def _update_patch_with_parameters(self, patch: Dict[str, Any], 
                                    parameters: Dict[str, float]) -> None:
        """Update patch with optimized parameters."""
        # Update delay parameters
        if 'delay_mix' in parameters:
            patch['delay']['mix'] = parameters['delay_mix']
        if 'delay_feedback' in parameters:
            patch['delay']['feedback'] = parameters['delay_feedback']
        if 'delay_time_ms' in parameters:
            patch['delay']['time_ms'] = parameters['delay_time_ms']
        
        # Update reverb parameters
        if 'reverb_mix' in parameters:
            patch['reverb']['mix'] = parameters['reverb_mix']
        if 'reverb_decay_s' in parameters:
            patch['reverb']['decay_s'] = parameters['reverb_decay_s']
        
        # Update amp parameters
        if 'treble' in parameters:
            patch['amp']['treble'] = parameters['treble']
        if 'presence' in parameters:
            patch['amp']['presence'] = parameters['presence']
        if 'gain' in parameters:
            patch['amp']['gain'] = parameters['gain']
        
        # Update modulation parameters
        if 'mod_depth' in parameters:
            patch['mod']['depth'] = parameters['mod_depth']
        if 'mod_rate_hz' in parameters:
            patch['mod']['rate_hz'] = parameters['mod_rate_hz']
        if 'mod_mix' in parameters:
            patch['mod']['mix'] = parameters['mod_mix']
    
    def optimize_patch(self, max_iterations: int = 20,
                      parameters_to_optimize: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Optimize patch parameters using Hardware-in-the-Loop.
        
        Args:
            max_iterations: Maximum optimization iterations
            parameters_to_optimize: List of parameters to optimize
            
        Returns:
            Optimization results
        """
        if not self.calibrated:
            raise RuntimeError("System must be calibrated before optimization")
        
        if self.current_patch is None:
            raise RuntimeError("No patch to optimize")
        
        self.logger.info("Starting Hardware-in-the-Loop optimization...")
        
        # Set up parameter space from current patch
        self._initialize_parameter_space_from_patch()
        
        # Select parameters to optimize
        if parameters_to_optimize is None:
            parameters_to_optimize = [
                'delay_mix', 'delay_feedback', 'reverb_mix',
                'treble', 'presence', 'mod_depth', 'mod_mix'
            ]
        
        # Create loss function
        loss_function = self.create_loss_function()
        
        # Create optimizer
        optimizer = CoordinateSearchOptimizer(
            self.parameter_space,
            loss_function,
            max_iterations=max_iterations
        )
        
        # Run optimization
        results = optimizer.optimize()
        
        # Update current patch with best parameters
        if results['success']:
            self._update_patch_with_parameters(self.current_patch, results['best_parameters'])
        
        self.optimization_results = results
        
        self.logger.info("Hardware-in-the-Loop optimization complete")
        return results
    
    def _initialize_parameter_space_from_patch(self) -> None:
        """Initialize parameter space from current patch."""
        if self.current_patch is None:
            return
        
        # Set initial values from patch
        if 'delay' in self.current_patch and self.current_patch['delay']['enabled']:
            self.parameter_space.set_parameter_value('delay_mix', self.current_patch['delay']['mix'])
            self.parameter_space.set_parameter_value('delay_feedback', self.current_patch['delay']['feedback'])
            self.parameter_space.set_parameter_value('delay_time_ms', self.current_patch['delay']['time_ms'])
        
        if 'reverb' in self.current_patch and self.current_patch['reverb']['enabled']:
            self.parameter_space.set_parameter_value('reverb_mix', self.current_patch['reverb']['mix'])
            self.parameter_space.set_parameter_value('reverb_decay_s', self.current_patch['reverb']['decay_s'])
        
        if 'amp' in self.current_patch:
            self.parameter_space.set_parameter_value('treble', self.current_patch['amp']['treble'])
            self.parameter_space.set_parameter_value('presence', self.current_patch['amp']['presence'])
            self.parameter_space.set_parameter_value('gain', self.current_patch['amp']['gain'])
        
        if 'mod' in self.current_patch and self.current_patch['mod']['enabled']:
            self.parameter_space.set_parameter_value('mod_depth', self.current_patch['mod']['depth'])
            self.parameter_space.set_parameter_value('mod_rate_hz', self.current_patch['mod']['rate_hz'])
            self.parameter_space.set_parameter_value('mod_mix', self.current_patch['mod']['mix'])
    
    def export_results(self, session_name: str = "hil_session") -> Dict[str, str]:
        """
        Export optimization results.
        
        Args:
            session_name: Name for output files
            
        Returns:
            Dictionary of exported file paths
        """
        self.logger.info("Exporting optimization results...")
        
        exported_files = {}
        
        # Export initial patch
        initial_patch_file = self.output_dir / f"{session_name}_initial.json"
        with open(initial_patch_file, 'w') as f:
            json.dump(self.current_patch, f, indent=2)
        exported_files['initial_patch'] = str(initial_patch_file)
        
        # Export initial SysEx
        initial_syx_data = self.magicstomp_adapter.json_to_syx(self.current_patch, 0)
        initial_syx_file = self.output_dir / f"{session_name}_initial.syx"
        self.magicstomp_adapter.save_to_file(initial_syx_data, str(initial_syx_file))
        exported_files['initial_syx'] = str(initial_syx_file)
        
        # Export optimized patch (if optimization was performed)
        if self.optimization_results and self.optimization_results['success']:
            optimized_patch_file = self.output_dir / f"{session_name}_optimized.json"
            with open(optimized_patch_file, 'w') as f:
                json.dump(self.current_patch, f, indent=2)
            exported_files['optimized_patch'] = str(optimized_patch_file)
            
            # Export optimized SysEx
            optimized_syx_data = self.magicstomp_adapter.json_to_syx(self.current_patch, 1)
            optimized_syx_file = self.output_dir / f"{session_name}_optimized.syx"
            self.magicstomp_adapter.save_to_file(optimized_syx_data, str(optimized_syx_file))
            exported_files['optimized_syx'] = str(optimized_syx_file)
        
        # Export target and DI signals
        target_file = self.output_dir / f"{session_name}_target.wav"
        self.audio_manager.save_recorded_signal(self.target_audio, str(target_file))
        exported_files['target_audio'] = str(target_file)
        
        di_file = self.output_dir / f"{session_name}_di.wav"
        self.audio_manager.save_recorded_signal(self.di_signal, str(di_file))
        exported_files['di_audio'] = str(di_file)
        
        # Export optimization report
        if self.optimization_results:
            report_file = self.output_dir / f"{session_name}_report.txt"
            with open(report_file, 'w') as f:
                f.write("Hardware-in-the-Loop Optimization Report\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Session: {session_name}\n")
                f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Iterations: {self.optimization_results['iterations']}\n")
                f.write(f"Initial Loss: {self.optimization_results['initial_loss']:.6f}\n")
                f.write(f"Final Loss: {self.optimization_results['final_loss']:.6f}\n")
                f.write(f"Improvement: {self.optimization_results['improvement']:.6f}\n\n")
                f.write("Best Parameters:\n")
                for param, value in self.optimization_results['best_parameters'].items():
                    f.write(f"  {param}: {value:.4f}\n")
            exported_files['report'] = str(report_file)
        
        self.logger.info("Results exported successfully")
        return exported_files
    
    def cleanup(self):
        """Cleanup resources."""
        self.audio_manager.close()
        self.logger.info("HIL tone matcher cleaned up")


def main():
    """Main entry point for HIL CLI."""
    parser = argparse.ArgumentParser(
        description="Hardware-in-the-Loop Magicstomp Tone Matching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List audio devices
  python cli/auto_match_hil.py --list-devices

  # Calibrate system
  python cli/auto_match_hil.py --calibrate --in-device "Focusrite" --out-device "Focusrite"

  # Full HIL optimization
  python cli/auto_match_hil.py target.wav --di-signal dry.wav --calibrate --optimize --send-patch

  # Send patch only
  python cli/auto_match_hil.py target.wav --di-signal dry.wav --send-patch --patch-number 5
        """
    )
    
    # Input files
    parser.add_argument('target', nargs='?', help='Target audio file')
    parser.add_argument('--di-signal', help='DI (Direct Input) signal for re-amping')
    
    # Audio device configuration
    parser.add_argument('--in-device', help='Input audio device name or ID')
    parser.add_argument('--out-device', help='Output audio device name or ID')
    parser.add_argument('--in-ch', type=int, nargs='+', default=[1], help='Input channels')
    parser.add_argument('--out-ch', type=int, nargs='+', default=[1], help='Output channels')
    
    # MIDI configuration
    parser.add_argument('--midi-port', help='MIDI port name for Magicstomp')
    parser.add_argument('--patch-number', type=int, default=0, help='Magicstomp patch number')
    
    # Operations
    parser.add_argument('--list-devices', action='store_true', help='List available audio devices')
    parser.add_argument('--calibrate', action='store_true', help='Calibrate audio system')
    parser.add_argument('--send-patch', action='store_true', help='Send patch to Magicstomp')
    parser.add_argument('--optimize', action='store_true', help='Run HIL optimization')
    
    # Optimization parameters
    parser.add_argument('--max-iterations', type=int, default=20, help='Maximum optimization iterations')
    parser.add_argument('--optimize-params', nargs='+', help='Parameters to optimize')
    
    # Backend selection
    parser.add_argument('--backend', choices=['auto', 'essentia', 'librosa'], default='auto', help='Audio analysis backend')
    
    # Output
    parser.add_argument('--session-name', default='hil_session', help='Session name for output files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    logger = logging.getLogger(__name__)
    
    # List devices if requested
    if args.list_devices:
        logger.info("Available audio devices:")
        list_audio_devices()
        return
    
    # Check required arguments
    if not args.target and not args.calibrate:
        parser.error("Target audio file is required (or use --calibrate)")
    
    if not args.di_signal and (args.send_patch or args.optimize):
        parser.error("DI signal is required for patch sending or optimization")
    
    try:
        # Initialize HIL tone matcher
        hil_matcher = HILToneMatcher(args.backend)
        
        # Setup audio devices
        if args.in_device or args.out_device:
            if not hil_matcher.setup_audio_devices(
                args.in_device, args.out_device,
                args.in_ch, args.out_ch
            ):
                logger.error("Failed to setup audio devices")
                sys.exit(1)
        
        # Load audio files
        if args.target:
            hil_matcher.load_target_audio(args.target)
        
        if args.di_signal:
            hil_matcher.load_di_signal(args.di_signal)
        
        # Calibrate system
        if args.calibrate:
            calibration_results = hil_matcher.calibrate_system()
            logger.info(f"Calibration complete: latency={calibration_results['latency_ms']:.1f}ms")
        
        # Analyze target (if provided)
        if args.target:
            initial_patch = hil_matcher.analyze_target(args.verbose)
            logger.info("Target analysis complete")
        
        # Send patch to Magicstomp
        if args.send_patch and hil_matcher.current_patch:
            hil_matcher.send_patch_to_magicstomp(
                hil_matcher.current_patch,
                args.patch_number,
                args.midi_port
            )
        
        # Run optimization
        if args.optimize and hil_matcher.calibrated:
            optimization_results = hil_matcher.optimize_patch(
                args.max_iterations,
                args.optimize_params
            )
            
            if optimization_results['success']:
                logger.info(f"Optimization complete: improvement={optimization_results['improvement']:.6f}")
            else:
                logger.warning("Optimization failed")
        
        # Export results
        if args.target:
            exported_files = hil_matcher.export_results(args.session_name)
            logger.info("Results exported:")
            for file_type, file_path in exported_files.items():
                logger.info(f"  {file_type}: {file_path}")
        
        logger.info("HIL processing complete!")
        
    except Exception as e:
        logger.error(f"HIL processing failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    finally:
        # Cleanup
        if 'hil_matcher' in locals():
            hil_matcher.cleanup()


if __name__ == "__main__":
    main()
