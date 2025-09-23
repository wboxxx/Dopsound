"""
Modulation Effect Widgets
========================

Widgets spécialisés pour les effets de modulation du Magicstomp.
Adaptés des widgets C++/Qt correspondants.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class ChorusWidget(BaseEffectWidget):
    """Widget pour l'effet chorus du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du chorus."""
        # Titre
        title = ttk.Label(self, text="Chorus", font=("Arial", 12, "bold"))
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
            max_val=40.0,
            step=0.05,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="freqHz",
            row=1, column=2
        )
        
        # AM Depth
        self.create_parameter_widget(
            "AM Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # PM Depth
        self.create_parameter_widget(
            "PM Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Mod. Delay
        self.create_parameter_widget(
            "Mod. Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=500.0,
            step=0.1,
            suffix=" ms",
            offset=4,
            length=1,
            conversion="timeMs",
            row=3, column=0
        )
        
        # LSH Freq.
        self.create_parameter_widget(
            "LSH Freq.",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=5,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # LSH Gain
        self.create_parameter_widget(
            "LSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # EQ Freq.
        self.create_parameter_widget(
            "EQ Freq.",
            param_type="double_spinbox",
            min_val=100.0,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=7,
            length=1,
            conversion="logScale",
            row=4, column=2
        )
        
        # EQ Gain
        self.create_parameter_widget(
            "EQ Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # EQ Q
        self.create_parameter_widget(
            "EQ Q",
            param_type="double_spinbox",
            min_val=0.10,
            max_val=10.0,
            step=0.1,
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # HSH Freq.
        self.create_parameter_widget(
            "HSH Freq.",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=10,
            length=1,
            conversion="logScale",
            row=6, column=0
        )
        
        # HSH Gain
        self.create_parameter_widget(
            "HSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=12,
            length=1,
            row=7, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du chorus."""
        params = {}
        
        # Chorus parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['freq'] = self.get_parameter_value("Freq.")
        params['am_depth'] = self.get_parameter_value("AM Depth")
        params['pm_depth'] = self.get_parameter_value("PM Depth")
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
        """Applique tous les paramètres du chorus."""
        # Chorus parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'am_depth' in params:
            self.set_parameter_value("AM Depth", params['am_depth'])
        if 'pm_depth' in params:
            self.set_parameter_value("PM Depth", params['pm_depth'])
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


class FlangeWidget(BaseEffectWidget):
    """Widget pour l'effet flanger du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du flanger."""
        # Titre
        title = ttk.Label(self, text="Flanger", font=("Arial", 12, "bold"))
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
            max_val=40.0,
            step=0.05,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="freqHz",
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
        
        # FB. Gain
        self.create_parameter_widget(
            "FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=3,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=2, column=2
        )
        
        # Mod. Delay
        self.create_parameter_widget(
            "Mod. Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=500.0,
            step=0.1,
            suffix=" ms",
            offset=5,
            length=1,
            conversion="timeMs",
            row=3, column=0
        )
        
        # LSH Freq.
        self.create_parameter_widget(
            "LSH Freq.",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # LSH Gain
        self.create_parameter_widget(
            "LSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=7,
            length=1,
            row=4, column=0
        )
        
        # EQ Freq.
        self.create_parameter_widget(
            "EQ Freq.",
            param_type="double_spinbox",
            min_val=100.0,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=8,
            length=1,
            conversion="logScale",
            row=4, column=2
        )
        
        # EQ Gain
        self.create_parameter_widget(
            "EQ Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=9,
            length=1,
            row=5, column=0
        )
        
        # EQ Q
        self.create_parameter_widget(
            "EQ Q",
            param_type="double_spinbox",
            min_val=0.10,
            max_val=10.0,
            step=0.1,
            offset=10,
            length=1,
            row=5, column=2
        )
        
        # HSH Freq.
        self.create_parameter_widget(
            "HSH Freq.",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=11,
            length=1,
            conversion="logScale",
            row=6, column=0
        )
        
        # HSH Gain
        self.create_parameter_widget(
            "HSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=12,
            length=1,
            row=6, column=2
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=13,
            length=1,
            row=7, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du flanger."""
        params = {}
        
        # Flanger parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['freq'] = self.get_parameter_value("Freq.")
        params['depth'] = self.get_parameter_value("Depth")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
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
        """Applique tous les paramètres du flanger."""
        # Flanger parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
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


class PhaserWidget(BaseEffectWidget):
    """Widget pour l'effet phaser du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du phaser."""
        # Titre
        title = ttk.Label(self, text="Phaser", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Stage
        self.create_parameter_widget(
            "Stage",
            param_type="combobox",
            values=["2", "4", "6", "8", "10", "12", "14", "16"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.0,
            step=0.05,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="freqHz",
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
        
        # FB. Gain
        self.create_parameter_widget(
            "FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=3,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=2, column=2
        )
        
        # Offset
        self.create_parameter_widget(
            "Offset",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=5,
            length=1,
            row=3, column=0
        )
        
        # Phase
        self.create_parameter_widget(
            "Phase",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=354.38,
            step=0.1,
            suffix=" deg",
            offset=6,
            length=1,
            row=3, column=2
        )
        
        # LSH Freq.
        self.create_parameter_widget(
            "LSH Freq.",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=7,
            length=1,
            conversion="logScale",
            row=4, column=0
        )
        
        # LSH Gain
        self.create_parameter_widget(
            "LSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=8,
            length=1,
            row=4, column=2
        )
        
        # HSH Freq.
        self.create_parameter_widget(
            "HSH Freq.",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=9,
            length=1,
            conversion="logScale",
            row=5, column=0
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
            row=5, column=2
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
            row=6, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du phaser."""
        params = {}
        
        # Phaser parameters
        params['stage'] = self.get_parameter_value("Stage")
        params['freq'] = self.get_parameter_value("Freq.")
        params['depth'] = self.get_parameter_value("Depth")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
        params['offset'] = self.get_parameter_value("Offset")
        params['phase'] = self.get_parameter_value("Phase")
        params['lsh_freq'] = self.get_parameter_value("LSH Freq.")
        params['lsh_gain'] = self.get_parameter_value("LSH Gain")
        params['hsh_freq'] = self.get_parameter_value("HSH Freq.")
        params['hsh_gain'] = self.get_parameter_value("HSH Gain")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du phaser."""
        # Phaser parameters
        if 'stage' in params:
            self.set_parameter_value("Stage", params['stage'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
        if 'offset' in params:
            self.set_parameter_value("Offset", params['offset'])
        if 'phase' in params:
            self.set_parameter_value("Phase", params['phase'])
        if 'lsh_freq' in params:
            self.set_parameter_value("LSH Freq.", params['lsh_freq'])
        if 'lsh_gain' in params:
            self.set_parameter_value("LSH Gain", params['lsh_gain'])
        if 'hsh_freq' in params:
            self.set_parameter_value("HSH Freq.", params['hsh_freq'])
        if 'hsh_gain' in params:
            self.set_parameter_value("HSH Gain", params['hsh_gain'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class TremoloWidget(BaseEffectWidget):
    """Widget pour l'effet tremolo du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du tremolo."""
        # Titre
        title = ttk.Label(self, text="Tremolo", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            values=["Sine", "Triangle", "Square"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.0,
            step=0.05,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="freqHz",
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
        
        # LSH Freq.
        self.create_parameter_widget(
            "LSH Freq.",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=3,
            length=1,
            conversion="logScale",
            row=2, column=2
        )
        
        # LSH Gain
        self.create_parameter_widget(
            "LSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # EQ Freq.
        self.create_parameter_widget(
            "EQ Freq.",
            param_type="double_spinbox",
            min_val=100.0,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=5,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # EQ Gain
        self.create_parameter_widget(
            "EQ Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # EQ Q
        self.create_parameter_widget(
            "EQ Q",
            param_type="double_spinbox",
            min_val=0.10,
            max_val=10.0,
            step=0.1,
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # HSH Freq.
        self.create_parameter_widget(
            "HSH Freq.",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=8,
            length=1,
            conversion="logScale",
            row=5, column=0
        )
        
        # HSH Gain
        self.create_parameter_widget(
            "HSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=9,
            length=1,
            row=5, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du tremolo."""
        params = {}
        
        # Tremolo parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['freq'] = self.get_parameter_value("Freq.")
        params['depth'] = self.get_parameter_value("Depth")
        params['lsh_freq'] = self.get_parameter_value("LSH Freq.")
        params['lsh_gain'] = self.get_parameter_value("LSH Gain")
        params['eq_freq'] = self.get_parameter_value("EQ Freq.")
        params['eq_gain'] = self.get_parameter_value("EQ Gain")
        params['eq_q'] = self.get_parameter_value("EQ Q")
        params['hsh_freq'] = self.get_parameter_value("HSH Freq.")
        params['hsh_gain'] = self.get_parameter_value("HSH Gain")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du tremolo."""
        # Tremolo parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
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
