"""
Analyzers Package - Dual Backend Audio Analysis
==============================================

Provides interchangeable audio analysis backends:
- LibrosaAnalyzer: Pure Python implementation
- EssentiaAnalyzer: C++ core with Python bindings

Usage:
    from analyzers.factory import get_analyzer
    analyzer = get_analyzer('auto')  # Auto-detect best available
    features = analyzer.analyze(audio_file)
"""

__version__ = "1.0.0"
__author__ = "Magicstomp Assistant"
