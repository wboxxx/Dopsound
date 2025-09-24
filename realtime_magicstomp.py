#!/usr/bin/env python3
"""
Real-time Magicstomp Parameter Tweaking
======================================

Permet de modifier des paramètres individuels du Magicstomp en temps réel
sans avoir à recharger le patch complet. Basé sur le format sysex de MagicstompFrenzy.

Usage:
    from realtime_magicstomp import RealtimeMagicstomp
    rt = RealtimeMagicstomp()
    rt.tweak_parameter(offset=10, value=64)  # Modifie le paramètre à l'offset 10
"""

import mido
import time
from typing import Dict, Any, List, Optional, Tuple
from collections import deque
import threading
import queue

from magicstomp_sysex import (
    PATCH_COMMON_LENGTH as SYSEX_PATCH_COMMON_LENGTH,
    PATCH_EFFECT_LENGTH as SYSEX_PATCH_EFFECT_LENGTH,
    PATCH_TOTAL_LENGTH as SYSEX_PATCH_TOTAL_LENGTH,
    SYSEX_HEADER,
    SYSEX_FOOTER,
    PARAMETER_SEND_CMD,
    build_parameter_message,
    calculate_checksum,
)


class RealtimeMagicstomp:
    """Adaptateur pour tweaking temps réel des paramètres Magicstomp."""
    
    # Constantes du format sysex Magicstomp (basé sur MagicstompFrenzy)
    SYX_HEADER = SYSEX_HEADER
    SYX_FOOTER = SYSEX_FOOTER
    PARAM_SEND_CMD = PARAMETER_SEND_CMD
    BULK_RESPONSE_HEADER = [0x43, 0x7D, 0x30, 0x55, 0x42, 0x39, 0x39]

    # Structure des patches (re-export depuis magicstomp_sysex pour compatibilité)
    PATCH_COMMON_LENGTH = SYSEX_PATCH_COMMON_LENGTH
    PATCH_EFFECT_LENGTH = SYSEX_PATCH_EFFECT_LENGTH
    PATCH_TOTAL_LENGTH = SYSEX_PATCH_TOTAL_LENGTH
    
    # Mappings des paramètres communs (offset dans le patch)
    COMMON_PARAMS = {
        'patch_type': 0,
        'control1': 2,
        'control2': 4, 
        'control3': 6,
        'patch_name': 16,  # 12 bytes
        'amp_type': 8,
        'amp_level': 9,
        'amp_gain': 10,
        'amp_treble': 11,
        'amp_middle': 12,
        'amp_bass': 13,
        'amp_presence': 14,
        'amp_master': 15
    }
    
    def __init__(self, midi_port_name: Optional[str] = None, auto_detect: bool = True):
        """
        Initialise l'adaptateur temps réel.
        
        Args:
            midi_port_name: Nom du port MIDI (None pour auto-détection)
            auto_detect: Si True, essaie l'auto-détection
        """
        self.midi_port_name = midi_port_name
        self.output_port = None
        self.input_port = None
        self.parameter_queue = queue.Queue()
        self.send_thread = None
        self.running = False
        
        # Cache des paramètres actuels pour éviter les doublons
        self.parameter_cache = {}
        self.cache_lock = threading.Lock()
        
        if auto_detect:
            self._initialize_midi()
        elif midi_port_name:
            self._connect_to_port(midi_port_name)
    
    def _initialize_midi(self):
        """Initialise les ports MIDI."""
        try:
            # Auto-détection du port Magicstomp
            if self.midi_port_name is None:
                ports = mido.get_output_names()
                print(f"🔍 Ports MIDI disponibles: {ports}")
                
                # Recherche spécifique pour Magicstomp
                magicstomp_ports = [p for p in ports if 'magicstomp' in p.lower()]
                if magicstomp_ports:
                    self.midi_port_name = magicstomp_ports[0]
                    print(f"✅ Magicstomp trouvé: {self.midi_port_name}")
                else:
                    # Recherche par modèle UB9 (Magicstomp)
                    ub9_ports = [p for p in ports if 'ub9' in p.lower()]
                    if ub9_ports:
                        self.midi_port_name = ub9_ports[0]
                        print(f"✅ Magicstomp UB9 trouvé: {self.midi_port_name}")
                    else:
                        # Recherche par ID Yamaha (0x43) ou nom générique
                        yamaha_ports = [p for p in ports if 'yamaha' in p.lower() and 'ag03' not in p.lower()]
                        if yamaha_ports:
                            self.midi_port_name = yamaha_ports[0]
                            print(f"⚠️ Yamaha trouvé (possible Magicstomp): {self.midi_port_name}")
                        else:
                            # Prendre le premier port disponible
                            self.midi_port_name = ports[0] if ports else None
                            print(f"⚠️ Aucun Magicstomp trouvé, utilisation du premier port: {self.midi_port_name}")
            
            if self.midi_port_name:
                self._connect_to_port(self.midi_port_name)
            else:
                print("❌ Aucun port MIDI trouvé")
                
        except Exception as e:
            print(f"❌ Erreur initialisation MIDI: {e}")
    
    def _connect_to_port(self, port_name: str):
        """Connecte à un port MIDI spécifique."""
        try:
            self.output_port = mido.open_output(port_name)
            print(f"✅ Port MIDI de sortie ouvert: {port_name}")
            
            # Essayer d'ouvrir aussi un port d'entrée pour les confirmations
            try:
                self.input_port = mido.open_input(port_name)
                print(f"✅ Port MIDI d'entrée ouvert: {port_name}")
            except:
                print("⚠️ Port MIDI d'entrée non disponible")
                
        except Exception as e:
            print(f"❌ Erreur connexion au port {port_name}: {e}")
    
    @staticmethod
    def list_midi_ports() -> Dict[str, List[str]]:
        """
        Liste tous les ports MIDI disponibles.
        
        Returns:
            Dict avec 'input' et 'output' ports
        """
        try:
            input_ports = mido.get_input_names()
            output_ports = mido.get_output_names()
            
            return {
                'input': input_ports,
                'output': output_ports
            }
        except Exception as e:
            print(f"❌ Erreur listing ports MIDI: {e}")
            return {'input': [], 'output': []}
    
    @staticmethod
    def select_magicstomp_port() -> Optional[str]:
        """
        Permet à l'utilisateur de sélectionner manuellement le port Magicstomp.
        
        Returns:
            Nom du port sélectionné ou None
        """
        ports_info = RealtimeMagicstomp.list_midi_ports()
        output_ports = ports_info['output']
        
        if not output_ports:
            print("❌ Aucun port MIDI de sortie trouvé")
            return None
        
        print("\n🔍 Ports MIDI de sortie disponibles:")
        for i, port in enumerate(output_ports):
            print(f"  {i}: {port}")
        
        # Suggestions pour Magicstomp
        magicstomp_suggestions = []
        for i, port in enumerate(output_ports):
            if 'magicstomp' in port.lower():
                magicstomp_suggestions.append((i, port))
            elif 'yamaha' in port.lower() and 'ag03' not in port.lower():
                magicstomp_suggestions.append((i, port))
        
        if magicstomp_suggestions:
            print("\n💡 Suggestions pour Magicstomp:")
            for i, port in magicstomp_suggestions:
                print(f"  → {i}: {port}")
        
        try:
            choice = input(f"\nSélectionnez un port (0-{len(output_ports)-1}) ou 'q' pour quitter: ")
            if choice.lower() == 'q':
                return None
            
            port_index = int(choice)
            if 0 <= port_index < len(output_ports):
                selected_port = output_ports[port_index]
                print(f"✅ Port sélectionné: {selected_port}")
                return selected_port
            else:
                print("❌ Index invalide")
                return None
                
        except (ValueError, KeyboardInterrupt):
            print("❌ Sélection annulée")
            return None
    
    def calculate_checksum(self, data: List[int]) -> int:
        """Proxy vers :func:`magicstomp_sysex.calculate_checksum`."""

        return calculate_checksum(data)

    def create_parameter_message(
        self,
        offset: int,
        values: List[int],
        *,
        section: Optional[int] = None,
    ) -> List[int]:
        """Crée un message sysex pour modifier un paramètre.

        Args:
            offset: Position du paramètre dans le patch. Si ``section`` n'est
                pas précisé, ``offset`` est interprété comme un offset global.
                Quand ``section`` vaut ``0`` ou ``1`` il s'agit d'un offset de
                section.
            values: Nouvelles valeurs du paramètre
            section: Forcer la section (0 = common, 1 = effect)

        Returns:
            Message sysex complet
        """

        if section is None:
            global_offset = offset
        elif section == 0:
            global_offset = offset
        elif section == 1:
            global_offset = self.PATCH_COMMON_LENGTH + offset
        else:
            raise ValueError(f"Section invalide: {section}")

        return build_parameter_message(global_offset, values)

    def tweak_parameter(
        self,
        offset: int,
        value: int,
        immediate: bool = False,
        *,
        section: Optional[int] = None,
    ):
        """
        Modifie un paramètre en temps réel.
        
        Args:
            offset: Position du paramètre (0-158)
            value: Nouvelle valeur (0-127)
            immediate: Si True, envoie immédiatement (bypasse la queue)
        """
        if not self.output_port:
            print("❌ Port MIDI non initialisé")
            return
        
        # Vérifie le cache pour éviter les doublons
        if section is None:
            cache_key = offset
        elif section == 0:
            cache_key = offset
        elif section == 1:
            cache_key = self.PATCH_COMMON_LENGTH + offset
        else:
            print(f"❌ Section invalide: {section}")
            return

        with self.cache_lock:
            if cache_key in self.parameter_cache and self.parameter_cache[cache_key] == value:
                return  # Pas de changement
            self.parameter_cache[cache_key] = value

        # Crée le message
        message = self.create_parameter_message(offset, [value], section=section)
        
        if immediate:
            # Envoi immédiat
            self._send_message_immediate(message)
        else:
            # Ajoute à la queue
            self.parameter_queue.put((message, time.time()))
            if not self.running:
                self._start_send_thread()
    
    def tweak_parameter_by_name(self, param_name: str, value: int, immediate: bool = False):
        """
        Modifie un paramètre par son nom.
        
        Args:
            param_name: Nom du paramètre (ex: 'amp_level', 'amp_gain')
            value: Nouvelle valeur
            immediate: Si True, envoie immédiatement
        """
        if param_name in self.COMMON_PARAMS:
            offset = self.COMMON_PARAMS[param_name]
            self.tweak_parameter(offset, value, immediate)
        else:
            print(f"❌ Paramètre inconnu: {param_name}")
            print(f"Paramètres disponibles: {list(self.COMMON_PARAMS.keys())}")
    
    def tweak_multiple_parameters(self, parameters: Dict[int, int], immediate: bool = False):
        """
        Modifie plusieurs paramètres en une fois.

        Args:
            parameters: Dict {offset: value}
            immediate: Si True, envoie immédiatement
        """
        for offset, value in parameters.items():
            self.tweak_parameter(offset, value, immediate)

    def request_patch(self, patch_index: int = 0, timeout: float = 2.0) -> Optional[Dict[str, Any]]:
        """Demande au Magicstomp d'envoyer le patch courant."""

        if not self.output_port:
            self._initialize_midi()

        if not self.output_port:
            print("❌ Aucun port MIDI de sortie disponible pour la requête de patch")
            return None

        if self.input_port is None:
            try:
                self.input_port = mido.open_input(self.midi_port_name)
                print(f"✅ Port MIDI d'entrée ouvert: {self.midi_port_name}")
            except Exception as exc:  # pragma: no cover - dépend du matériel
                print(f"❌ Erreur ouverture port MIDI d'entrée: {exc}")
                return None

        if self.input_port:
            while self.input_port.poll() is not None:
                pass

        request = [0x43, 0x7D, 0x50, 0x55, 0x42, 0x30, 0x01, patch_index & 0x7F]
        try:
            self.output_port.send(mido.Message('sysex', data=request))
            print(f"📥 Requête de dump envoyée pour le patch {patch_index + 1:02d}")
        except Exception as exc:  # pragma: no cover - dépend du matériel
            print(f"❌ Erreur envoi requête de dump: {exc}")
            return None

        start = time.time()
        common_data: Optional[List[int]] = None
        effect_data: Optional[List[int]] = None
        received_index = patch_index

        while time.time() - start < timeout:
            msg = self.input_port.poll() if self.input_port else None
            if msg is None:
                time.sleep(0.01)
                continue

            if msg.type != 'sysex':
                continue

            data = list(msg.data)
            if len(data) < 10 or data[:7] != self.BULK_RESPONSE_HEADER:
                continue

            length = data[8]
            command = data[9]

            if length == 0 and command == 0x30:
                if len(data) >= 12:
                    sub_command = data[10]
                    received_index = data[11]
                    if sub_command == 0x11 and common_data and effect_data:
                        break
                continue

            if command != 0x20 or len(data) < 13:
                continue

            section = data[10]
            section_offset = data[11]
            payload = data[12:12 + length]

            if section == 0x00 and section_offset == 0x00 and length >= self.PATCH_COMMON_LENGTH:
                common_data = payload[: self.PATCH_COMMON_LENGTH]
                print(f"📦 Données 'common' reçues ({len(common_data)} octets)")
            elif section == 0x01 and section_offset == 0x00 and length >= self.PATCH_EFFECT_LENGTH:
                effect_data = payload[: self.PATCH_EFFECT_LENGTH]
                print(f"🎛️ Données d'effet reçues ({len(effect_data)} octets)")

            if common_data and effect_data:
                break

        if not common_data or not effect_data:
            print("❌ Patch incomplet reçu depuis le Magicstomp")
            return None

        return {
            'patch_index': received_index,
            'common': common_data,
            'effect': effect_data,
        }
    
    def _send_message_immediate(self, message: List[int]):
        """Envoie un message immédiatement."""
        try:
            self.output_port.send(mido.Message('sysex', data=message[1:-1]))  # Exclut F0 et F7
            print(f"📤 Paramètre envoyé: {message[8:10]} = {message[10]}")
        except Exception as e:
            print(f"❌ Erreur envoi MIDI: {e}")
    
    def _start_send_thread(self):
        """Démarre le thread d'envoi des messages."""
        if self.running:
            return
        
        self.running = True
        self.send_thread = threading.Thread(target=self._send_worker, daemon=True)
        self.send_thread.start()
        print("🚀 Thread d'envoi temps réel démarré")
    
    def _send_worker(self):
        """Worker thread pour l'envoi des messages."""
        last_send_time = 0
        min_interval = 0.01  # 10ms minimum entre les messages
        
        while self.running:
            try:
                # Récupère le prochain message avec timeout
                message, timestamp = self.parameter_queue.get(timeout=1.0)
                
                # Respecte l'intervalle minimum
                current_time = time.time()
                time_since_last = current_time - last_send_time
                if time_since_last < min_interval:
                    time.sleep(min_interval - time_since_last)
                
                # Envoie le message
                self._send_message_immediate(message)
                last_send_time = time.time()
                
                # Marque la tâche comme terminée
                self.parameter_queue.task_done()
                
            except queue.Empty:
                # Timeout - vérifie si on doit continuer
                continue
            except Exception as e:
                print(f"❌ Erreur dans le worker d'envoi: {e}")
    
    def stop(self):
        """Arrête le système temps réel."""
        self.running = False
        if self.send_thread:
            self.send_thread.join(timeout=1.0)
        
        if self.output_port:
            self.output_port.close()
        if self.input_port:
            self.input_port.close()
        
        print("🛑 Système temps réel arrêté")
    
    def get_parameter_info(self, offset: int) -> Dict[str, Any]:
        """
        Retourne les informations sur un paramètre.
        
        Args:
            offset: Position du paramètre
            
        Returns:
            Dict avec les infos du paramètre
        """
        info = {
            'offset': offset,
            'section': 'common' if offset < self.PATCH_COMMON_LENGTH else 'effect',
            'section_offset': offset if offset < self.PATCH_COMMON_LENGTH else offset - self.PATCH_COMMON_LENGTH
        }
        
        # Trouve le nom du paramètre
        for name, param_offset in self.COMMON_PARAMS.items():
            if param_offset == offset:
                info['name'] = name
                break
        
        return info
    
    def __enter__(self):
        return self
    
    def connect(self):
        """Connect to MIDI ports."""
        if not self.output_port:
            self._initialize_midi()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


# Exemple d'utilisation
if __name__ == "__main__":
    # Test du système temps réel
    with RealtimeMagicstomp() as rt:
        print("🎸 Test du tweaking temps réel Magicstomp")
        
        # Test modification par nom
        print("\n📝 Test modification par nom:")
        rt.tweak_parameter_by_name('amp_level', 64, immediate=True)
        rt.tweak_parameter_by_name('amp_gain', 80, immediate=True)
        
        # Test modification par offset
        print("\n📝 Test modification par offset:")
        rt.tweak_parameter(9, 70, immediate=True)  # amp_level
        rt.tweak_parameter(10, 75, immediate=True)  # amp_gain
        
        # Test modification multiple
        print("\n📝 Test modification multiple:")
        params = {9: 60, 10: 85, 11: 70}  # level, gain, treble
        rt.tweak_multiple_parameters(params, immediate=True)
        
        time.sleep(1)
        print("✅ Tests terminés")
