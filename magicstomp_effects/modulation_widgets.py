"""
Modulation Effect Widgets
========================

Widgets spécialisés pour les effets de modulation du Magicstomp.
Adaptés des widgets C++/Qt correspondants.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class ChorusWidget(BaseEffectWidget):
    """Widget pour l'effet chorus du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du chorus."""
        # Titre
        title = ttk.Label(self, text="Chorus", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Wave (Forme d'onde)
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            min_val=["Sine", "Triangle"],
            max_val=1,
            offset=0,
            length=1,
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
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Rate (Taux de modulation)
        self.create_parameter_widget(
            "Rate",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            suffix=" Hz",
            offset=2,
            length=1,
            conversion="freqHz",
            row=2, column=0
        )
        
        # Depth (Profondeur)
        self.create_parameter_widget(
            "Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Delay (Délai de base)
        self.create_parameter_widget(
            "Delay",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=50.0,
            step=0.1,
            suffix=" ms",
            offset=4,
            length=1,
            conversion="timeMs",
            row=3, column=0
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="spinbox",
            min_val=0,
            max_val=99,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=3, column=2
        )


class FlangeWidget(BaseEffectWidget):
    """Widget pour l'effet flanger du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du flanger."""
        # Titre
        title = ttk.Label(self, text="Flanger", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            min_val=["Sine", "Triangle"],
            max_val=1,
            offset=0,
            length=1,
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
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Rate
        self.create_parameter_widget(
            "Rate",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            suffix=" Hz",
            offset=2,
            length=1,
            conversion="freqHz",
            row=2, column=0
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Delay
        self.create_parameter_widget(
            "Delay",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=10.0,
            step=0.1,
            suffix=" ms",
            offset=4,
            length=1,
            conversion="timeMs",
            row=3, column=0
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="spinbox",
            min_val=0,
            max_val=99,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=3, column=2
        )


class PhaserWidget(BaseEffectWidget):
    """Widget pour l'effet phaser du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du phaser."""
        # Titre
        title = ttk.Label(self, text="Phaser", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Rate
        self.create_parameter_widget(
            "Rate",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="freqHz",
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
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="spinbox",
            min_val=0,
            max_val=99,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Stages (Nombre d'étages)
        self.create_parameter_widget(
            "Stages",
            param_type="spinbox",
            min_val=2,
            max_val=12,
            step=1,
            offset=4,
            length=1,
            row=3, column=0
        )


class TremoloWidget(BaseEffectWidget):
    """Widget pour l'effet tremolo du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du tremolo."""
        # Titre
        title = ttk.Label(self, text="Tremolo", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Rate
        self.create_parameter_widget(
            "Rate",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="freqHz",
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
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            min_val=["Sine", "Triangle", "Square"],
            max_val=2,
            offset=3,
            length=1,
            row=2, column=2
        )
