#!/usr/bin/env python3
"""
Real-time Magicstomp Optimizer with Live Parameter Tweaking
===========================================================

Intègre le système de tweaking temps réel dans la boucle d'optimisation
pour permettre des ajustements de paramètres sans recharger le patch complet.

Usage:
    from realtime_optimizer import RealtimeOptimizer
    optimizer = RealtimeOptimizer()
    results = optimizer.optimize_with_realtime_tweaking(target_audio, di_audio)
"""

import numpy as np
import logging
import time
from typing import Dict, Any, List, Tuple, Optional, Callable
from pathlib import Path

from realtime_magicstomp import RealtimeMagicstomp
from optimize.search import CoordinateSearchOptimizer, ParameterSpace, ParameterBounds
from optimize.loss import PerceptualLoss
from hil.io import AudioDeviceManager
from adapter_magicstomp import MagicstompAdapter


class RealtimeParameterSpace(ParameterSpace):
    """
    Parameter space adapté pour le tweaking temps réel.
    
    Étend ParameterSpace avec des mappings vers les offsets Magicstomp
    et des méthodes pour les modifications temps réel.
    """
    
    # Mapping des paramètres vers les offsets Magicstomp
    PARAMETER_OFFSETS = {
        # Paramètres d'amplificateur
        'amp_level': 9,
        'amp_gain': 10, 
        'amp_treble': 11,
        'amp_middle': 12,
        'amp_bass': 13,
        'amp_presence': 14,
        'amp_master': 15,
        
        # Paramètres de delay
        'delay_time': 0x21,  # Offset dans la section effet
        'delay_feedback': 0x22,
        'delay_level': 0x23,
        'delay_hi_damp': 0x24,
        
        # Paramètres de reverb
        'reverb_type': 0x31,
        'reverb_time': 0x32,
        'reverb_level': 0x33,
        'reverb_hi_freq': 0x34,
        'reverb_hi_ratio': 0x35,
        
        # Paramètres de modulation
        'mod_rate': 0x41,
        'mod_depth': 0x42,
        'mod_level': 0x43,
        
        # Paramètres de distorsion
        'dist_drive': 0x51,
        'dist_level': 0x52,
        'dist_tone': 0x53,
    }
    
    def __init__(self):
        super().__init__()
        self.realtime_adapter = None
        
    def set_realtime_adapter(self, adapter: RealtimeMagicstomp):
        """Définit l'adaptateur temps réel."""
        self.realtime_adapter = adapter
    
    def add_parameter_with_offset(self, name: str, offset: int, 
                                min_val: float, max_val: float, 
                                step_size: float, current_val: float):
        """
        Ajoute un paramètre avec son offset Magicstomp.
        
        Args:
            name: Nom du paramètre
            offset: Offset dans le patch Magicstomp
            min_val: Valeur minimale
            max_val: Valeur maximale  
            step_size: Pas d'incrémentation
            current_val: Valeur actuelle
        """
        bounds = ParameterBounds(min_val, max_val, step_size, current_val)
        self.parameters[name] = bounds
        self.PARAMETER_OFFSETS[name] = offset
    
    def set_parameter_value_realtime(self, name: str, value: float) -> bool:
        """
        Modifie un paramètre en temps réel via MIDI.
        
        Args:
            name: Nom du paramètre
            value: Nouvelle valeur
            
        Returns:
            True si la modification a été envoyée
        """
        if name not in self.parameters:
            return False
        
        # Vérifie les limites
        bounds = self.parameters[name]
        clamped_value = bounds.clamp(value)
        
        if not bounds.is_valid(clamped_value):
            return False
        
        # Met à jour la valeur dans l'espace de paramètres
        bounds.current_val = clamped_value
        
        # Envoie la modification temps réel si l'adaptateur est disponible
        if self.realtime_adapter and name in self.PARAMETER_OFFSETS:
            offset = self.PARAMETER_OFFSETS[name]
            midi_value = int(clamped_value * 127 / (bounds.max_val - bounds.min_val))
            self.realtime_adapter.tweak_parameter(offset, midi_value, immediate=True)
            return True
        
        return False


