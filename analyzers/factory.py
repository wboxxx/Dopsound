#!/usr/bin/env python3
"""
Audio Analyzer Factory
======================

Factory for creating audio analyzer backends with automatic fallback.
Supports runtime selection via CLI flags, environment variables, or auto-detection.
"""

import os
import logging
from typing import Optional, Dict, Any
from argparse import Namespace

from .base import AudioAnalyzer

# Try to import backends
try:
    from .librosa_backend import LibrosaAnalyzer
    LIBROSA_AVAILABLE = True
except ImportError as e:
    LIBROSA_AVAILABLE = False
    LibrosaAnalyzer = None

try:
    from .essentia_backend import EssentiaAnalyzer, ESSENTIA_AVAILABLE
except ImportError as e:
    ESSENTIA_AVAILABLE = False
    EssentiaAnalyzer = None


class AnalyzerFactory:
    """
    Factory for creating audio analyzer instances.
    
    Handles backend selection, availability checking, and graceful fallback.
    """
    
    def __init__(self):
        """Initialize the factory."""
        self.logger = logging.getLogger(__name__)
        self._check_availability()
    
    def _check_availability(self) -> None:
        """Check which backends are available and log status."""
        self.logger.info("Checking backend availability:")
        
        if LIBROSA_AVAILABLE:
            self.logger.info("  ✅ Librosa backend available")
        else:
            self.logger.warning("  ❌ Librosa backend unavailable")
        
        if ESSENTIA_AVAILABLE:
            self.logger.info("  ✅ Essentia backend available")
        else:
            self.logger.warning("  ❌ Essentia backend unavailable")
        
        if not LIBROSA_AVAILABLE and not ESSENTIA_AVAILABLE:
            self.logger.error("  🚨 No backends available! Install librosa or essentia.")
    
    def get_available_backends(self) -> Dict[str, bool]:
        """
        Get dictionary of available backends.
        
        Returns:
            Dictionary mapping backend names to availability
        """
        return {
            'librosa': LIBROSA_AVAILABLE,
            'essentia': ESSENTIA_AVAILABLE
        }
    
    def create_analyzer(self, preferred: Optional[str] = None, 
                       sample_rate: int = 44100) -> AudioAnalyzer:
        """
        Create an audio analyzer instance.
        
        Args:
            preferred: Preferred backend ('librosa', 'essentia', 'auto', or None)
            sample_rate: Target sample rate for analysis
            
        Returns:
            AudioAnalyzer instance
            
        Raises:
            RuntimeError: If no backends are available
        """
        # Determine backend selection
        backend = self._select_backend(preferred)
        
        # Create analyzer instance
        if backend == 'librosa':
            if not LIBROSA_AVAILABLE:
                raise RuntimeError("Librosa backend requested but not available")
            analyzer = LibrosaAnalyzer(sample_rate)
            self.logger.info("Created Librosa analyzer")
            
        elif backend == 'essentia':
            if not ESSENTIA_AVAILABLE:
                raise RuntimeError("Essentia backend requested but not available")
            analyzer = EssentiaAnalyzer(sample_rate)
            self.logger.info("Created Essentia analyzer")
            
        else:
            raise RuntimeError(f"Unknown backend: {backend}")
        
        return analyzer
    
    def _select_backend(self, preferred: Optional[str] = None) -> str:
        """
        Select the best available backend based on preference.
        
        Args:
            preferred: Preferred backend name or 'auto'
            
        Returns:
            Selected backend name
        """
        # Handle auto selection
        if preferred == 'auto' or preferred is None:
            # Try Essentia first (faster), then fallback to Librosa
            if ESSENTIA_AVAILABLE:
                self.logger.info("Auto-selected Essentia backend")
                return 'essentia'
            elif LIBROSA_AVAILABLE:
                self.logger.info("Auto-selected Librosa backend (fallback)")
                return 'librosa'
            else:
                raise RuntimeError("No backends available for auto-selection")
        
        # Handle specific backend selection
        if preferred == 'librosa':
            if LIBROSA_AVAILABLE:
                return 'librosa'
            else:
                raise RuntimeError("Librosa backend not available")
        
        elif preferred == 'essentia':
            if ESSENTIA_AVAILABLE:
                return 'essentia'
            else:
                raise RuntimeError("Essentia backend not available")
        
        else:
            raise ValueError(f"Invalid backend preference: {preferred}")


# Global factory instance
_factory = AnalyzerFactory()


def get_analyzer(preferred: Optional[str] = None, sample_rate: int = 44100) -> AudioAnalyzer:
    """
    Get an audio analyzer instance using the global factory.
    
    This is the main entry point for creating analyzers.
    
    Args:
        preferred: Preferred backend ('librosa', 'essentia', 'auto', or None)
        sample_rate: Target sample rate for analysis
        
    Returns:
        AudioAnalyzer instance
        
    Examples:
        # Auto-select best available backend
        analyzer = get_analyzer()
        
        # Force Essentia backend
        analyzer = get_analyzer('essentia')
        
        # Force Librosa backend
        analyzer = get_analyzer('librosa')
        
        # Custom sample rate
        analyzer = get_analyzer('auto', sample_rate=48000)
    """
    return _factory.create_analyzer(preferred, sample_rate)


def get_available_backends() -> Dict[str, bool]:
    """
    Get information about available backends.
    
    Returns:
        Dictionary mapping backend names to availability
    """
    return _factory.get_available_backends()


def select_backend_from_args(args: Namespace) -> str:
    """
    Select backend from command line arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Selected backend name
    """
    # Priority: CLI flag > Environment variable > default
    backend = None
    
    # Check CLI flag
    if hasattr(args, 'backend') and args.backend:
        backend = args.backend
    
    # Check environment variable
    if backend is None:
        backend = os.environ.get('AUDIO_BACKEND')
    
    # Default to auto
    if backend is None:
        backend = 'auto'
    
    return backend


def setup_backend_logging(verbose: bool = False) -> None:
    """
    Setup logging for backend selection and analysis.
    
    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Set backend-specific log levels
    if verbose:
        logging.getLogger('analyzers').setLevel(logging.DEBUG)
        logging.getLogger('LibrosaAnalyzer').setLevel(logging.DEBUG)
        logging.getLogger('EssentiaAnalyzer').setLevel(logging.DEBUG)
    else:
        logging.getLogger('analyzers').setLevel(logging.INFO)


# Convenience functions for common use cases
def create_librosa_analyzer(sample_rate: int = 44100) -> AudioAnalyzer:
    """Create a Librosa analyzer instance."""
    return get_analyzer('librosa', sample_rate)


def create_essentia_analyzer(sample_rate: int = 44100) -> AudioAnalyzer:
    """Create an Essentia analyzer instance."""
    return get_analyzer('essentia', sample_rate)


def create_auto_analyzer(sample_rate: int = 44100) -> AudioAnalyzer:
    """Create an auto-selected analyzer instance."""
    return get_analyzer('auto', sample_rate)
