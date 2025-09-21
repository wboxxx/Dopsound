#!/usr/bin/env python3
"""
Auto Tone Match Magicstomp
==========================

Automated audio analysis and Magicstomp patch generation with dual backend support.
Uses either Essentia (C++ core) or librosa (pure Python) for audio analysis.

Usage:
    python auto_tone_match_magicstomp.py input.wav --backend auto
    python auto_tone_match_magicstomp.py input.wav --backend essentia --send
    python auto_tone_match_magicstomp.py input.wav --backend librosa --verbose

Features:
- Dual backend audio analysis (Essentia + librosa)
- Automatic effect detection and parameter mapping
- Magicstomp SysEx generation and USB-MIDI support
- Runtime backend selection with graceful fallback
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any

from analyzers.factory import get_analyzer, select_backend_from_args, setup_backend_logging, get_available_backends
from adapter_magicstomp import MagicstompAdapter


class AutoToneMatcher:
    """
    Automated tone matching system for Magicstomp patches.
    
    Analyzes audio files and generates compatible Magicstomp patches
    using dual backend audio analysis.
    """
    
    def __init__(self, backend: str = 'auto', sample_rate: int = 44100):
        """
        Initialize the tone matcher.
        
        Args:
            backend: Audio analysis backend ('auto', 'essentia', 'librosa')
            sample_rate: Target sample rate for analysis
        """
        self.sample_rate = sample_rate
        self.logger = logging.getLogger(__name__)
        
        # Create analyzer
        try:
            self.analyzer = get_analyzer(backend, sample_rate)
            self.backend_name = self.analyzer.get_backend_name()
            self.logger.info(f"Initialized analyzer with {self.backend_name} backend")
        except Exception as e:
            self.logger.error(f"Failed to create analyzer: {e}")
            raise
        
        # Create Magicstomp adapter
        self.adapter = MagicstompAdapter()
        
        # Analysis results
        self.features = {}
        self.patch = {}
    
    def analyze_audio(self, audio_path: str, verbose: bool = False) -> Dict[str, Any]:
        """
        Analyze audio file and extract features.
        
        Args:
            audio_path: Path to audio file
            verbose: Enable verbose logging
            
        Returns:
            Dictionary of extracted features
        """
        self.logger.info(f"Analyzing audio: {audio_path}")
        
        if verbose:
            self.logger.info(f"Using {self.backend_name} backend")
        
        # Perform analysis
        self.features = self.analyzer.analyze(audio_path)
        
        # Log analysis results
        self._log_analysis_results(verbose)
        
        return self.features
    
    def _log_analysis_results(self, verbose: bool = False) -> None:
        """Log analysis results with detailed explanations."""
        features = self.features
        
        self.logger.info("=== Analysis Results ===")
        
        # Spectral features
        tilt = features.get('spectral_tilt_db', 0)
        centroid = features.get('spectral_centroid_mean', 0)
        self.logger.info(f"Spectral tilt: {tilt:.1f} dB (brightness indicator)")
        self.logger.info(f"Spectral centroid: {centroid:.0f} Hz (frequency center)")
        
        # Distortion
        thd = features.get('thd_proxy', 0)
        if thd > 0.1:
            self.logger.info(f"Distortion detected: THD≈{thd:.3f} (drive level indicator)")
        else:
            self.logger.info("Clean signal detected")
        
        # Delay
        delay_ms, feedback = features.get('onset_delay_ms', (0, 0))
        if delay_ms > 10:
            self.logger.info(f"Delay detected: {delay_ms:.0f}ms, feedback≈{feedback:.2f}")
        else:
            self.logger.info("No significant delay detected")
        
        # Reverb
        decay_s, mix = features.get('reverb_estimate', (0, 0))
        if decay_s > 0.8:
            self.logger.info(f"Reverb detected: decay≈{decay_s:.1f}s, mix≈{mix:.2f}")
        else:
            self.logger.info("No significant reverb detected")
        
        # LFO/Modulation
        lfo_rate, lfo_strength = features.get('lfo_rate_hz', (None, 0))
        if lfo_rate is not None:
            self.logger.info(f"Modulation detected: {lfo_rate:.2f}Hz, strength≈{lfo_strength:.2f}")
        else:
            self.logger.info("No significant modulation detected")
        
        # Tempo
        tempo = features.get('tempo_bpm')
        if tempo is not None:
            self.logger.info(f"Tempo detected: {tempo:.1f} BPM")
        else:
            self.logger.info("No clear tempo detected")
        
        if verbose:
            self.logger.debug("Full features: " + json.dumps(features, indent=2))
    
    def map_to_patch(self) -> Dict[str, Any]:
        """
        Map extracted features to Magicstomp patch parameters.
        
        Returns:
            Magicstomp patch configuration
        """
        self.logger.info("Mapping features to Magicstomp patch...")
        
        features = self.features
        
        # Map amplifier settings
        amp_config = self._map_amplifier(features)
        
        # Map booster settings
        booster_config = self._map_booster(features)
        
        # Map delay settings
        delay_config = self._map_delay(features)
        
        # Map reverb settings
        reverb_config = self._map_reverb(features)
        
        # Map modulation settings
        mod_config = self._map_modulation(features)
        
        # Create complete patch
        self.patch = {
            "amp": amp_config,
            "booster": booster_config,
            "delay": delay_config,
            "reverb": reverb_config,
            "mod": mod_config,
            "meta": {
                "backend": self.backend_name,
                "analysis_version": "2.0",
                "features": features
            }
        }
        
        self.logger.info("Patch mapping complete")
        return self.patch
    
    def _map_amplifier(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Map features to amplifier settings."""
        tilt = features.get('spectral_tilt_db', 0)
        centroid = features.get('spectral_centroid_mean', 2000)
        thd = features.get('thd_proxy', 0)
        
        # Select amplifier model based on spectral characteristics
        if tilt > 5 and centroid > 3000:
            amp_model = "BRIT_TOP_BOOST"
            cab = "2x12_ALNICO"
        elif tilt < -5 and centroid < 2000:
            amp_model = "TWEED_BASSMAN"
            cab = "4x10_TWEED"
        else:
            amp_model = "JCM800"
            cab = "4x12_VINTAGE"
        
        # Map gain based on distortion
        if thd > 0.5:
            gain = min(0.9, 0.3 + thd * 0.6)
        else:
            gain = min(0.7, 0.2 + thd * 0.5)
        
        # Map EQ based on spectral characteristics
        treble = min(1.0, max(0.0, (centroid - 1000) / 3000))
        bass = min(1.0, max(0.0, (1500 - centroid) / 1000))
        mid = 0.5 + (centroid - 2000) / 4000
        mid = min(1.0, max(0.0, mid))
        presence = min(1.0, treble * 1.2)
        
        return {
            "model": amp_model,
            "gain": gain,
            "bass": bass,
            "mid": mid,
            "treble": treble,
            "presence": presence,
            "cab": cab
        }
    
    def _map_booster(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Map features to booster settings."""
        tilt = features.get('spectral_tilt_db', 0)
        thd = features.get('thd_proxy', 0)
        
        if tilt > 3 and thd < 0.2:
            booster_type = "TREBLE"
            level = 0.6
        elif thd > 0.3:
            booster_type = "DISTORTION"
            level = 0.4
        else:
            booster_type = "CLEAN"
            level = 0.3
        
        return {
            "type": booster_type,
            "level": level
        }
    
    def _map_delay(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Map features to delay settings."""
        delay_ms, feedback = features.get('onset_delay_ms', (0, 0))
        
        if delay_ms > 10:
            return {
                "enabled": True,
                "time_ms": delay_ms,
                "feedback": feedback,
                "mix": min(0.4, feedback * 0.6)
            }
        else:
            return {"enabled": False}
    
    def _map_reverb(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Map features to reverb settings."""
        decay_s, mix = features.get('reverb_estimate', (0, 0))
        
        if decay_s > 0.8:
            # Determine reverb type based on decay time
            if decay_s > 2.5:
                reverb_type = "HALL"
            elif decay_s > 1.5:
                reverb_type = "PLATE"
            else:
                reverb_type = "ROOM"
            
            return {
                "enabled": True,
                "type": reverb_type,
                "decay_s": min(3.0, decay_s),
                "mix": mix
            }
        else:
            return {"enabled": False}
    
    def _map_modulation(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Map features to modulation settings."""
        lfo_rate, lfo_strength = features.get('lfo_rate_hz', (None, 0))
        
        if lfo_rate is not None and lfo_strength > 0.1:
            # Determine modulation type based on rate
            if lfo_rate < 1.5:
                mod_type = "CHORUS"
            elif lfo_rate < 4.0:
                mod_type = "PHASER"
            else:
                mod_type = "TREMOLO"
            
            return {
                "enabled": True,
                "type": mod_type,
                "rate_hz": lfo_rate,
                "depth": min(0.7, lfo_strength * 3.0),
                "mix": min(0.3, lfo_strength * 2.0)
            }
        else:
            return {"enabled": False}
    
    def save_patch(self, output_path: str) -> None:
        """
        Save patch to JSON file.
        
        Args:
            output_path: Path to output JSON file
        """
        self.logger.info(f"Saving patch to {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.patch, f, indent=2, ensure_ascii=False)
        
        self.logger.info("Patch saved successfully")
    
    def generate_syx(self, patch_number: int = 0) -> list:
        """
        Generate SysEx data from patch.
        
        Args:
            patch_number: Magicstomp patch number
            
        Returns:
            SysEx data bytes
        """
        self.logger.info(f"Generating SysEx for patch #{patch_number}")
        
        syx_data = self.adapter.json_to_syx(self.patch, patch_number)
        
        self.logger.info(f"Generated {len(syx_data)} bytes of SysEx data")
        return syx_data
    
    def save_syx(self, syx_data: list, output_path: str) -> None:
        """
        Save SysEx data to file.
        
        Args:
            syx_data: SysEx data bytes
            output_path: Path to output .syx file
        """
        self.logger.info(f"Saving SysEx to {output_path}")
        
        self.adapter.save_to_file(syx_data, output_path)
        
        self.logger.info("SysEx file saved successfully")
    
    def send_to_device(self, syx_data: list) -> bool:
        """
        Send SysEx data to Magicstomp device.
        
        Args:
            syx_data: SysEx data bytes
            
        Returns:
            True if successful
        """
        self.logger.info("Sending patch to Magicstomp device...")
        
        success = self.adapter.send_to_device(syx_data)
        
        if success:
            self.logger.info("Patch sent successfully")
        else:
            self.logger.warning("Failed to send patch to device")
        
        return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Auto Tone Match Magicstomp - Dual Backend Audio Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-select backend and analyze
  python auto_tone_match_magicstomp.py guitar.wav

  # Force Essentia backend with verbose output
  python auto_tone_match_magicstomp.py guitar.wav --backend essentia --verbose

  # Force Librosa backend and send to device
  python auto_tone_match_magicstomp.py guitar.wav --backend librosa --send

  # Generate SysEx file with custom patch number
  python auto_tone_match_magicstomp.py guitar.wav --syx output.syx --patch 5

  # Check available backends
  python auto_tone_match_magicstomp.py --list-backends
        """
    )
    
    # Input file
    parser.add_argument('input', nargs='?', help='Input audio file')
    
    # Backend selection
    parser.add_argument('--backend', choices=['auto', 'essentia', 'librosa'],
                       default='auto', help='Audio analysis backend')
    
    # Output options
    parser.add_argument('--output', '-o', help='Output JSON file')
    parser.add_argument('--syx', help='Output SysEx file')
    parser.add_argument('--patch', '-p', type=int, default=0,
                       help='Magicstomp patch number (0-99)')
    
    # Device options
    parser.add_argument('--send', action='store_true',
                       help='Send patch directly to Magicstomp device')
    
    # Utility options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--list-backends', action='store_true',
                       help='List available backends and exit')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_backend_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # List backends if requested
    if args.list_backends:
        logger.info("Available backends:")
        backends = get_available_backends()
        for name, available in backends.items():
            status = "✅ Available" if available else "❌ Not available"
            logger.info(f"  {name}: {status}")
        return
    
    # Check input file
    if not args.input:
        parser.error("Input audio file is required")
    
    if not Path(args.input).exists():
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)
    
    try:
        # Create tone matcher
        tone_matcher = AutoToneMatcher(args.backend)
        
        # Analyze audio
        features = tone_matcher.analyze_audio(args.input, args.verbose)
        
        # Map to patch
        patch = tone_matcher.map_to_patch()
        
        # Save JSON if requested
        if args.output:
            tone_matcher.save_patch(args.output)
        elif not args.syx and not args.send:
            # Auto-generate JSON filename
            auto_json = Path(args.input).with_suffix('.json')
            tone_matcher.save_patch(str(auto_json))
        
        # Generate and save SysEx if requested
        if args.syx or args.send:
            syx_data = tone_matcher.generate_syx(args.patch)
            
            if args.syx:
                tone_matcher.save_syx(syx_data, args.syx)
            
            if args.send:
                tone_matcher.send_to_device(syx_data)
        
        logger.info("Processing complete!")
        
        # Print summary
        if args.verbose:
            logger.info("=== Summary ===")
            logger.info(f"Backend: {tone_matcher.backend_name}")
            logger.info(f"Input: {args.input}")
            if args.output:
                logger.info(f"JSON: {args.output}")
            if args.syx:
                logger.info(f"SysEx: {args.syx}")
            if args.send:
                logger.info(f"Sent to device (patch #{args.patch})")
    
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
