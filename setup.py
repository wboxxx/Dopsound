#!/usr/bin/env python3
"""
Setup script for Magicstomp Audio Pipeline
==========================================

Script d'installation et de configuration du pipeline Audio → Magicstomp.
"""

from setuptools import setup, find_packages
import sys

# Vérifie la version Python
if sys.version_info < (3, 10):
    print("❌ Python 3.10+ requis")
    sys.exit(1)

setup(
    name="magicstomp-audio-pipeline",
    version="1.0.0",
    description="Pipeline Audio → Magicstomp Patch Generator",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Magicstomp Assistant",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "librosa>=0.10.1",
        "mido>=1.3.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "pedalboard>=0.7.4",
        "soundfile>=0.12.1",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "analyze2json=analyze2json:main",
            "adapter-magicstomp=adapter_magicstomp:main",
            "analyze2stomp=cli.analyze2stomp:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Musicians",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="audio analysis guitar effects magicstomp yamaha midi sysex",
)
