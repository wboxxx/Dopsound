"""
Early Reflection Widgets
========================

Widgets pour les effets de réflexions précoces du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class EarlyRefWidget(BaseEffectWidget):
    """Widget pour l'effet early reflections du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface des early reflections."""
        # Titre
        title = ttk.Label(self, text="Early Reflections", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["Small Hall", "Large Hall", "Random", "Reverse", "Plate", "Spring"],
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
        
        # FB. Gain
        self.create_parameter_widget(
            "FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Room Size
        self.create_parameter_widget(
            "Room Size",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=3,
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
            offset=4,
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
            offset=5,
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
            offset=6,
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
        """Retourne tous les paramètres des early reflections."""
        params = {}
        
        # Early Reflections parameters
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
        """Applique tous les paramètres des early reflections."""
        # Early Reflections parameters
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


class ReverseGateWidget(BaseEffectWidget):
    """Widget pour l'effet reverse gate du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du reverse gate."""
        # Titre
        title = ttk.Label(self, text="Reverse Gate", font=("Arial", 12, "bold"))
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
            conversion="logScale",
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
            length=1,
            row=2, column=0
        )
        
        # Room Size
        self.create_parameter_widget(
            "Room Size",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=3,
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
            offset=4,
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
            offset=5,
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
            offset=6,
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
        """Retourne tous les paramètres du reverse gate."""
        params = {}
        
        # Reverse Gate parameters
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
        """Applique tous les paramètres du reverse gate."""
        # Reverse Gate parameters
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
