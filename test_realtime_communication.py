#!/usr/bin/env python3
"""
Test de la communication temps réel corrigée
===========================================

Teste que le système d'effets peut maintenant communiquer avec le Magicstomp.
"""

import time
from realtime_magicstomp import RealtimeMagicstomp
from adapter_magicstomp import MagicstompAdapter

def test_realtime_magicstomp():
    """Teste RealtimeMagicstomp avec auto-détection."""
    print("🧪 Test RealtimeMagicstomp avec auto-détection")
    
    try:
        # Initialise avec auto-détection
        rt = RealtimeMagicstomp(auto_detect=True)
        
        if rt.output_port:
            print(f"✅ RealtimeMagicstomp connecté: {rt.midi_port_name}")
            
            # Test envoi paramètre DHPF
            print("📤 Test envoi paramètre DHPF (offset 71) = 64")
            rt.tweak_parameter(71, 64, immediate=True)
            
            time.sleep(1)
            
            # Test envoi paramètre DLVL  
            print("📤 Test envoi paramètre DLVL (offset 67) = 80")
            rt.tweak_parameter(67, 80, immediate=True)
            
            print("✅ RealtimeMagicstomp fonctionne !")
            return True
        else:
            print("❌ RealtimeMagicstomp non connecté")
            return False
            
    except Exception as e:
        print(f"❌ Erreur RealtimeMagicstomp: {e}")
        return False
    finally:
        if 'rt' in locals():
            rt.stop()

def test_magicstomp_adapter():
    """Teste MagicstompAdapter avec le nouveau format temps réel."""
    print("\n🧪 Test MagicstompAdapter avec format temps réel")
    
    try:
        adapter = MagicstompAdapter()
        
        # Trouve le port Magicstomp
        import mido
        ports = mido.get_output_names()
        magicstomp_port = None
        for port in ports:
            if 'ub9' in port.lower() or 'magicstomp' in port.lower():
                magicstomp_port = port
                break
        
        if not magicstomp_port:
            print("❌ Aucun port Magicstomp trouvé")
            return False
        
        print(f"✅ Port Magicstomp trouvé: {magicstomp_port}")
        
        # Ouvre le port et teste
        with mido.open_output(magicstomp_port) as port:
            print("✅ Port MIDI ouvert")
            
            # Test envoi paramètre DHPF
            print("📤 Test envoi paramètre DHPF (offset 71) = 64")
            adapter.tweak_parameter(71, 64, port)
            
            time.sleep(1)
            
            # Test envoi paramètre DLVL
            print("📤 Test envoi paramètre DLVL (offset 67) = 80") 
            adapter.tweak_parameter(67, 80, port)
            
            print("✅ MagicstompAdapter fonctionne !")
            return True
            
    except Exception as e:
        print(f"❌ Erreur MagicstompAdapter: {e}")
        return False

def test_parameter_mapping():
    """Teste le mapping des paramètres d'effets."""
    print("\n🧪 Test du mapping des paramètres")
    
    # Paramètres testés précédemment
    test_params = [
        (71, "DHPF (Delay High Pass Filter)"),
        (67, "DLVL (Delay Level)"),
        (53, "Flanger Depth"),
        (54, "Flanger Feedback"),
    ]
    
    try:
        rt = RealtimeMagicstomp(auto_detect=True)
        
        if not rt.output_port:
            print("❌ Pas de connexion MIDI pour le test de mapping")
            return False
        
        print("✅ Connexion MIDI établie, test du mapping...")
        
        for offset, name in test_params:
            print(f"📤 Test {name} (offset {offset}) = 50")
            rt.tweak_parameter(offset, 50, immediate=True)
            time.sleep(0.5)
        
        print("✅ Mapping des paramètres fonctionne !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur mapping paramètres: {e}")
        return False
    finally:
        if 'rt' in locals():
            rt.stop()

def main():
    """Lance tous les tests de communication."""
    print("🎸 Test de la communication temps réel corrigée")
    print("=" * 50)
    
    tests = [
        test_realtime_magicstomp,
        test_magicstomp_adapter,
        test_parameter_mapping
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
    print("=" * 50)
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Test {i}: {test.__name__} - {status}")
    
    all_passed = all(results)
    if all_passed:
        print("\n🎉 Tous les tests sont passés ! La communication est rétablie.")
        print("💡 Le système d'effets peut maintenant communiquer avec le Magicstomp.")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez les problèmes ci-dessus.")
    
    return all_passed

if __name__ == "__main__":
    main()
