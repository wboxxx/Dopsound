"""
Effect Registry
==============

Registre central pour tous les effets Magicstomp disponibles.
Permet la création dynamique d'effets basée sur leur type.
"""

from typing import Dict, Type, Optional
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
from .simple_effects_widgets import (
    DigitalDistortionWidget,
    SymphonicWidget,
    AutoPanWidget,
    RotaryWidget,
    RingModWidget
)
from .vintage_effects_widgets import (
    VintageFlangeWidget,
    MonoVintagePhaserWidget,
    StereoVintagePhaserWidget
)
from .modulation_filter_widgets import (
    ModFilterWidget,
    DynaFilterWidget
)
from .early_reflection_widgets import (
    EarlyRefWidget,
    ReverseGateWidget
)
from .dynamics_widgets import (
    MBandDynaWidget,
    DynaFlangeWidget,
    DynaPhaserWidget
)
from .tape_echo_widget import TapeEchoWidget
from .complex_delay_widgets import (
    DelayLCRWidget,
    ShortMediumLongModDelayWidget
)
from .combined_effects_widgets import (
    ReverbChorusWidget,
    ReverbFlangeWidget
)
from .combined_effects_widgets_part2 import (
    ReverbArrowChorusWidget,
    ReverbSymphonicWidget
)
from .multitap_delay_widgets import (
    EightBandParallelDelayWidget,
    FourBandTwoTapModDelayWidget
)
from .multitap_delay_widgets_part2 import (
    EightBandSeriesDelayWidget,
    TwoBandFourTapModDelayWidget
)
from .multitap_delay_widgets_part3 import (
    EightMultiTapModDelayWidget,
    TwoBandLongFourShortModDelayWidget
)
from .final_effects_widgets import (
    ReverbArrowSymphonicWidget,
    AcousticMultiWidget
)
from .filter_widgets import (
    MultiFilterWidget,
    DynamicFilterWidget,
    CompressorWidget,
    ThreeBandEQWidget
)
from .pitch_widgets import (
    HQPitchWidget,
    DualPitchWidget
)


