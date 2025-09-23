"""
Multi-Tap Delay Widgets Part 3
==============================

Widgets pour les derniers effets de delay multi-tap du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class EightMultiTapModDelayWidget(BaseEffectWidget):
    """Widget pour l'effet 8 Multi Tap Mod. Delay du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du 8 Multi Tap Mod. Delay."""
        # Titre
        title = ttk.Label(self, text="8 Multi Tap Mod. Delay", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Wave Form
        self.create_parameter_widget(
            "Wave Form",
            param_type="combobox",
            values=["Triangle", "Saw Up", "Saw Down"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Effect Level
        self.create_parameter_widget(
            "Effect Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Direct Level
        self.create_parameter_widget(
            "Direct Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Direct Pan
        self.create_parameter_widget(
            "Direct Pan",
            param_type="double_spinbox",
            min_val=-10.0,
            max_val=10.0,
            step=0.1,
            suffix=" (L/R)",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Time (Page1 only)
        self.create_parameter_widget(
            "Time",
            param_type="double_spinbox",
            min_val=0.5,
            max_val=5890.0,
            step=0.1,
            suffix=" ms",
            offset=4,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # Low Cut Filter (Page1 only)
        self.create_parameter_widget(
            "Low Cut Filter",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # High Cut Filter (Page1 only)
        self.create_parameter_widget(
            "High Cut Filter",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Feedback (Page1 only)
        self.create_parameter_widget(
            "Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            values=["Sine", "Other"],
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Phase
        self.create_parameter_widget(
            "Phase",
            param_type="combobox",
            values=["Normal", "Reverse"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Tap
        self.create_parameter_widget(
            "Tap",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # Speed
        self.create_parameter_widget(
            "Speed",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=12,
            length=1,
            row=7, column=0
        )
        
        # Pan
        self.create_parameter_widget(
            "Pan",
            param_type="double_spinbox",
            min_val=-10.0,
            max_val=10.0,
            step=0.1,
            suffix=" (L/R)",
            offset=13,
            length=1,
            row=7, column=2
        )
        
        # Level
        self.create_parameter_widget(
            "Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=14,
            length=1,
            row=8, column=0
        )
        
        # Sync
        self.create_parameter_widget(
            "Sync",
            param_type="spinbox",
            min_val=1,
            max_val=8,
            step=1,
            offset=15,
            length=1,
            row=8, column=2
        )
        
        # Note: Pour simplifier, on ne montre que les paramètres généraux
        note = ttk.Label(self, text="Note: Only general parameters shown. Full version would have 8 individual taps.", 
                        font=("Arial", 8, "italic"), foreground="gray")
        note.grid(row=9, column=0, columnspan=6, pady=(5, 0))
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du 8 Multi Tap Mod. Delay."""
        params = {}
        
        # 8 Multi Tap Mod. Delay parameters
        params['wave_form'] = self.get_parameter_value("Wave Form")
        params['effect_level'] = self.get_parameter_value("Effect Level")
        params['direct_level'] = self.get_parameter_value("Direct Level")
        params['direct_pan'] = self.get_parameter_value("Direct Pan")
        params['time'] = self.get_parameter_value("Time")
        params['low_cut_filter'] = self.get_parameter_value("Low Cut Filter")
        params['high_cut_filter'] = self.get_parameter_value("High Cut Filter")
        params['feedback'] = self.get_parameter_value("Feedback")
        params['wave'] = self.get_parameter_value("Wave")
        params['phase'] = self.get_parameter_value("Phase")
        params['tap'] = self.get_parameter_value("Tap")
        params['speed'] = self.get_parameter_value("Speed")
        params['depth'] = self.get_parameter_value("Depth")
        params['pan'] = self.get_parameter_value("Pan")
        params['level'] = self.get_parameter_value("Level")
        params['sync'] = self.get_parameter_value("Sync")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du 8 Multi Tap Mod. Delay."""
        # 8 Multi Tap Mod. Delay parameters
        if 'wave_form' in params:
            self.set_parameter_value("Wave Form", params['wave_form'])
        if 'effect_level' in params:
            self.set_parameter_value("Effect Level", params['effect_level'])
        if 'direct_level' in params:
            self.set_parameter_value("Direct Level", params['direct_level'])
        if 'direct_pan' in params:
            self.set_parameter_value("Direct Pan", params['direct_pan'])
        if 'time' in params:
            self.set_parameter_value("Time", params['time'])
        if 'low_cut_filter' in params:
            self.set_parameter_value("Low Cut Filter", params['low_cut_filter'])
        if 'high_cut_filter' in params:
            self.set_parameter_value("High Cut Filter", params['high_cut_filter'])
        if 'feedback' in params:
            self.set_parameter_value("Feedback", params['feedback'])
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'phase' in params:
            self.set_parameter_value("Phase", params['phase'])
        if 'tap' in params:
            self.set_parameter_value("Tap", params['tap'])
        if 'speed' in params:
            self.set_parameter_value("Speed", params['speed'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'pan' in params:
            self.set_parameter_value("Pan", params['pan'])
        if 'level' in params:
            self.set_parameter_value("Level", params['level'])
        if 'sync' in params:
            self.set_parameter_value("Sync", params['sync'])


class TwoBandLongFourShortModDelayWidget(BaseEffectWidget):
    """Widget pour l'effet 2 Band Long + 4 Short Mod. Delay du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du 2 Band Long + 4 Short Mod. Delay."""
        # Titre
        title = ttk.Label(self, text="2 Band Long + 4 Short Mod. Delay", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Wave Form
        self.create_parameter_widget(
            "Wave Form",
            param_type="combobox",
            values=["Triangle", "Saw Up", "Saw Down"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Effect Level
        self.create_parameter_widget(
            "Effect Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Direct Level
        self.create_parameter_widget(
            "Direct Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Direct Pan
        self.create_parameter_widget(
            "Direct Pan",
            param_type="double_spinbox",
            min_val=-10.0,
            max_val=10.0,
            step=0.1,
            suffix=" (L/R)",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Long Band Time
        self.create_parameter_widget(
            "Long Band Time",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=696.0,
            step=0.1,
            suffix=" ms",
            offset=4,
            length=1,
            conversion="logScale",
            row=3, column=0
        )
        
        # Long Band Low Cut Filter
        self.create_parameter_widget(
            "Long Band Low Cut Filter",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Long Band High Cut Filter
        self.create_parameter_widget(
            "Long Band High Cut Filter",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Long Band Feedback
        self.create_parameter_widget(
            "Long Band Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            values=["Sine", "Other"],
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Phase
        self.create_parameter_widget(
            "Phase",
            param_type="combobox",
            values=["Normal", "Reverse"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Tap
        self.create_parameter_widget(
            "Tap",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # Speed
        self.create_parameter_widget(
            "Speed",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=12,
            length=1,
            row=7, column=0
        )
        
        # Pan
        self.create_parameter_widget(
            "Pan",
            param_type="double_spinbox",
            min_val=-10.0,
            max_val=10.0,
            step=0.1,
            suffix=" (L/R)",
            offset=13,
            length=1,
            row=7, column=2
        )
        
        # Level
        self.create_parameter_widget(
            "Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=14,
            length=1,
            row=8, column=0
        )
        
        # Sync
        self.create_parameter_widget(
            "Sync",
            param_type="spinbox",
            min_val=1,
            max_val=8,
            step=1,
            offset=15,
            length=1,
            row=8, column=2
        )
        
        # Note: Pour simplifier, on ne montre que les paramètres généraux
        note = ttk.Label(self, text="Note: Only general parameters shown. Full version would have 2 long bands + 4 short bands.", 
                        font=("Arial", 8, "italic"), foreground="gray")
        note.grid(row=9, column=0, columnspan=6, pady=(5, 0))
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du 2 Band Long + 4 Short Mod. Delay."""
        params = {}
        
        # 2 Band Long + 4 Short Mod. Delay parameters
        params['wave_form'] = self.get_parameter_value("Wave Form")
        params['effect_level'] = self.get_parameter_value("Effect Level")
        params['direct_level'] = self.get_parameter_value("Direct Level")
        params['direct_pan'] = self.get_parameter_value("Direct Pan")
        params['long_band_time'] = self.get_parameter_value("Long Band Time")
        params['long_band_low_cut_filter'] = self.get_parameter_value("Long Band Low Cut Filter")
        params['long_band_high_cut_filter'] = self.get_parameter_value("Long Band High Cut Filter")
        params['long_band_feedback'] = self.get_parameter_value("Long Band Feedback")
        params['wave'] = self.get_parameter_value("Wave")
        params['phase'] = self.get_parameter_value("Phase")
        params['tap'] = self.get_parameter_value("Tap")
        params['speed'] = self.get_parameter_value("Speed")
        params['depth'] = self.get_parameter_value("Depth")
        params['pan'] = self.get_parameter_value("Pan")
        params['level'] = self.get_parameter_value("Level")
        params['sync'] = self.get_parameter_value("Sync")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du 2 Band Long + 4 Short Mod. Delay."""
        # 2 Band Long + 4 Short Mod. Delay parameters
        if 'wave_form' in params:
            self.set_parameter_value("Wave Form", params['wave_form'])
        if 'effect_level' in params:
            self.set_parameter_value("Effect Level", params['effect_level'])
        if 'direct_level' in params:
            self.set_parameter_value("Direct Level", params['direct_level'])
        if 'direct_pan' in params:
            self.set_parameter_value("Direct Pan", params['direct_pan'])
        if 'long_band_time' in params:
            self.set_parameter_value("Long Band Time", params['long_band_time'])
        if 'long_band_low_cut_filter' in params:
            self.set_parameter_value("Long Band Low Cut Filter", params['long_band_low_cut_filter'])
        if 'long_band_high_cut_filter' in params:
            self.set_parameter_value("Long Band High Cut Filter", params['long_band_high_cut_filter'])
        if 'long_band_feedback' in params:
            self.set_parameter_value("Long Band Feedback", params['long_band_feedback'])
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'phase' in params:
            self.set_parameter_value("Phase", params['phase'])
        if 'tap' in params:
            self.set_parameter_value("Tap", params['tap'])
        if 'speed' in params:
            self.set_parameter_value("Speed", params['speed'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'pan' in params:
            self.set_parameter_value("Pan", params['pan'])
        if 'level' in params:
            self.set_parameter_value("Level", params['level'])
        if 'sync' in params:
            self.set_parameter_value("Sync", params['sync'])
