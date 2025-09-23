"""
Delay Effect Widgets
===================

Widgets spécialisés pour les effets de delay du Magicstomp.
Adaptés des widgets C++/Qt correspondants.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class MonoDelayWidget(BaseEffectWidget):
    """Widget pour le delay mono du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du delay mono."""
        # Titre
        title = ttk.Label(self, text="Mono Delay", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Time (Temps)
        self.create_parameter_widget(
            "Time",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.2,
            suffix=" ms",
            offset=0,
            length=2,
            conversion="timeMs",
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
            offset=2,
            length=1,
            row=1, column=2
        )
        
        # FB Gain (Feedback Gain)
        self.create_parameter_widget(
            "FB Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=3,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=2, column=0
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=5,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=2, column=2
        )
        
        # High Pass Filter
        self.create_parameter_widget(
            "High Pass Filter",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # Low Pass Filter
        self.create_parameter_widget(
            "Low Pass Filter",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=7,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du delay mono."""
        params = {}
        
        # Delay parameters
        params['time'] = self.get_parameter_value("Time")
        params['mix'] = self.get_parameter_value("Mix")
        params['feedback'] = self.get_parameter_value("FB Gain")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['low_cut'] = self.get_parameter_value("High Pass Filter")
        params['high_cut'] = self.get_parameter_value("Low Pass Filter")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du delay mono."""
        # Delay parameters
        if 'time' in params:
            self.set_parameter_value("Time", params['time'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])
        if 'feedback' in params:
            self.set_parameter_value("FB Gain", params['feedback'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'low_cut' in params:
            self.set_parameter_value("High Pass Filter", params['low_cut'])
        if 'high_cut' in params:
            self.set_parameter_value("Low Pass Filter", params['high_cut'])


class StereoDelayWidget(BaseEffectWidget):
    """Widget pour le delay stéréo du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du delay stéréo."""
        # Titre
        title = ttk.Label(self, text="Stereo Delay", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Delay L (Temps canal gauche)
        self.create_parameter_widget(
            "Delay L",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1350.0,
            step=0.2,
            suffix=" ms",
            offset=0,
            length=2,
            conversion="timeMs",
            row=1, column=0
        )
        
        # Delay R (Temps canal droit)
        self.create_parameter_widget(
            "Delay R",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1350.0,
            step=0.2,
            suffix=" ms",
            offset=2,
            length=2,
            conversion="timeMs",
            row=1, column=2
        )
        
        # FB. Gain L
        self.create_parameter_widget(
            "FB. Gain L",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=4,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=2, column=0
        )
        
        # FB. Gain R
        self.create_parameter_widget(
            "FB. Gain R",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=6,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=2, column=2
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=8,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=3, column=0
        )
        
        # High Pass Filter
        self.create_parameter_widget(
            "High Pass Filter",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=9,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # Low Pass Filter
        self.create_parameter_widget(
            "Low Pass Filter",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=10,
            length=1,
            conversion="logScale",
            row=4, column=0
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
            row=4, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du delay stéréo."""
        params = {}
        
        # Stereo Delay parameters
        params['delay_l'] = self.get_parameter_value("Delay L")
        params['delay_r'] = self.get_parameter_value("Delay R")
        params['fb_gain_l'] = self.get_parameter_value("FB. Gain L")
        params['fb_gain_r'] = self.get_parameter_value("FB. Gain R")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['low_cut'] = self.get_parameter_value("High Pass Filter")
        params['high_cut'] = self.get_parameter_value("Low Pass Filter")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du delay stéréo."""
        # Stereo Delay parameters
        if 'delay_l' in params:
            self.set_parameter_value("Delay L", params['delay_l'])
        if 'delay_r' in params:
            self.set_parameter_value("Delay R", params['delay_r'])
        if 'fb_gain_l' in params:
            self.set_parameter_value("FB. Gain L", params['fb_gain_l'])
        if 'fb_gain_r' in params:
            self.set_parameter_value("FB. Gain R", params['fb_gain_r'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'low_cut' in params:
            self.set_parameter_value("High Pass Filter", params['low_cut'])
        if 'high_cut' in params:
            self.set_parameter_value("Low Pass Filter", params['high_cut'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class ModDelayWidget(BaseEffectWidget):
    """Widget pour le delay modulé du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du delay modulé."""
        # Titre
        title = ttk.Label(self, text="Modulated Delay", font=("Arial", 12, "bold"))
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
        
        # Delay
        self.create_parameter_widget(
            "Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2725.0,
            step=0.2,
            suffix=" ms",
            offset=1,
            length=2,
            conversion="timeMs",
            row=1, column=2
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
            row=2, column=0
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.0,
            step=0.05,
            suffix=" Hz",
            offset=5,
            length=1,
            conversion="freqHz",
            row=2, column=2
        )
        
        # High Pass Filter
        self.create_parameter_widget(
            "High Pass Filter",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # Low Pass Filter
        self.create_parameter_widget(
            "Low Pass Filter",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=7,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=8,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=4, column=0
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=9,
            length=1,
            row=4, column=2
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
            row=5, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du delay modulé."""
        params = {}
        
        # Modulated Delay parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['delay'] = self.get_parameter_value("Delay")
        params['feedback'] = self.get_parameter_value("FB. Gain")
        params['freq'] = self.get_parameter_value("Freq.")
        params['low_cut'] = self.get_parameter_value("High Pass Filter")
        params['high_cut'] = self.get_parameter_value("Low Pass Filter")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['depth'] = self.get_parameter_value("Depth")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du delay modulé."""
        # Modulated Delay parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'delay' in params:
            self.set_parameter_value("Delay", params['delay'])
        if 'feedback' in params:
            self.set_parameter_value("FB. Gain", params['feedback'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'low_cut' in params:
            self.set_parameter_value("High Pass Filter", params['low_cut'])
        if 'high_cut' in params:
            self.set_parameter_value("Low Pass Filter", params['high_cut'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class EchoWidget(BaseEffectWidget):
    """Widget pour l'effet echo du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface de l'echo."""
        # Titre
        title = ttk.Label(self, text="Echo", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Delay L
        self.create_parameter_widget(
            "Delay L",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1350.0,
            step=0.2,
            suffix=" ms",
            offset=0,
            length=2,
            conversion="timeMs",
            row=1, column=0
        )
        
        # Delay R
        self.create_parameter_widget(
            "Delay R",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1350.0,
            step=0.2,
            suffix=" ms",
            offset=2,
            length=2,
            conversion="timeMs",
            row=1, column=2
        )
        
        # FB. Delay L
        self.create_parameter_widget(
            "FB. Delay L",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1350.0,
            step=0.2,
            suffix=" ms",
            offset=4,
            length=1,
            row=2, column=0
        )
        
        # FB. Delay R
        self.create_parameter_widget(
            "FB. Delay R",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1350.0,
            step=0.2,
            suffix=" ms",
            offset=5,
            length=1,
            conversion="timeMs",
            row=2, column=2
        )
        
        # FB. Gain L
        self.create_parameter_widget(
            "FB. Gain L",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=6,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=3, column=0
        )
        
        # FB. Gain R
        self.create_parameter_widget(
            "FB. Gain R",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=8,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=3, column=2
        )
        
        # L->R FB. Gain
        self.create_parameter_widget(
            "L->R FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=10,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=4, column=0
        )
        
        # R->L FB. Gain
        self.create_parameter_widget(
            "R->L FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=12,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=4, column=2
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=14,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=5, column=0
        )
        
        # High Pass Filter
        self.create_parameter_widget(
            "High Pass Filter",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=15,
            length=1,
            conversion="logScale",
            row=5, column=2
        )
        
        # Low Pass Filter
        self.create_parameter_widget(
            "Low Pass Filter",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=16,
            length=1,
            conversion="logScale",
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
            offset=17,
            length=1,
            row=6, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres de l'echo."""
        params = {}
        
        # Echo parameters
        params['delay_l'] = self.get_parameter_value("Delay L")
        params['delay_r'] = self.get_parameter_value("Delay R")
        params['fb_delay_l'] = self.get_parameter_value("FB. Delay L")
        params['fb_delay_r'] = self.get_parameter_value("FB. Delay R")
        params['fb_gain_l'] = self.get_parameter_value("FB. Gain L")
        params['fb_gain_r'] = self.get_parameter_value("FB. Gain R")
        params['l_to_r_fb_gain'] = self.get_parameter_value("L->R FB. Gain")
        params['r_to_l_fb_gain'] = self.get_parameter_value("R->L FB. Gain")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['low_cut'] = self.get_parameter_value("High Pass Filter")
        params['high_cut'] = self.get_parameter_value("Low Pass Filter")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres de l'echo."""
        # Echo parameters
        if 'delay_l' in params:
            self.set_parameter_value("Delay L", params['delay_l'])
        if 'delay_r' in params:
            self.set_parameter_value("Delay R", params['delay_r'])
        if 'fb_delay_l' in params:
            self.set_parameter_value("FB. Delay L", params['fb_delay_l'])
        if 'fb_delay_r' in params:
            self.set_parameter_value("FB. Delay R", params['fb_delay_r'])
        if 'fb_gain_l' in params:
            self.set_parameter_value("FB. Gain L", params['fb_gain_l'])
        if 'fb_gain_r' in params:
            self.set_parameter_value("FB. Gain R", params['fb_gain_r'])
        if 'l_to_r_fb_gain' in params:
            self.set_parameter_value("L->R FB. Gain", params['l_to_r_fb_gain'])
        if 'r_to_l_fb_gain' in params:
            self.set_parameter_value("R->L FB. Gain", params['r_to_l_fb_gain'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'low_cut' in params:
            self.set_parameter_value("High Pass Filter", params['low_cut'])
        if 'high_cut' in params:
            self.set_parameter_value("Low Pass Filter", params['high_cut'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])
