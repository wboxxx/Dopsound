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
        
        # Type 1
        self.create_parameter_widget(
            "Type 1",
            param_type="combobox",
            values=["Low Pass Filter", "High Pass Filter", "Band Pass Filter"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Freq. 1
        self.create_parameter_widget(
            "Freq. 1",
            param_type="double_spinbox",
            min_val=28.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=1,
            length=1,
            conversion="logScale",
            row=1, column=2
        )
        
        # Level 1
        self.create_parameter_widget(
            "Level 1",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Resonance 1
        self.create_parameter_widget(
            "Resonance 1",
            param_type="spinbox",
            min_val=0,
            max_val=20,
            step=1,
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Mix
        self.create_parameter_widget(
            "Mix",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Type 2
        self.create_parameter_widget(
            "Type 2",
            param_type="combobox",
            values=["Low Pass Filter", "High Pass Filter", "Band Pass Filter"],
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Freq. 2
        self.create_parameter_widget(
            "Freq. 2",
            param_type="double_spinbox",
            min_val=28.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=6,
            length=1,
            conversion="logScale",
            row=4, column=0
        )
        
        # Level 2
        self.create_parameter_widget(
            "Level 2",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Resonance 2
        self.create_parameter_widget(
            "Resonance 2",
            param_type="spinbox",
            min_val=0,
            max_val=20,
            step=1,
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Type 3
        self.create_parameter_widget(
            "Type 3",
            param_type="combobox",
            values=["Low Pass Filter", "High Pass Filter", "Band Pass Filter"],
            offset=9,
            length=1,
            row=5, column=2
        )
        
        # Freq. 3
        self.create_parameter_widget(
            "Freq. 3",
            param_type="double_spinbox",
            min_val=28.0,
            max_val=16000.0,
            step=10.0,
            suffix=" Hz",
            offset=10,
            length=1,
            conversion="logScale",
            row=6, column=0
        )
        
        # Level 3
        self.create_parameter_widget(
            "Level 3",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=11,
            length=1,
            row=6, column=2
        )
        
        # Resonance 3
        self.create_parameter_widget(
            "Resonance 3",
            param_type="spinbox",
            min_val=0,
            max_val=20,
            step=1,
            offset=12,
            length=1,
            row=7, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du multi-filtre."""
        params = {}
        
        # Multi Filter parameters
        params['type1'] = self.get_parameter_value("Type 1")
        params['freq1'] = self.get_parameter_value("Freq. 1")
        params['level1'] = self.get_parameter_value("Level 1")
        params['resonance1'] = self.get_parameter_value("Resonance 1")
        params['mix'] = self.get_parameter_value("Mix")
        params['type2'] = self.get_parameter_value("Type 2")
        params['freq2'] = self.get_parameter_value("Freq. 2")
        params['level2'] = self.get_parameter_value("Level 2")
        params['resonance2'] = self.get_parameter_value("Resonance 2")
        params['type3'] = self.get_parameter_value("Type 3")
        params['freq3'] = self.get_parameter_value("Freq. 3")
        params['level3'] = self.get_parameter_value("Level 3")
        params['resonance3'] = self.get_parameter_value("Resonance 3")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du multi-filtre."""
        # Multi Filter parameters
        if 'type1' in params:
            self.set_parameter_value("Type 1", params['type1'])
        if 'freq1' in params:
            self.set_parameter_value("Freq. 1", params['freq1'])
        if 'level1' in params:
            self.set_parameter_value("Level 1", params['level1'])
        if 'resonance1' in params:
            self.set_parameter_value("Resonance 1", params['resonance1'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])
        if 'type2' in params:
            self.set_parameter_value("Type 2", params['type2'])
        if 'freq2' in params:
            self.set_parameter_value("Freq. 2", params['freq2'])
        if 'level2' in params:
            self.set_parameter_value("Level 2", params['level2'])
        if 'resonance2' in params:
            self.set_parameter_value("Resonance 2", params['resonance2'])
        if 'type3' in params:
            self.set_parameter_value("Type 3", params['type3'])
        if 'freq3' in params:
            self.set_parameter_value("Freq. 3", params['freq3'])
        if 'level3' in params:
            self.set_parameter_value("Level 3", params['level3'])
        if 'resonance3' in params:
            self.set_parameter_value("Resonance 3", params['resonance3'])


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
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["Low Pass Filter", "High Pass Filter", "Band Pass Filter"],
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Decay
        self.create_parameter_widget(
            "Decay",
            param_type="spinbox",
            min_val=6,
            max_val=46000,
            step=10,
            suffix=" ms",
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
        
        # Resonance
        self.create_parameter_widget(
            "Resonance",
            param_type="spinbox",
            min_val=0,
            max_val=20,
            step=1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Level
        self.create_parameter_widget(
            "Level",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=6,
            length=1,
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
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du filtre dynamique."""
        params = {}
        
        # Dynamic Filter parameters
        params['type'] = self.get_parameter_value("Type")
        params['decay'] = self.get_parameter_value("Decay")
        params['direction'] = self.get_parameter_value("Direction")
        params['sense'] = self.get_parameter_value("Sense")
        params['offset'] = self.get_parameter_value("Offset")
        params['resonance'] = self.get_parameter_value("Resonance")
        params['level'] = self.get_parameter_value("Level")
        params['mix'] = self.get_parameter_value("Mix")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du filtre dynamique."""
        # Dynamic Filter parameters
        if 'type' in params:
            self.set_parameter_value("Type", params['type'])
        if 'decay' in params:
            self.set_parameter_value("Decay", params['decay'])
        if 'direction' in params:
            self.set_parameter_value("Direction", params['direction'])
        if 'sense' in params:
            self.set_parameter_value("Sense", params['sense'])
        if 'offset' in params:
            self.set_parameter_value("Offset", params['offset'])
        if 'resonance' in params:
            self.set_parameter_value("Resonance", params['resonance'])
        if 'level' in params:
            self.set_parameter_value("Level", params['level'])
        if 'mix' in params:
            self.set_parameter_value("Mix", params['mix'])


class CompressorWidget(BaseEffectWidget):
    """Widget pour le compressor du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du compressor."""
        # Titre
        title = ttk.Label(self, text="Compressor", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=(0, 10))
        
        # Threshold
        self.create_parameter_widget(
            "Threshold",
            param_type="double_spinbox",
            min_val=-96.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # Ratio
        self.create_parameter_widget(
            "Ratio",
            param_type="double_spinbox",
            min_val=1.0,
            max_val=20.0,
            step=0.1,
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # Attack
        self.create_parameter_widget(
            "Attack",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=120.0,
            step=1.0,
            suffix=" ms",
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # Release
        self.create_parameter_widget(
            "Release",
            param_type="double_spinbox",
            min_val=6.0,
            max_val=11500.0,
            step=10.0,
            suffix=" ms",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # Slope
        self.create_parameter_widget(
            "Slope",
            param_type="spinbox",
            min_val=0,
            max_val=1,
            step=1,
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # Low Gain
        self.create_parameter_widget(
            "Low Gain",
            param_type="double_spinbox",
            min_val=-96.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # Mid Gain
        self.create_parameter_widget(
            "Mid Gain",
            param_type="double_spinbox",
            min_val=-96.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # High Gain
        self.create_parameter_widget(
            "High Gain",
            param_type="double_spinbox",
            min_val=-96.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # Lookup
        self.create_parameter_widget(
            "Lookup",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=100.0,
            step=0.1,
            suffix=" ms",
            offset=8,
            length=1,
            row=5, column=0
        )
        
        # Ceiling
        self.create_parameter_widget(
            "Ceiling",
            param_type="double_spinbox",
            min_val=-6.0,
            max_val=0.0,
            step=0.1,
            suffix=" dB",
            offset=9,
            length=1,
            row=5, column=2
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du compressor."""
        params = {}
        
        # Compressor parameters
        params['threshold'] = self.get_parameter_value("Threshold")
        params['ratio'] = self.get_parameter_value("Ratio")
        params['attack'] = self.get_parameter_value("Attack")
        params['release'] = self.get_parameter_value("Release")
        params['slope'] = self.get_parameter_value("Slope")
        params['low_gain'] = self.get_parameter_value("Low Gain")
        params['mid_gain'] = self.get_parameter_value("Mid Gain")
        params['high_gain'] = self.get_parameter_value("High Gain")
        params['lookup'] = self.get_parameter_value("Lookup")
        params['ceiling'] = self.get_parameter_value("Ceiling")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du compressor."""
        # Compressor parameters
        if 'threshold' in params:
            self.set_parameter_value("Threshold", params['threshold'])
        if 'ratio' in params:
            self.set_parameter_value("Ratio", params['ratio'])
        if 'attack' in params:
            self.set_parameter_value("Attack", params['attack'])
        if 'release' in params:
            self.set_parameter_value("Release", params['release'])
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
        
        # EQ1 Gain (Low)
        self.create_parameter_widget(
            "EQ1 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=0,
            length=1,
            row=1, column=0
        )
        
        # EQ1 Frequency (Low)
        self.create_parameter_widget(
            "EQ1 Freq",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=400.0,
            step=10.0,
            suffix=" Hz",
            offset=1,
            length=1,
            row=1, column=2
        )
        
        # EQ1 Q (Low)
        self.create_parameter_widget(
            "EQ1 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=2,
            length=1,
            row=2, column=0
        )
        
        # EQ2 Gain (Mid)
        self.create_parameter_widget(
            "EQ2 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=3,
            length=1,
            row=2, column=2
        )
        
        # EQ2 Frequency (Mid)
        self.create_parameter_widget(
            "EQ2 Freq",
            param_type="double_spinbox",
            min_val=200.0,
            max_val=1600.0,
            step=10.0,
            suffix=" Hz",
            offset=4,
            length=1,
            row=3, column=0
        )
        
        # EQ2 Q (Mid)
        self.create_parameter_widget(
            "EQ2 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=5,
            length=1,
            row=3, column=2
        )
        
        # EQ3 Gain (High)
        self.create_parameter_widget(
            "EQ3 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=6,
            length=1,
            row=4, column=0
        )
        
        # EQ3 Frequency (High)
        self.create_parameter_widget(
            "EQ3 Freq",
            param_type="double_spinbox",
            min_val=600.0,
            max_val=4800.0,
            step=10.0,
            suffix=" Hz",
            offset=7,
            length=1,
            row=4, column=2
        )
        
        # EQ3 Q (High)
        self.create_parameter_widget(
            "EQ3 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=8,
            length=1,
            row=5, column=0
        )
    
    def get_all_parameters(self):
        """Retourne tous les paramètres de l'égaliseur 3 bandes."""
        params = {}
        
        # EQ parameters
        params['eq1_gain'] = self.get_parameter_value("EQ1 Gain")
        params['eq1_freq'] = self.get_parameter_value("EQ1 Freq")
        params['eq1_q'] = self.get_parameter_value("EQ1 Q")
        params['eq2_gain'] = self.get_parameter_value("EQ2 Gain")
        params['eq2_freq'] = self.get_parameter_value("EQ2 Freq")
        params['eq2_q'] = self.get_parameter_value("EQ2 Q")
        params['eq3_gain'] = self.get_parameter_value("EQ3 Gain")
        params['eq3_freq'] = self.get_parameter_value("EQ3 Freq")
        params['eq3_q'] = self.get_parameter_value("EQ3 Q")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres de l'égaliseur 3 bandes."""
        # EQ parameters
        if 'eq1_gain' in params:
            self.set_parameter_value("EQ1 Gain", params['eq1_gain'])
        if 'eq1_freq' in params:
            self.set_parameter_value("EQ1 Freq", params['eq1_freq'])
        if 'eq1_q' in params:
            self.set_parameter_value("EQ1 Q", params['eq1_q'])
        if 'eq2_gain' in params:
            self.set_parameter_value("EQ2 Gain", params['eq2_gain'])
        if 'eq2_freq' in params:
            self.set_parameter_value("EQ2 Freq", params['eq2_freq'])
        if 'eq2_q' in params:
            self.set_parameter_value("EQ2 Q", params['eq2_q'])
        if 'eq3_gain' in params:
            self.set_parameter_value("EQ3 Gain", params['eq3_gain'])
        if 'eq3_freq' in params:
            self.set_parameter_value("EQ3 Freq", params['eq3_freq'])
        if 'eq3_q' in params:
            self.set_parameter_value("EQ3 Q", params['eq3_q'])
