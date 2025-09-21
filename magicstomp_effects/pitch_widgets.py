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
        
        # Pitch Shift
        self.create_parameter_widget(
            "Pitch Shift",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" semitones",
            offset=0,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=1, column=0
        )
        
        # Fine Tune
        self.create_parameter_widget(
            "Fine Tune",
            param_type="spinbox",
            min_val=-50,
            max_val=50,
            step=1,
            suffix=" cents",
            offset=1,
            length=1,
            conversion="scaleAndAdd(1, -50)",
            row=1, column=2
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
            row=2, column=0
        )
        
        # Formant Shift
        self.create_parameter_widget(
            "Formant Shift",
            param_type="spinbox",
            min_val=-50,
            max_val=50,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            conversion="scaleAndAdd(1, -50)",
            row=2, column=2
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="spinbox",
            min_val=0,
            max_val=99,
            step=1,
            suffix=" %",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Delay
        self.create_parameter_widget(
            "Delay",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=100.0,
            step=0.1,
            suffix=" ms",
            offset=5,
            length=1,
            conversion="timeMs",
            row=3, column=2
        )


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
        
        # Voice 1 Pitch Shift
        self.create_parameter_widget(
            "Voice 1 Pitch",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" semitones",
            offset=0,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=1, column=0
        )
        
        # Voice 1 Fine Tune
        self.create_parameter_widget(
            "Voice 1 Fine",
            param_type="spinbox",
            min_val=-50,
            max_val=50,
            step=1,
            suffix=" cents",
            offset=1,
            length=1,
            conversion="scaleAndAdd(1, -50)",
            row=1, column=2
        )
        
        # Voice 1 Level
        self.create_parameter_widget(
            "Voice 1 Level",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Voice 2 Pitch Shift
        self.create_parameter_widget(
            "Voice 2 Pitch",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" semitones",
            offset=3,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=2, column=2
        )
        
        # Voice 2 Fine Tune
        self.create_parameter_widget(
            "Voice 2 Fine",
            param_type="spinbox",
            min_val=-50,
            max_val=50,
            step=1,
            suffix=" cents",
            offset=4,
            length=1,
            conversion="scaleAndAdd(1, -50)",
            row=3, column=0
        )
        
        # Voice 2 Level
        self.create_parameter_widget(
            "Voice 2 Level",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Dry Level
        self.create_parameter_widget(
            "Dry Level",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="spinbox",
            min_val=0,
            max_val=99,
            step=1,
            suffix=" %",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Delay
        self.create_parameter_widget(
            "Delay",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=100.0,
            step=0.1,
            suffix=" ms",
            offset=8,
            length=1,
            conversion="timeMs",
            row=5, column=0
        )
        
        # Detune
        self.create_parameter_widget(
            "Detune",
            param_type="spinbox",
            min_val=0,
            max_val=50,
            step=1,
            suffix=" cents",
            offset=9,
            length=1,
            row=5, column=2
        )
