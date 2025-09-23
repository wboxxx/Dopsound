"""
Modulation Filter Widgets
=========================

Widgets pour les effets de filtrage modulé du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class ModFilterWidget(BaseEffectWidget):
    """Widget pour l'effet modulation filter du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du modulation filter."""
        # Titre
        title = ttk.Label(self, text="Modulation Filter", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["Low Pass Filter", "High Pass Filter", "Band Pass Filter"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Freq.
        self.create_parameter_widget(
            "Freq.",
            param_type="double_spinbox",
            min_val=0.05,
            max_val=40.00,
            step=0.05,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="logScale",
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
        
        # Phase
        self.create_parameter_widget(
            "Phase",
            param_type="double_spinbox",
            min_val=0.00,
            max_val=354.38,
            step=0.01,
            suffix="°",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Offset
        self.create_parameter_widget(
            "Offset",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Resonance
        self.create_parameter_widget(
            "Resonance",
            param_type="spinbox",
            min_val=0,
            max_val=20,
            step=1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Level
        self.create_parameter_widget(
            "Level",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=6,
            length=1,
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
            offset=7,
            length=1,
            row=4, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du modulation filter."""
        params = {}
        
        # Mod. Filter parameters
        params['type'] = self.get_parameter_value("Type")
        params['freq'] = self.get_parameter_value("Freq.")
        params['depth'] = self.get_parameter_value("Depth")
        params['phase'] = self.get_parameter_value("Phase")
        params['offset'] = self.get_parameter_value("Offset")
        params['resonance'] = self.get_parameter_value("Resonance")
        params['level'] = self.get_parameter_value("Level")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du modulation filter."""
        # Mod. Filter parameters
        if 'type' in params:
            self.set_parameter_value("Type", params['type'])
        if 'freq' in params:
            self.set_parameter_value("Freq.", params['freq'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'phase' in params:
            self.set_parameter_value("Phase", params['phase'])
        if 'offset' in params:
            self.set_parameter_value("Offset", params['offset'])
        if 'resonance' in params:
            self.set_parameter_value("Resonance", params['resonance'])
        if 'level' in params:
            self.set_parameter_value("Level", params['level'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class DynaFilterWidget(BaseEffectWidget):
    """Widget pour l'effet dynamic filter du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du dynamic filter."""
        # Titre
        title = ttk.Label(self, text="Dynamic Filter", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["Low Pass Filter", "High Pass Filter", "Band Pass Filter"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Decay
        self.create_parameter_widget(
            "Decay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Direction
        self.create_parameter_widget(
            "Direction",
            param_type="combobox",
            values=["Down", "Up"],
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Sense
        self.create_parameter_widget(
            "Sense",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Offset
        self.create_parameter_widget(
            "Offset",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Resonance
        self.create_parameter_widget(
            "Resonance",
            param_type="spinbox",
            min_val=0,
            max_val=20,
            step=1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Level
        self.create_parameter_widget(
            "Level",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=6,
            length=1,
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
            offset=7,
            length=1,
            row=4, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du dynamic filter."""
        params = {}
        
        # Dynamic Filter parameters
        params['type'] = self.get_parameter_value("Type")
        params['decay'] = self.get_parameter_value("Decay")
        params['direction'] = self.get_parameter_value("Direction")
        params['sense'] = self.get_parameter_value("Sense")
        params['offset'] = self.get_parameter_value("Offset")
        params['resonance'] = self.get_parameter_value("Resonance")
        params['level'] = self.get_parameter_value("Level")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du dynamic filter."""
        # Dynamic Filter parameters
        if 'type' in params:
            self.set_parameter_value("Type", params['type'])
        if 'decay' in params:
            self.set_parameter_value("Decay", params['decay'])
        if 'direction' in params:
            self.set_parameter_value("Direction", params['direction'])
        if 'sense' in params:
            self.set_parameter_value("Sense", params['sense'])
        if 'offset' in params:
            self.set_parameter_value("Offset", params['offset'])
        if 'resonance' in params:
            self.set_parameter_value("Resonance", params['resonance'])
        if 'level' in params:
            self.set_parameter_value("Level", params['level'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])
