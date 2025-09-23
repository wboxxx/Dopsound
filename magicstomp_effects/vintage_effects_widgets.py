"""
Vintage Effects Widgets
=======================

Widgets pour les effets vintage du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


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


class MonoVintagePhaserWidget(BaseEffectWidget):
    """Widget pour l'effet mono vintage phaser du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du mono vintage phaser."""
        # Titre
        title = ttk.Label(self, text="Mono Vintage Phaser", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Stage
        self.create_parameter_widget(
            "Stage",
            param_type="combobox",
            values=["4", "6", "8", "10", "12", "16"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Mode
        self.create_parameter_widget(
            "Mode",
            param_type="combobox",
            values=["1", "2"],
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Speed
        self.create_parameter_widget(
            "Speed",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Manual
        self.create_parameter_widget(
            "Manual",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Color
        self.create_parameter_widget(
            "Color",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du mono vintage phaser."""
        params = {}
        
        # Mono Vintage Phaser parameters
        params['stage'] = self.get_parameter_value("Stage")
        params['mode'] = self.get_parameter_value("Mode")
        params['speed'] = self.get_parameter_value("Speed")
        params['depth'] = self.get_parameter_value("Depth")
        params['manual'] = self.get_parameter_value("Manual")
        params['feedback'] = self.get_parameter_value("Feedback")
        params['color'] = self.get_parameter_value("Color")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du mono vintage phaser."""
        # Mono Vintage Phaser parameters
        if 'stage' in params:
            self.set_parameter_value("Stage", params['stage'])
        if 'mode' in params:
            self.set_parameter_value("Mode", params['mode'])
        if 'speed' in params:
            self.set_parameter_value("Speed", params['speed'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'manual' in params:
            self.set_parameter_value("Manual", params['manual'])
        if 'feedback' in params:
            self.set_parameter_value("Feedback", params['feedback'])
        if 'color' in params:
            self.set_parameter_value("Color", params['color'])


class StereoVintagePhaserWidget(BaseEffectWidget):
    """Widget pour l'effet stereo vintage phaser du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du stereo vintage phaser."""
        # Titre
        title = ttk.Label(self, text="Stereo Vintage Phaser", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Stage
        self.create_parameter_widget(
            "Stage",
            param_type="combobox",
            values=["4", "6", "8", "10"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Mode
        self.create_parameter_widget(
            "Mode",
            param_type="combobox",
            values=["1", "2"],
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Speed
        self.create_parameter_widget(
            "Speed",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Manual
        self.create_parameter_widget(
            "Manual",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Color
        self.create_parameter_widget(
            "Color",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Spread
        self.create_parameter_widget(
            "Spread",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=7,
            length=1,
            row=4, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du stereo vintage phaser."""
        params = {}
        
        # Stereo Vintage Phaser parameters
        params['stage'] = self.get_parameter_value("Stage")
        params['mode'] = self.get_parameter_value("Mode")
        params['speed'] = self.get_parameter_value("Speed")
        params['depth'] = self.get_parameter_value("Depth")
        params['manual'] = self.get_parameter_value("Manual")
        params['feedback'] = self.get_parameter_value("Feedback")
        params['color'] = self.get_parameter_value("Color")
        params['spread'] = self.get_parameter_value("Spread")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du stereo vintage phaser."""
        # Stereo Vintage Phaser parameters
        if 'stage' in params:
            self.set_parameter_value("Stage", params['stage'])
        if 'mode' in params:
            self.set_parameter_value("Mode", params['mode'])
        if 'speed' in params:
            self.set_parameter_value("Speed", params['speed'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'manual' in params:
            self.set_parameter_value("Manual", params['manual'])
        if 'feedback' in params:
            self.set_parameter_value("Feedback", params['feedback'])
        if 'color' in params:
            self.set_parameter_value("Color", params['color'])
        if 'spread' in params:
            self.set_parameter_value("Spread", params['spread'])
