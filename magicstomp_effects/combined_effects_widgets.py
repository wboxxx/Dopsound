"""
Combined Effects Widgets
========================

Widgets pour les effets combinés du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class ReverbChorusWidget(BaseEffectWidget):
    """Widget pour l'effet Reverb+Chorus du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du Reverb+Chorus."""
        # Titre
        title = ttk.Label(self, text="Reverb+Chorus", font=("Arial", 12, "bold"))
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
        
        # Initial Delay
        self.create_parameter_widget(
            "Initial Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=500.0,
            step=0.1,
            suffix=" ms",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.00,
            step=0.05,
            suffix=" Hz",
            offset=2,
            length=1,
            conversion="logScale",
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
        
        # Reverb Time
        self.create_parameter_widget(
            "Reverb Time",
            param_type="double_spinbox",
            min_val=0.3,
            max_val=99.0,
            step=0.1,
            suffix=" s",
            offset=4,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.01,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Diffusion
        self.create_parameter_widget(
            "Diffusion",
            param_type="spinbox",
            min_val=0,
            max_val=10,
            step=1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Density
        self.create_parameter_widget(
            "Density",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # High Pass Filter
        self.create_parameter_widget(
            "High Pass Filter",
            param_type="combobox",
            values=["Thru", "21.2 Hz", "50 Hz", "100 Hz", "200 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz", "8 kHz"],
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Low Pass Filter
        self.create_parameter_widget(
            "Low Pass Filter",
            param_type="combobox",
            values=["50 Hz", "100 Hz", "200 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz", "8 kHz", "16 kHz", "Thru"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Reverb/Chorus
        self.create_parameter_widget(
            "Reverb/Chorus",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # AM Depth
        self.create_parameter_widget(
            "AM Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # PM Depth
        self.create_parameter_widget(
            "PM Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=12,
            length=1,
            row=7, column=0
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
            row=7, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du Reverb+Chorus."""
        params = {}
        
        # Reverb+Chorus parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['initial_delay'] = self.get_parameter_value("Initial Delay")
        params['freq'] = self.get_parameter_value("Freq.")
        params['mod_delay'] = self.get_parameter_value("Mod. Delay")
        params['reverb_time'] = self.get_parameter_value("Reverb Time")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['diffusion'] = self.get_parameter_value("Diffusion")
        params['density'] = self.get_parameter_value("Density")
        params['high_pass_filter'] = self.get_parameter_value("High Pass Filter")
        params['low_pass_filter'] = self.get_parameter_value("Low Pass Filter")
        params['reverb_chorus'] = self.get_parameter_value("Reverb/Chorus")
        params['am_depth'] = self.get_parameter_value("AM Depth")
        params['pm_depth'] = self.get_parameter_value("PM Depth")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du Reverb+Chorus."""
        # Reverb+Chorus parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'initial_delay' in params:
            self.set_parameter_value("Initial Delay", params['initial_delay'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'mod_delay' in params:
            self.set_parameter_value("Mod. Delay", params['mod_delay'])
        if 'reverb_time' in params:
            self.set_parameter_value("Reverb Time", params['reverb_time'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'diffusion' in params:
            self.set_parameter_value("Diffusion", params['diffusion'])
        if 'density' in params:
            self.set_parameter_value("Density", params['density'])
        if 'high_pass_filter' in params:
            self.set_parameter_value("High Pass Filter", params['high_pass_filter'])
        if 'low_pass_filter' in params:
            self.set_parameter_value("Low Pass Filter", params['low_pass_filter'])
        if 'reverb_chorus' in params:
            self.set_parameter_value("Reverb/Chorus", params['reverb_chorus'])
        if 'am_depth' in params:
            self.set_parameter_value("AM Depth", params['am_depth'])
        if 'pm_depth' in params:
            self.set_parameter_value("PM Depth", params['pm_depth'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class ReverbFlangeWidget(BaseEffectWidget):
    """Widget pour l'effet Reverb+Flange du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du Reverb+Flange."""
        # Titre
        title = ttk.Label(self, text="Reverb+Flange", font=("Arial", 12, "bold"))
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
        
        # Initial Delay
        self.create_parameter_widget(
            "Initial Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=500.0,
            step=0.1,
            suffix=" ms",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.00,
            step=0.05,
            suffix=" Hz",
            offset=2,
            length=1,
            conversion="logScale",
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
        
        # Reverb Time
        self.create_parameter_widget(
            "Reverb Time",
            param_type="double_spinbox",
            min_val=0.3,
            max_val=99.0,
            step=0.1,
            suffix=" s",
            offset=4,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.01,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Diffusion
        self.create_parameter_widget(
            "Diffusion",
            param_type="spinbox",
            min_val=0,
            max_val=10,
            step=1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Density
        self.create_parameter_widget(
            "Density",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # High Pass Filter
        self.create_parameter_widget(
            "High Pass Filter",
            param_type="combobox",
            values=["Thru", "21.2 Hz", "50 Hz", "100 Hz", "200 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz", "8 kHz"],
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Low Pass Filter
        self.create_parameter_widget(
            "Low Pass Filter",
            param_type="combobox",
            values=["50 Hz", "100 Hz", "200 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz", "8 kHz", "16 kHz", "Thru"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Reverb/Flange
        self.create_parameter_widget(
            "Reverb/Flange",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # FB. Gain
        self.create_parameter_widget(
            "FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=12,
            length=1,
            row=7, column=0
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
            row=7, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du Reverb+Flange."""
        params = {}
        
        # Reverb+Flange parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['initial_delay'] = self.get_parameter_value("Initial Delay")
        params['freq'] = self.get_parameter_value("Freq.")
        params['mod_delay'] = self.get_parameter_value("Mod. Delay")
        params['reverb_time'] = self.get_parameter_value("Reverb Time")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['diffusion'] = self.get_parameter_value("Diffusion")
        params['density'] = self.get_parameter_value("Density")
        params['high_pass_filter'] = self.get_parameter_value("High Pass Filter")
        params['low_pass_filter'] = self.get_parameter_value("Low Pass Filter")
        params['reverb_flange'] = self.get_parameter_value("Reverb/Flange")
        params['depth'] = self.get_parameter_value("Depth")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du Reverb+Flange."""
        # Reverb+Flange parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'initial_delay' in params:
            self.set_parameter_value("Initial Delay", params['initial_delay'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'mod_delay' in params:
            self.set_parameter_value("Mod. Delay", params['mod_delay'])
        if 'reverb_time' in params:
            self.set_parameter_value("Reverb Time", params['reverb_time'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'diffusion' in params:
            self.set_parameter_value("Diffusion", params['diffusion'])
        if 'density' in params:
            self.set_parameter_value("Density", params['density'])
        if 'high_pass_filter' in params:
            self.set_parameter_value("High Pass Filter", params['high_pass_filter'])
        if 'low_pass_filter' in params:
            self.set_parameter_value("Low Pass Filter", params['low_pass_filter'])
        if 'reverb_flange' in params:
            self.set_parameter_value("Reverb/Flange", params['reverb_flange'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])
