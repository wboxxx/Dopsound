#!/usr/bin/env python3
"""
HIL Audio I/O Module
===================

Handles real-time audio input/output for Hardware-in-the-Loop optimization.
Provides calibration, latency measurement, and audio device management.
"""

import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import json
import logging
from typing import Tuple, Optional, Dict, Any, List
from pathlib import Path


class AudioDeviceManager:
    """
    Manages audio device I/O for HIL operations.
    
    Handles input/output device selection, calibration, and real-time audio
    processing for Magicstomp optimization.
    """
    
    def __init__(self, sample_rate: int = 44100, buffer_size: int = 1024):
        """
        Initialize audio device manager.
        
        Args:
            sample_rate: Audio sample rate
            buffer_size: Audio buffer size for real-time processing
        """
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.logger = logging.getLogger(__name__)
        
        # Device configuration
        self.input_device = None
        self.output_device = None
        self.input_channels = [1]  # Mono input by default
        self.output_channels = [1]  # Mono output by default
        
        # Calibration data
        self.calibration_data = {}
        self.round_trip_latency = 0  # samples
        self.gain_compensation = 1.0
        
        # Audio streams
        self.input_stream = None
        self.output_stream = None
    
    def list_audio_devices(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        List available audio devices.
        
        Returns:
            Dictionary with input and output devices
        """
        devices = sd.query_devices()
        
        input_devices = []
        output_devices = []
        
        for i, device in enumerate(devices):
            device_info = {
                'id': i,
                'name': device['name'],
                'channels_in': device['max_input_channels'],
                'channels_out': device['max_output_channels'],
                'default_samplerate': device['default_samplerate']
            }
            
            if device['max_input_channels'] > 0:
                input_devices.append(device_info)
            
            if device['max_output_channels'] > 0:
                output_devices.append(device_info)
        
        return {
            'input': input_devices,
            'output': output_devices
        }
    
    def set_input_device(self, device_id: Optional[int] = None, 
                        device_name: Optional[str] = None,
                        channels: List[int] = None) -> bool:
        """
        Set input audio device.
        
        Args:
            device_id: Device ID number
            device_name: Device name (partial match)
            channels: Input channels to use
            
        Returns:
            True if device set successfully
        """
        try:
            if device_name:
                devices = sd.query_devices()
                for i, device in enumerate(devices):
                    if device_name.lower() in device['name'].lower():
                        device_id = i
                        break
            
            if device_id is not None:
                device_info = sd.query_devices(device_id)
                if device_info['max_input_channels'] == 0:
                    self.logger.error(f"Device {device_id} has no input channels")
                    return False
                
                self.input_device = device_id
                self.input_channels = channels or [1]
                self.logger.info(f"Input device set: {device_info['name']} (channels: {self.input_channels})")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to set input device: {e}")
            return False
    
    def set_output_device(self, device_id: Optional[int] = None,
                         device_name: Optional[str] = None,
                         channels: List[int] = None) -> bool:
        """
        Set output audio device.
        
        Args:
            device_id: Device ID number
            device_name: Device name (partial match)
            channels: Output channels to use
            
        Returns:
            True if device set successfully
        """
        try:
            if device_name:
                devices = sd.query_devices()
                for i, device in enumerate(devices):
                    if device_name.lower() in device['name'].lower():
                        device_id = i
                        break
            
            if device_id is not None:
                device_info = sd.query_devices(device_id)
                if device_info['max_output_channels'] == 0:
                    self.logger.error(f"Device {device_id} has no output channels")
                    return False
                
                self.output_device = device_id
                self.output_channels = channels or [1]
                self.logger.info(f"Output device set: {device_info['name']} (channels: {self.output_channels})")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to set output device: {e}")
            return False
    
    def calibrate_system(self, duration: float = 2.0) -> Dict[str, Any]:
        """
        Calibrate the audio system for latency and gain.
        
        Performs round-trip latency measurement and gain calibration
        by sending a test signal and measuring the response.
        
        Args:
            duration: Duration of calibration signal in seconds
            
        Returns:
            Calibration results dictionary
        """
        self.logger.info("Starting audio system calibration...")
        
        if self.input_device is None or self.output_device is None:
            raise RuntimeError("Input and output devices must be set before calibration")
        
        # Generate calibration signal (click train)
        click_interval = 0.5  # seconds
        num_clicks = int(duration / click_interval)
        
        # Create click signal
        click_duration = 0.01  # 10ms clicks
        click_samples = int(click_duration * self.sample_rate)
        signal_length = int(duration * self.sample_rate)
        
        calibration_signal = np.zeros(signal_length)
        
        for i in range(num_clicks):
            click_start = int(i * click_interval * self.sample_rate)
            click_end = click_start + click_samples
            if click_end < signal_length:
                calibration_signal[click_start:click_end] = 0.8  # 80% amplitude
        
        # Record while playing
        self.logger.info("Recording calibration signal...")
        
        recorded_audio = sd.playrec(
            calibration_signal,
            samplerate=self.sample_rate,
            input_device=self.input_device,
            output_device=self.output_device,
            channels=max(len(self.input_channels), len(self.output_channels))
        )
        
        sd.wait()  # Wait for recording to complete
        
        # Analyze recorded signal
        recorded_audio = recorded_audio.flatten()
        
        # Find latency by correlating sent and received signals
        latency_samples = self._measure_latency(calibration_signal, recorded_audio)
        latency_ms = latency_samples * 1000 / self.sample_rate
        
        # Measure gain compensation
        sent_rms = np.sqrt(np.mean(calibration_signal**2))
        received_rms = np.sqrt(np.mean(recorded_audio**2))
        
        if received_rms > 0:
            gain_ratio = sent_rms / received_rms
            # Target -1 dBFS (0.89)
            target_gain = 0.89 / received_rms
            gain_compensation = min(target_gain, 2.0)  # Limit to 2x gain
        else:
            gain_compensation = 1.0
        
        # Store calibration results
        self.calibration_data = {
            'timestamp': time.time(),
            'sample_rate': self.sample_rate,
            'latency_samples': latency_samples,
            'latency_ms': latency_ms,
            'gain_compensation': gain_compensation,
            'sent_rms': sent_rms,
            'received_rms': received_rms,
            'input_device': self.input_device,
            'output_device': self.output_device,
            'input_channels': self.input_channels,
            'output_channels': self.output_channels
        }
        
        self.round_trip_latency = latency_samples
        self.gain_compensation = gain_compensation
        
        self.logger.info(f"Calibration complete:")
        self.logger.info(f"  Latency: {latency_ms:.1f}ms ({latency_samples} samples)")
        self.logger.info(f"  Gain compensation: {gain_compensation:.3f}")
        
        return self.calibration_data
    
    def _measure_latency(self, sent_signal: np.ndarray, received_signal: np.ndarray) -> int:
        """
        Measure round-trip latency using cross-correlation.
        
        Args:
            sent_signal: Original signal sent to output
            received_signal: Signal recorded from input
            
        Returns:
            Latency in samples
        """
        # Find the best alignment using cross-correlation
        correlation = np.correlate(received_signal, sent_signal, mode='full')
        
        # Find the peak (best alignment)
        peak_idx = np.argmax(np.abs(correlation))
        
        # Calculate latency (offset from center)
        center_idx = len(sent_signal) - 1
        latency = peak_idx - center_idx
        
        # Ensure positive latency
        if latency < 0:
            latency = 0
        
        return int(latency)
    
    def save_calibration(self, filepath: str) -> None:
        """
        Save calibration data to file.
        
        Args:
            filepath: Path to save calibration JSON file
        """
        if not self.calibration_data:
            raise RuntimeError("No calibration data to save")
        
        with open(filepath, 'w') as f:
            json.dump(self.calibration_data, f, indent=2)
        
        self.logger.info(f"Calibration saved to {filepath}")
    
    def load_calibration(self, filepath: str) -> None:
        """
        Load calibration data from file.
        
        Args:
            filepath: Path to calibration JSON file
        """
        with open(filepath, 'r') as f:
            self.calibration_data = json.load(f)
        
        self.round_trip_latency = self.calibration_data['latency_samples']
        self.gain_compensation = self.calibration_data['gain_compensation']
        
        self.logger.info(f"Calibration loaded from {filepath}")
        self.logger.info(f"  Latency: {self.calibration_data['latency_ms']:.1f}ms")
        self.logger.info(f"  Gain compensation: {self.gain_compensation:.3f}")
    
    def play_and_record(self, audio_data: np.ndarray, 
                       duration: Optional[float] = None) -> np.ndarray:
        """
        Play audio and record the return signal.
        
        Args:
            audio_data: Audio signal to play
            duration: Recording duration (if None, uses audio_data length)
            
        Returns:
            Recorded audio signal
        """
        if self.input_device is None or self.output_device is None:
            raise RuntimeError("Audio devices must be set before play/record")
        
        if duration is None:
            duration = len(audio_data) / self.sample_rate
        
        # Apply gain compensation
        compensated_audio = audio_data * self.gain_compensation
        
        self.logger.debug(f"Playing {len(compensated_audio)} samples, recording {duration:.2f}s")
        
        # Record while playing
        recorded = sd.playrec(
            compensated_audio,
            samplerate=self.sample_rate,
            input_device=self.input_device,
            output_device=self.output_device,
            channels=max(len(self.input_channels), len(self.output_channels))
        )
        
        sd.wait()  # Wait for completion
        
        # Convert to mono and apply latency compensation
        recorded = recorded.flatten()
        
        if self.round_trip_latency > 0:
            # Remove latency offset
            recorded = recorded[self.round_trip_latency:]
        
        return recorded
    
    def load_di_signal(self, filepath: str) -> np.ndarray:
        """
        Load a DI (Direct Input) signal for re-amping.
        
        Args:
            filepath: Path to DI audio file
            
        Returns:
            Loaded audio signal
        """
        audio_data, sr = sf.read(filepath)
        
        if sr != self.sample_rate:
            self.logger.warning(f"Sample rate mismatch: file={sr}Hz, system={self.sample_rate}Hz")
        
        # Ensure mono
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val * 0.8
        
        self.logger.info(f"Loaded DI signal: {len(audio_data)} samples, {len(audio_data)/self.sample_rate:.2f}s")
        
        return audio_data
    
    def save_recorded_signal(self, audio_data: np.ndarray, filepath: str) -> None:
        """
        Save recorded audio signal to file.
        
        Args:
            audio_data: Audio signal to save
            filepath: Path to save the audio file
        """
        sf.write(filepath, audio_data, self.sample_rate)
        self.logger.info(f"Recorded signal saved to {filepath}")
    
    def close(self):
        """Close audio streams and cleanup."""
        if self.input_stream:
            self.input_stream.close()
        if self.output_stream:
            self.output_stream.close()
        
        sd.stop()
        self.logger.info("Audio device manager closed")


def list_audio_devices() -> None:
    """List available audio devices for debugging."""
    manager = AudioDeviceManager()
    devices = manager.list_audio_devices()
    
    print("🎤 Input Devices:")
    for device in devices['input']:
        print(f"  {device['id']}: {device['name']} ({device['channels_in']} channels)")
    
    print("\n🔊 Output Devices:")
    for device in devices['output']:
        print(f"  {device['id']}: {device['name']} ({device['channels_out']} channels)")


if __name__ == "__main__":
    # Demo: List audio devices
    list_audio_devices()
