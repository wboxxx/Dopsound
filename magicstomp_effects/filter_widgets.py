"""
Filter Effect Widgets
====================

Widgets spécialisés pour les effets de filtre du Magicstomp.
Adaptés des widgets C++/Qt correspondants.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class MultiFilterWidget(BaseEffectWidget):
    """Widget pour le multi-filtre du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du multi-filtre."""
        # Titre
        title = ttk.Label(self, text="Multi Filter", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Filter 1 Type
        filter_types = ["LPF", "HPF", "BPF", "Notch", "All Pass"]
        self.create_parameter_widget(
            "Filter 1 Type",
            param_type="combobox",
            min_val=filter_types,
            max_val=len(filter_types)-1,
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Filter 1 Frequency
        self.create_parameter_widget(
            "Filter 1 Freq",
            param_type="double_spinbox",
            min_val=20.0,
            max_val=20000.0,
            step=10.0,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Filter 1 Q
        self.create_parameter_widget(
            "Filter 1 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=2, column=0
        )
        
        # Filter 1 Gain
        self.create_parameter_widget(
            "Filter 1 Gain",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" dB",
            offset=3,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=2, column=2
        )
        
        # Filter 2 Type
        self.create_parameter_widget(
            "Filter 2 Type",
            param_type="combobox",
            min_val=filter_types,
            max_val=len(filter_types)-1,
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Filter 2 Frequency
        self.create_parameter_widget(
            "Filter 2 Freq",
            param_type="double_spinbox",
            min_val=20.0,
            max_val=20000.0,
            step=10.0,
            suffix=" Hz",
            offset=5,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # Filter 2 Q
        self.create_parameter_widget(
            "Filter 2 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=4, column=0
        )
        
        # Filter 2 Gain
        self.create_parameter_widget(
            "Filter 2 Gain",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" dB",
            offset=7,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=4, column=2
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=8,
            length=1,
            row=5, column=0
        )


class DynamicFilterWidget(BaseEffectWidget):
    """Widget pour le filtre dynamique du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du filtre dynamique."""
        # Titre
        title = ttk.Label(self, text="Dynamic Filter", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Filter Type
        filter_types = ["LPF", "HPF", "BPF", "Notch"]
        self.create_parameter_widget(
            "Filter Type",
            param_type="combobox",
            min_val=filter_types,
            max_val=len(filter_types)-1,
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Base Frequency
        self.create_parameter_widget(
            "Base Freq",
            param_type="double_spinbox",
            min_val=20.0,
            max_val=20000.0,
            step=10.0,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Q
        self.create_parameter_widget(
            "Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=2, column=0
        )
        
        # Sensitivity
        self.create_parameter_widget(
            "Sensitivity",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Range
        self.create_parameter_widget(
            "Range",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=10.0,
            step=0.1,
            suffix=" oct",
            offset=4,
            length=1,
            conversion="scaleAndAdd(0.1, 0.1)",
            row=3, column=0
        )
        
        # Attack
        self.create_parameter_widget(
            "Attack",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=1000.0,
            step=0.1,
            suffix=" ms",
            offset=5,
            length=1,
            conversion="timeMs",
            row=3, column=2
        )
        
        # Release
        self.create_parameter_widget(
            "Release",
            param_type="double_spinbox",
            min_val=1.0,
            max_val=5000.0,
            step=1.0,
            suffix=" ms",
            offset=6,
            length=1,
            conversion="timeMs",
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


class ThreeBandEQWidget(BaseEffectWidget):
    """Widget pour l'égaliseur 3 bandes du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface de l'égaliseur 3 bandes."""
        # Titre
        title = ttk.Label(self, text="3 Band Parametric EQ", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Low Gain
        self.create_parameter_widget(
            "Low Gain",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" dB",
            offset=0,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=1, column=0
        )
        
        # Low Frequency
        self.create_parameter_widget(
            "Low Freq",
            param_type="double_spinbox",
            min_val=80.0,
            max_val=500.0,
            step=10.0,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Low Q
        self.create_parameter_widget(
            "Low Q",
            param_type="double_spinbox",
            min_val=0.5,
            max_val=5.0,
            step=0.1,
            offset=2,
            length=1,
            conversion="scaleAndAdd(0.1, 0.5)",
            row=2, column=0
        )
        
        # Mid Gain
        self.create_parameter_widget(
            "Mid Gain",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" dB",
            offset=3,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=2, column=2
        )
        
        # Mid Frequency
        self.create_parameter_widget(
            "Mid Freq",
            param_type="double_spinbox",
            min_val=200.0,
            max_val=5000.0,
            step=50.0,
            suffix=" Hz",
            offset=4,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # Mid Q
        self.create_parameter_widget(
            "Mid Q",
            param_type="double_spinbox",
            min_val=0.5,
            max_val=5.0,
            step=0.1,
            offset=5,
            length=1,
            conversion="scaleAndAdd(0.1, 0.5)",
            row=3, column=2
        )
        
        # High Gain
        self.create_parameter_widget(
            "High Gain",
            param_type="spinbox",
            min_val=-12,
            max_val=12,
            step=1,
            suffix=" dB",
            offset=6,
            length=1,
            conversion="scaleAndAdd(1, -12)",
            row=4, column=0
        )
        
        # High Frequency
        self.create_parameter_widget(
            "High Freq",
            param_type="double_spinbox",
            min_val=2000.0,
            max_val=8000.0,
            step=100.0,
            suffix=" Hz",
            offset=7,
            length=1,
            conversion="logScale",
            row=4, column=2
        )
        
        # High Q
        self.create_parameter_widget(
            "High Q",
            param_type="double_spinbox",
            min_val=0.5,
            max_val=5.0,
            step=0.1,
            offset=8,
            length=1,
            conversion="scaleAndAdd(0.1, 0.5)",
            row=5, column=0
        )
