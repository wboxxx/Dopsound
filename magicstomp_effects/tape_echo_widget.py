"""
Tape Echo Widget
================

Widget pour l'effet tape echo du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class TapeEchoWidget(BaseEffectWidget):
    """Widget pour l'effet tape echo du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du tape echo."""
        # Titre
        title = ttk.Label(self, text="Tape Echo", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Time
        self.create_parameter_widget(
            "Time",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Level
        self.create_parameter_widget(
            "Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du tape echo."""
        params = {}
        
        # Tape Echo parameters
        params['time'] = self.get_parameter_value("Time")
        params['feedback'] = self.get_parameter_value("Feedback")
        params['level'] = self.get_parameter_value("Level")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du tape echo."""
        # Tape Echo parameters
        if 'time' in params:
            self.set_parameter_value("Time", params['time'])
        if 'feedback' in params:
            self.set_parameter_value("Feedback", params['feedback'])
        if 'level' in params:
            self.set_parameter_value("Level", params['level'])