class RealtimeOptimizer:
    """
    Optimiseur avec tweaking temps réel des paramètres Magicstomp.
    
    Combine l'optimisation par recherche de coordonnées avec la modification
    temps réel des paramètres via MIDI sysex.
    """
    
    def __init__(self, 
                 midi_port: Optional[str] = None,
                 sample_rate: int = 44100,
                 buffer_size: int = 1024):
        """
        Initialise l'optimiseur temps réel.
        
        Args:
            midi_port: Port MIDI pour le Magicstomp
            sample_rate: Fréquence d'échantillonnage audio
            buffer_size: Taille du buffer audio
        """
        self.logger = logging.getLogger(__name__)
        
        # Initialise les composants
        self.realtime_adapter = RealtimeMagicstomp(midi_port)
        self.audio_manager = AudioDeviceManager(sample_rate, buffer_size)
        self.parameter_space = RealtimeParameterSpace()
        self.perceptual_loss = PerceptualLoss()
        
        # Connecte l'adaptateur temps réel
        self.parameter_space.set_realtime_adapter(self.realtime_adapter)
        
        # État de l'optimisation
        self.current_patch_data = None
        self.target_audio = None
        self.di_audio = None
        
        self.logger.info("🎸 RealtimeOptimizer initialisé")
    
    def setup_optimization_parameters(self, 
                                    patch_type: str = "amp_simulator",
                                    parameters_to_optimize: List[str] = None):
        """
        Configure les paramètres à optimiser.
        
        Args:
            patch_type: Type de patch Magicstomp
            parameters_to_optimize: Liste des paramètres à optimiser
        """
        if parameters_to_optimize is None:
            parameters_to_optimize = [
                'amp_level', 'amp_gain', 'amp_treble', 'amp_middle', 'amp_bass'
            ]
        
        # Définit les paramètres selon le type de patch
        if patch_type == "amp_simulator":
            self._setup_amp_parameters(parameters_to_optimize)
        elif patch_type == "delay":
            self._setup_delay_parameters(parameters_to_optimize)
        elif patch_type == "reverb":
            self._setup_reverb_parameters(parameters_to_optimize)
        elif patch_type == "distortion":
            self._setup_distortion_parameters(parameters_to_optimize)
        
        self.logger.info(f"📝 Paramètres configurés pour {patch_type}: {parameters_to_optimize}")
    
    def _setup_amp_parameters(self, param_names: List[str]):
        """Configure les paramètres d'amplificateur."""
        param_configs = {
            'amp_level': (0.0, 127.0, 2.0, 64.0),      # min, max, step, current
            'amp_gain': (0.0, 127.0, 3.0, 60.0),
            'amp_treble': (0.0, 127.0, 2.0, 64.0),
            'amp_middle': (0.0, 127.0, 2.0, 64.0),
            'amp_bass': (0.0, 127.0, 2.0, 64.0),
            'amp_presence': (0.0, 127.0, 2.0, 64.0),
            'amp_master': (0.0, 127.0, 2.0, 64.0)
        }
        
        for name in param_names:
            if name in param_configs:
                min_val, max_val, step, current = param_configs[name]
                offset = self.parameter_space.PARAMETER_OFFSETS.get(name, 0)
                self.parameter_space.add_parameter_with_offset(
                    name, offset, min_val, max_val, step, current
                )
    
    def _setup_delay_parameters(self, param_names: List[str]):
        """Configure les paramètres de delay."""
        param_configs = {
            'delay_time': (0.0, 127.0, 5.0, 64.0),
            'delay_feedback': (0.0, 127.0, 3.0, 40.0),
            'delay_level': (0.0, 127.0, 2.0, 50.0),
            'delay_hi_damp': (0.0, 127.0, 2.0, 64.0)
        }
        
        for name in param_names:
            if name in param_configs:
                min_val, max_val, step, current = param_configs[name]
                offset = self.parameter_space.PARAMETER_OFFSETS.get(name, 0)
                self.parameter_space.add_parameter_with_offset(
                    name, offset, min_val, max_val, step, current
                )
    
    def _setup_reverb_parameters(self, param_names: List[str]):
        """Configure les paramètres de reverb."""
        param_configs = {
            'reverb_type': (0.0, 127.0, 1.0, 32.0),
            'reverb_time': (0.0, 127.0, 3.0, 64.0),
            'reverb_level': (0.0, 127.0, 2.0, 50.0),
            'reverb_hi_freq': (0.0, 127.0, 2.0, 64.0),
            'reverb_hi_ratio': (0.0, 127.0, 2.0, 64.0)
        }
        
        for name in param_names:
            if name in param_configs:
                min_val, max_val, step, current = param_configs[name]
                offset = self.parameter_space.PARAMETER_OFFSETS.get(name, 0)
                self.parameter_space.add_parameter_with_offset(
                    name, offset, min_val, max_val, step, current
                )
    
    def _setup_distortion_parameters(self, param_names: List[str]):
        """Configure les paramètres de distorsion."""
        param_configs = {
            'dist_drive': (0.0, 127.0, 3.0, 70.0),
            'dist_level': (0.0, 127.0, 2.0, 60.0),
            'dist_tone': (0.0, 127.0, 2.0, 64.0)
        }
        
        for name in param_names:
            if name in param_configs:
                min_val, max_val, step, current = param_configs[name]
                offset = self.parameter_space.PARAMETER_OFFSETS.get(name, 0)
                self.parameter_space.add_parameter_with_offset(
                    name, offset, min_val, max_val, step, current
                )
    
    def calibrate_audio_system(self, duration: float = 2.0):
        """
        Calibre le système audio pour l'optimisation.
        
        Args:
            duration: Durée de la calibration en secondes
            
        Returns:
            Résultats de la calibration
        """
        self.logger.info("🎵 Calibration du système audio...")
        calibration_results = self.audio_manager.calibrate_system(duration)
        return calibration_results
    
    def load_audio_files(self, target_file: str, di_file: str):
        """
        Charge les fichiers audio pour l'optimisation.
        
        Args:
            target_file: Fichier audio cible
            di_file: Fichier DI (Direct Input)
        """
        self.logger.info(f"📁 Chargement des fichiers audio:")
        self.logger.info(f"  Target: {target_file}")
        self.logger.info(f"  DI: {di_file}")
        
        # Charge le signal cible
        self.target_audio = self.audio_manager.load_di_signal(target_file)
        
        # Charge le signal DI
        self.di_audio = self.audio_manager.load_di_signal(di_file)
        
        self.logger.info(f"✅ Fichiers chargés: {len(self.target_audio)} samples")
    
    def _loss_function_realtime(self, parameters: Dict[str, float]) -> float:
        """
        Fonction de perte avec tweaking temps réel.
        
        Args:
            parameters: Dictionnaire des paramètres
            
        Returns:
            Valeur de la perte
        """
        # Applique les paramètres en temps réel
        for param_name, value in parameters.items():
            self.parameter_space.set_parameter_value_realtime(param_name, value)
        
        # Attend un peu pour que les paramètres se stabilisent
        time.sleep(0.1)
        
        # Joue le signal DI et enregistre la sortie
        processed_audio = self.audio_manager.play_and_record(self.di_audio)
        
        # Calcule la perte perceptuelle
        loss = self.perceptual_loss.compute_loss(self.target_audio, processed_audio)
        
        self.logger.debug(f"Loss: {loss:.6f} pour params: {parameters}")
        return loss
    
    def optimize_with_realtime_tweaking(self,
                                      max_iterations: int = 20,
                                      min_improvement: float = 1e-6) -> Dict[str, Any]:
        """
        Optimise avec tweaking temps réel des paramètres.
        
        Args:
            max_iterations: Nombre maximum d'itérations
            min_improvement: Amélioration minimale pour continuer
            
        Returns:
            Résultats de l'optimisation
        """
        if self.target_audio is None or self.di_audio is None:
            raise ValueError("Fichiers audio non chargés. Utilisez load_audio_files().")
        
        self.logger.info("🚀 Démarrage de l'optimisation temps réel")
        
        # Crée l'optimiseur
        optimizer = CoordinateSearchOptimizer(
            parameter_space=self.parameter_space,
            loss_function=self._loss_function_realtime,
            max_iterations=max_iterations,
            min_improvement=min_improvement
        )
        
        # Démarre l'optimisation
        start_time = time.time()
        results = optimizer.optimize()
        end_time = time.time()
        
        # Ajoute des métadonnées temps réel
        results['realtime_optimization'] = True
        results['optimization_time'] = end_time - start_time
        results['parameters_tweaked'] = list(self.parameter_space.parameters.keys())
        
        self.logger.info(f"✅ Optimisation terminée en {results['optimization_time']:.2f}s")
        self.logger.info(f"📊 Amélioration: {results['improvement']:.6f}")
        
        return results
    
    def quick_parameter_test(self, parameter_name: str, 
                           test_values: List[float]) -> Dict[str, float]:
        """
        Test rapide d'un paramètre avec différentes valeurs.
        
        Args:
            parameter_name: Nom du paramètre à tester
            test_values: Liste des valeurs à tester
            
        Returns:
            Dictionnaire {valeur: loss}
        """
        if parameter_name not in self.parameter_space.parameters:
            raise ValueError(f"Paramètre inconnu: {parameter_name}")
        
        self.logger.info(f"🧪 Test rapide du paramètre {parameter_name}")
        
        results = {}
        current_params = self.parameter_space.get_parameter_dict()
        
        for value in test_values:
            # Modifie le paramètre
            test_params = current_params.copy()
            test_params[parameter_name] = value
            
            # Calcule la perte
            loss = self._loss_function_realtime(test_params)
            results[value] = loss
            
            self.logger.debug(f"  {value}: loss={loss:.6f}")
        
        # Restaure les paramètres originaux
        self.parameter_space.set_parameter_value_realtime(parameter_name, 
                                                         current_params[parameter_name])
        
        return results
    
    def close(self):
        """Ferme les ressources."""
        self.realtime_adapter.stop()
        self.audio_manager.close()
        self.logger.info("🛑 RealtimeOptimizer fermé")


# Exemple d'utilisation
if __name__ == "__main__":
    import logging
    
    # Configure le logging
    logging.basicConfig(level=logging.INFO)
    
    # Test de l'optimiseur temps réel
    with RealtimeOptimizer() as optimizer:
        print("🎸 Test de l'optimiseur temps réel")
        
        # Configure les paramètres d'amplificateur
        optimizer.setup_optimization_parameters("amp_simulator", 
                                               ["amp_level", "amp_gain", "amp_treble"])
        
        # Calibre le système audio
        optimizer.calibrate_audio_system(duration=1.0)
        
        # Charge les fichiers audio (exemples)
        # optimizer.load_audio_files("target.wav", "di.wav")
        
        # Test rapide d'un paramètre
        test_results = optimizer.quick_parameter_test("amp_level", [50, 60, 70, 80])
        print(f"Résultats du test: {test_results}")
        
        # Optimisation complète (nécessite des fichiers audio)
        # results = optimizer.optimize_with_realtime_tweaking(max_iterations=10)
        # print(f"Optimisation terminée: {results}")
        
        print("✅ Test terminé")


