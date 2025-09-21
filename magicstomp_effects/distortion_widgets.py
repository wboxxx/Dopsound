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
        title = ttk.Label(self, text="Digital Distortion", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Type
        distortion_types = [
            "Overdrive", "Distortion", "Fuzz", "Crackle", "Bit Crusher",
            "Wave Shaper", "Tube Amp", "Solid State"
        ]
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            min_val=distortion_types,
            max_val=len(distortion_types)-1,
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
            suffix=" %",
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Level
        self.create_parameter_widget(
            "Level",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Tone
        self.create_parameter_widget(
            "Tone",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Bass
        self.create_parameter_widget(
            "Bass",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Mid
        self.create_parameter_widget(
            "Mid",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Treble
        self.create_parameter_widget(
            "Treble",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=6,
            length=1,
            row=4, column=0
        )


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
        
        # Type
        amp_types = [
            "Clean", "Crunch", "Lead", "Metal", "Vintage", "Modern",
            "British", "American", "German", "Japanese"
        ]
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            min_val=amp_types,
            max_val=len(amp_types)-1,
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Gain
        self.create_parameter_widget(
            "Gain",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Master Volume
        self.create_parameter_widget(
            "Master Volume",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Bass
        self.create_parameter_widget(
            "Bass",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Mid
        self.create_parameter_widget(
            "Mid",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Treble
        self.create_parameter_widget(
            "Treble",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Presence
        self.create_parameter_widget(
            "Presence",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Bright Switch
        self.create_parameter_widget(
            "Bright",
            param_type="combobox",
            min_val=["Off", "On"],
            max_val=1,
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Cabinet
        cabinet_types = [
            "1x8", "1x10", "1x12", "2x12", "4x10", "4x12", 
            "8x10", "Open Back", "Closed Back"
        ]
        self.create_parameter_widget(
            "Cabinet",
            param_type="combobox",
            min_val=cabinet_types,
            max_val=len(cabinet_types)-1,
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Microphone
        mic_types = [
            "Dynamic 57", "Dynamic 421", "Condenser 414", 
            "Ribbon 121", "Multi-mic"
        ]
        self.create_parameter_widget(
            "Microphone",
            param_type="combobox",
            min_val=mic_types,
            max_val=len(mic_types)-1,
            offset=9,
            length=1,
            row=5, column=2
        )
