"""
Dynamics Widgets
================

Widgets pour les effets de dynamique du Magicstomp.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class MBandDynaWidget(BaseEffectWidget):
    """Widget pour l'effet multi-band dynamics du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du multi-band dynamics."""
        # Titre
        title = ttk.Label(self, text="Multi-Band Dynamics", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Slope
        self.create_parameter_widget(
            "Slope",
            param_type="combobox",
            values=["–6 dB", "–12 dB"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Low Gain
        self.create_parameter_widget(
            "Low Gain",
            param_type="double_spinbox",
            min_val=-96.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Mid Gain
        self.create_parameter_widget(
            "Mid Gain",
            param_type="double_spinbox",
            min_val=-96.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # High Gain
        self.create_parameter_widget(
            "High Gain",
            param_type="double_spinbox",
            min_val=-96.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Lookup
        self.create_parameter_widget(
            "Lookup",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=100.0,
            step=0.1,
            suffix=" ms",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Ceiling
        self.create_parameter_widget(
            "Ceiling",
            param_type="combobox",
            values=["Off", "–6.0 dB", "–5.0 dB", "–4.0 dB", "–3.0 dB", "–2.0 dB", "–1.0 dB", "0.0 dB"],
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # L–M Xover
        self.create_parameter_widget(
            "L–M Xover",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=0.1,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=4, column=0
        )
        
        # M–H Xover
        self.create_parameter_widget(
            "M–H Xover",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=0.1,
            suffix=" Hz",
            offset=7,
            length=1,
            conversion="logScale",
            row=4, column=2
        )
        
        # Presence
        self.create_parameter_widget(
            "Presence",
            param_type="spinbox",
            min_val=-10,
            max_val=10,
            step=1,
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Comp. Bypass
        self.create_parameter_widget(
            "Comp. Bypass",
            param_type="combobox",
            values=["Off", "On"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Comp. Threshold
        self.create_parameter_widget(
            "Comp. Threshold",
            param_type="double_spinbox",
            min_val=24.0,
            max_val=0.0,
            step=0.1,
            suffix=" dB",
            offset=10,
            length=1,
            row=6, column=0
        )
        
        # Comp. Ratio
        self.create_parameter_widget(
            "Comp. Ratio",
            param_type="combobox",
            values=["1:1", "2:1", "3:1", "4:1", "5:1", "6:1", "8:1", "10:1", "12:1", "15:1", "20:1"],
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Comp. Attack
        self.create_parameter_widget(
            "Comp. Attack",
            param_type="spinbox",
            min_val=0,
            max_val=120,
            step=1,
            suffix=" ms",
            offset=12,
            length=1,
            row=7, column=0
        )
        
        # Comp. Release
        self.create_parameter_widget(
            "Comp. Release",
            param_type="double_spinbox",
            min_val=6.0,
            max_val=11500.0,
            step=1.0,
            suffix=" ms",
            offset=13,
            length=1,
            conversion="logScale",
            row=7, column=2
        )
        
        # Comp. Knee
        self.create_parameter_widget(
            "Comp. Knee",
            param_type="spinbox",
            min_val=0,
            max_val=5,
            step=1,
            offset=14,
            length=1,
            row=8, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du multi-band dynamics."""
        params = {}
        
        # Multi-Band Dynamics parameters
        params['slope'] = self.get_parameter_value("Slope")
        params['low_gain'] = self.get_parameter_value("Low Gain")
        params['mid_gain'] = self.get_parameter_value("Mid Gain")
        params['high_gain'] = self.get_parameter_value("High Gain")
        params['lookup'] = self.get_parameter_value("Lookup")
        params['ceiling'] = self.get_parameter_value("Ceiling")
        params['l_m_xover'] = self.get_parameter_value("L–M Xover")
        params['m_h_xover'] = self.get_parameter_value("M–H Xover")
        params['presence'] = self.get_parameter_value("Presence")
        params['comp_bypass'] = self.get_parameter_value("Comp. Bypass")
        params['comp_threshold'] = self.get_parameter_value("Comp. Threshold")
        params['comp_ratio'] = self.get_parameter_value("Comp. Ratio")
        params['comp_attack'] = self.get_parameter_value("Comp. Attack")
        params['comp_release'] = self.get_parameter_value("Comp. Release")
        params['comp_knee'] = self.get_parameter_value("Comp. Knee")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du multi-band dynamics."""
        # Multi-Band Dynamics parameters
        if 'slope' in params:
            self.set_parameter_value("Slope", params['slope'])
        if 'low_gain' in params:
            self.set_parameter_value("Low Gain", params['low_gain'])
        if 'mid_gain' in params:
            self.set_parameter_value("Mid Gain", params['mid_gain'])
        if 'high_gain' in params:
            self.set_parameter_value("High Gain", params['high_gain'])
        if 'lookup' in params:
            self.set_parameter_value("Lookup", params['lookup'])
        if 'ceiling' in params:
            self.set_parameter_value("Ceiling", params['ceiling'])
        if 'l_m_xover' in params:
            self.set_parameter_value("L–M Xover", params['l_m_xover'])
        if 'm_h_xover' in params:
            self.set_parameter_value("M–H Xover", params['m_h_xover'])
        if 'presence' in params:
            self.set_parameter_value("Presence", params['presence'])
        if 'comp_bypass' in params:
            self.set_parameter_value("Comp. Bypass", params['comp_bypass'])
        if 'comp_threshold' in params:
            self.set_parameter_value("Comp. Threshold", params['comp_threshold'])
        if 'comp_ratio' in params:
            self.set_parameter_value("Comp. Ratio", params['comp_ratio'])
        if 'comp_attack' in params:
            self.set_parameter_value("Comp. Attack", params['comp_attack'])
        if 'comp_release' in params:
            self.set_parameter_value("Comp. Release", params['comp_release'])
        if 'comp_knee' in params:
            self.set_parameter_value("Comp. Knee", params['comp_knee'])


class DynaFlangeWidget(BaseEffectWidget):
    """Widget pour l'effet dynamic flange du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du dynamic flange."""
        # Titre
        title = ttk.Label(self, text="Dynamic Flange", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Decay
        self.create_parameter_widget(
            "Decay",
            param_type="double_spinbox",
            min_val=6.0,
            max_val=46000.0,
            step=1.0,
            suffix=" ms",
            offset=0,
            length=1,
            conversion="logScale",
            row=1, column=0
        )
        
        # FB. Gain
        self.create_parameter_widget(
            "FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Direction
        self.create_parameter_widget(
            "Direction",
            param_type="combobox",
            values=["Up", "Down"],
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
        
        # LSH Freq.
        self.create_parameter_widget(
            "LSH Freq.",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=0.1,
            suffix=" Hz",
            offset=5,
            length=1,
            conversion="logScale",
            row=3, column=2
        )
        
        # LSH Gain
        self.create_parameter_widget(
            "LSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # EQ Freq.
        self.create_parameter_widget(
            "EQ Freq.",
            param_type="double_spinbox",
            min_val=100.0,
            max_val=8000.0,
            step=1.0,
            suffix=" Hz",
            offset=7,
            length=1,
            conversion="logScale",
            row=4, column=2
        )
        
        # EQ Gain
        self.create_parameter_widget(
            "EQ Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # EQ Q
        self.create_parameter_widget(
            "EQ Q",
            param_type="double_spinbox",
            min_val=0.10,
            max_val=10.0,
            step=0.01,
            offset=9,
            length=1,
            conversion="logScale",
            row=5, column=2
        )
        
        # HSH Freq.
        self.create_parameter_widget(
            "HSH Freq.",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=1.0,
            suffix=" Hz",
            offset=10,
            length=1,
            conversion="logScale",
            row=6, column=0
        )
        
        # HSH Gain
        self.create_parameter_widget(
            "HSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=12,
            length=1,
            row=7, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du dynamic flange."""
        params = {}
        
        # Dynamic Flange parameters
        params['decay'] = self.get_parameter_value("Decay")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
        params['direction'] = self.get_parameter_value("Direction")
        params['sense'] = self.get_parameter_value("Sense")
        params['offset'] = self.get_parameter_value("Offset")
        params['lsh_freq'] = self.get_parameter_value("LSH Freq.")
        params['lsh_gain'] = self.get_parameter_value("LSH Gain")
        params['eq_freq'] = self.get_parameter_value("EQ Freq.")
        params['eq_gain'] = self.get_parameter_value("EQ Gain")
        params['eq_q'] = self.get_parameter_value("EQ Q")
        params['hsh_freq'] = self.get_parameter_value("HSH Freq.")
        params['hsh_gain'] = self.get_parameter_value("HSH Gain")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du dynamic flange."""
        # Dynamic Flange parameters
        if 'decay' in params:
            self.set_parameter_value("Decay", params['decay'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
        if 'direction' in params:
            self.set_parameter_value("Direction", params['direction'])
        if 'sense' in params:
            self.set_parameter_value("Sense", params['sense'])
        if 'offset' in params:
            self.set_parameter_value("Offset", params['offset'])
        if 'lsh_freq' in params:
            self.set_parameter_value("LSH Freq.", params['lsh_freq'])
        if 'lsh_gain' in params:
            self.set_parameter_value("LSH Gain", params['lsh_gain'])
        if 'eq_freq' in params:
            self.set_parameter_value("EQ Freq.", params['eq_freq'])
        if 'eq_gain' in params:
            self.set_parameter_value("EQ Gain", params['eq_gain'])
        if 'eq_q' in params:
            self.set_parameter_value("EQ Q", params['eq_q'])
        if 'hsh_freq' in params:
            self.set_parameter_value("HSH Freq.", params['hsh_freq'])
        if 'hsh_gain' in params:
            self.set_parameter_value("HSH Gain", params['hsh_gain'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class DynaPhaserWidget(BaseEffectWidget):
    """Widget pour l'effet dynamic phaser du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du dynamic phaser."""
        # Titre
        title = ttk.Label(self, text="Dynamic Phaser", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Decay
        self.create_parameter_widget(
            "Decay",
            param_type="double_spinbox",
            min_val=6.0,
            max_val=46000.0,
            step=1.0,
            suffix=" ms",
            offset=0,
            length=1,
            conversion="logScale",
            row=1, column=0
        )
        
        # FB. Gain
        self.create_parameter_widget(
            "FB. Gain",
            param_type="spinbox",
            min_val=-99,
            max_val=99,
            step=1,
            suffix=" %",
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Direction
        self.create_parameter_widget(
            "Direction",
            param_type="combobox",
            values=["Up", "Down"],
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
        
        # Stage
        self.create_parameter_widget(
            "Stage",
            param_type="combobox",
            values=["2", "4", "6", "8", "10", "12", "14", "16"],
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # LSH Freq.
        self.create_parameter_widget(
            "LSH Freq.",
            param_type="double_spinbox",
            min_val=21.2,
            max_val=8000.0,
            step=0.1,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=4, column=0
        )
        
        # LSH Gain
        self.create_parameter_widget(
            "LSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # HSH Freq.
        self.create_parameter_widget(
            "HSH Freq.",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=16000.0,
            step=1.0,
            suffix=" Hz",
            offset=8,
            length=1,
            conversion="logScale",
            row=5, column=0
        )
        
        # HSH Gain
        self.create_parameter_widget(
            "HSH Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=10,
            length=1,
            row=6, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du dynamic phaser."""
        params = {}
        
        # Dynamic Phaser parameters
        params['decay'] = self.get_parameter_value("Decay")
        params['fb_gain'] = self.get_parameter_value("FB. Gain")
        params['direction'] = self.get_parameter_value("Direction")
        params['sense'] = self.get_parameter_value("Sense")
        params['offset'] = self.get_parameter_value("Offset")
        params['stage'] = self.get_parameter_value("Stage")
        params['lsh_freq'] = self.get_parameter_value("LSH Freq.")
        params['lsh_gain'] = self.get_parameter_value("LSH Gain")
        params['hsh_freq'] = self.get_parameter_value("HSH Freq.")
        params['hsh_gain'] = self.get_parameter_value("HSH Gain")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du dynamic phaser."""
        # Dynamic Phaser parameters
        if 'decay' in params:
            self.set_parameter_value("Decay", params['decay'])
        if 'fb_gain' in params:
            self.set_parameter_value("FB. Gain", params['fb_gain'])
        if 'direction' in params:
            self.set_parameter_value("Direction", params['direction'])
        if 'sense' in params:
            self.set_parameter_value("Sense", params['sense'])
        if 'offset' in params:
            self.set_parameter_value("Offset", params['offset'])
        if 'stage' in params:
            self.set_parameter_value("Stage", params['stage'])
        if 'lsh_freq' in params:
            self.set_parameter_value("LSH Freq.", params['lsh_freq'])
        if 'lsh_gain' in params:
            self.set_parameter_value("LSH Gain", params['lsh_gain'])
        if 'hsh_freq' in params:
            self.set_parameter_value("HSH Freq.", params['hsh_freq'])
        if 'hsh_gain' in params:
            self.set_parameter_value("HSH Gain", params['hsh_gain'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])
