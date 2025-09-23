"""
Multi-Tap Delay Widgets
=======================

Widgets pour les effets de delay multi-tap du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class EightBandParallelDelayWidget(BaseEffectWidget):
    """Widget pour l'effet 8 Band Parallel Delay du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du 8 Band Parallel Delay."""
        # Titre
        title = ttk.Label(self, text="8 Band Parallel Delay", font=("Arial", 12, "bold"))
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
        
        # Band 1 Time
        self.create_parameter_widget(
            "Band 1 Time",
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
        
        # Band 1 Low Cut Filter
        self.create_parameter_widget(
            "Band 1 Low Cut Filter",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Band 1 High Cut Filter
        self.create_parameter_widget(
            "Band 1 High Cut Filter",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Band 1 Feedback
        self.create_parameter_widget(
            "Band 1 Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Band 1 Wave
        self.create_parameter_widget(
            "Band 1 Wave",
            param_type="combobox",
            values=["Sine", "Other"],
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Band 1 Phase
        self.create_parameter_widget(
            "Band 1 Phase",
            param_type="combobox",
            values=["Normal", "Reverse"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Band 1 Tap
        self.create_parameter_widget(
            "Band 1 Tap",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # Band 1 Speed
        self.create_parameter_widget(
            "Band 1 Speed",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Band 1 Depth
        self.create_parameter_widget(
            "Band 1 Depth",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=12,
            length=1,
            row=7, column=0
        )
        
        # Band 1 Pan
        self.create_parameter_widget(
            "Band 1 Pan",
            param_type="double_spinbox",
            min_val=-10.0,
            max_val=10.0,
            step=0.1,
            suffix=" (L/R)",
            offset=13,
            length=1,
            row=7, column=2
        )
        
        # Band 1 Level
        self.create_parameter_widget(
            "Band 1 Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=14,
            length=1,
            row=8, column=0
        )
        
        # Band 1 Sync
        self.create_parameter_widget(
            "Band 1 Sync",
            param_type="spinbox",
            min_val=1,
            max_val=8,
            step=1,
            offset=15,
            length=1,
            row=8, column=2
        )
        
        # Note: Pour simplifier, on ne montre que les paramètres de la première bande
        # En réalité, il y aurait 8 bandes avec les mêmes paramètres
        note = ttk.Label(self, text="Note: Only Band 1 parameters shown. Full version would have 8 bands.", 
                        font=("Arial", 8, "italic"), foreground="gray")
        note.grid(row=9, column=0, columnspan=6, pady=(5, 0))
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du 8 Band Parallel Delay."""
        params = {}
        
        # 8 Band Parallel Delay parameters
        params['wave_form'] = self.get_parameter_value("Wave Form")
        params['effect_level'] = self.get_parameter_value("Effect Level")
        params['direct_level'] = self.get_parameter_value("Direct Level")
        params['direct_pan'] = self.get_parameter_value("Direct Pan")
        
        # Band 1 parameters (simplified)
        params['band1_time'] = self.get_parameter_value("Band 1 Time")
        params['band1_low_cut_filter'] = self.get_parameter_value("Band 1 Low Cut Filter")
        params['band1_high_cut_filter'] = self.get_parameter_value("Band 1 High Cut Filter")
        params['band1_feedback'] = self.get_parameter_value("Band 1 Feedback")
        params['band1_wave'] = self.get_parameter_value("Band 1 Wave")
        params['band1_phase'] = self.get_parameter_value("Band 1 Phase")
        params['band1_tap'] = self.get_parameter_value("Band 1 Tap")
        params['band1_speed'] = self.get_parameter_value("Band 1 Speed")
        params['band1_depth'] = self.get_parameter_value("Band 1 Depth")
        params['band1_pan'] = self.get_parameter_value("Band 1 Pan")
        params['band1_level'] = self.get_parameter_value("Band 1 Level")
        params['band1_sync'] = self.get_parameter_value("Band 1 Sync")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du 8 Band Parallel Delay."""
        # 8 Band Parallel Delay parameters
        if 'wave_form' in params:
            self.set_parameter_value("Wave Form", params['wave_form'])
        if 'effect_level' in params:
            self.set_parameter_value("Effect Level", params['effect_level'])
        if 'direct_level' in params:
            self.set_parameter_value("Direct Level", params['direct_level'])
        if 'direct_pan' in params:
            self.set_parameter_value("Direct Pan", params['direct_pan'])
        
        # Band 1 parameters (simplified)
        if 'band1_time' in params:
            self.set_parameter_value("Band 1 Time", params['band1_time'])
        if 'band1_low_cut_filter' in params:
            self.set_parameter_value("Band 1 Low Cut Filter", params['band1_low_cut_filter'])
        if 'band1_high_cut_filter' in params:
            self.set_parameter_value("Band 1 High Cut Filter", params['band1_high_cut_filter'])
        if 'band1_feedback' in params:
            self.set_parameter_value("Band 1 Feedback", params['band1_feedback'])
        if 'band1_wave' in params:
            self.set_parameter_value("Band 1 Wave", params['band1_wave'])
        if 'band1_phase' in params:
            self.set_parameter_value("Band 1 Phase", params['band1_phase'])
        if 'band1_tap' in params:
            self.set_parameter_value("Band 1 Tap", params['band1_tap'])
        if 'band1_speed' in params:
            self.set_parameter_value("Band 1 Speed", params['band1_speed'])
        if 'band1_depth' in params:
            self.set_parameter_value("Band 1 Depth", params['band1_depth'])
        if 'band1_pan' in params:
            self.set_parameter_value("Band 1 Pan", params['band1_pan'])
        if 'band1_level' in params:
            self.set_parameter_value("Band 1 Level", params['band1_level'])
        if 'band1_sync' in params:
            self.set_parameter_value("Band 1 Sync", params['band1_sync'])


class FourBandTwoTapModDelayWidget(BaseEffectWidget):
    """Widget pour l'effet 4 Band 2 Tap Mod. Delay du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du 4 Band 2 Tap Mod. Delay."""
        # Titre
        title = ttk.Label(self, text="4 Band 2 Tap Mod. Delay", font=("Arial", 12, "bold"))
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
        
        # Band 1 Time
        self.create_parameter_widget(
            "Band 1 Time",
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
        
        # Band 1 Low Cut Filter
        self.create_parameter_widget(
            "Band 1 Low Cut Filter",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Band 1 High Cut Filter
        self.create_parameter_widget(
            "Band 1 High Cut Filter",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # Band 1 Feedback
        self.create_parameter_widget(
            "Band 1 Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Band 1 Wave
        self.create_parameter_widget(
            "Band 1 Wave",
            param_type="combobox",
            values=["Sine", "Other"],
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Band 1 Phase
        self.create_parameter_widget(
            "Band 1 Phase",
            param_type="combobox",
            values=["Normal", "Reverse"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Band 1 Tap
        self.create_parameter_widget(
            "Band 1 Tap",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # Band 1 Speed
        self.create_parameter_widget(
            "Band 1 Speed",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Band 1 Depth
        self.create_parameter_widget(
            "Band 1 Depth",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=12,
            length=1,
            row=7, column=0
        )
        
        # Band 1 Pan
        self.create_parameter_widget(
            "Band 1 Pan",
            param_type="double_spinbox",
            min_val=-10.0,
            max_val=10.0,
            step=0.1,
            suffix=" (L/R)",
            offset=13,
            length=1,
            row=7, column=2
        )
        
        # Band 1 Level
        self.create_parameter_widget(
            "Band 1 Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=14,
            length=1,
            row=8, column=0
        )
        
        # Band 1 Sync
        self.create_parameter_widget(
            "Band 1 Sync",
            param_type="spinbox",
            min_val=1,
            max_val=8,
            step=1,
            offset=15,
            length=1,
            row=8, column=2
        )
        
        # Note: Pour simplifier, on ne montre que les paramètres de la première bande
        note = ttk.Label(self, text="Note: Only Band 1 parameters shown. Full version would have 4 bands with 2 taps each.", 
                        font=("Arial", 8, "italic"), foreground="gray")
        note.grid(row=9, column=0, columnspan=6, pady=(5, 0))
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du 4 Band 2 Tap Mod. Delay."""
        params = {}
        
        # 4 Band 2 Tap Mod. Delay parameters
        params['wave_form'] = self.get_parameter_value("Wave Form")
        params['effect_level'] = self.get_parameter_value("Effect Level")
        params['direct_level'] = self.get_parameter_value("Direct Level")
        params['direct_pan'] = self.get_parameter_value("Direct Pan")
        
        # Band 1 parameters (simplified)
        params['band1_time'] = self.get_parameter_value("Band 1 Time")
        params['band1_low_cut_filter'] = self.get_parameter_value("Band 1 Low Cut Filter")
        params['band1_high_cut_filter'] = self.get_parameter_value("Band 1 High Cut Filter")
        params['band1_feedback'] = self.get_parameter_value("Band 1 Feedback")
        params['band1_wave'] = self.get_parameter_value("Band 1 Wave")
        params['band1_phase'] = self.get_parameter_value("Band 1 Phase")
        params['band1_tap'] = self.get_parameter_value("Band 1 Tap")
        params['band1_speed'] = self.get_parameter_value("Band 1 Speed")
        params['band1_depth'] = self.get_parameter_value("Band 1 Depth")
        params['band1_pan'] = self.get_parameter_value("Band 1 Pan")
        params['band1_level'] = self.get_parameter_value("Band 1 Level")
        params['band1_sync'] = self.get_parameter_value("Band 1 Sync")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du 4 Band 2 Tap Mod. Delay."""
        # 4 Band 2 Tap Mod. Delay parameters
        if 'wave_form' in params:
            self.set_parameter_value("Wave Form", params['wave_form'])
        if 'effect_level' in params:
            self.set_parameter_value("Effect Level", params['effect_level'])
        if 'direct_level' in params:
            self.set_parameter_value("Direct Level", params['direct_level'])
        if 'direct_pan' in params:
            self.set_parameter_value("Direct Pan", params['direct_pan'])
        
        # Band 1 parameters (simplified)
        if 'band1_time' in params:
            self.set_parameter_value("Band 1 Time", params['band1_time'])
        if 'band1_low_cut_filter' in params:
            self.set_parameter_value("Band 1 Low Cut Filter", params['band1_low_cut_filter'])
        if 'band1_high_cut_filter' in params:
            self.set_parameter_value("Band 1 High Cut Filter", params['band1_high_cut_filter'])
        if 'band1_feedback' in params:
            self.set_parameter_value("Band 1 Feedback", params['band1_feedback'])
        if 'band1_wave' in params:
            self.set_parameter_value("Band 1 Wave", params['band1_wave'])
        if 'band1_phase' in params:
            self.set_parameter_value("Band 1 Phase", params['band1_phase'])
        if 'band1_tap' in params:
            self.set_parameter_value("Band 1 Tap", params['band1_tap'])
        if 'band1_speed' in params:
            self.set_parameter_value("Band 1 Speed", params['band1_speed'])
        if 'band1_depth' in params:
            self.set_parameter_value("Band 1 Depth", params['band1_depth'])
        if 'band1_pan' in params:
            self.set_parameter_value("Band 1 Pan", params['band1_pan'])
        if 'band1_level' in params:
            self.set_parameter_value("Band 1 Level", params['band1_level'])
        if 'band1_sync' in params:
            self.set_parameter_value("Band 1 Sync", params['band1_sync'])
