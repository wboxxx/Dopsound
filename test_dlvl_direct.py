#!/usr/bin/env python3
"""
Test direct du paramètre DLVL (Delay Level)
===========================================

Le potentiomètre 3 est maintenant assigné à DLVL.
Testons de modifier directement la valeur du paramètre DLVL.
"""

import sys
import time
from realtime_magicstomp import RealtimeMagicstomp

def test_dlvl_direct():
    """Test direct du paramètre DLVL."""
    print("🎸 Test DLVL (Delay Level) - Direct")
    print("=" * 50)
    print("Le potentiomètre 3 est maintenant assigné à DLVL")
    print("Testons de modifier directement la valeur du paramètre DLVL")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
        print("✅ Connexion MIDI établie")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print("\nD'après le mapping MagicstompFrenzy:")
    print("- DelayLevel = offset 78 (0x4E) dans AmpMultiWidget")
    print("- L'offset 78 > 32 donc c'est la section effet")
    
    # Test avec des valeurs progressives
    test_values = [0, 32, 64, 96, 127]
    
    for i, value in enumerate(test_values):
        print(f"\nTest {i+1}/5: DLVL = {value}")
        
        # Modifier directement le paramètre Delay Level
        # Offset 78 = DelayLevel dans la section effet
        success = ms.tweak_parameter(78, value)
        
        print(f"📤 Message envoyé: DLVL (offset 78) = {value}")
        print("👀 Regardez l'écran du Magicstomp...")
        print("   La valeur du potentiomètre 3 (DLVL) a-t-elle changé?")
        print("   Tapez 'O' si oui, 'N' si non")
        
        response = input("La valeur DLVL a changé? (O/N): ").strip().upper()
        
        if response == 'O':
            print(f"🎉 SUCCESS! DLVL {value} a changé la valeur affichée!")
            print("On peut contrôler directement les paramètres d'effets!")
            return True
        else:
            print("❌ La valeur DLVL n'a pas changé")
        
        time.sleep(2)
    
    print("\n❌ La valeur DLVL n'a pas changé avec aucune valeur")
    print("Peut-être que l'offset 78 n'est pas correct pour DLVL")
    return False

def test_other_delay_offsets():
    """Test d'autres offsets possibles pour DLVL."""
    print("\n🔍 Test d'autres offsets possibles pour DLVL...")
    
    ms = RealtimeMagicstomp()
    
    try:
        ms._initialize_midi()
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # D'après le mapping MagicstompFrenzy, DLVL pourrait être à différents offsets
    possible_offsets = [
        (78, "DelayLevel (AmpMultiWidget)"),
        (67, "Delay Level (AmpMultiChorus)"),
        (29, "Mix (MonoDelayKnobParameters)"),
        (29, "Mix (StereoDelayKnobParameters)")
    ]
    
    for offset, description in possible_offsets:
        print(f"\nTest offset {offset}: {description}")
        print("Valeur test: 64")
        
        success = ms.tweak_parameter(offset, 64)
        
        print(f"📤 Message envoyé: Offset {offset} = 64")
        response = input("La valeur a changé? (O/N): ").strip().upper()
        if response == 'O':
            print(f"🎉 SUCCESS! Offset {offset} contrôle bien DLVL!")
            return offset
        else:
            print("❌ Pas de changement")
        
        time.sleep(1)
    
    return None

def main():
    """Test du paramètre DLVL."""
    print("🎸 Test DLVL (Delay Level) - Paramètre Direct")
    print("=" * 50)
    
    # Test direct
    if test_dlvl_direct():
        return
    
    # Test d'autres offsets
    working_offset = test_other_delay_offsets()
    if working_offset:
        print(f"\n🎉 Offset {working_offset} fonctionne pour DLVL!")
    else:
        print("\n❌ Aucun offset trouvé pour DLVL")

if __name__ == "__main__":
    main()
