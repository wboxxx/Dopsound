"""
Complex Delay Widgets
=====================

Widgets pour les effets de delay complexes du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class DelayLCRWidget(BaseEffectWidget):
    """Widget pour l'effet delay LCR du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du delay LCR."""
        # Titre
        title = ttk.Label(self, text="Delay LCR", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Delay L
        self.create_parameter_widget(
            "Delay L",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.1,
            suffix=" ms",
            offset=0,
            length=1,
            conversion="logScale",
            row=1, column=0
        )
        
        # Delay C
        self.create_parameter_widget(
            "Delay C",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.1,
            suffix=" ms",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Delay R
        self.create_parameter_widget(
            "Delay R",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.1,
            suffix=" ms",
            offset=2,
            length=1,
            conversion="logScale",
            row=2, column=0
        )
        
        # Delay FB.
        self.create_parameter_widget(
            "Delay FB.",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.1,
            suffix=" ms",
            offset=3,
            length=1,
            conversion="logScale",
            row=2, column=2
        )
        
        # Level L
        self.create_parameter_widget(
            "Level L",
            param_type="spinbox",
            min_val=-100,
            max_val=100,
            step=1,
            suffix=" %",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Level C
        self.create_parameter_widget(
            "Level C",
            param_type="spinbox",
            min_val=-100,
            max_val=100,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Level R
        self.create_parameter_widget(
            "Level R",
            param_type="spinbox",
            min_val=-100,
            max_val=100,
            step=1,
            suffix=" %",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # FB. Gain
        self.create_parameter_widget(
            "FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.01,
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # High Pass Filter
        self.create_parameter_widget(
            "High Pass Filter",
            param_type="combobox",
            values=["Thru", "21.2 Hz", "50 Hz", "100 Hz", "200 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz", "8 kHz"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Low Pass Filter
        self.create_parameter_widget(
            "Low Pass Filter",
            param_type="combobox",
            values=["50 Hz", "100 Hz", "200 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz", "8 kHz", "16 kHz", "Thru"],
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
        """Retourne tous les paramètres du delay LCR."""
        params = {}
        
        # Delay LCR parameters
        params['delay_l'] = self.get_parameter_value("Delay L")
        params['delay_c'] = self.get_parameter_value("Delay C")
        params['delay_r'] = self.get_parameter_value("Delay R")
        params['delay_fb'] = self.get_parameter_value("Delay FB.")
        params['level_l'] = self.get_parameter_value("Level L")
        params['level_c'] = self.get_parameter_value("Level C")
        params['level_r'] = self.get_parameter_value("Level R")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['high_pass_filter'] = self.get_parameter_value("High Pass Filter")
        params['low_pass_filter'] = self.get_parameter_value("Low Pass Filter")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du delay LCR."""
        # Delay LCR parameters
        if 'delay_l' in params:
            self.set_parameter_value("Delay L", params['delay_l'])
        if 'delay_c' in params:
            self.set_parameter_value("Delay C", params['delay_c'])
        if 'delay_r' in params:
            self.set_parameter_value("Delay R", params['delay_r'])
        if 'delay_fb' in params:
            self.set_parameter_value("Delay FB.", params['delay_fb'])
        if 'level_l' in params:
            self.set_parameter_value("Level L", params['level_l'])
        if 'level_c' in params:
            self.set_parameter_value("Level C", params['level_c'])
        if 'level_r' in params:
            self.set_parameter_value("Level R", params['level_r'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'high_pass_filter' in params:
            self.set_parameter_value("High Pass Filter", params['high_pass_filter'])
        if 'low_pass_filter' in params:
            self.set_parameter_value("Low Pass Filter", params['low_pass_filter'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class ShortMediumLongModDelayWidget(BaseEffectWidget):
    """Widget pour l'effet Short + Medium + Long Mod. Delay du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du Short + Medium + Long Mod. Delay."""
        # Titre
        title = ttk.Label(self, text="Short + Medium + Long Mod. Delay", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Short Delay
        self.create_parameter_widget(
            "Short Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.1,
            suffix=" ms",
            offset=0,
            length=1,
            conversion="logScale",
            row=1, column=0
        )
        
        # Medium Delay
        self.create_parameter_widget(
            "Medium Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.1,
            suffix=" ms",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Long Delay
        self.create_parameter_widget(
            "Long Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.1,
            suffix=" ms",
            offset=2,
            length=1,
            conversion="logScale",
            row=2, column=0
        )
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            values=["Sine", "Triangle"],
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.00,
            step=0.05,
            suffix=" Hz",
            offset=4,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # FB. Gain
        self.create_parameter_widget(
            "FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.01,
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
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=10,
            length=1,
            row=6, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du Short + Medium + Long Mod. Delay."""
        params = {}
        
        # Short + Medium + Long Mod. Delay parameters
        params['short_delay'] = self.get_parameter_value("Short Delay")
        params['medium_delay'] = self.get_parameter_value("Medium Delay")
        params['long_delay'] = self.get_parameter_value("Long Delay")
        params['wave'] = self.get_parameter_value("Wave")
        params['freq'] = self.get_parameter_value("Freq.")
        params['depth'] = self.get_parameter_value("Depth")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['high_pass_filter'] = self.get_parameter_value("High Pass Filter")
        params['low_pass_filter'] = self.get_parameter_value("Low Pass Filter")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du Short + Medium + Long Mod. Delay."""
        # Short + Medium + Long Mod. Delay parameters
        if 'short_delay' in params:
            self.set_parameter_value("Short Delay", params['short_delay'])
        if 'medium_delay' in params:
            self.set_parameter_value("Medium Delay", params['medium_delay'])
        if 'long_delay' in params:
            self.set_parameter_value("Long Delay", params['long_delay'])
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'high_pass_filter' in params:
            self.set_parameter_value("High Pass Filter", params['high_pass_filter'])
        if 'low_pass_filter' in params:
            self.set_parameter_value("Low Pass Filter", params['low_pass_filter'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])
