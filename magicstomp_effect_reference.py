#!/usr/bin/env python3
"""
Référence complète des effets Magicstomp
=======================================

Basé sur MagicstompFrenzy - correspondance exacte entre offsets et effets.
"""

# =============================================================================
# CORRESPONDANCE OFFSET → EFFET
# =============================================================================

# Paramètres d'amplificateur (très audibles)
AMP_PARAMETERS = {
    30: {"name": "Gain", "range": "0-127", "audible": "TRÈS", "description": "Gain de l'amplificateur"},
    31: {"name": "Master", "range": "0-127", "audible": "TRÈS", "description": "Volume maître"},
    34: {"name": "Tone", "range": "0-127", "audible": "OUI", "description": "Tone de l'amplificateur"},
    36: {"name": "Treble", "range": "0-127", "audible": "OUI", "description": "Aigus"},
    37: {"name": "HighMiddle", "range": "0-127", "audible": "OUI", "description": "Médiums aigus"},
    38: {"name": "LowMiddle", "range": "0-127", "audible": "OUI", "description": "Médiums graves"},
    39: {"name": "Bass", "range": "0-127", "audible": "OUI", "description": "Graves"},
    40: {"name": "Presence", "range": "0-127", "audible": "OUI", "description": "Présence"},
}

# Paramètres de delay (très audibles)
DELAY_PARAMETERS = {
    78: {"name": "DelayLevel", "range": "0-127", "audible": "TRÈS", "description": "Niveau du delay"},
    82: {"name": "DelayHPF", "range": "0-127", "audible": "OUI", "description": "Filtre passe-haut du delay"},
    83: {"name": "DelayLPF", "range": "0-127", "audible": "OUI", "description": "Filtre passe-bas du delay"},
    74: {"name": "DelayTapL", "range": "0-100", "audible": "OUI", "description": "Tap gauche du delay"},
    75: {"name": "DelayTapR", "range": "0-100", "audible": "OUI", "description": "Tap droit du delay"},
    76: {"name": "DelayFeedbackGain", "range": "0-127", "audible": "OUI", "description": "Feedback du delay"},
}

# Paramètres de flanger (audibles)
FLANGER_PARAMETERS = {
    53: {"name": "FlangerDepth", "range": "0-127", "audible": "OUI", "description": "Profondeur du flanger"},
    54: {"name": "FlangerFeedback", "range": "0-127", "audible": "OUI", "description": "Feedback du flanger"},
    55: {"name": "FlangerLevel", "range": "0-127", "audible": "OUI", "description": "Niveau du flanger"},
    52: {"name": "FlangerSpeed", "range": "0-127", "audible": "OUI", "description": "Vitesse du flanger"},
}

# Paramètres de compression (audibles)
COMPRESSOR_PARAMETERS = {
    52: {"name": "CompressorThreshold", "range": "0-127", "audible": "OUI", "description": "Seuil de compression"},
    53: {"name": "CompressorRatio", "range": "0-127", "audible": "OUI", "description": "Ratio de compression"},
    54: {"name": "CompressorAttack", "range": "0-127", "audible": "OUI", "description": "Attack de compression"},
    55: {"name": "CompressorRelease", "range": "0-127", "audible": "OUI", "description": "Release de compression"},
}

# Paramètres de reverb (audibles)
REVERB_PARAMETERS = {
    85: {"name": "ReverbTime", "range": "0-127", "audible": "OUI", "description": "Temps de reverb"},
    86: {"name": "ReverbHigh", "range": "0-127", "audible": "OUI", "description": "Reverb aigus"},
    87: {"name": "ReverbDiffusion", "range": "0-127", "audible": "OUI", "description": "Diffusion reverb"},
    88: {"name": "ReverbDensity", "range": "0-127", "audible": "OUI", "description": "Densité reverb"},
    89: {"name": "ReverbLevel", "range": "0-127", "audible": "OUI", "description": "Niveau reverb"},
}

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_parameter_info(offset):
    """
    Retourne les informations d'un paramètre basé sur son offset.
    
    Args:
        offset: Offset du paramètre
        
    Returns:
        Dict avec name, range, audible, description ou None
    """
    # Recherche dans tous les dictionnaires
    all_params = {
        **AMP_PARAMETERS,
        **DELAY_PARAMETERS, 
        **FLANGER_PARAMETERS,
        **COMPRESSOR_PARAMETERS,
        **REVERB_PARAMETERS
    }
    
    return all_params.get(offset)

def get_most_audible_parameters():
    """Retourne les paramètres les plus audibles pour l'optimisation."""
    most_audible = []
    
    all_params = {
        **AMP_PARAMETERS,
        **DELAY_PARAMETERS, 
        **FLANGER_PARAMETERS,
        **COMPRESSOR_PARAMETERS,
        **REVERB_PARAMETERS
    }
    
    for offset, info in all_params.items():
        if info["audible"] == "TRÈS":
            most_audible.append((offset, info))
    
    return most_audible

def print_reference():
    """Affiche la référence complète."""
    print("🎸 RÉFÉRENCE COMPLÈTE DES EFFETS MAGICSTOMP")
    print("=" * 60)
    print("Basé sur MagicstompFrenzy - Offsets et effets")
    print()
    
    print("🔥 PARAMÈTRES TRÈS AUDIBLES (pour optimisation):")
    print("-" * 50)
    for offset, info in get_most_audible_parameters():
        print(f"Offset {offset:2d}: {info['name']:15s} | {info['description']}")
    
    print("\n🎛️ PARAMÈTRES D'AMPLIFICATEUR:")
    print("-" * 40)
    for offset, info in AMP_PARAMETERS.items():
        print(f"Offset {offset:2d}: {info['name']:15s} | {info['audible']:4s} | {info['description']}")
    
    print("\n⏰ PARAMÈTRES DE DELAY:")
    print("-" * 30)
    for offset, info in DELAY_PARAMETERS.items():
        print(f"Offset {offset:2d}: {info['name']:15s} | {info['audible']:4s} | {info['description']}")
    
    print("\n🌀 PARAMÈTRES DE FLANGER:")
    print("-" * 35)
    for offset, info in FLANGER_PARAMETERS.items():
        print(f"Offset {offset:2d}: {info['name']:15s} | {info['audible']:4s} | {info['description']}")
    
    print("\n📊 PARAMÈTRES DE COMPRESSION:")
    print("-" * 40)
    for offset, info in COMPRESSOR_PARAMETERS.items():
        print(f"Offset {offset:2d}: {info['name']:15s} | {info['audible']:4s} | {info['description']}")
    
    print("\n🏛️ PARAMÈTRES DE REVERB:")
    print("-" * 30)
    for offset, info in REVERB_PARAMETERS.items():
        print(f"Offset {offset:2d}: {info['name']:15s} | {info['audible']:4s} | {info['description']}")
    
    print("\n💡 UTILISATION:")
    print("-" * 15)
    print("1. Identifiez l'effet sur votre patch U01")
    print("2. Utilisez l'offset correspondant")
    print("3. Envoyez une valeur 0-127")
    print("4. Testez l'effet audible")
    
    print("\n🎯 POUR L'OPTIMISATION:")
    print("-" * 25)
    print("Commencez par les paramètres 'TRÈS' audibles:")
    for offset, info in get_most_audible_parameters():
        print(f"  - Offset {offset}: {info['name']}")

if __name__ == "__main__":
    print_reference()


