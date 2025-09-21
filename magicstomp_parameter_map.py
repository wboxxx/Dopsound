#!/usr/bin/env python3
"""
Mapping des paramètres Magicstomp
=================================

Correspondance des offsets avec les fonctions d'effets basée sur MagicstompFrenzy.
"""

# Paramètres communs (section 0x00)
COMMON_PARAMETERS = {
    0: "PatchType",
    2: "Control1 (Knob 1)",  # Assignation du potentiomètre 1
    4: "Control2 (Knob 2)",  # Assignation du potentiomètre 2  
    6: "Control3 (Knob 3)",  # Assignation du potentiomètre 3
    16: "PatchName",
}

# Paramètres d'effets (section 0x01) - AmpMultiWidget
EFFECT_PARAMETERS = {
    # Compresseur
    4: "CompressorThreshold",
    34: "CompressorRatio", 
    35: "CompressorAttack",
    36: "CompressorRelease",
    37: "CompressorKnee",
    38: "CompressorGain",
    
    # Amplificateur
    16: "AmpType",
    17: "SpeakerSimulator", 
    30: "Gain",  # 0x1E
    31: "Master",  # 0x1F
    34: "Tone",  # 0x22
    36: "Treble",  # 0x24
    37: "HighMiddle",  # 0x25
    38: "LowMiddle",  # 0x26
    39: "Bass",  # 0x27
    40: "Presence",  # 0x28
    
    # Noise Gate
    42: "NoiseGateThreshold",  # 0x2A
    43: "NoiseGateAttack",  # 0x2B
    44: "NoiseGateHold",  # 0x2C
    45: "NoiseGateDecay",  # 0x2D
    
    # Modulation
    25: "ModWave",  # 0x19
    63: "ModSpeed",  # 0x3F
    64: "ModDepth",  # 0x40
    65: "ChorusLevel",  # 0x41
    66: "FlangePhaserLevel",  # 0x42
    
    # Delay
    74: "DelayTapL",  # 0x4A
    75: "DelayTapR",  # 0x4B
    76: "DelayFeedbackGain",  # 0x4C
    77: "DelayHeigh",  # 0x4D
    78: "DelayLevel",  # 0x4E
    
    # Filtres Delay
    82: "DelayHPF",  # 0x52
    83: "DelayLPF",  # 0x53
    
    # Reverb
    85: "ReverbTime",  # 0x55
    86: "ReverbHigh",  # 0x56
    87: "ReverbDiffusion",  # 0x57
    88: "ReverbDensity",  # 0x58
    89: "ReverbLevel",  # 0x59
}

def get_parameter_name(offset, section):
    """
    Retourne le nom du paramètre basé sur l'offset et la section.
    
    Args:
        offset: Offset du paramètre
        section: 0 pour section commune, 1 pour section effet
        
    Returns:
        Nom du paramètre ou description générique
    """
    if section == 0:  # Section commune
        return COMMON_PARAMETERS.get(offset, f"CommonParam_{offset}")
    else:  # Section effet
        return EFFECT_PARAMETERS.get(offset, f"EffectParam_{offset}")

def explain_our_tests():
    """Explique ce qu'on a testé basé sur les mappings."""
    print("🎸 Analyse de nos tests basée sur MagicstompFrenzy")
    print("=" * 60)
    
    print("\n📊 Ce qu'on a testé:")
    print("  Offset 2, valeur 0 → Control1 (Knob 1) = 0")
    print("    → Assignation du potentiomètre 1 à une fonction")
    print("    → Vous avez vu 'DHPF' = Delay High Pass Filter")
    
    print("\n  Offset 6, valeur 64 → Control3 (Knob 3) = 64") 
    print("    → Assignation du potentiomètre 3 à une fonction")
    print("    → Vous avez vu 'DLVL' puis '4556' = Delay Level")
    
    print("\n  Offset 4, valeur 0/1 → Control2 (Knob 2) = 0/1")
    print("    → Assignation du potentiomètre 2")
    print("    → Vous avez vu des icônes de portes")
    
    print("\n🔍 Ce qu'on devrait tester maintenant:")
    print("  Offset 78 (0x4E) → DelayLevel (niveau du delay)")
    print("  Offset 82 (0x52) → DelayHPF (filtre passe-haut du delay)")
    print("  Offset 83 (0x53) → DelayLPF (filtre passe-bas du delay)")
    print("  Offset 30 (0x1E) → Gain (gain de l'amplificateur)")
    print("  Offset 31 (0x1F) → Master (volume maître)")
    
    print("\n💡 Conclusion:")
    print("  On a testé les ASSIGNATIONS des potentiomètres, pas les paramètres eux-mêmes!")
    print("  Il faut maintenant tester les paramètres d'effets directement.")

if __name__ == "__main__":
    explain_our_tests()
