#!/usr/bin/env python3
"""
Configuration du Pipeline Magicstomp
===================================

Paramètres de configuration pour personnaliser les mappings
et les seuils de détection d'effets.
"""

from magicstomp_sysex import (
    SYSEX_HEADER,
    SYSEX_FOOTER,
    PARAMETER_SEND_CMD,
    PATCH_COMMON_LENGTH,
    PATCH_EFFECT_LENGTH,
    PATCH_TOTAL_LENGTH,
)

# Seuils de détection d'effets
DETECTION_THRESHOLDS = {
    "delay": {
        "min_peak_height": 0.3,
        "min_delay_samples": 100,
        "min_delay_ms": 10,
        "max_delay_ms": 2000
    },
    "reverb": {
        "min_decay_time_s": 0.8,
        "min_high_freq_ratio": 0.1,
        "max_decay_time_s": 5.0
    },
    "modulation": {
        "min_mod_strength": 0.1,
        "min_mod_rate_hz": 0.3,
        "max_mod_rate_hz": 8.0,
        "low_freq_cutoff_hz": 20
    },
    "distortion": {
        "min_clipping_ratio": 0.01,
        "min_thd": 0.1,
        "clipping_threshold": 0.95
    }
}

# Mappings des modèles d'amplificateur
AMP_MODELS = {
    "BRIT_TOP_BOOST": {
        "id": 0x01,
        "description": "Vox AC30 Top Boost - Bright, clair",
        "spectral_centroid_min": 3000,
        "spectral_bandwidth_min": 1500
    },
    "TWEED_BASSMAN": {
        "id": 0x02,
        "description": "Fender Bassman - Chaleureux, vintage",
        "spectral_centroid_max": 2000,
        "spectral_bandwidth_max": 1000
    },
    "JCM800": {
        "id": 0x03,
        "description": "Marshall JCM800 - Équilibré, rock",
        "spectral_centroid_min": 2000,
        "spectral_centroid_max": 3000
    },
    "AC30": {
        "id": 0x04,
        "description": "Vox AC30 - Britannique classique"
    },
    "FENDER_TWIN": {
        "id": 0x05,
        "description": "Fender Twin Reverb - Clean, cristallin"
    },
    "MESA_BOOGIE": {
        "id": 0x06,
        "description": "Mesa Boogie - High gain, métal"
    }
}

# Mappings des cabines
CAB_MODELS = {
    "2x12_ALNICO": {
        "id": 0x01,
        "description": "2x12 Alnico - Brillant, équilibré"
    },
    "4x10_TWEED": {
        "id": 0x02,
        "description": "4x10 Tweed - Vintage, chaleureux"
    },
    "4x12_VINTAGE": {
        "id": 0x03,
        "description": "4x12 Vintage - Classique rock"
    },
    "4x12_MODERN": {
        "id": 0x04,
        "description": "4x12 Modern - Puissant, agressif"
    },
    "1x12_BLACKFACE": {
        "id": 0x05,
        "description": "1x12 Blackface - Fender clean"
    },
    "2x12_CELESTION": {
        "id": 0x06,
        "description": "2x12 Celestion - Britannique"
    }
}

# Mappings des boosters
BOOSTER_TYPES = {
    "TREBLE": {
        "id": 0x01,
        "description": "Treble Booster - Brillance, présence"
    },
    "TUBE_SCREAMER": {
        "id": 0x02,
        "description": "Tube Screamer - Overdrive classique"
    },
    "CLEAN": {
        "id": 0x03,
        "description": "Clean Boost - Gain transparent"
    },
    "DISTORTION": {
        "id": 0x04,
        "description": "Distortion - Saturation agressive"
    },
    "FUZZ": {
        "id": 0x05,
        "description": "Fuzz - Distorsion vintage"
    }
}

# Mappings des types de reverb
REVERB_TYPES = {
    "ROOM": {
        "id": 0x01,
        "description": "Room - Ambiance naturelle",
        "decay_range": (0.5, 1.5)
    },
    "PLATE": {
        "id": 0x02,
        "description": "Plate - Réverbération artificielle",
        "decay_range": (1.0, 2.5)
    },
    "HALL": {
        "id": 0x03,
        "description": "Hall - Grand espace",
        "decay_range": (2.0, 4.0)
    },
    "SPRING": {
        "id": 0x04,
        "description": "Spring - Vintage, caractéristique",
        "decay_range": (0.8, 2.0)
    },
    "CHURCH": {
        "id": 0x05,
        "description": "Church - Très long decay",
        "decay_range": (3.0, 6.0)
    }
}