class EffectRegistry:
    """
    Registre central pour tous les effets Magicstomp.
    
    Basé sur les types d'effets définis dans magicstomptext.h du code original.
    """
    
    # Mapping des types d'effets vers leurs widgets Python
    EFFECT_WIDGETS: Dict[int, Type[BaseEffectWidget]] = {
        # Delays
        0x0D: MonoDelayWidget,      # "Mono Delay"
        0x0E: StereoDelayWidget,    # "Stereo Delay" 
        0x0F: ModDelayWidget,       # "Mod. Delay"
        0x11: EchoWidget,           # "Echo"
        
        # Modulation
        0x12: ChorusWidget,         # "Chorus"
        0x13: FlangeWidget,         # "Flange"
        0x15: PhaserWidget,         # "Phaser"
        0x17: TremoloWidget,        # "Tremolo"
        
        # Reverb
        0x09: ReverbWidget,         # "Reverb"
        0x0B: GateReverbWidget,     # "Gate Reverb"
        0x22: SpringReverbWidget,   # "Spring Reverb"
        
        # Distortion
        0x2F: DistortionWidget,     # "Distortion"
        0x08: AmpSimulatorWidget,   # "Amp Simulator"
        0x1D: DigitalDistortionWidget,  # "Digital Distortion"
        
        # Simple Effects
        0x14: SymphonicWidget,      # "Symphonic"
        0x16: AutoPanWidget,        # "Auto Pan"
        0x1A: RotaryWidget,         # "Rotary"
        0x1B: RingModWidget,        # "Ring Mod."
        
        # Vintage Effects
        0x30: VintageFlangeWidget,  # "Vintage Flange"
        0x31: MonoVintagePhaserWidget,  # "Mono Vintage Phaser"
        0x32: StereoVintagePhaserWidget,  # "Stereo Vintage Phaser"
        
        # Modulation Filters
        0x1C: ModFilterWidget,      # "Mod. Filter"
        
        # Early Reflections
        0x0A: EarlyRefWidget,       # "Early Ref."
        0x0C: ReverseGateWidget,    # "Reverse Gate"
        
        # Dynamics
        0x2E: MBandDynaWidget,      # "M.Band Dyna."
        0x1F: DynaFlangeWidget,     # "Dyna. Flange"
        0x20: DynaPhaserWidget,     # "Dyna. Phaser"
        0x35: TapeEchoWidget,       # "Tape Echo"
        
        # Complex Delays
        0x10: DelayLCRWidget,       # "Delay LCR"
        0x07: ShortMediumLongModDelayWidget,  # "Short + Medium + Long Mod. Delay"
        
        # Combined Effects
        0x22: ReverbChorusWidget,   # "Reverb+Chorus"
        0x24: ReverbFlangeWidget,   # "Reverb+Flange"
        0x23: ReverbArrowChorusWidget,  # "Reverb->Chorus"
        0x26: ReverbSymphonicWidget,    # "Reverb+Symphonic"
        0x27: ReverbArrowSymphonicWidget,  # "Reverb->Symphonic"
        
        # Multi-Tap Delays
        0x01: EightBandParallelDelayWidget,  # "8 Band Parallel Delay"
        0x02: EightBandSeriesDelayWidget,    # "8 Band Series Delay"
        0x03: FourBandTwoTapModDelayWidget,  # "4 Band 2 Tap Mod. Delay"
        0x04: TwoBandFourTapModDelayWidget,  # "2 Band 4 Tap Mod. Delay"
        0x05: EightMultiTapModDelayWidget,   # "8 Multi Tap Mod. Delay"
        0x06: TwoBandLongFourShortModDelayWidget,  # "2 Band Long + 4 Short Mod. Delay"
        
        # Filters
        0x2D: MultiFilterWidget,    # "Multi Filter"
        0x1E: DynamicFilterWidget,  # "Dynamic Filter"
        0x21: ThreeBandEQWidget,    # "3 Band Parametric EQ"
        0x36: CompressorWidget,     # "Compressor"
        
        # Multi Effects
        0x00: AcousticMultiWidget,  # "Acoustic Multi"
        
        # Pitch
        0x18: HQPitchWidget,        # "HQ Pitch"
        0x19: DualPitchWidget,      # "Dual Pitch"
    }
    
    # Noms des effets (basés sur magicstomptext.h)
    EFFECT_NAMES: Dict[int, str] = {
        0x00: "Acoustic Multi",
        0x01: "8 Band Parallel Delay",
        0x02: "8 Band Series Delay", 
        0x03: "4 Band 2 Tap Mod. Delay",
        0x04: "2 Band 4 Tap Mod. Delay",
        0x05: "8 Multi Tap Mod. Delay",
        0x06: "2 Band Long + 4 Short Mod. Delay",
        0x07: "Short + Medium + Long Mod. Delay",
        0x08: "Amp Simulator",
        0x09: "Reverb",
        0x0A: "Early Reflections",
        0x0B: "Gate Reverb",
        0x0C: "Reverse Gate",
        0x0D: "Mono Delay",
        0x0E: "Stereo Delay",
        0x0F: "Mod. Delay",
        0x10: "Delay LCR",
        0x11: "Echo",
        0x12: "Chorus",
        0x13: "Flange",
        0x14: "Symphonic",
        0x15: "Phaser",
        0x16: "AutoPan",
        0x17: "Tremolo",
        0x18: "HQ Pitch",
        0x19: "Dual Pitch",
        0x1A: "Rotary",
        0x1B: "Ring Mod.",
        0x1C: "Mod. Filter",
        0x1D: "Digital Distortion",
        0x1E: "Dynamic Filter",
        0x1F: "Dynamic Flange",
        0x20: "Dynamic Phaser",
        0x21: "3 Band Parametric EQ",
        0x22: "Reverb -> Chorus",
        0x23: "Reverb + Flange",
        0x24: "Reverb -> Flange",
        0x25: "Reverb + Symphonic",
        0x26: "Reverb -> Symphonic",
        0x27: "Reverb -> Pan",
        0x28: "Delay + Early Ref.",
        0x29: "Delay -> Early Ref.",
        0x2A: "Delay + Reverb",
        0x2B: "Delay -> Reverb",
        0x2C: "Distortion -> Delay",
        0x2D: "Multi Filter",
        0x36: "Compressor",
        0x2E: "M. Band Dynamic Processor",
        0x2F: "Distortion",
        0x30: "Vintage Flange",
        0x31: "Mono Vintage Phaser",
        0x32: "Stereo Vintage Phaser",
        0x33: "3 Band Parametric EQ",
        0x34: "Spring Reverb",
        0x35: "Tape Echo",
        0x36: "Compressor",
        0x37: "Amp Multi (Chorus)",
        0x38: "Amp Multi (Flange)",
        0x39: "Amp Multi (Tremolo)",
        0x3A: "Amp Multi (Phaser)",
        0x3B: "Distortion Multi (Chorus)",
        0x3C: "Distortion Multi (Flange)",
        0x3D: "Distortion Multi (Tremolo)",
        0x3E: "Distortion Multi (Phaser)",
        0x3F: "Bass Preamp",
    }
    
    @classmethod
    def create_effect_widget(cls, effect_type: int, parent=None) -> Optional[BaseEffectWidget]:
        """
        Crée un widget d'effet basé sur son type.
        
        Args:
            effect_type: Type d'effet (hex)
            parent: Widget parent
            
        Returns:
            Widget d'effet ou None si le type n'est pas supporté
        """
        widget_class = cls.EFFECT_WIDGETS.get(effect_type)
        if widget_class:
            return widget_class(parent)
        return None
    
    @classmethod
    def get_effect_name(cls, effect_type: int) -> str:
        """
        Récupère le nom d'un effet basé sur son type.
        
        Args:
            effect_type: Type d'effet (hex)
            
        Returns:
            Nom de l'effet ou "Unknown Effect"
        """
        return cls.EFFECT_NAMES.get(effect_type, f"Unknown Effect (0x{effect_type:02X})")
    
    @classmethod
    def is_effect_supported(cls, effect_type: int) -> bool:
        """
        Vérifie si un type d'effet est supporté.
        
        Args:
            effect_type: Type d'effet (hex)
            
        Returns:
            True si l'effet est supporté
        """
        return effect_type in cls.EFFECT_WIDGETS
    
    @classmethod
    def get_supported_effects(cls) -> Dict[int, str]:
        """
        Récupère tous les effets supportés.
        
        Returns:
            Dictionnaire {type_effet: nom_effet}
        """
        return {
            effect_type: cls.EFFECT_NAMES.get(effect_type, f"Effect 0x{effect_type:02X}")
            for effect_type in cls.EFFECT_WIDGETS.keys()
        }
    
    @classmethod
    def get_all_effect_names(cls) -> Dict[int, str]:
        """
        Récupère tous les noms d'effets (supportés ou non).
        
        Returns:
            Dictionnaire {type_effet: nom_effet}
        """
        return cls.EFFECT_NAMES.copy()
