"""
Magicstomp Effects Widgets for Dopsound
=======================================

Adaptation Python des widgets d'effets MagicstompFrenzy pour Dopsound.
Basé sur le code C++/Qt original sous licence GPL-3.0.

Ce module fournit des widgets d'effets spécialisés pour le Yamaha Magicstomp,
permettant une visualisation et un contrôle précis des paramètres d'effets.
"""

from .base_effect_widget import BaseEffectWidget
from .delay_widgets import (
    MonoDelayWidget, 
    StereoDelayWidget, 
    ModDelayWidget,
    EchoWidget
)
from .modulation_widgets import (
    ChorusWidget,
    FlangeWidget,
    PhaserWidget,
    TremoloWidget
)
from .reverb_widgets import (
    ReverbWidget,
    GateReverbWidget,
    SpringReverbWidget
)
from .distortion_widgets import (
    DistortionWidget,
    AmpSimulatorWidget
)
from .filter_widgets import (
    MultiFilterWidget,
    DynamicFilterWidget,
    ThreeBandEQWidget
)
from .pitch_widgets import (
    HQPitchWidget,
    DualPitchWidget
)
from .effect_registry import EffectRegistry

__all__ = [
    'BaseEffectWidget',
    'MonoDelayWidget',
    'StereoDelayWidget', 
    'ModDelayWidget',
    'EchoWidget',
    'ChorusWidget',
    'FlangeWidget',
    'PhaserWidget',
    'TremoloWidget',
    'ReverbWidget',
    'GateReverbWidget',
    'SpringReverbWidget',
    'DistortionWidget',
    'AmpSimulatorWidget',
    'MultiFilterWidget',
    'DynamicFilterWidget',
    'ThreeBandEQWidget',
    'HQPitchWidget',
    'DualPitchWidget',
    'EffectRegistry'
]
