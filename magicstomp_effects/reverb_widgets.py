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
        
        # Type
        reverb_types = [
            "Room", "Hall", "Plate", "Spring", "Chamber", 
            "Cathedral", "Ambience", "Gated", "Reverse"
        ]
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            min_val=reverb_types,
            max_val=len(reverb_types)-1,
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Time (Temps de reverb)
        self.create_parameter_widget(
            "Time",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            suffix=" s",
            offset=1,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
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
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=3,
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
            offset=4,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=3, column=0
        )
        
        # HPF (High Pass Filter)
        self.create_parameter_widget(
            "HPF",
            param_type="double_spinbox",
            min_val=20.0,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=5,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # LPF (Low Pass Filter)
        self.create_parameter_widget(
            "LPF",
            param_type="double_spinbox",
            min_val=1000.0,
            max_val=20000.0,
            step=100.0,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=4, column=0
        )


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
        
        # Time
        self.create_parameter_widget(
            "Time",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            suffix=" s",
            offset=0,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
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
        
        # Gate Time (Temps de gate)
        self.create_parameter_widget(
            "Gate Time",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=5.0,
            step=0.1,
            suffix=" s",
            offset=2,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=2, column=0
        )
        
        # High Ratio
        self.create_parameter_widget(
            "High Ratio",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1.0,
            step=0.1,
            offset=3,
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
            offset=4,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=3, column=0
        )
        
        # HPF
        self.create_parameter_widget(
            "HPF",
            param_type="double_spinbox",
            min_val=20.0,
            max_val=8000.0,
            step=10.0,
            suffix=" Hz",
            offset=5,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # LPF
        self.create_parameter_widget(
            "LPF",
            param_type="double_spinbox",
            min_val=1000.0,
            max_val=20000.0,
            step=100.0,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=4, column=0
        )


class SpringReverbWidget(BaseEffectWidget):
    """Widget pour l'effet spring reverb du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du spring reverb."""
        # Titre
        title = ttk.Label(self, text="Spring Reverb", font=("Arial", 12, "bold"))
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
        
        # Damping (Amortissement)
        self.create_parameter_widget(
            "Damping",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Spring Length (Longueur du ressort)
        self.create_parameter_widget(
            "Spring Length",
            param_type="spinbox",
            min_val=1,
            max_val=10,
            step=1,
            suffix="",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Character (Caractère)
        self.create_parameter_widget(
            "Character",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
