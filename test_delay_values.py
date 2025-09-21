import time
from realtime_magicstomp import RealtimeMagicstomp

def test_delay_values():
    print("🎸 Test des valeurs des paramètres Delay")
    print("========================================")
    print("Paramètres affichés:")
    print("- Potentiomètre 1: DHPF (Delay High Pass Filter)")
    print("- Potentiomètre 3: DLVL (Delay Level)")
    print()
    print("Ce test va modifier les valeurs de ces paramètres")
    print("Regardez l'écran du Magicstomp pour voir les changements")
    print()
    
    ms = RealtimeMagicstomp()
    if not ms._initialize_midi():
        print("❌ Échec de l'initialisation MIDI.")
        return
    
    # Offsets des paramètres Delay d'après knobparameters.h
    # Pour MonoDelay: High Pass Filter = 71, Delay Level = 67
    DHPF_OFFSET = 71  # High Pass Filter
    DLVL_OFFSET = 67  # Delay Level
    
    test_values = [0, 32, 64, 96, 127]
    
    try:
        print("🔄 Test des valeurs DHPF (Delay High Pass Filter)")
        print("------------------------------------------------")
        for value in test_values:
            print(f"📤 Envoi DHPF = {value}")
            ms.tweak_parameter(DHPF_OFFSET, value)
            print(f"👀 Vous devriez voir la valeur {value} sur le potentiomètre 1 (DHPF)")
            time.sleep(3)
        
        print("\n🔄 Test des valeurs DLVL (Delay Level)")
        print("-------------------------------------")
        for value in test_values:
            print(f"📤 Envoi DLVL = {value}")
            ms.tweak_parameter(DLVL_OFFSET, value)
            print(f"👀 Vous devriez voir la valeur {value} sur le potentiomètre 3 (DLVL)")
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nTest interrompu par l'utilisateur.")
    finally:
        ms.stop_realtime_send()
        ms.close_midi_port()
        print("✅ Test terminé.")

if __name__ == "__main__":
    test_delay_values()
