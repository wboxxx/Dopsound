"""
Final Effects Widgets
=====================

Widgets pour les derniers effets du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class ReverbArrowSymphonicWidget(BaseEffectWidget):
    """Widget pour l'effet Reverb->Symphonic du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du Reverb->Symphonic."""
        # Titre
        title = ttk.Label(self, text="Reverb->Symphonic", font=("Arial", 12, "bold"))
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
        
        # Reverb Balance
        self.create_parameter_widget(
            "Reverb Balance",
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
        """Retourne tous les paramètres du Reverb->Symphonic."""
        params = {}
        
        # Reverb->Symphonic parameters
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
        params['reverb_balance'] = self.get_parameter_value("Reverb Balance")
        params['depth'] = self.get_parameter_value("Depth")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du Reverb->Symphonic."""
        # Reverb->Symphonic parameters
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
        if 'reverb_balance' in params:
            self.set_parameter_value("Reverb Balance", params['reverb_balance'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class AcousticMultiWidget(BaseEffectWidget):
    """Widget pour l'effet Acoustic Multi du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du Acoustic Multi."""
        # Titre
        title = ttk.Label(self, text="Acoustic Multi", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Mic Type
        self.create_parameter_widget(
            "Mic Type",
            param_type="combobox",
            values=["Condenser1", "Condenser2", "Dynamic1", "Dynamic2", "Tube1", "Tube2", "Nylon String1", "Nylon String2"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Blend
        self.create_parameter_widget(
            "Blend",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Bass
        self.create_parameter_widget(
            "Bass",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Middle
        self.create_parameter_widget(
            "Middle",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Treble
        self.create_parameter_widget(
            "Treble",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Presence
        self.create_parameter_widget(
            "Presence",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Volume
        self.create_parameter_widget(
            "Volume",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Stereo
        self.create_parameter_widget(
            "Stereo",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Bass Freq.
        self.create_parameter_widget(
            "Bass Freq.",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=400.0,
            step=1.0,
            suffix=" Hz",
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Middle Freq.
        self.create_parameter_widget(
            "Middle Freq.",
            param_type="double_spinbox",
            min_val=200.0,
            max_val=1800.0,
            step=10.0,
            suffix=" Hz",
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Treble Freq.
        self.create_parameter_widget(
            "Treble Freq.",
            param_type="double_spinbox",
            min_val=600.0,
            max_val=4800.0,
            step=50.0,
            suffix=" Hz",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # Presence Freq.
        self.create_parameter_widget(
            "Presence Freq.",
            param_type="double_spinbox",
            min_val=2000.0,
            max_val=16000.0,
            step=100.0,
            suffix=" Hz",
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Limiter
        self.create_parameter_widget(
            "Limiter",
            param_type="combobox",
            values=["Off", "On"],
            offset=12,
            length=1,
            row=7, column=0
        )
        
        # Chorus/Delay
        self.create_parameter_widget(
            "Chorus/Delay",
            param_type="combobox",
            values=["Off", "Chorus", "Delay"],
            offset=13,
            length=1,
            row=7, column=2
        )
        
        # Reverb Type
        self.create_parameter_widget(
            "Reverb Type",
            param_type="combobox",
            values=["Off", "Hall", "Room", "Plate"],
            offset=14,
            length=1,
            row=8, column=0
        )
        
        # Limiter Level
        self.create_parameter_widget(
            "Limiter Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=15,
            length=1,
            row=8, column=2
        )
        
        # Speed/Time
        self.create_parameter_widget(
            "Speed/Time",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=16,
            length=1,
            row=9, column=0
        )
        
        # Depth/FB.
        self.create_parameter_widget(
            "Depth/FB.",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=17,
            length=1,
            row=9, column=2
        )
        
        # Effect Level
        self.create_parameter_widget(
            "Effect Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=18,
            length=1,
            row=10, column=0
        )
        
        # Reverb
        self.create_parameter_widget(
            "Reverb",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=19,
            length=1,
            row=10, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du Acoustic Multi."""
        params = {}
        
        # Acoustic Multi parameters
        params['mic_type'] = self.get_parameter_value("Mic Type")
        params['blend'] = self.get_parameter_value("Blend")
        params['bass'] = self.get_parameter_value("Bass")
        params['middle'] = self.get_parameter_value("Middle")
        params['treble'] = self.get_parameter_value("Treble")
        params['presence'] = self.get_parameter_value("Presence")
        params['volume'] = self.get_parameter_value("Volume")
        params['stereo'] = self.get_parameter_value("Stereo")
        params['bass_freq'] = self.get_parameter_value("Bass Freq.")
        params['middle_freq'] = self.get_parameter_value("Middle Freq.")
        params['treble_freq'] = self.get_parameter_value("Treble Freq.")
        params['presence_freq'] = self.get_parameter_value("Presence Freq.")
        params['limiter'] = self.get_parameter_value("Limiter")
        params['chorus_delay'] = self.get_parameter_value("Chorus/Delay")
        params['reverb_type'] = self.get_parameter_value("Reverb Type")
        params['limiter_level'] = self.get_parameter_value("Limiter Level")
        params['speed_time'] = self.get_parameter_value("Speed/Time")
        params['depth_fb'] = self.get_parameter_value("Depth/FB.")
        params['effect_level'] = self.get_parameter_value("Effect Level")
        params['reverb'] = self.get_parameter_value("Reverb")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du Acoustic Multi."""
        # Acoustic Multi parameters
        if 'mic_type' in params:
            self.set_parameter_value("Mic Type", params['mic_type'])
        if 'blend' in params:
            self.set_parameter_value("Blend", params['blend'])
        if 'bass' in params:
            self.set_parameter_value("Bass", params['bass'])
        if 'middle' in params:
            self.set_parameter_value("Middle", params['middle'])
        if 'treble' in params:
            self.set_parameter_value("Treble", params['treble'])
        if 'presence' in params:
            self.set_parameter_value("Presence", params['presence'])
        if 'volume' in params:
            self.set_parameter_value("Volume", params['volume'])
        if 'stereo' in params:
            self.set_parameter_value("Stereo", params['stereo'])
        if 'bass_freq' in params:
            self.set_parameter_value("Bass Freq.", params['bass_freq'])
        if 'middle_freq' in params:
            self.set_parameter_value("Middle Freq.", params['middle_freq'])
        if 'treble_freq' in params:
            self.set_parameter_value("Treble Freq.", params['treble_freq'])
        if 'presence_freq' in params:
            self.set_parameter_value("Presence Freq.", params['presence_freq'])
        if 'limiter' in params:
            self.set_parameter_value("Limiter", params['limiter'])
        if 'chorus_delay' in params:
            self.set_parameter_value("Chorus/Delay", params['chorus_delay'])
        if 'reverb_type' in params:
            self.set_parameter_value("Reverb Type", params['reverb_type'])
        if 'limiter_level' in params:
            self.set_parameter_value("Limiter Level", params['limiter_level'])
        if 'speed_time' in params:
            self.set_parameter_value("Speed/Time", params['speed_time'])
        if 'depth_fb' in params:
            self.set_parameter_value("Depth/FB.", params['depth_fb'])
        if 'effect_level' in params:
            self.set_parameter_value("Effect Level", params['effect_level'])
        if 'reverb' in params:
            self.set_parameter_value("Reverb", params['reverb'])
