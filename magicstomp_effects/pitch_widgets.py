"""
Pitch Effect Widgets
==================

Widgets spécialisés pour les effets de pitch du Magicstomp.
Adaptés des widgets C++/Qt correspondants.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class HQPitchWidget(BaseEffectWidget):
    """Widget pour l'effet pitch haute qualité du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du pitch HQ."""
        # Titre
        title = ttk.Label(self, text="HQ Pitch", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Mode
        self.create_parameter_widget(
            "Mode",
            param_type="spinbox",
            min_val=1,
            max_val=10,
            step=1,
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Delay
        self.create_parameter_widget(
            "Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1000.0,
            step=0.1,
            suffix=" ms",
            offset=1,
            length=1,
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
        
        # Pitch
        self.create_parameter_widget(
            "Pitch",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" semitones",
            offset=4,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=2, column=2
        )
        
        # Fine
        self.create_parameter_widget(
            "Fine",
            param_type="spinbox",
            min_val=-50,
            max_val=50,
            step=1,
            suffix=" cents",
            offset=5,
            length=1,
            conversion="scaleAndAdd(1, -50)",
            row=3, column=0
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=6,
            length=1,
            row=3, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du pitch HQ."""
        params = {}
        
        # HQ Pitch parameters
        params['mode'] = self.get_parameter_value("Mode")
        params['delay'] = self.get_parameter_value("Delay")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
        params['pitch'] = self.get_parameter_value("Pitch")
        params['fine'] = self.get_parameter_value("Fine")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du pitch HQ."""
        # HQ Pitch parameters
        if 'mode' in params:
            self.set_parameter_value("Mode", params['mode'])
        if 'delay' in params:
            self.set_parameter_value("Delay", params['delay'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
        if 'pitch' in params:
            self.set_parameter_value("Pitch", params['pitch'])
        if 'fine' in params:
            self.set_parameter_value("Fine", params['fine'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class DualPitchWidget(BaseEffectWidget):
    """Widget pour l'effet dual pitch du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du dual pitch."""
        # Titre
        title = ttk.Label(self, text="Dual Pitch", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=8, pady=(0, 10))
        
        # Mode
        self.create_parameter_widget(
            "Mode",
            param_type="spinbox",
            min_val=1,
            max_val=10,
            step=1,
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Delay 1
        self.create_parameter_widget(
            "Delay 1",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1000.0,
            step=0.1,
            suffix=" ms",
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # FB. Gain 1
        self.create_parameter_widget(
            "FB. Gain 1",
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
        
        # Pitch 1
        self.create_parameter_widget(
            "Pitch 1",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" semitones",
            offset=4,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=2, column=2
        )
        
        # Fine 1
        self.create_parameter_widget(
            "Fine 1",
            param_type="spinbox",
            min_val=-50,
            max_val=50,
            step=1,
            suffix=" cents",
            offset=5,
            length=1,
            conversion="scaleAndAdd(1, -50)",
            row=3, column=0
        )
        
        # Delay 2
        self.create_parameter_widget(
            "Delay 2",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1000.0,
            step=0.1,
            suffix=" ms",
            offset=6,
            length=1,
            row=3, column=2
        )
        
        # FB. Gain 2
        self.create_parameter_widget(
            "FB. Gain 2",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=7,
            length=2,
            conversion="scaleAndAdd(1, -99)",
            row=4, column=0
        )
        
        # Pitch 2
        self.create_parameter_widget(
            "Pitch 2",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" semitones",
            offset=9,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=4, column=2
        )
        
        # Fine 2
        self.create_parameter_widget(
            "Fine 2",
            param_type="spinbox",
            min_val=-50,
            max_val=50,
            step=1,
            suffix=" cents",
            offset=10,
            length=1,
            conversion="scaleAndAdd(1, -50)",
            row=5, column=0
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
            row=5, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du dual pitch."""
        params = {}
        
        # Dual Pitch parameters
        params['mode'] = self.get_parameter_value("Mode")
        params['delay1'] = self.get_parameter_value("Delay 1")
        params['fb_gain1'] = self.get_parameter_value("FB. Gain 1")
        params['pitch1'] = self.get_parameter_value("Pitch 1")
        params['fine1'] = self.get_parameter_value("Fine 1")
        params['delay2'] = self.get_parameter_value("Delay 2")
        params['fb_gain2'] = self.get_parameter_value("FB. Gain 2")
        params['pitch2'] = self.get_parameter_value("Pitch 2")
        params['fine2'] = self.get_parameter_value("Fine 2")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du dual pitch."""
        # Dual Pitch parameters
        if 'mode' in params:
            self.set_parameter_value("Mode", params['mode'])
        if 'delay1' in params:
            self.set_parameter_value("Delay 1", params['delay1'])
        if 'fb_gain1' in params:
            self.set_parameter_value("FB. Gain 1", params['fb_gain1'])
        if 'pitch1' in params:
            self.set_parameter_value("Pitch 1", params['pitch1'])
        if 'fine1' in params:
            self.set_parameter_value("Fine 1", params['fine1'])
        if 'delay2' in params:
            self.set_parameter_value("Delay 2", params['delay2'])
        if 'fb_gain2' in params:
            self.set_parameter_value("FB. Gain 2", params['fb_gain2'])
        if 'pitch2' in params:
            self.set_parameter_value("Pitch 2", params['pitch2'])
        if 'fine2' in params:
            self.set_parameter_value("Fine 2", params['fine2'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])

