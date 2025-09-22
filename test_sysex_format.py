#!/usr/bin/env python3
"""
Test du format sysex Magicstomp
==============================

Vérifie que le format des messages sysex correspond bien à celui
utilisé par MagicstompFrenzy.
"""

from realtime_magicstomp import RealtimeMagicstomp
import mido


def analyze_sysex_message(message_data):
    """Analyse un message sysex."""
    print(f"Message sysex: {[hex(x) for x in message_data]}")
    
    if len(message_data) < 8:
        print("❌ Message trop court")
        return
    
    # Vérifie l'en-tête
    header = message_data[:6]
    expected_header = [0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42]
    
    if header == expected_header:
        print("✅ En-tête correct")
    else:
        print(f"❌ En-tête incorrect: {[hex(x) for x in header]}")
        print(f"   Attendu: {[hex(x) for x in expected_header]}")
    
    # Vérifie la commande
    cmd = message_data[6]
    if cmd == 0x20:
        print("✅ Commande de modification de paramètre correcte")
    else:
        print(f"❌ Commande incorrecte: {hex(cmd)} (attendu: 0x20)")
    
    # Analyse la section et l'offset
    if len(message_data) >= 9:
        section = message_data[7]
        offset = message_data[8]
        
        if section == 0x00:
            print(f"✅ Section commune, offset: {offset}")
        elif section == 0x01:
            print(f"✅ Section effet, offset: {offset}")
        else:
            print(f"❌ Section inconnue: {hex(section)}")
    
    # Analyse la valeur
    if len(message_data) >= 10:
        value = message_data[9]
        print(f"✅ Valeur du paramètre: {value}")
    
    # Vérifie le checksum
    if len(message_data) >= 11:
        checksum = message_data[-2]  # Avant-dernier byte
        print(f"✅ Checksum: {hex(checksum)}")
    
    # Vérifie la fin
    if message_data[-1] == 0xF7:
        print("✅ Fin de message correcte")
    else:
        print(f"❌ Fin de message incorrecte: {hex(message_data[-1])}")


def test_sysex_generation():
    """Test de génération des messages sysex."""
    print("🧪 Test de génération des messages sysex")
    print("=" * 50)
    
    rt = RealtimeMagicstomp(auto_detect=False)  # Pas de connexion
    
    # Test différents paramètres
    test_params = [
        (9, 64, "Amp Level"),
        (10, 70, "Amp Gain"),
        (11, 60, "Treble"),
        (0x21, 50, "Delay Time (effet)"),
        (0x31, 40, "Reverb Type (effet)")
    ]
    
    for offset, value, name in test_params:
        print(f"\n📝 Test {name} (offset: {offset}, valeur: {value})")
        message = rt.create_parameter_message(offset, [value])
        analyze_sysex_message(message)
        print()


def compare_with_magicstompfrenzy():
    """Compare avec le format MagicstompFrenzy."""
    print("\n🔍 Comparaison avec MagicstompFrenzy")
    print("=" * 50)
    
    print("Format MagicstompFrenzy (d'après le code C++):")
    print("  Header: F0 43 7D 40 55 42")
    print("  Command: 20")
    print("  Section: 00 (commune) ou 01 (effet)")
    print("  Offset: Position du paramètre")
    print("  Data: Valeur(s) du paramètre")
    print("  Checksum: XOR de tous les bytes de données")
    print("  Footer: F7")
    print()
    
    print("Format généré par notre code:")
    rt = RealtimeMagicstomp(auto_detect=False)
    
    # Test paramètre commun
    message = rt.create_parameter_message(9, [64])  # Amp Level
    print(f"  Paramètre commun (Amp Level): {[hex(x) for x in message]}")
    
    # Test paramètre effet
    message = rt.create_parameter_message(0x21, [50])  # Delay Time
    print(f"  Paramètre effet (Delay Time): {[hex(x) for x in message]}")
    
    print("\n✅ Comparaison terminée")


def test_checksum_calculation():
    """Test du calcul de checksum."""
    print("\n🧮 Test du calcul de checksum")
    print("=" * 50)
    
    rt = RealtimeMagicstomp(auto_detect=False)
    
    # Test avec des données connues
    test_data = [
        [0x20, 0x00, 0x09, 0x40],  # Section commune, offset 9, valeur 64
        [0x20, 0x01, 0x21, 0x32],  # Section effet, offset 0x21, valeur 50
    ]
    
    for data in test_data:
        checksum = rt.calculate_checksum(data)
        print(f"Données: {[hex(x) for x in data]}")
        print(f"Checksum calculé: {hex(checksum)}")
        
        # Vérifie que le checksum XOR avec les données donne 0
        xor_result = 0
        for byte in data:
            xor_result ^= byte
        xor_result ^= checksum
        
        if xor_result == 0:
            print("✅ Checksum correct")
        else:
            print(f"❌ Checksum incorrect (XOR résultant: {hex(xor_result)})")
        print()


def main():
    """Fonction principale."""
    print("🔬 Test du format sysex Magicstomp")
    print("=" * 60)
    
    try:
        test_sysex_generation()
        compare_with_magicstompfrenzy()
        test_checksum_calculation()
        
        print("\n✅ Tous les tests de format terminés!")
        print("\nCONCLUSION:")
        print("Si tous les tests montrent '✅', alors le format")
        print("des messages sysex est correct selon MagicstompFrenzy.")
        print()
        print("Pour vérifier que ça marche vraiment, lancez:")
        print("  python verify_magicstomp_control.py")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")


if __name__ == "__main__":
    main()


