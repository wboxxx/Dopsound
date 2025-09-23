"""
Simple Effects Widgets
======================

Widgets pour les effets simples du Magicstomp manquants.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class DigitalDistortionWidget(BaseEffectWidget):
    """Widget pour l'effet digital distortion du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface de la digital distortion."""
        # Titre
        title = ttk.Label(self, text="Digital Distortion", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["Distortion1", "Distortion2", "Overdrive1", "Overdrive2", "Crunch"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Drive
        self.create_parameter_widget(
            "Drive",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Master
        self.create_parameter_widget(
            "Master",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Tone
        self.create_parameter_widget(
            "Tone",
            param_type="spinbox",
            min_val=-10,
            max_val=10,
            step=1,
            offset=3,
            length=1,
            conversion="scaleAndAdd(1, -10)",
            row=2, column=2
        )
        
        # Noise Gate
        self.create_parameter_widget(
            "Noise Gate",
            param_type="spinbox",
            min_val=0,
            max_val=20,
            step=1,
            offset=4,
            length=1,
            row=3, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres de la digital distortion."""
        params = {}
        
        # Digital Distortion parameters
        params['type'] = self.get_parameter_value("Type")
        params['drive'] = self.get_parameter_value("Drive")
        params['master'] = self.get_parameter_value("Master")
        params['tone'] = self.get_parameter_value("Tone")
        params['noise_gate'] = self.get_parameter_value("Noise Gate")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres de la digital distortion."""
        # Digital Distortion parameters
        if 'type' in params:
            self.set_parameter_value("Type", params['type'])
        if 'drive' in params:
            self.set_parameter_value("Drive", params['drive'])
        if 'master' in params:
            self.set_parameter_value("Master", params['master'])
        if 'tone' in params:
            self.set_parameter_value("Tone", params['tone'])
        if 'noise_gate' in params:
            self.set_parameter_value("Noise Gate", params['noise_gate'])


class SymphonicWidget(BaseEffectWidget):
    """Widget pour l'effet symphonic du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du symphonic."""
        # Titre
        title = ttk.Label(self, text="Symphonic", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            values=["Sine", "Triangle"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.00,
            step=0.05,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Mod. Delay
        self.create_parameter_widget(
            "Mod. Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=500.0,
            step=0.1,
            suffix=" ms",
            offset=3,
            length=1,
            conversion="logScale",
            row=2, column=2
        )
        
        # LSH Freq.
        self.create_parameter_widget(
            "LSH Freq.",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=0.1,
            suffix=" Hz",
            offset=4,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # LSH Gain
        self.create_parameter_widget(
            "LSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # EQ Freq.
        self.create_parameter_widget(
            "EQ Freq.",
            param_type="double_spinbox",
            min_val=100.0,
            max_val=8000.0,
            step=1.0,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=4, column=0
        )
        
        # EQ Gain
        self.create_parameter_widget(
            "EQ Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # EQ Q
        self.create_parameter_widget(
            "EQ Q",
            param_type="double_spinbox",
            min_val=0.10,
            max_val=10.0,
            step=0.01,
            offset=8,
            length=1,
            conversion="logScale",
            row=5, column=0
        )
        
        # HSH Freq.
        self.create_parameter_widget(
            "HSH Freq.",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=1.0,
            suffix=" Hz",
            offset=9,
            length=1,
            conversion="logScale",
            row=5, column=2
        )
        
        # HSH Gain
        self.create_parameter_widget(
            "HSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=11,
            length=1,
            row=6, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du symphonic."""
        params = {}
        
        # Symphonic parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['freq'] = self.get_parameter_value("Freq.")
        params['depth'] = self.get_parameter_value("Depth")
        params['mod_delay'] = self.get_parameter_value("Mod. Delay")
        params['lsh_freq'] = self.get_parameter_value("LSH Freq.")
        params['lsh_gain'] = self.get_parameter_value("LSH Gain")
        params['eq_freq'] = self.get_parameter_value("EQ Freq.")
        params['eq_gain'] = self.get_parameter_value("EQ Gain")
        params['eq_q'] = self.get_parameter_value("EQ Q")
        params['hsh_freq'] = self.get_parameter_value("HSH Freq.")
        params['hsh_gain'] = self.get_parameter_value("HSH Gain")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du symphonic."""
        # Symphonic parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'mod_delay' in params:
            self.set_parameter_value("Mod. Delay", params['mod_delay'])
        if 'lsh_freq' in params:
            self.set_parameter_value("LSH Freq.", params['lsh_freq'])
        if 'lsh_gain' in params:
            self.set_parameter_value("LSH Gain", params['lsh_gain'])
        if 'eq_freq' in params:
            self.set_parameter_value("EQ Freq.", params['eq_freq'])
        if 'eq_gain' in params:
            self.set_parameter_value("EQ Gain", params['eq_gain'])
        if 'eq_q' in params:
            self.set_parameter_value("EQ Q", params['eq_q'])
        if 'hsh_freq' in params:
            self.set_parameter_value("HSH Freq.", params['hsh_freq'])
        if 'hsh_gain' in params:
            self.set_parameter_value("HSH Gain", params['hsh_gain'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class AutoPanWidget(BaseEffectWidget):
    """Widget pour l'effet auto pan du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface de l'auto pan."""
        # Titre
        title = ttk.Label(self, text="Auto Pan", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            values=["Sine", "Triangle"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.00,
            step=0.05,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres de l'auto pan."""
        params = {}
        
        # Auto Pan parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['freq'] = self.get_parameter_value("Freq.")
        params['depth'] = self.get_parameter_value("Depth")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres de l'auto pan."""
        # Auto Pan parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class RotaryWidget(BaseEffectWidget):
    """Widget pour l'effet rotary du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du rotary."""
        # Titre
        title = ttk.Label(self, text="Rotary", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Speed
        self.create_parameter_widget(
            "Speed",
            param_type="combobox",
            values=["Slow", "Fast"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=1,
            length=1,
            row=1, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du rotary."""
        params = {}
        
        # Rotary parameters
        params['speed'] = self.get_parameter_value("Speed")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du rotary."""
        # Rotary parameters
        if 'speed' in params:
            self.set_parameter_value("Speed", params['speed'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class RingModWidget(BaseEffectWidget):
    """Widget pour l'effet ring modulator du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du ring modulator."""
        # Titre
        title = ttk.Label(self, text="Ring Modulator", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=20.0,
            max_val=8000.0,
            step=1.0,
            suffix=" Hz",
            offset=0,
            length=1,
            conversion="logScale",
            row=1, column=0
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=1,
            length=1,
            row=1, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du ring modulator."""
        params = {}
        
        # Ring Modulator parameters
        params['freq'] = self.get_parameter_value("Freq.")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du ring modulator."""
        # Ring Modulator parameters
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class VintageFlangeWidget(BaseEffectWidget):
    """Widget pour l'effet vintage flange du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du vintage flange."""
        # Titre
        title = ttk.Label(self, text="Vintage Flange", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["1", "2", "3"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Speed
        self.create_parameter_widget(
            "Speed",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Manual
        self.create_parameter_widget(
            "Manual",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Spread
        self.create_parameter_widget(
            "Spread",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du vintage flange."""
        params = {}
        
        # Vintage Flange parameters
        params['type'] = self.get_parameter_value("Type")
        params['speed'] = self.get_parameter_value("Speed")
        params['depth'] = self.get_parameter_value("Depth")
        params['manual'] = self.get_parameter_value("Manual")
        params['feedback'] = self.get_parameter_value("Feedback")
        params['spread'] = self.get_parameter_value("Spread")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du vintage flange."""
        # Vintage Flange parameters
        if 'type' in params:
            self.set_parameter_value("Type", params['type'])
        if 'speed' in params:
            self.set_parameter_value("Speed", params['speed'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'manual' in params:
            self.set_parameter_value("Manual", params['manual'])
        if 'feedback' in params:
            self.set_parameter_value("Feedback", params['feedback'])
        if 'spread' in params:
            self.set_parameter_value("Spread", params['spread'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])
