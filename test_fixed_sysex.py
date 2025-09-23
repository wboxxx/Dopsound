#!/usr/bin/env python3
"""
Test du format SysEx corrigé
============================

Teste que le MagicstompAdapter utilise maintenant le bon format SysEx
compatible avec MagicstompFrenzy.
"""

import mido
from adapter_magicstomp import MagicstompAdapter
from realtime_magicstomp import RealtimeMagicstomp

def test_checksum_calculation():
    """Teste que les deux adaptateurs utilisent le même checksum."""
    print("🧪 Test du calcul de checksum")
    
    # Données de test
    test_data = [0x43, 0x7D, 0x40, 0x55, 0x42, 0x20, 0x00, 0x0A, 0x40]
    
    # MagicstompAdapter
    adapter = MagicstompAdapter()
    adapter_checksum = adapter.calculate_checksum(test_data)
    
    # RealtimeMagicstomp
    rt = RealtimeMagicstomp(auto_detect=False)
    rt_checksum = rt.calculate_checksum(test_data)
    
    print(f"📊 MagicstompAdapter checksum: 0x{adapter_checksum:02X}")
    print(f"📊 RealtimeMagicstomp checksum: 0x{rt_checksum:02X}")
    
    if adapter_checksum == rt_checksum:
        print("✅ Checksums identiques - format compatible !")
        return True
    else:
        print("❌ Checksums différents - problème de compatibilité !")
        return False

def test_sysex_message_format():
    """Teste que les messages SysEx ont le bon format."""
    print("\n🧪 Test du format des messages SysEx")
    
    # MagicstompAdapter - message temps réel
    adapter = MagicstompAdapter()
    adapter_message = adapter.create_realtime_parameter_message(71, 64)  # DHPF = 64
    
    # RealtimeMagicstomp - message temps réel
    rt = RealtimeMagicstomp(auto_detect=False)
    rt_message = rt.create_parameter_message(71, [64])  # DHPF = 64
    
    print(f"📤 MagicstompAdapter message: {[hex(x) for x in adapter_message]}")
    print(f"📤 RealtimeMagicstomp message: {[hex(x) for x in rt_message]}")
    
    # Vérifie que les messages sont identiques
    if adapter_message == rt_message:
        print("✅ Messages SysEx identiques - format compatible !")
        return True
    else:
        print("❌ Messages SysEx différents - problème de format !")
        return False

def test_midi_connection():
    """Teste la connexion MIDI avec le nouveau format."""
    print("\n🧪 Test de connexion MIDI")
    
    try:
        # Liste les ports
        ports = mido.get_output_names()
        print(f"🔍 Ports MIDI disponibles: {ports}")
        
        # Trouve le Magicstomp
        magicstomp_port = None
        for port in ports:
            if 'ub9' in port.lower() or 'magicstomp' in port.lower():
                magicstomp_port = port
                break
        
        if not magicstomp_port:
            print("❌ Aucun port Magicstomp trouvé")
            return False
        
        print(f"✅ Port Magicstomp trouvé: {magicstomp_port}")
        
        # Test avec MagicstompAdapter
        adapter = MagicstompAdapter()
        
        # Ouvre le port
        with mido.open_output(magicstomp_port) as port:
            print("✅ Port MIDI ouvert")
            
            # Test envoi paramètre DHPF (Delay High Pass Filter)
            print("📤 Test envoi paramètre DHPF (offset 71) = 64")
            adapter.tweak_parameter(71, 64, port)
            
            print("✅ Message envoyé avec succès !")
            return True
            
    except Exception as e:
        print(f"❌ Erreur connexion MIDI: {e}")
        return False

def main():
    """Lance tous les tests."""
    print("🎸 Test du format SysEx corrigé")
    print("=" * 40)
    
    tests = [
        test_checksum_calculation,
        test_sysex_message_format,
        test_midi_connection
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans le test {test.__name__}: {e}")
            results.append(False)
    
    print("\n📊 Résultats des tests:")
    print("=" * 40)
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Test {i}: {test.__name__} - {status}")
    
    all_passed = all(results)
    if all_passed:
        print("\n🎉 Tous les tests sont passés ! Le format SysEx est corrigé.")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez les problèmes ci-dessus.")
    
    return all_passed

if __name__ == "__main__":
    main()
