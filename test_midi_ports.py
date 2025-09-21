#!/usr/bin/env python3
"""
Test des ports MIDI pour Magicstomp
==================================

Script simple pour lister les ports MIDI et tester la connexion.
"""

import mido
import time
from realtime_magicstomp import RealtimeMagicstomp


def list_all_midi_ports():
    """Liste tous les ports MIDI disponibles."""
    print("🔍 Recherche des ports MIDI...")
    
    try:
        input_ports = mido.get_input_names()
        output_ports = mido.get_output_names()
        
        print(f"\n📥 Ports MIDI d'ENTRÉE ({len(input_ports)}):")
        for i, port in enumerate(input_ports):
            print(f"  {i}: {port}")
        
        print(f"\n📤 Ports MIDI de SORTIE ({len(output_ports)}):")
        for i, port in enumerate(output_ports):
            print(f"  {i}: {port}")
        
        # Analyse pour Magicstomp
        print(f"\n🎸 Analyse pour Magicstomp:")
        
        magicstomp_inputs = [p for p in input_ports if 'magicstomp' in p.lower()]
        magicstomp_outputs = [p for p in output_ports if 'magicstomp' in p.lower()]
        
        yamaha_inputs = [p for p in input_ports if 'yamaha' in p.lower() and 'ag03' not in p.lower()]
        yamaha_outputs = [p for p in output_ports if 'yamaha' in p.lower() and 'ag03' not in p.lower()]
        
        if magicstomp_inputs:
            print(f"  ✅ Magicstomp INPUT trouvé: {magicstomp_inputs}")
        else:
            print(f"  ❌ Aucun port Magicstomp INPUT trouvé")
        
        if magicstomp_outputs:
            print(f"  ✅ Magicstomp OUTPUT trouvé: {magicstomp_outputs}")
        else:
            print(f"  ❌ Aucun port Magicstomp OUTPUT trouvé")
        
        if yamaha_inputs:
            print(f"  ⚠️ Yamaha INPUT (possible Magicstomp): {yamaha_inputs}")
        
        if yamaha_outputs:
            print(f"  ⚠️ Yamaha OUTPUT (possible Magicstomp): {yamaha_outputs}")
        
        return {
            'input': input_ports,
            'output': output_ports,
            'magicstomp_input': magicstomp_inputs,
            'magicstomp_output': magicstomp_outputs,
            'yamaha_input': yamaha_inputs,
            'yamaha_output': yamaha_outputs
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche des ports: {e}")
        return None


def test_port_connection(port_name: str):
    """Test la connexion à un port spécifique."""
    print(f"\n🧪 Test de connexion au port: {port_name}")
    
    try:
        # Test de sortie
        output_port = mido.open_output(port_name)
        print(f"  ✅ Port de sortie ouvert avec succès")
        
        # Test d'envoi d'un message simple
        test_message = mido.Message('control_change', channel=0, control=1, value=64)
        output_port.send(test_message)
        print(f"  ✅ Message de test envoyé")
        
        output_port.close()
        print(f"  ✅ Port fermé proprement")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur de connexion: {e}")
        return False


def interactive_port_selection():
    """Sélection interactive du port."""
    ports_info = RealtimeMagicstomp.list_midi_ports()
    output_ports = ports_info['output']
    
    if not output_ports:
        print("❌ Aucun port MIDI de sortie trouvé")
        return None
    
    print(f"\n🔍 Ports MIDI de sortie disponibles:")
    for i, port in enumerate(output_ports):
        print(f"  {i}: {port}")
    
    # Suggestions pour Magicstomp
    suggestions = []
    for i, port in enumerate(output_ports):
        if 'magicstomp' in port.lower():
            suggestions.append((i, port, "🎸 Magicstomp"))
        elif 'yamaha' in port.lower() and 'ag03' not in port.lower():
            suggestions.append((i, port, "⚠️ Yamaha (possible Magicstomp)"))
    
    if suggestions:
        print(f"\n💡 Suggestions:")
        for i, port, desc in suggestions:
            print(f"  → {i}: {port} ({desc})")
    
    try:
        choice = input(f"\nSélectionnez un port (0-{len(output_ports)-1}) ou 'q' pour quitter: ")
        if choice.lower() == 'q':
            return None
        
        port_index = int(choice)
        if 0 <= port_index < len(output_ports):
            selected_port = output_ports[port_index]
            return selected_port
        else:
            print("❌ Index invalide")
            return None
            
    except (ValueError, KeyboardInterrupt):
        print("❌ Sélection annulée")
        return None


def test_realtime_adapter_with_port(port_name: str):
    """Test de l'adaptateur temps réel avec un port spécifique."""
    print(f"\n🎸 Test de l'adaptateur temps réel avec le port: {port_name}")
    
    try:
        # Crée l'adaptateur avec le port spécifique
        rt = RealtimeMagicstomp(midi_port_name=port_name, auto_detect=False)
        
        if rt.output_port is None:
            print("❌ Échec de la connexion")
            return False
        
        print("✅ Adaptateur connecté")
        
        # Test des paramètres
        print("📝 Test des paramètres d'amplificateur:")
        
        # Amp Level
        print("  - Amp Level: 64")
        rt.tweak_parameter(9, 64, immediate=True)
        time.sleep(0.5)
        
        print("  - Amp Level: 80")
        rt.tweak_parameter(9, 80, immediate=True)
        time.sleep(0.5)
        
        # Amp Gain
        print("  - Amp Gain: 70")
        rt.tweak_parameter(10, 70, immediate=True)
        time.sleep(0.5)
        
        print("✅ Test terminé avec succès")
        
        # Ferme l'adaptateur
        rt.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False


def main():
    """Fonction principale."""
    print("🎸 Test des ports MIDI pour Magicstomp")
    print("=" * 50)
    
    # Liste tous les ports
    ports_info = list_all_midi_ports()
    
    if ports_info is None:
        return
    
    # Si on trouve des ports Magicstomp, on les teste
    if ports_info['magicstomp_output']:
        print(f"\n🧪 Test automatique des ports Magicstomp:")
        for port in ports_info['magicstomp_output']:
            test_port_connection(port)
    
    # Sélection interactive
    print(f"\n🎯 Sélection interactive du port:")
    selected_port = interactive_port_selection()
    
    if selected_port:
        # Test de connexion
        if test_port_connection(selected_port):
            # Test de l'adaptateur temps réel
            test_realtime_adapter_with_port(selected_port)
    
    print(f"\n✅ Test terminé")


if __name__ == "__main__":
    main()
