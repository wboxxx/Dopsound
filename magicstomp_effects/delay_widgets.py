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
        
        # Low Ratio
        self.create_parameter_widget(
            "Low Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=6,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=3, column=0
        )


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
        
        # L Time (Temps canal gauche)
        self.create_parameter_widget(
            "L Time",
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
        
        # R Time (Temps canal droit)
        self.create_parameter_widget(
            "R Time",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.2,
            suffix=" ms",
            offset=2,
            length=2,
            conversion="timeMs",
            row=1, column=2
        )
        
        # L Mix
        self.create_parameter_widget(
            "L Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=4,
            length=1,
            row=2, column=0
        )
        
        # R Mix
        self.create_parameter_widget(
            "R Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=2, column=2
        )
        
        # L FB Gain
        self.create_parameter_widget(
            "L FB Gain",
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
        
        # R FB Gain
        self.create_parameter_widget(
            "R FB Gain",
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
        
        # Time
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
        
        # FB Gain
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
        
        # Rate (Taux de modulation)
        self.create_parameter_widget(
            "Rate",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            suffix=" Hz",
            offset=5,
            length=1,
            conversion="freqHz",
            row=2, column=2
        )
        
        # Depth (Profondeur de modulation)
        self.create_parameter_widget(
            "Depth",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=6,
            length=1,
            row=3, column=0
        )


class EchoWidget(BaseEffectWidget):
    """Widget pour l'effet echo du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface de l'echo."""
        # Titre
        title = ttk.Label(self, text="Echo", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # L Time
        self.create_parameter_widget(
            "L Time",
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
        
        # R Time
        self.create_parameter_widget(
            "R Time",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=2730.0,
            step=0.2,
            suffix=" ms",
            offset=2,
            length=2,
            conversion="timeMs",
            row=1, column=2
        )
        
        # L Mix
        self.create_parameter_widget(
            "L Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=4,
            length=1,
            row=2, column=0
        )
        
        # R Mix
        self.create_parameter_widget(
            "R Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=2, column=2
        )
        
        # L FB Gain
        self.create_parameter_widget(
            "L FB Gain",
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
        
        # R FB Gain
        self.create_parameter_widget(
            "R FB Gain",
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
