"""
Reverb Effect Widgets
====================

Widgets spécialisés pour les effets de reverb du Magicstomp.
Adaptés des widgets C++/Qt correspondants.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class ReverbWidget(BaseEffectWidget):
    """Widget pour l'effet reverb du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du reverb."""
        # Titre
        title = ttk.Label(self, text="Reverb", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Reverb Type
        self.create_parameter_widget(
            "Reverb Type",
            param_type="combobox",
            values=["Hall", "Room", "Stage", "Plate"],
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
            conversion="timeMs",
            row=1, column=2
        )
        
        # ER/Rev Delay
        self.create_parameter_widget(
            "ER/Rev Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=100.0,
            step=0.1,
            suffix=" ms",
            offset=2,
            length=1,
            conversion="timeMs",
            row=2, column=0
        )
        
        # Reverb Time
        self.create_parameter_widget(
            "Reverb Time",
            param_type="double_spinbox",
            min_val=0.3,
            max_val=99.0,
            step=0.1,
            suffix=" s",
            offset=3,
            length=1,
            conversion="scaleAndAdd(0.1, 0.3)",
            row=2, column=2
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=4,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=3, column=0
        )
        
        # Low Ratio
        self.create_parameter_widget(
            "Low Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=2.4,
            step=0.1,
            offset=5,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
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
        
        # ER/Rev Balance
        self.create_parameter_widget(
            "ER/Rev Balance",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=8,
            length=1,
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
            offset=9,
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
            offset=10,
            length=1,
            conversion="logScale",
            row=6, column=0
        )
        
        # Gate Level
        self.create_parameter_widget(
            "Gate Level",
            param_type="double_spinbox",
            min_val=-60.0,
            max_val=0.0,
            step=1.0,
            suffix=" dB",
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Attack
        self.create_parameter_widget(
            "Attack",
            param_type="spinbox",
            min_val=0,
            max_val=120,
            step=1,
            suffix=" ms",
            offset=12,
            length=1,
            row=7, column=0
        )
        
        # Hold
        self.create_parameter_widget(
            "Hold",
            param_type="double_spinbox",
            min_val=0.02,
            max_val=2040.0,
            step=0.1,
            suffix=" ms",
            offset=13,
            length=1,
            conversion="timeMs",
            row=7, column=2
        )
        
        # Decay
        self.create_parameter_widget(
            "Decay",
            param_type="spinbox",
            min_val=6,
            max_val=44500,
            step=10,
            suffix=" ms",
            offset=14,
            length=1,
            row=8, column=0
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=15,
            length=1,
            row=8, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du reverb."""
        params = {}
        
        # Reverb parameters
        params['reverb_type'] = self.get_parameter_value("Reverb Type")
        params['initial_delay'] = self.get_parameter_value("Initial Delay")
        params['er_rev_delay'] = self.get_parameter_value("ER/Rev Delay")
        params['reverb_time'] = self.get_parameter_value("Reverb Time")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['low_ratio'] = self.get_parameter_value("Low Ratio")
        params['diffusion'] = self.get_parameter_value("Diffusion")
        params['density'] = self.get_parameter_value("Density")
        params['er_rev_balance'] = self.get_parameter_value("ER/Rev Balance")
        params['high_pass_filter'] = self.get_parameter_value("High Pass Filter")
        params['low_pass_filter'] = self.get_parameter_value("Low Pass Filter")
        params['gate_level'] = self.get_parameter_value("Gate Level")
        params['attack'] = self.get_parameter_value("Attack")
        params['hold'] = self.get_parameter_value("Hold")
        params['decay'] = self.get_parameter_value("Decay")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du reverb."""
        # Reverb parameters
        if 'reverb_type' in params:
            self.set_parameter_value("Reverb Type", params['reverb_type'])
        if 'initial_delay' in params:
            self.set_parameter_value("Initial Delay", params['initial_delay'])
        if 'er_rev_delay' in params:
            self.set_parameter_value("ER/Rev Delay", params['er_rev_delay'])
        if 'reverb_time' in params:
            self.set_parameter_value("Reverb Time", params['reverb_time'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'low_ratio' in params:
            self.set_parameter_value("Low Ratio", params['low_ratio'])
        if 'diffusion' in params:
            self.set_parameter_value("Diffusion", params['diffusion'])
        if 'density' in params:
            self.set_parameter_value("Density", params['density'])
        if 'er_rev_balance' in params:
            self.set_parameter_value("ER/Rev Balance", params['er_rev_balance'])
        if 'high_pass_filter' in params:
            self.set_parameter_value("High Pass Filter", params['high_pass_filter'])
        if 'low_pass_filter' in params:
            self.set_parameter_value("Low Pass Filter", params['low_pass_filter'])
        if 'gate_level' in params:
            self.set_parameter_value("Gate Level", params['gate_level'])
        if 'attack' in params:
            self.set_parameter_value("Attack", params['attack'])
        if 'hold' in params:
            self.set_parameter_value("Hold", params['hold'])
        if 'decay' in params:
            self.set_parameter_value("Decay", params['decay'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class GateReverbWidget(BaseEffectWidget):
    """Widget pour l'effet gate reverb du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du gate reverb."""
        # Titre
        title = ttk.Label(self, text="Gate Reverb", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["Type-A", "Type-B"],
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
            offset=2,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=2, column=0
        )
        
        # Room Size
        self.create_parameter_widget(
            "Room Size",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=4,
            length=1,
            row=2, column=2
        )
        
        # Liveness
        self.create_parameter_widget(
            "Liveness",
            param_type="spinbox",
            min_val=0,
            max_val=10,
            step=1,
            offset=5,
            length=1,
            row=3, column=0
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
            row=3, column=2
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
            row=4, column=0
        )
        
        # ER Number
        self.create_parameter_widget(
            "ER Number",
            param_type="spinbox",
            min_val=1,
            max_val=19,
            step=1,
            offset=8,
            length=1,
            row=4, column=2
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=9,
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
            offset=10,
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
            offset=11,
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
            offset=12,
            length=1,
            row=6, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du gate reverb."""
        params = {}
        
        # Gate Reverb parameters
        params['type'] = self.get_parameter_value("Type")
        params['initial_delay'] = self.get_parameter_value("Initial Delay")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
        params['room_size'] = self.get_parameter_value("Room Size")
        params['liveness'] = self.get_parameter_value("Liveness")
        params['diffusion'] = self.get_parameter_value("Diffusion")
        params['density'] = self.get_parameter_value("Density")
        params['er_number'] = self.get_parameter_value("ER Number")
        params['high_ratio'] = self.get_parameter_value("High Ratio")
        params['high_pass_filter'] = self.get_parameter_value("High Pass Filter")
        params['low_pass_filter'] = self.get_parameter_value("Low Pass Filter")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du gate reverb."""
        # Gate Reverb parameters
        if 'type' in params:
            self.set_parameter_value("Type", params['type'])
        if 'initial_delay' in params:
            self.set_parameter_value("Initial Delay", params['initial_delay'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
        if 'room_size' in params:
            self.set_parameter_value("Room Size", params['room_size'])
        if 'liveness' in params:
            self.set_parameter_value("Liveness", params['liveness'])
        if 'diffusion' in params:
            self.set_parameter_value("Diffusion", params['diffusion'])
        if 'density' in params:
            self.set_parameter_value("Density", params['density'])
        if 'er_number' in params:
            self.set_parameter_value("ER Number", params['er_number'])
        if 'high_ratio' in params:
            self.set_parameter_value("High Ratio", params['high_ratio'])
        if 'high_pass_filter' in params:
            self.set_parameter_value("High Pass Filter", params['high_pass_filter'])
        if 'low_pass_filter' in params:
            self.set_parameter_value("Low Pass Filter", params['low_pass_filter'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class SpringReverbWidget(BaseEffectWidget):
    """Widget pour l'effet spring reverb du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du spring reverb."""
        # Titre
        title = ttk.Label(self, text="Spring Reverb", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Reverb
        self.create_parameter_widget(
            "Reverb",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=0,
            length=1,
            row=1, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du spring reverb."""
        params = {}
        
        # Spring Reverb parameters
        params['reverb'] = self.get_parameter_value("Reverb")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du spring reverb."""
        # Spring Reverb parameters
        if 'reverb' in params:
            self.set_parameter_value("Reverb", params['reverb'])
