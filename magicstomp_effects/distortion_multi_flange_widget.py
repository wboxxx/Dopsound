"""
Distortion Multi (Flange) Widget
================================

Widget spécialisé pour l'effet Distortion Multi (Flange) du Magicstomp.
Cet effet combine distorsion, noise gate, compressor, flanger, delay et reverb.
"""

import tkinter as tk
from tkinter import ttk
from .base_effect_widget import BaseEffectWidget


class DistortionMultiFlangeWidget(BaseEffectWidget):
    """Widget pour l'effet Distortion Multi (Flange) du Magicstomp."""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée l'interface du Distortion Multi (Flange)."""
        # Titre principal
        title = ttk.Label(self, text="Distortion Multi (Flange)", font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, columnspan=8, pady=(0, 15))
        
        # === SECTION DISTORSION ===
        dist_title = ttk.Label(self, text="Distortion", font=("Arial", 12, "bold"))
        dist_title.grid(row=1, column=0, columnspan=8, pady=(10, 5), sticky='w')
        
        # Type
        self.create_parameter_widget(
            "Type",
            param_type="combobox",
            values=["Lead1", "Lead2", "Drive1", "Drive2", "Crunch1", "Crunch2", 
                   "Fuzz1", "Fuzz2", "Distortion1", "Distortion2", "Overdrive1", 
                   "Overdrive2", "Tube", "Solidstate"],
            offset=11,
            length=1,
            row=2, column=0
        )
        
        # Gain
        self.create_parameter_widget(
            "Gain",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=8,
            length=1,
            row=2, column=2
        )
        
        # Master
        self.create_parameter_widget(
            "Master",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=9,
            length=1,
            row=2, column=4
        )
        
        # Tone
        self.create_parameter_widget(
            "Tone",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=10,
            length=1,
            row=3, column=0
        )
        
        # EQ 1 Freq
        self.create_parameter_widget(
            "EQ 1 Freq",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=400.0,
            step=10.0,
            suffix=" Hz",
            offset=0,
            length=1,
            row=3, column=2
        )
        
        # EQ 1 Gain
        self.create_parameter_widget(
            "EQ 1 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=19,
            length=1,
            row=3, column=4
        )
        
        # EQ 1 Q
        self.create_parameter_widget(
            "EQ 1 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=20,
            length=1,
            row=4, column=0
        )
        
        # EQ 2 Freq
        self.create_parameter_widget(
            "EQ 2 Freq",
            param_type="double_spinbox",
            min_val=200.0,
            max_val=1600.0,
            step=10.0,
            suffix=" Hz",
            offset=21,
            length=1,
            row=4, column=2
        )
        
        # EQ 2 Gain
        self.create_parameter_widget(
            "EQ 2 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=22,
            length=1,
            row=4, column=4
        )
        
        # EQ 2 Q
        self.create_parameter_widget(
            "EQ 2 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=23,
            length=1,
            row=5, column=0
        )
        
        # EQ 3 Freq
        self.create_parameter_widget(
            "EQ 3 Freq",
            param_type="double_spinbox",
            min_val=600.0,
            max_val=4800.0,
            step=10.0,
            suffix=" Hz",
            offset=24,
            length=1,
            row=5, column=2
        )
        
        # EQ 3 Gain
        self.create_parameter_widget(
            "EQ 3 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=25,
            length=1,
            row=5, column=4
        )
        
        # EQ 3 Q
        self.create_parameter_widget(
            "EQ 3 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=26,
            length=1,
            row=6, column=0
        )
        
        # EQ 4 Freq
        self.create_parameter_widget(
            "EQ 4 Freq",
            param_type="double_spinbox",
            min_val=2000.0,
            max_val=16000.0,
            step=100.0,
            suffix=" Hz",
            offset=27,
            length=1,
            row=6, column=2
        )
        
        # EQ 4 Gain
        self.create_parameter_widget(
            "EQ 4 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=28,
            length=1,
            row=6, column=4
        )
        
        # EQ 4 Q
        self.create_parameter_widget(
            "EQ 4 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=29,
            length=1,
            row=7, column=0
        )
        
        # Pre EQ Level
        self.create_parameter_widget(
            "Pre EQ Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=1,
            length=1,
            row=7, column=2
        )
        
        # Pre EQ 1 Freq
        self.create_parameter_widget(
            "Pre EQ 1 Freq",
            param_type="double_spinbox",
            min_val=50.0,
            max_val=400.0,
            step=10.0,
            suffix=" Hz",
            offset=32,
            length=1,
            row=8, column=0
        )
        
        # Pre EQ 1 Gain
        self.create_parameter_widget(
            "Pre EQ 1 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=33,
            length=1,
            row=8, column=2
        )
        
        # Pre EQ 1 Q
        self.create_parameter_widget(
            "Pre EQ 1 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=34,
            length=1,
            row=8, column=4
        )
        
        # Pre EQ 2 Freq
        self.create_parameter_widget(
            "Pre EQ 2 Freq",
            param_type="double_spinbox",
            min_val=200.0,
            max_val=1600.0,
            step=10.0,
            suffix=" Hz",
            offset=35,
            length=1,
            row=9, column=0
        )
        
        # Pre EQ 2 Gain
        self.create_parameter_widget(
            "Pre EQ 2 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=36,
            length=1,
            row=9, column=2
        )
        
        # Pre EQ 2 Q
        self.create_parameter_widget(
            "Pre EQ 2 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=37,
            length=1,
            row=9, column=4
        )
        
        # Pre EQ 3 Freq
        self.create_parameter_widget(
            "Pre EQ 3 Freq",
            param_type="double_spinbox",
            min_val=1000.0,
            max_val=8000.0,
            step=100.0,
            suffix=" Hz",
            offset=38,
            length=1,
            row=10, column=0
        )
        
        # Pre EQ 3 Gain
        self.create_parameter_widget(
            "Pre EQ 3 Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=39,
            length=1,
            row=10, column=2
        )
        
        # Pre EQ 3 Q
        self.create_parameter_widget(
            "Pre EQ 3 Q",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=20.0,
            step=0.1,
            offset=40,
            length=1,
            row=10, column=4
        )
        
        # === SECTION NOISE GATE ===
        gate_title = ttk.Label(self, text="Noise Gate", font=("Arial", 12, "bold"))
        gate_title.grid(row=11, column=0, columnspan=8, pady=(15, 5), sticky='w')
        
        # Threshold
        self.create_parameter_widget(
            "Gate Threshold",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=100.0,
            step=0.1,
            offset=48,
            length=1,
            row=12, column=0
        )
        
        # Hold
        self.create_parameter_widget(
            "Hold",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1000.0,
            step=0.1,
            suffix=" ms",
            offset=50,
            length=1,
            conversion="timeMs",
            row=12, column=2
        )
        
        # Attack
        self.create_parameter_widget(
            "Gate Attack",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=100.0,
            step=0.1,
            suffix=" ms",
            offset=49,
            length=1,
            conversion="timeMs",
            row=12, column=4
        )
        
        # Decay
        self.create_parameter_widget(
            "Decay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1000.0,
            step=0.1,
            suffix=" ms",
            offset=51,
            length=1,
            conversion="timeMs",
            row=13, column=0
        )
        
        # === SECTION COMPRESSOR ===
        comp_title = ttk.Label(self, text="Compressor", font=("Arial", 12, "bold"))
        comp_title.grid(row=14, column=0, columnspan=8, pady=(15, 5), sticky='w')
        
        # Threshold
        self.create_parameter_widget(
            "Comp Threshold",
            param_type="double_spinbox",
            min_val=-60.0,
            max_val=0.0,
            step=0.1,
            suffix=" dB",
            offset=2,
            length=1,
            row=15, column=0
        )
        
        # Attack
        self.create_parameter_widget(
            "Comp Attack",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=100.0,
            step=0.1,
            suffix=" ms",
            offset=42,
            length=1,
            conversion="timeMs",
            row=15, column=2
        )
        
        # Knee
        self.create_parameter_widget(
            "Knee",
            param_type="spinbox",
            min_val=0,
            max_val=10,
            step=1,
            offset=44,
            length=1,
            row=15, column=4
        )
        
        # Ratio
        self.create_parameter_widget(
            "Ratio",
            param_type="combobox",
            values=["1 : 1", "1.5 : 1", "2 : 1", "3 : 1", "4 : 1", "6 : 1", "8 : 1", "10 : 1", "∞ : 1"],
            offset=41,
            length=1,
            row=16, column=0
        )
        
        # Release
        self.create_parameter_widget(
            "Release",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1000.0,
            step=0.1,
            suffix=" ms",
            offset=43,
            length=1,
            conversion="timeMs",
            row=16, column=2
        )
        
        # Gain
        self.create_parameter_widget(
            "Gain",
            param_type="double_spinbox",
            min_val=-12.0,
            max_val=12.0,
            step=0.1,
            suffix=" dB",
            offset=45,
            length=1,
            row=16, column=4
        )
        
        # === SECTION FLANGE ===
        flange_title = ttk.Label(self, text="Flange", font=("Arial", 12, "bold"))
        flange_title.grid(row=17, column=0, columnspan=8, pady=(15, 5), sticky='w')
        
        # Wave
        self.create_parameter_widget(
            "Wave",
            param_type="combobox",
            values=["Sine", "Triangle"],
            offset=14,
            length=1,
            row=18, column=0
        )
        
        # Speed
        self.create_parameter_widget(
            "Speed",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=10.0,
            step=0.1,
            offset=53,
            length=1,
            conversion="freqHz",
            row=18, column=2
        )
        
        # Delay
        self.create_parameter_widget(
            "Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            suffix=" ms",
            offset=3,
            length=1,
            conversion="timeMs",
            row=18, column=4
        )
        
        # Level
        self.create_parameter_widget(
            "Flange Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=54,
            length=1,
            row=19, column=0
        )
        
        # Depth
        self.create_parameter_widget(
            "Depth",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=53,
            length=1,
            row=19, column=2
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=55,
            length=1,
            row=19, column=4
        )
        
        # === SECTION DELAY ===
        delay_title = ttk.Label(self, text="Delay", font=("Arial", 12, "bold"))
        delay_title.grid(row=20, column=0, columnspan=8, pady=(15, 5), sticky='w')
        
        # Level
        self.create_parameter_widget(
            "Delay Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=67,
            length=1,
            row=21, column=0
        )
        
        # Tap L
        self.create_parameter_widget(
            "Tap L",
            param_type="spinbox",
            min_val=0,
            max_val=200,
            step=1,
            offset=63,
            length=1,
            row=21, column=2
        )
        
        # Tap R
        self.create_parameter_widget(
            "Tap R",
            param_type="spinbox",
            min_val=0,
            max_val=200,
            step=1,
            offset=64,
            length=1,
            row=21, column=4
        )
        
        # HPF
        self.create_parameter_widget(
            "HPF",
            param_type="combobox",
            values=["Thru", "50Hz", "100Hz", "200Hz", "400Hz", "800Hz"],
            offset=71,
            length=1,
            row=22, column=0
        )
        
        # Feedback
        self.create_parameter_widget(
            "Feedback",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1000.0,
            step=0.1,
            suffix=" ms",
            offset=4,
            length=1,
            conversion="timeMs",
            row=22, column=2
        )
        
        # Feedback Gain
        self.create_parameter_widget(
            "Feedback Gain",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            suffix=" %",
            offset=65,
            length=1,
            row=22, column=4
        )
        
        # High
        self.create_parameter_widget(
            "Delay High",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1.0,
            step=0.1,
            offset=66,
            length=1,
            row=23, column=0
        )
        
        # LPF
        self.create_parameter_widget(
            "LPF",
            param_type="combobox",
            values=["Thru", "2kHz", "4kHz", "8kHz", "16kHz"],
            offset=72,
            length=1,
            row=23, column=2
        )
        
        # === SECTION REVERB ===
        reverb_title = ttk.Label(self, text="Reverb", font=("Arial", 12, "bold"))
        reverb_title.grid(row=24, column=0, columnspan=8, pady=(15, 5), sticky='w')
        
        # Level
        self.create_parameter_widget(
            "Reverb Level",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=10.0,
            step=0.1,
            offset=78,
            length=1,
            row=25, column=0
        )
        
        # High
        self.create_parameter_widget(
            "Reverb High",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=1.0,
            step=0.1,
            offset=75,
            length=1,
            row=25, column=2
        )
        
        # Ini. Delay
        self.create_parameter_widget(
            "Ini. Delay",
            param_type="double_spinbox",
            min_val=0.0,
            max_val=100.0,
            step=0.1,
            suffix=" ms",
            offset=5,
            length=1,
            conversion="timeMs",
            row=25, column=4
        )
        
        # Time
        self.create_parameter_widget(
            "Time",
            param_type="double_spinbox",
            min_val=0.1,
            max_val=10.0,
            step=0.1,
            suffix=" s",
            offset=74,
            length=1,
            row=26, column=0
        )
        
        # Diffusion
        self.create_parameter_widget(
            "Diffusion",
            param_type="spinbox",
            min_val=0,
            max_val=10,
            step=1,
            offset=76,
            length=1,
            row=26, column=2
        )
        
        # Density
        self.create_parameter_widget(
            "Density",
            param_type="spinbox",
            min_val=0,
            max_val=100,
            step=1,
            offset=77,
            length=1,
            row=26, column=4
        )
    
    def apply_magicstomp_data(self, effect_data):
        """
        Applique les données SYSEX reçues du Magicstomp au widget.
        
        Args:
            effect_data: Données d'effet SYSEX (127 bytes pour Distortion Multi Flange)
        """
        if not effect_data:
            return {}
        
        # Convertit en liste si nécessaire
        if isinstance(effect_data, bytes):
            data = list(effect_data)
        else:
            data = list(effect_data)
        
        print(f"🔍 DEBUG: Applying Magicstomp data to DistortionMultiFlangeWidget: {len(data)} bytes")
        print(f"🔍 DEBUG: First 20 bytes: {data[:20]}")
        
        # Utilise la méthode de la classe de base pour parser automatiquement
        applied_params = super().apply_magicstomp_data(data)
        
        print(f"🔍 DEBUG: Applied parameters: {applied_params}")
        return applied_params
    
    def get_all_parameters(self):
        """Retourne tous les paramètres du Distortion Multi (Flange)."""
        params = {}
        
        # Distortion parameters
        params['type'] = self.get_parameter_value("Type")
        params['gain'] = self.get_parameter_value("Gain")
        params['master'] = self.get_parameter_value("Master")
        params['tone'] = self.get_parameter_value("Tone")
        params['eq1_freq'] = self.get_parameter_value("EQ 1 Freq")
        params['eq1_gain'] = self.get_parameter_value("EQ 1 Gain")
        params['eq1_q'] = self.get_parameter_value("EQ 1 Q")
        params['eq2_freq'] = self.get_parameter_value("EQ 2 Freq")
        params['eq2_gain'] = self.get_parameter_value("EQ 2 Gain")
        params['eq2_q'] = self.get_parameter_value("EQ 2 Q")
        params['eq3_freq'] = self.get_parameter_value("EQ 3 Freq")
        params['eq3_gain'] = self.get_parameter_value("EQ 3 Gain")
        params['eq3_q'] = self.get_parameter_value("EQ 3 Q")
        params['eq4_freq'] = self.get_parameter_value("EQ 4 Freq")
        params['eq4_gain'] = self.get_parameter_value("EQ 4 Gain")
        params['eq4_q'] = self.get_parameter_value("EQ 4 Q")
        params['pre_eq_level'] = self.get_parameter_value("Pre EQ Level")
        params['pre_eq1_freq'] = self.get_parameter_value("Pre EQ 1 Freq")
        params['pre_eq1_gain'] = self.get_parameter_value("Pre EQ 1 Gain")
        params['pre_eq1_q'] = self.get_parameter_value("Pre EQ 1 Q")
        params['pre_eq2_freq'] = self.get_parameter_value("Pre EQ 2 Freq")
        params['pre_eq2_gain'] = self.get_parameter_value("Pre EQ 2 Gain")
        params['pre_eq2_q'] = self.get_parameter_value("Pre EQ 2 Q")
        params['pre_eq3_freq'] = self.get_parameter_value("Pre EQ 3 Freq")
        params['pre_eq3_gain'] = self.get_parameter_value("Pre EQ 3 Gain")
        params['pre_eq3_q'] = self.get_parameter_value("Pre EQ 3 Q")
        
        # Noise Gate parameters
        params['threshold'] = self.get_parameter_value("Gate Threshold")
        params['hold'] = self.get_parameter_value("Hold")
        params['attack'] = self.get_parameter_value("Gate Attack")
        params['decay'] = self.get_parameter_value("Decay")
        
        # Compressor parameters
        params['comp_threshold'] = self.get_parameter_value("Comp Threshold")
        params['comp_attack'] = self.get_parameter_value("Comp Attack")
        params['knee'] = self.get_parameter_value("Knee")
        params['ratio'] = self.get_parameter_value("Ratio")
        params['release'] = self.get_parameter_value("Release")
        params['comp_gain'] = self.get_parameter_value("Gain")
        
        # Flange parameters
        params['wave'] = self.get_parameter_value("Wave")
        params['speed'] = self.get_parameter_value("Speed")
        params['delay'] = self.get_parameter_value("Delay")
        params['level'] = self.get_parameter_value("Flange Level")
        params['depth'] = self.get_parameter_value("Depth")
        params['feedback'] = self.get_parameter_value("Feedback")
        
        # Delay parameters
        params['delay_level'] = self.get_parameter_value("Delay Level")
        params['tap_l'] = self.get_parameter_value("Tap L")
        params['tap_r'] = self.get_parameter_value("Tap R")
        params['hpf'] = self.get_parameter_value("HPF")
        params['delay_feedback'] = self.get_parameter_value("Feedback")
        params['feedback_gain'] = self.get_parameter_value("Feedback Gain")
        params['high'] = self.get_parameter_value("Delay High")
        params['lpf'] = self.get_parameter_value("LPF")
        
        # Reverb parameters
        params['reverb_level'] = self.get_parameter_value("Reverb Level")
        params['reverb_high'] = self.get_parameter_value("Reverb High")
        params['ini_delay'] = self.get_parameter_value("Ini. Delay")
        params['time'] = self.get_parameter_value("Time")
        params['diffusion'] = self.get_parameter_value("Diffusion")
        params['density'] = self.get_parameter_value("Density")
        
        return params
    
    def set_all_parameters(self, params):
        """Applique tous les paramètres du Distortion Multi (Flange)."""
        # Distortion parameters
        if 'type' in params:
            self.set_parameter_value("Type", params['type'])
        if 'gain' in params:
            self.set_parameter_value("Gain", params['gain'])
        if 'master' in params:
            self.set_parameter_value("Master", params['master'])
        if 'tone' in params:
            self.set_parameter_value("Tone", params['tone'])
        if 'eq1_freq' in params:
            self.set_parameter_value("EQ 1 Freq", params['eq1_freq'])
        if 'eq1_gain' in params:
            self.set_parameter_value("EQ 1 Gain", params['eq1_gain'])
        if 'eq1_q' in params:
            self.set_parameter_value("EQ 1 Q", params['eq1_q'])
        if 'eq2_freq' in params:
            self.set_parameter_value("EQ 2 Freq", params['eq2_freq'])
        if 'eq2_gain' in params:
            self.set_parameter_value("EQ 2 Gain", params['eq2_gain'])
        if 'eq2_q' in params:
            self.set_parameter_value("EQ 2 Q", params['eq2_q'])
        if 'eq3_freq' in params:
            self.set_parameter_value("EQ 3 Freq", params['eq3_freq'])
        if 'eq3_gain' in params:
            self.set_parameter_value("EQ 3 Gain", params['eq3_gain'])
        if 'eq3_q' in params:
            self.set_parameter_value("EQ 3 Q", params['eq3_q'])
        if 'eq4_freq' in params:
            self.set_parameter_value("EQ 4 Freq", params['eq4_freq'])
        if 'eq4_gain' in params:
            self.set_parameter_value("EQ 4 Gain", params['eq4_gain'])
        if 'eq4_q' in params:
            self.set_parameter_value("EQ 4 Q", params['eq4_q'])
        if 'pre_eq_level' in params:
            self.set_parameter_value("Pre EQ Level", params['pre_eq_level'])
        if 'pre_eq1_freq' in params:
            self.set_parameter_value("Pre EQ 1 Freq", params['pre_eq1_freq'])
        if 'pre_eq1_gain' in params:
            self.set_parameter_value("Pre EQ 1 Gain", params['pre_eq1_gain'])
        if 'pre_eq1_q' in params:
            self.set_parameter_value("Pre EQ 1 Q", params['pre_eq1_q'])
        if 'pre_eq2_freq' in params:
            self.set_parameter_value("Pre EQ 2 Freq", params['pre_eq2_freq'])
        if 'pre_eq2_gain' in params:
            self.set_parameter_value("Pre EQ 2 Gain", params['pre_eq2_gain'])
        if 'pre_eq2_q' in params:
            self.set_parameter_value("Pre EQ 2 Q", params['pre_eq2_q'])
        if 'pre_eq3_freq' in params:
            self.set_parameter_value("Pre EQ 3 Freq", params['pre_eq3_freq'])
        if 'pre_eq3_gain' in params:
            self.set_parameter_value("Pre EQ 3 Gain", params['pre_eq3_gain'])
        if 'pre_eq3_q' in params:
            self.set_parameter_value("Pre EQ 3 Q", params['pre_eq3_q'])
        
        # Noise Gate parameters
        if 'threshold' in params:
            self.set_parameter_value("Gate Threshold", params['threshold'])
        if 'hold' in params:
            self.set_parameter_value("Hold", params['hold'])
        if 'attack' in params:
            self.set_parameter_value("Gate Attack", params['attack'])
        if 'decay' in params:
            self.set_parameter_value("Decay", params['decay'])
        
        # Compressor parameters
        if 'comp_threshold' in params:
            self.set_parameter_value("Comp Threshold", params['comp_threshold'])
        if 'comp_attack' in params:
            self.set_parameter_value("Comp Attack", params['comp_attack'])
        if 'knee' in params:
            self.set_parameter_value("Knee", params['knee'])
        if 'ratio' in params:
            self.set_parameter_value("Ratio", params['ratio'])
        if 'release' in params:
            self.set_parameter_value("Release", params['release'])
        if 'comp_gain' in params:
            self.set_parameter_value("Gain", params['comp_gain'])
        
        # Flange parameters
        if 'wave' in params:
            self.set_parameter_value("Wave", params['wave'])
        if 'speed' in params:
            self.set_parameter_value("Speed", params['speed'])
        if 'delay' in params:
            self.set_parameter_value("Delay", params['delay'])
        if 'level' in params:
            self.set_parameter_value("Flange Level", params['level'])
        if 'depth' in params:
            self.set_parameter_value("Depth", params['depth'])
        if 'feedback' in params:
            self.set_parameter_value("Feedback", params['feedback'])
        
        # Delay parameters
        if 'delay_level' in params:
            self.set_parameter_value("Delay Level", params['delay_level'])
        if 'tap_l' in params:
            self.set_parameter_value("Tap L", params['tap_l'])
        if 'tap_r' in params:
            self.set_parameter_value("Tap R", params['tap_r'])
        if 'hpf' in params:
            self.set_parameter_value("HPF", params['hpf'])
        if 'delay_feedback' in params:
            self.set_parameter_value("Feedback", params['delay_feedback'])
        if 'feedback_gain' in params:
            self.set_parameter_value("Feedback Gain", params['feedback_gain'])
        if 'high' in params:
            self.set_parameter_value("Delay High", params['high'])
        if 'lpf' in params:
            self.set_parameter_value("LPF", params['lpf'])
        
        # Reverb parameters
        if 'reverb_level' in params:
            self.set_parameter_value("Reverb Level", params['reverb_level'])
        if 'reverb_high' in params:
            self.set_parameter_value("Reverb High", params['reverb_high'])
        if 'ini_delay' in params:
            self.set_parameter_value("Ini. Delay", params['ini_delay'])
        if 'time' in params:
            self.set_parameter_value("Time", params['time'])
        if 'diffusion' in params:
            self.set_parameter_value("Diffusion", params['diffusion'])
        if 'density' in params:
            self.set_parameter_value("Density", params['density'])
