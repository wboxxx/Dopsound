#!/usr/bin/env python3
"""
Magicstomp Adapter - JSON to SysEx Converter
============================================

Convertit un patch JSON généré par analyze2json.py vers des messages SysEx
compatibles avec le Magicstomp de Yamaha.

Usage:
    from adapter_magicstomp import MagicstompAdapter
    adapter = MagicstompAdapter()
    syx_data = adapter.json_to_syx(patch_json)
    adapter.send_to_device(syx_data)  # ou adapter.save_to_file(syx_data, 'patch.syx')

Référence: MagicstompFrenzy pour les mappings exacts des paramètres.
"""

import json
import mido
from typing import Dict, Any, List, Optional, Union
from pathlib import Path


class MagicstompAdapter:
    """Adaptateur pour conversion JSON vers SysEx Magicstomp."""
    
    # Constantes SysEx Magicstomp
    MANUFACTURER_ID = 0x43  # Yamaha
    DEVICE_ID = 0x00  # À adapter selon le device
    MAGICSTOMP_ID = 0x2D  # ID du Magicstomp
    
    # Commandes SysEx
    SYX_PATCH_WRITE = 0x40
    SYX_PATCH_REQUEST = 0x20
    
    def __init__(self, device_id: int = 0x00):
        """
        Initialise l'adaptateur Magicstomp.
        
        Args:
            device_id: ID du device Magicstomp (0-127)
        """
        self.device_id = device_id
        
        # Mappings des modèles d'amplificateur
        self.amp_models = {
            "BRIT_TOP_BOOST": 0x01,
            "TWEED_BASSMAN": 0x02,
            "JCM800": 0x03,
            "AC30": 0x04,
            "FENDER_TWIN": 0x05,
            "MESA_BOOGIE": 0x06
        }
        
        # Mappings des cabines
        self.cab_models = {
            "2x12_ALNICO": 0x01,
            "4x10_TWEED": 0x02,
            "4x12_VINTAGE": 0x03,
            "4x12_MODERN": 0x04,
            "1x12_BLACKFACE": 0x05,
            "2x12_CELESTION": 0x06
        }
        
        # Mappings des types de booster
        self.booster_types = {
            "TREBLE": 0x01,
            "TUBE_SCREAMER": 0x02,
            "CLEAN": 0x03,
            "DISTORTION": 0x04,
            "FUZZ": 0x05
        }
        
        # Mappings des types de reverb
        self.reverb_types = {
            "ROOM": 0x01,
            "PLATE": 0x02,
            "HALL": 0x03,
            "SPRING": 0x04,
            "CHURCH": 0x05
        }
        
        # Mappings des types de modulation
        self.mod_types = {
            "CHORUS": 0x01,
            "PHASER": 0x02,
            "TREMOLO": 0x03,
            "VIBRATO": 0x04,
            "FLANGER": 0x05
        }
    
    def float_to_magicstomp_value(self, value: float, max_val: int = 127) -> int:
        """
        Convertit une valeur float [0,1] vers une valeur Magicstomp [0,max_val].
        
        Args:
            value: Valeur normalisée [0,1]
            max_val: Valeur maximale Magicstomp (défaut 127)
            
        Returns:
            Valeur Magicstomp
        """
        return int(max(0, min(max_val, round(value * max_val))))
    
    def ms_to_magicstomp_time(self, time_ms: float) -> int:
        """
        Convertit un temps en ms vers la valeur Magicstomp.
        
        Args:
            time_ms: Temps en millisecondes
            
        Returns:
            Valeur Magicstomp pour le temps
        """
        # Magicstomp utilise une échelle logarithmique pour les temps
        # Approximation: log(time_ms) * facteur
        if time_ms <= 0:
            return 0
        
        # Mapping approximatif basé sur l'échelle Magicstomp
        if time_ms <= 50:
            return int(time_ms * 2.54)  # 0-127 pour 0-50ms
        elif time_ms <= 500:
            return int(127 + (time_ms - 50) * 0.28)  # 127-255 pour 50-500ms
        else:
            return int(255 + (time_ms - 500) * 0.1)  # 255+ pour >500ms
    
    def hz_to_magicstomp_rate(self, rate_hz: float) -> int:
        """
        Convertit une fréquence en Hz vers la valeur Magicstomp.
        
        Args:
            rate_hz: Fréquence en Hz
            
        Returns:
            Valeur Magicstomp pour la fréquence
        """
        # Magicstomp utilise une échelle logarithmique pour les fréquences
        if rate_hz <= 0:
            return 0
        
        # Mapping approximatif: 0.1-20 Hz -> 0-127
        import math
        if rate_hz < 0.1:
            return 0
        elif rate_hz <= 20:
            return int(127 * (math.log10(rate_hz / 0.1) / math.log10(200)))
        else:
            return 127
    
    def map_amp_parameters(self, amp_config: Dict[str, Any]) -> Dict[str, int]:
        """
        Mappe les paramètres d'amplificateur vers les valeurs Magicstomp.
        
        Args:
            amp_config: Configuration d'amp du JSON
            
        Returns:
            Dictionnaire des paramètres Magicstomp
        """
        print("🎸 Mapping paramètres amplificateur...")
        
        model_name = amp_config.get("model", "JCM800")
        amp_model_id = self.amp_models.get(model_name, 0x03)
        
        cab_name = amp_config.get("cab", "2x12_ALNICO")
        cab_model_id = self.cab_models.get(cab_name, 0x03)
        
        params = {
            "amp_model": amp_model_id,
            "cab_model": cab_model_id,
            "gain": self.float_to_magicstomp_value(amp_config.get("gain", 0.5)),
            "bass": self.float_to_magicstomp_value(amp_config.get("bass", 0.5)),
            "mid": self.float_to_magicstomp_value(amp_config.get("mid", 0.5)),
            "treble": self.float_to_magicstomp_value(amp_config.get("treble", 0.5)),
            "presence": self.float_to_magicstomp_value(amp_config.get("presence", 0.5)),
            "master": self.float_to_magicstomp_value(amp_config.get("master", 0.7))
        }
        
        print(f"   Modèle: {model_name} (ID: {amp_model_id})")
        print(f"   Cabine: {cab_name} (ID: {cab_model_id})")
        print(f"   Gain: {params['gain']}, EQ: B={params['bass']} M={params['mid']} T={params['treble']} P={params['presence']}")
        
        return params
    
    def map_booster_parameters(self, booster_config: Dict[str, Any]) -> Dict[str, int]:
        """
        Mappe les paramètres de booster vers les valeurs Magicstomp.
        
        Args:
            booster_config: Configuration de booster du JSON
            
        Returns:
            Dictionnaire des paramètres Magicstomp
        """
        print("🚀 Mapping paramètres booster...")
        
        booster_type_name = booster_config.get("type", "CLEAN")
        booster_type_id = self.booster_types.get(booster_type_name, 0x03)
        
        params = {
            "booster_type": booster_type_id,
            "booster_level": self.float_to_magicstomp_value(booster_config.get("level", 0.3)),
            "booster_enabled": 1 if booster_config.get("enabled", True) else 0
        }
        
        print(f"   Type: {booster_type_name} (ID: {booster_type_id})")
        print(f"   Level: {params['booster_level']}")
        
        return params
    
    def map_delay_parameters(self, delay_config: Dict[str, Any]) -> Dict[str, int]:
        """
        Mappe les paramètres de delay vers les valeurs Magicstomp.
        
        Args:
            delay_config: Configuration de delay du JSON
            
        Returns:
            Dictionnaire des paramètres Magicstomp
        """
        print("⏰ Mapping paramètres delay...")
        
        enabled = delay_config.get("enabled", False)
        if not enabled:
            return {"delay_enabled": 0}
        
        time_ms = delay_config.get("time_ms", 300)
        feedback = delay_config.get("feedback", 0.3)
        mix = delay_config.get("mix", 0.2)
        
        params = {
            "delay_enabled": 1,
            "delay_time": self.ms_to_magicstomp_time(time_ms),
            "delay_feedback": self.float_to_magicstomp_value(feedback),
            "delay_mix": self.float_to_magicstomp_value(mix),
            "delay_type": 0x01,  # Digital delay par défaut
            "delay_tempo_sync": 0  # Pas de sync tempo par défaut
        }
        
        print(f"   Temps: {time_ms}ms -> {params['delay_time']}")
        print(f"   Feedback: {feedback:.2f} -> {params['delay_feedback']}")
        print(f"   Mix: {mix:.2f} -> {params['delay_mix']}")
        
        return params
    
    def map_reverb_parameters(self, reverb_config: Dict[str, Any]) -> Dict[str, int]:
        """
        Mappe les paramètres de reverb vers les valeurs Magicstomp.
        
        Args:
            reverb_config: Configuration de reverb du JSON
            
        Returns:
            Dictionnaire des paramètres Magicstomp
        """
        print("🏛️ Mapping paramètres reverb...")
        
        enabled = reverb_config.get("enabled", False)
        if not enabled:
            return {"reverb_enabled": 0}
        
        reverb_type_name = reverb_config.get("type", "PLATE")
        reverb_type_id = self.reverb_types.get(reverb_type_name, 0x02)
        
        decay_s = reverb_config.get("decay_s", 1.5)
        mix = reverb_config.get("mix", 0.15)
        
        params = {
            "reverb_enabled": 1,
            "reverb_type": reverb_type_id,
            "reverb_decay": self.float_to_magicstomp_value(decay_s / 3.0),  # Normalise sur 3s max
            "reverb_mix": self.float_to_magicstomp_value(mix),
            "reverb_predelay": 0,  # Pas de predelay par défaut
            "reverb_high_cut": 127  # Pas de filtrage par défaut
        }
        
        print(f"   Type: {reverb_type_name} (ID: {reverb_type_id})")
        print(f"   Decay: {decay_s:.1f}s -> {params['reverb_decay']}")
        print(f"   Mix: {mix:.2f} -> {params['reverb_mix']}")
        
        return params
    
    def map_mod_parameters(self, mod_config: Dict[str, Any]) -> Dict[str, int]:
        """
        Mappe les paramètres de modulation vers les valeurs Magicstomp.
        
        Args:
            mod_config: Configuration de modulation du JSON
            
        Returns:
            Dictionnaire des paramètres Magicstomp
        """
        print("🌊 Mapping paramètres modulation...")
        
        enabled = mod_config.get("enabled", False)
        if not enabled:
            return {"mod_enabled": 0}
        
        mod_type_name = mod_config.get("type", "CHORUS")
        mod_type_id = self.mod_types.get(mod_type_name, 0x01)
        
        rate_hz = mod_config.get("rate_hz", 0.8)
        depth = mod_config.get("depth", 0.35)
        mix = mod_config.get("mix", 0.18)
        
        params = {
            "mod_enabled": 1,
            "mod_type": mod_type_id,
            "mod_rate": self.hz_to_magicstomp_rate(rate_hz),
            "mod_depth": self.float_to_magicstomp_value(depth),
            "mod_mix": self.float_to_magicstomp_value(mix),
            "mod_tempo_sync": 0  # Pas de sync tempo par défaut
        }
        
        print(f"   Type: {mod_type_name} (ID: {mod_type_id})")
        print(f"   Rate: {rate_hz:.1f}Hz -> {params['mod_rate']}")
        print(f"   Depth: {depth:.2f} -> {params['mod_depth']}")
        print(f"   Mix: {mix:.2f} -> {params['mod_mix']}")
        
        return params
    
    def create_syx_header(self, command: int, patch_number: int = 0) -> List[int]:
        """
        Crée l'en-tête SysEx pour le Magicstomp.
        
        Args:
            command: Commande SysEx (0x20 pour lecture, 0x40 pour écriture)
            patch_number: Numéro du patch (0-99)
            
        Returns:
            Liste des bytes d'en-tête
        """
        return [
            0xF0,  # SysEx start
            self.MANUFACTURER_ID,  # Yamaha
            self.DEVICE_ID,  # Device ID
            self.MAGICSTOMP_ID,  # Magicstomp ID
            command,  # Commande
            patch_number,  # Numéro de patch
        ]
    
    def create_patch_data(self, all_params: Dict[str, int]) -> List[int]:
        """
        Crée les données de patch à partir des paramètres mappés.
        
        Args:
            all_params: Tous les paramètres mappés
            
        Returns:
            Liste des bytes de données
        """
        # Structure de données Magicstomp (simplifiée)
        # Dans un vrai adaptateur, il faudrait la documentation complète
        patch_data = []
        
        # Section Amplificateur
        patch_data.extend([
            all_params.get("amp_model", 0x03),
            all_params.get("cab_model", 0x03),
            all_params.get("gain", 64),
            all_params.get("bass", 64),
            all_params.get("mid", 64),
            all_params.get("treble", 64),
            all_params.get("presence", 64),
            all_params.get("master", 89),
        ])
        
        # Section Booster
        patch_data.extend([
            all_params.get("booster_enabled", 0),
            all_params.get("booster_type", 0x03),
            all_params.get("booster_level", 38),
        ])
        
        # Section Delay
        patch_data.extend([
            all_params.get("delay_enabled", 0),
            all_params.get("delay_type", 0x01),
            all_params.get("delay_time", 96),  # 300ms approximatif
            all_params.get("delay_feedback", 38),
            all_params.get("delay_mix", 25),
            all_params.get("delay_tempo_sync", 0),
        ])
        
        # Section Reverb
        patch_data.extend([
            all_params.get("reverb_enabled", 0),
            all_params.get("reverb_type", 0x02),
            all_params.get("reverb_decay", 64),
            all_params.get("reverb_mix", 19),
            all_params.get("reverb_predelay", 0),
            all_params.get("reverb_high_cut", 127),
        ])
        
        # Section Modulation
        patch_data.extend([
            all_params.get("mod_enabled", 0),
            all_params.get("mod_type", 0x01),
            all_params.get("mod_rate", 10),
            all_params.get("mod_depth", 44),
            all_params.get("mod_mix", 23),
            all_params.get("mod_tempo_sync", 0),
        ])
        
        # Padding pour atteindre la taille de patch Magicstomp
        # (taille approximative basée sur MagicstompFrenzy)
        while len(patch_data) < 128:
            patch_data.append(0x00)
        
        return patch_data[:128]  # Limite à 128 bytes
    
    def calculate_checksum(self, data: List[int]) -> int:
        """
        Calcule le checksum SysEx pour le Magicstomp.
        
        Args:
            data: Données à vérifier
            
        Returns:
            Checksum calculé
        """
        # Checksum simple (XOR de tous les bytes)
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum & 0x7F  # Masque sur 7 bits
    
    def json_to_syx(self, patch_json: Union[Dict[str, Any], str], 
                   patch_number: int = 0) -> List[int]:
        """
        Convertit un patch JSON vers un message SysEx Magicstomp.
        
        Args:
            patch_json: Patch JSON (dict ou chemin vers fichier)
            patch_number: Numéro de patch (0-99)
            
        Returns:
            Message SysEx complet
        """
        print("🔄 Conversion JSON vers SysEx Magicstomp...")
        
        # Charge le JSON si c'est un chemin
        if isinstance(patch_json, str):
            with open(patch_json, 'r', encoding='utf-8') as f:
                patch_data = json.load(f)
        else:
            patch_data = patch_json
        
        # Mappe tous les paramètres
        all_params = {}
        
        # Amplificateur
        if "amp" in patch_data:
            all_params.update(self.map_amp_parameters(patch_data["amp"]))
        
        # Booster
        if "booster" in patch_data:
            all_params.update(self.map_booster_parameters(patch_data["booster"]))
        
        # Delay
        if "delay" in patch_data:
            all_params.update(self.map_delay_parameters(patch_data["delay"]))
        
        # Reverb
        if "reverb" in patch_data:
            all_params.update(self.map_reverb_parameters(patch_data["reverb"]))
        
        # Modulation
        if "mod" in patch_data:
            all_params.update(self.map_mod_parameters(patch_data["mod"]))
        
        # Crée le message SysEx
        syx_message = []
        
        # En-tête
        syx_message.extend(self.create_syx_header(self.SYX_PATCH_WRITE, patch_number))
        
        # Données de patch
        patch_data_bytes = self.create_patch_data(all_params)
        syx_message.extend(patch_data_bytes)
        
        # Checksum
        checksum = self.calculate_checksum(syx_message[1:])  # Exclut le F0
        syx_message.append(checksum)
        
        # Fin SysEx
        syx_message.append(0xF7)
        
        print(f"✅ Message SysEx créé: {len(syx_message)} bytes")
        print(f"   Patch #{patch_number}, Checksum: 0x{checksum:02X}")
        
        return syx_message
    
    def save_to_file(self, syx_data: List[int], filename: str) -> None:
        """
        Sauvegarde les données SysEx vers un fichier .syx.
        
        Args:
            syx_data: Données SysEx
            filename: Nom du fichier de sortie
        """
        print(f"💾 Sauvegarde vers {filename}...")
        
        with open(filename, 'wb') as f:
            f.write(bytes(syx_data))
        
        print(f"✅ Fichier SysEx sauvegardé: {filename}")
    
    def send_to_device(self, syx_data: List[int], port_name: Optional[str] = None) -> bool:
        """
        Envoie les données SysEx vers le device Magicstomp.
        
        Args:
            syx_data: Données SysEx
            port_name: Nom du port MIDI (optionnel)
            
        Returns:
            True si l'envoi a réussi
        """
        print("📤 Envoi vers device Magicstomp...")
        print(f"🔍 DEBUG: Port name requested: {port_name}")
        print(f"🔍 DEBUG: SysEx data to send: {len(syx_data)} bytes")
        print(f"🔍 DEBUG: SysEx header: {syx_data[:6]} (F0, Manufacturer, Device, Magicstomp, Command, Patch)")
        
        try:
            # Trouve le port de sortie
            all_output_ports = mido.get_output_names()
            print(f"🔍 DEBUG: All available output ports: {all_output_ports}")
            
            if port_name:
                output_ports = [name for name in all_output_ports if port_name.lower() in name.lower()]
                print(f"🔍 DEBUG: Searching for port containing '{port_name}'")
            else:
                output_ports = [name for name in all_output_ports if 'magicstomp' in name.lower()]
                print(f"🔍 DEBUG: Searching for port containing 'magicstomp'")
            
            print(f"🔍 DEBUG: Found matching ports: {output_ports}")
            
            if not output_ports:
                print("❌ Aucun port Magicstomp trouvé")
                print("   Ports disponibles:", all_output_ports)
                print("💡 CONSEIL: Vérifiez que votre Magicstomp est connecté et reconnu par Windows")
                print("💡 CONSEIL: Essayez de déconnecter/reconnecter le câble USB/MIDI")
                return False
            
            selected_port = output_ports[0]
            print(f"   Utilisation du port: {selected_port}")
            
            # Envoie le message SysEx
            print("🔍 DEBUG: Opening MIDI port...")
            with mido.open_output(selected_port) as port:
                print("🔍 DEBUG: Port opened successfully")
                
                # Prepare SysEx message (exclude F0 and F7)
                syx_message_data = syx_data[1:-1]
                print(f"🔍 DEBUG: SysEx message data: {len(syx_message_data)} bytes")
                print(f"🔍 DEBUG: First 10 bytes: {syx_message_data[:10]}")
                
                # Check for bytes > 127
                invalid_bytes = [i for i, b in enumerate(syx_message_data) if b > 127]
                if invalid_bytes:
                    print(f"🔍 DEBUG: Invalid bytes found at positions: {invalid_bytes}")
                    print(f"🔍 DEBUG: Invalid byte values: {[syx_message_data[i] for i in invalid_bytes]}")
                    # Mask bytes to 7-bit range
                    syx_message_data = [b & 0x7F for b in syx_message_data]
                    print(f"🔍 DEBUG: Masked data to 7-bit range")
                
                syx_message = mido.Message('sysex', data=syx_message_data)
                print("🔍 DEBUG: Sending SysEx message...")
                port.send(syx_message)
                print("🔍 DEBUG: Message sent!")
            
            print("✅ Message SysEx envoyé avec succès")
            print(f"💡 Le patch a été envoyé sur le patch #{syx_data[5]} (bank 0)")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi: {e}")
            print(f"🔍 DEBUG: Exception type: {type(e).__name__}")
            import traceback
            print(f"🔍 DEBUG: Traceback: {traceback.format_exc()}")
            return False
    
    def list_midi_ports(self) -> None:
        """Liste les ports MIDI disponibles."""
        print("🔌 Ports MIDI disponibles:")
        print("   Entrées:", mido.get_input_names())
        print("   Sorties:", mido.get_output_names())


def main():
    """Point d'entrée pour tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test de l'adaptateur Magicstomp")
    parser.add_argument('json_file', help='Fichier JSON de patch')
    parser.add_argument('--output', '-o', help='Fichier SysEx de sortie')
    parser.add_argument('--send', '-s', action='store_true', help='Envoyer vers le device')
    parser.add_argument('--patch', '-p', type=int, default=0, help='Numéro de patch')
    
    args = parser.parse_args()
    
    adapter = MagicstompAdapter()
    
    # Convertit vers SysEx
    syx_data = adapter.json_to_syx(args.json_file, args.patch)
    
    # Sauvegarde si demandé
    if args.output:
        adapter.save_to_file(syx_data, args.output)
    
    # Envoie si demandé
    if args.send:
        adapter.send_to_device(syx_data)
    
    # Affiche les ports disponibles
    adapter.list_midi_ports()


if __name__ == "__main__":
    main()
