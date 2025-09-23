"""
Distortion Effect Widgets
========================

Widgets spécialisés pour les effets de distorsion du Magicstomp.
Adaptés des widgets C++/Qt correspondants.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class DistortionWidget(BaseEffectWidget):
    """Widget pour l'effet distorsion du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface de la distorsion."""
        # Titre
        title = ttk.Label(self, text="Distortion", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["Lead1", "Lead2", "Drive1", "Drive2", "Crunch1", "Crunch2", 
                   "Fuzz1", "Fuzz2", "Distortion1", "Distortion2", "Overdrive1", 
                   "Overdrive2", "Tube", "Solidstate"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Gain
        self.create_parameter_widget(
            "Gain",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Master
        self.create_parameter_widget(
            "Master",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Tone
        self.create_parameter_widget(
            "Tone",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # EQ 1 Freq
        self.create_parameter_widget(
            "EQ 1 Freq",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=400.0,
            step=10.0,
            suffix=" Hz",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # EQ 1 Gain
        self.create_parameter_widget(
            "EQ 1 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # EQ 1 Q
        self.create_parameter_widget(
            "EQ 1 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # EQ 2 Freq
        self.create_parameter_widget(
            "EQ 2 Freq",
            param_type="double_spinbox",
            min_val=200.0,
            max_val=1600.0,
            step=10.0,
            suffix=" Hz",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # EQ 2 Gain
        self.create_parameter_widget(
            "EQ 2 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # EQ 2 Q
        self.create_parameter_widget(
            "EQ 2 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # EQ 3 Freq
        self.create_parameter_widget(
            "EQ 3 Freq",
            param_type="double_spinbox",
            min_val=600.0,
            max_val=4800.0,
            step=10.0,
            suffix=" Hz",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # EQ 3 Gain
        self.create_parameter_widget(
            "EQ 3 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # EQ 3 Q
        self.create_parameter_widget(
            "EQ 3 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=12,
            length=1,
            row=7, column=0
        )
        
        # EQ 4 Freq
        self.create_parameter_widget(
            "EQ 4 Freq",
            param_type="double_spinbox",
            min_val=2000.0,
            max_val=16000.0,
            step=100.0,
            suffix=" Hz",
            offset=13,
            length=1,
            row=7, column=2
        )
        
        # EQ 4 Gain
        self.create_parameter_widget(
            "EQ 4 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=14,
            length=1,
            row=8, column=0
        )
        
        # EQ 4 Q
        self.create_parameter_widget(
            "EQ 4 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=15,
            length=1,
            row=8, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres de la distorsion."""
        params = {}
        
        # Distortion parameters
        params['type'] = self.get_parameter_value("Type")
        params['gain'] = self.get_parameter_value("Gain")
        params['master'] = self.get_parameter_value("Master")
        params['tone'] = self.get_parameter_value("Tone")
        params['eq1_freq'] = self.get_parameter_value("EQ 1 Freq")
        params['eq1_gain'] = self.get_parameter_value("EQ 1 Gain")
        params['eq1_q'] = self.get_parameter_value("EQ 1 Q")
        params['eq2_freq'] = self.get_parameter_value("EQ 2 Freq")
        params['eq2_gain'] = self.get_parameter_value("EQ 2 Gain")
        params['eq2_q'] = self.get_parameter_value("EQ 2 Q")
        params['eq3_freq'] = self.get_parameter_value("EQ 3 Freq")
        params['eq3_gain'] = self.get_parameter_value("EQ 3 Gain")
        params['eq3_q'] = self.get_parameter_value("EQ 3 Q")
        params['eq4_freq'] = self.get_parameter_value("EQ 4 Freq")
        params['eq4_gain'] = self.get_parameter_value("EQ 4 Gain")
        params['eq4_q'] = self.get_parameter_value("EQ 4 Q")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres de la distorsion."""
        # Distortion parameters
        if 'type' in params:
            self.set_parameter_value("Type", params['type'])
        if 'gain' in params:
            self.set_parameter_value("Gain", params['gain'])
        if 'master' in params:
            self.set_parameter_value("Master", params['master'])
        if 'tone' in params:
            self.set_parameter_value("Tone", params['tone'])
        if 'eq1_freq' in params:
            self.set_parameter_value("EQ 1 Freq", params['eq1_freq'])
        if 'eq1_gain' in params:
            self.set_parameter_value("EQ 1 Gain", params['eq1_gain'])
        if 'eq1_q' in params:
            self.set_parameter_value("EQ 1 Q", params['eq1_q'])
        if 'eq2_freq' in params:
            self.set_parameter_value("EQ 2 Freq", params['eq2_freq'])
        if 'eq2_gain' in params:
            self.set_parameter_value("EQ 2 Gain", params['eq2_gain'])
        if 'eq2_q' in params:
            self.set_parameter_value("EQ 2 Q", params['eq2_q'])
        if 'eq3_freq' in params:
            self.set_parameter_value("EQ 3 Freq", params['eq3_freq'])
        if 'eq3_gain' in params:
            self.set_parameter_value("EQ 3 Gain", params['eq3_gain'])
        if 'eq3_q' in params:
            self.set_parameter_value("EQ 3 Q", params['eq3_q'])
        if 'eq4_freq' in params:
            self.set_parameter_value("EQ 4 Freq", params['eq4_freq'])
        if 'eq4_gain' in params:
            self.set_parameter_value("EQ 4 Gain", params['eq4_gain'])
        if 'eq4_q' in params:
            self.set_parameter_value("EQ 4 Q", params['eq4_q'])


class AmpSimulatorWidget(BaseEffectWidget):
    """Widget pour le simulateur d'ampli du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du simulateur d'ampli."""
        # Titre
        title = ttk.Label(self, text="Amp Simulator", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Amp Type
        self.create_parameter_widget(
            "Amp Type",
            param_type="combobox",
            values=["Heavy1", "Heavy2", "Lead1", "Lead2", "Drive1", "Drive2", 
                   "Crunch1", "Crunch2", "Clean1", "Clean2", "Solid"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Gain
        self.create_parameter_widget(
            "Gain",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Master
        self.create_parameter_widget(
            "Master",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Tone
        self.create_parameter_widget(
            "Tone",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Treble
        self.create_parameter_widget(
            "Treble",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # High Middle
        self.create_parameter_widget(
            "High Middle",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Low Middle
        self.create_parameter_widget(
            "Low Middle",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Bass
        self.create_parameter_widget(
            "Bass",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=7,
            length=1,
            row=4, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du simulateur d'ampli."""
        params = {}
        
        # Amp Simulator parameters
        params['amp_type'] = self.get_parameter_value("Amp Type")
        params['gain'] = self.get_parameter_value("Gain")
        params['master'] = self.get_parameter_value("Master")
        params['tone'] = self.get_parameter_value("Tone")
        params['treble'] = self.get_parameter_value("Treble")
        params['high_middle'] = self.get_parameter_value("High Middle")
        params['low_middle'] = self.get_parameter_value("Low Middle")
        params['bass'] = self.get_parameter_value("Bass")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du simulateur d'ampli."""
        # Amp Simulator parameters
        if 'amp_type' in params:
            self.set_parameter_value("Amp Type", params['amp_type'])
        if 'gain' in params:
            self.set_parameter_value("Gain", params['gain'])
        if 'master' in params:
            self.set_parameter_value("Master", params['master'])
        if 'tone' in params:
            self.set_parameter_value("Tone", params['tone'])
        if 'treble' in params:
            self.set_parameter_value("Treble", params['treble'])
        if 'high_middle' in params:
            self.set_parameter_value("High Middle", params['high_middle'])
        if 'low_middle' in params:
            self.set_parameter_value("Low Middle", params['low_middle'])
        if 'bass' in params:
            self.set_parameter_value("Bass", params['bass'])


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
