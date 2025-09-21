#!/usr/bin/env python3
"""
Test Factory and Backend Selection
=================================

Tests for the analyzer factory and backend selection logic.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analyzers.factory import AnalyzerFactory, get_analyzer, get_available_backends
from analyzers.librosa_backend import LibrosaAnalyzer


class TestAnalyzerFactory(unittest.TestCase):
    """Test the analyzer factory functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.factory = AnalyzerFactory()
    
    def test_factory_initialization(self):
        """Test factory initialization."""
        self.assertIsInstance(self.factory, AnalyzerFactory)
        self.assertIsNotNone(self.factory.logger)
    
    def test_get_available_backends(self):
        """Test getting available backends."""
        backends = self.factory.get_available_backends()
        self.assertIsInstance(backends, dict)
        self.assertIn('librosa', backends)
        self.assertIn('essentia', backends)
        self.assertIsInstance(backends['librosa'], bool)
        self.assertIsInstance(backends['essentia'], bool)
    
    def test_librosa_analyzer_creation(self):
        """Test creating Librosa analyzer."""
        if self.factory.get_available_backends()['librosa']:
            analyzer = self.factory.create_analyzer('librosa')
            self.assertIsInstance(analyzer, LibrosaAnalyzer)
            self.assertEqual(analyzer.sample_rate, 44100)
    
    def test_auto_selection_logic(self):
        """Test auto-selection logic."""
        backends = self.factory.get_available_backends()
        
        # Test auto selection
        try:
            analyzer = self.factory.create_analyzer('auto')
            self.assertIsNotNone(analyzer)
            
            # Should prefer Essentia if available, else librosa
            if backends['essentia']:
                self.assertEqual(analyzer.get_backend_name(), 'essentia')
            elif backends['librosa']:
                self.assertEqual(analyzer.get_backend_name(), 'librosa')
        except RuntimeError as e:
            # Should only fail if no backends are available
            self.assertFalse(backends['librosa'] and backends['essentia'])
    
    def test_invalid_backend_selection(self):
        """Test invalid backend selection."""
        with self.assertRaises(ValueError):
            self.factory.create_analyzer('invalid_backend')
    
    def test_unavailable_backend_selection(self):
        """Test selection of unavailable backend."""
        backends = self.factory.get_available_backends()
        
        if not backends['essentia']:
            with self.assertRaises(RuntimeError):
                self.factory.create_analyzer('essentia')
        
        if not backends['librosa']:
            with self.assertRaises(RuntimeError):
                self.factory.create_analyzer('librosa')


class TestFactoryFunctions(unittest.TestCase):
    """Test factory convenience functions."""
    
    def test_get_analyzer_function(self):
        """Test the get_analyzer convenience function."""
        try:
            analyzer = get_analyzer('auto')
            self.assertIsNotNone(analyzer)
        except RuntimeError:
            # Skip if no backends available
            pass
    
    def test_get_available_backends_function(self):
        """Test the get_available_backends convenience function."""
        backends = get_available_backends()
        self.assertIsInstance(backends, dict)
        self.assertIn('librosa', backends)
        self.assertIn('essentia', backends)


class TestBackendAvailability(unittest.TestCase):
    """Test backend availability detection."""
    
    def test_librosa_availability(self):
        """Test Librosa backend availability."""
        try:
            from analyzers.librosa_backend import LibrosaAnalyzer
            analyzer = LibrosaAnalyzer()
            self.assertIsNotNone(analyzer)
        except ImportError:
            self.fail("Librosa backend should be available")
    
    def test_essentia_availability(self):
        """Test Essentia backend availability."""
        try:
            from analyzers.essentia_backend import EssentiaAnalyzer, ESSENTIA_AVAILABLE
            if ESSENTIA_AVAILABLE:
                analyzer = EssentiaAnalyzer()
                self.assertIsNotNone(analyzer)
            else:
                self.skipTest("Essentia not available")
        except ImportError:
            self.skipTest("Essentia not installed")


class TestBackendSelection(unittest.TestCase):
    """Test backend selection from arguments and environment."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear environment variables
        self.original_env = os.environ.get('AUDIO_BACKEND')
        if 'AUDIO_BACKEND' in os.environ:
            del os.environ['AUDIO_BACKEND']
    
    def tearDown(self):
        """Clean up test environment."""
        if self.original_env is not None:
            os.environ['AUDIO_BACKEND'] = self.original_env
    
    def test_environment_variable_selection(self):
        """Test backend selection from environment variable."""
        # Test with valid backend
        os.environ['AUDIO_BACKEND'] = 'librosa'
        
        # Mock argparse Namespace
        from argparse import Namespace
        args = Namespace()
        
        from analyzers.factory import select_backend_from_args
        backend = select_backend_from_args(args)
        
        self.assertEqual(backend, 'librosa')
    
    def test_environment_variable_auto(self):
        """Test environment variable with auto selection."""
        os.environ['AUDIO_BACKEND'] = 'auto'
        
        from argparse import Namespace
        args = Namespace()
        
        from analyzers.factory import select_backend_from_args
        backend = select_backend_from_args(args)
        
        self.assertEqual(backend, 'auto')
    
    def test_default_selection(self):
        """Test default backend selection."""
        # No environment variable set
        from argparse import Namespace
        args = Namespace()
        
        from analyzers.factory import select_backend_from_args
        backend = select_backend_from_args(args)
        
        self.assertEqual(backend, 'auto')


if __name__ == '__main__':
    unittest.main()