# Mappings des types de modulation
MOD_TYPES = {
    "CHORUS": {
        "id": 0x01,
        "description": "Chorus - Doublage, épaisseur",
        "rate_range": (0.1, 2.0)
    },
    "PHASER": {
        "id": 0x02,
        "description": "Phaser - Balayage de phase",
        "rate_range": (0.2, 4.0)
    },
    "TREMOLO": {
        "id": 0x03,
        "description": "Tremolo - Modulation d'amplitude",
        "rate_range": (1.0, 8.0)
    },
    "VIBRATO": {
        "id": 0x04,
        "description": "Vibrato - Modulation de pitch",
        "rate_range": (2.0, 10.0)
    },
    "FLANGER": {
        "id": 0x05,
        "description": "Flanger - Effet avion",
        "rate_range": (0.1, 1.0)
    }
}

# Paramètres SysEx Magicstomp (format MagicstompFrenzy)
from magicstomp_sysex import (
    SYSEX_HEADER,
    SYSEX_FOOTER,
    PARAMETER_SEND_CMD,
    PATCH_COMMON_LENGTH,
    PATCH_EFFECT_LENGTH,
    PATCH_TOTAL_LENGTH,
)


SYSEX_CONFIG = {
    "parameter_send": {
        "header": SYSEX_HEADER,
        "command": PARAMETER_SEND_CMD,
        "footer": SYSEX_FOOTER,
    },
    "patch_structure": {
        "common_length": PATCH_COMMON_LENGTH,
        "effect_length": PATCH_EFFECT_LENGTH,
        "total_length": PATCH_TOTAL_LENGTH,
    },
}

# Paramètres d'analyse audio
AUDIO_CONFIG = {
    "sample_rate": 44100,
    "normalization_level": 0.7,  # Niveau de normalisation RMS
    "analysis_window_ms": 4096,  # Taille de fenêtre d'analyse
    "hop_length_ms": 512,        # Pas de décalage
    "max_frequency_hz": 22050,   # Fréquence maximale d'analyse
    "min_frequency_hz": 80       # Fréquence minimale (guitare)
}

# Paramètres de mapping
MAPPING_CONFIG = {
    "value_range": {
        "min": 0,
        "max": 127
    },
    "delay_time_mapping": {
        "linear_range_ms": (0, 50),
        "log_range_ms": (50, 2000),
        "max_value": 255
    },
    "modulation_rate_mapping": {
        "min_hz": 0.1,
        "max_hz": 20.0,
        "log_base": 10
    }
}

def get_config():
    """Retourne la configuration complète."""
    return {
        "detection_thresholds": DETECTION_THRESHOLDS,
        "amp_models": AMP_MODELS,
        "cab_models": CAB_MODELS,
        "booster_types": BOOSTER_TYPES,
        "reverb_types": REVERB_TYPES,
        "mod_types": MOD_TYPES,
        "sysex_config": SYSEX_CONFIG,
        "audio_config": AUDIO_CONFIG,
        "mapping_config": MAPPING_CONFIG
    }

def print_config():
    """Affiche la configuration actuelle."""
    config = get_config()
    
    print("🔧 Configuration du Pipeline Magicstomp")
    print("=" * 50)
    
    print(f"\n🎵 Analyse audio:")
    audio = config["audio_config"]
    print(f"   Sample rate: {audio['sample_rate']}Hz")
    print(f"   Normalisation: {audio['normalization_level']}")
    print(f"   Fenêtre d'analyse: {audio['analysis_window_ms']}ms")
    
    print(f"\n🎸 Amplificateurs supportés:")
    for name, info in config["amp_models"].items():
        print(f"   {name}: {info['description']}")
    
    print(f"\n🏛️ Types de reverb:")
    for name, info in config["reverb_types"].items():
        print(f"   {name}: {info['description']}")
    
    print(f"\n🌊 Types de modulation:")
    for name, info in config["mod_types"].items():
        print(f"   {name}: {info['description']}")
    
    print(f"\n📡 Configuration SysEx:")
    sysex = config["sysex_config"]
    header = sysex["parameter_send"]["header"]
    command = sysex["parameter_send"]["command"]
    print(
        "   Header parameter-send: "
        + " ".join(f"0x{byte:02X}" for byte in header)
    )
    print(f"   Commande parameter-send: 0x{command:02X}")
    patch_info = sysex["patch_structure"]
    print(
        "   Structure patch: common={common} bytes, effect={effect} bytes, total={total} bytes".format(
            common=patch_info["common_length"],
            effect=patch_info["effect_length"],
            total=patch_info["total_length"],
        )
    )

if __name__ == "__main__":
    print_config()
