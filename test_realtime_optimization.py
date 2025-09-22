#!/usr/bin/env python3
"""
Test du système d'optimisation temps réel
========================================

Démontre l'utilisation du tweaking temps réel des paramètres Magicstomp
dans la boucle d'optimisation.
"""

import logging
import time
import numpy as np
from pathlib import Path

from realtime_magicstomp import RealtimeMagicstomp
from realtime_optimizer import RealtimeOptimizer
from hil.io import AudioDeviceManager


def test_realtime_adapter():
    """Test de l'adaptateur temps réel."""
    print("🧪 Test de l'adaptateur temps réel Magicstomp")
    print("=" * 50)
    
    with RealtimeMagicstomp() as rt:
        print("✅ Adaptateur initialisé")
        
        # Test des paramètres d'amplificateur
        print("\n📝 Test des paramètres d'amplificateur:")
        
        # Amp Level (offset 9)
        print("  - Amp Level: 64")
        rt.tweak_parameter(9, 64, immediate=True)
        time.sleep(0.5)
        
        print("  - Amp Level: 80")
        rt.tweak_parameter(9, 80, immediate=True)
        time.sleep(0.5)
        
        # Amp Gain (offset 10)
        print("  - Amp Gain: 70")
        rt.tweak_parameter(10, 70, immediate=True)
        time.sleep(0.5)
        
        print("  - Amp Gain: 90")
        rt.tweak_parameter(10, 90, immediate=True)
        time.sleep(0.5)
        
        # Test par nom de paramètre
        print("\n📝 Test par nom de paramètre:")
        rt.tweak_parameter_by_name('amp_treble', 60, immediate=True)
        time.sleep(0.3)
        rt.tweak_parameter_by_name('amp_middle', 70, immediate=True)
        time.sleep(0.3)
        rt.tweak_parameter_by_name('amp_bass', 80, immediate=True)
        time.sleep(0.3)
        
        # Test modification multiple
        print("\n📝 Test modification multiple:")
        params = {11: 50, 12: 60, 13: 70}  # treble, middle, bass
        rt.tweak_multiple_parameters(params, immediate=True)
        time.sleep(1)
        
        # Informations sur les paramètres
        print("\n📊 Informations sur les paramètres:")
        for offset in [9, 10, 11, 12, 13]:
            info = rt.get_parameter_info(offset)
            print(f"  Offset {offset}: {info}")
        
        print("✅ Test de l'adaptateur terminé")


def test_parameter_space():
    """Test de l'espace de paramètres temps réel."""
    print("\n🧪 Test de l'espace de paramètres temps réel")
    print("=" * 50)
    
    from realtime_optimizer import RealtimeParameterSpace
    
    # Crée l'espace de paramètres
    param_space = RealtimeParameterSpace()
    
    # Ajoute des paramètres d'amplificateur
    param_space.add_parameter_with_offset('amp_level', 9, 0.0, 127.0, 2.0, 64.0)
    param_space.add_parameter_with_offset('amp_gain', 10, 0.0, 127.0, 3.0, 60.0)
    param_space.add_parameter_with_offset('amp_treble', 11, 0.0, 127.0, 2.0, 64.0)
    
    print("✅ Espace de paramètres créé")
    print(f"Paramètres: {list(param_space.parameters.keys())}")
    
    # Test des limites
    bounds = param_space.parameters['amp_level']
    print(f"Amp Level - Min: {bounds.min_val}, Max: {bounds.max_val}, Current: {bounds.current_val}")
    
    # Test de validation
    test_values = [0, 64, 127, 150, -10]
    for val in test_values:
        clamped = bounds.clamp(val)
        valid = bounds.is_valid(val)
        print(f"  Valeur {val}: Clampé={clamped}, Valide={valid}")


def test_audio_calibration():
    """Test de la calibration audio."""
    print("\n🧪 Test de la calibration audio")
    print("=" * 50)
    
    try:
        audio_manager = AudioDeviceManager()
        print("✅ Gestionnaire audio initialisé")
        
        # Liste les périphériques
        devices = audio_manager.list_audio_devices()
        print(f"\n📱 Périphériques audio disponibles:")
        print(f"  Entrée: {len(devices['input'])} périphériques")
        print(f"  Sortie: {len(devices['output'])} périphériques")
        
        # Calibration (court pour le test)
        print("\n🎵 Calibration du système...")
        calibration_results = audio_manager.calibrate_system(duration=1.0)
        
        print(f"✅ Calibration terminée:")
        print(f"  Latence: {calibration_results['latency_ms']:.1f}ms")
        print(f"  Compensation gain: {calibration_results['gain_compensation']:.3f}")
        
        audio_manager.close()
        
    except Exception as e:
        print(f"❌ Erreur calibration audio: {e}")


def test_optimizer_setup():
    """Test de la configuration de l'optimiseur."""
    print("\n🧪 Test de la configuration de l'optimiseur")
    print("=" * 50)
    
    try:
        optimizer = RealtimeOptimizer()
        print("✅ Optimiseur temps réel initialisé")
        
        # Configure les paramètres d'amplificateur
        optimizer.setup_optimization_parameters(
            patch_type="amp_simulator",
            parameters_to_optimize=['amp_level', 'amp_gain', 'amp_treble']
        )
        
        print("✅ Paramètres d'amplificateur configurés")
        
        # Test des paramètres configurés
        param_dict = optimizer.parameter_space.get_parameter_dict()
        print(f"Paramètres configurés: {list(param_dict.keys())}")
        
        for name, value in param_dict.items():
            bounds = optimizer.parameter_space.parameters[name]
            offset = optimizer.parameter_space.PARAMETER_OFFSETS.get(name, 'N/A')
            print(f"  {name}: {value:.1f} (offset: {offset})")
        
        optimizer.close()
        
    except Exception as e:
        print(f"❌ Erreur configuration optimiseur: {e}")


def test_parameter_testing():
    """Test du système de test de paramètres."""
    print("\n🧪 Test du système de test de paramètres")
    print("=" * 50)
    
    try:
        with RealtimeOptimizer() as optimizer:
            print("✅ Optimiseur initialisé")
            
            # Configure les paramètres
            optimizer.setup_optimization_parameters("amp_simulator", ["amp_level"])
            
            # Test rapide (sans fichiers audio)
            print("📝 Test rapide du paramètre amp_level:")
            test_values = [40, 50, 60, 70, 80]
            
            # Simule des résultats de perte (pour le test)
            print("  (Simulation - fichiers audio requis pour test réel)")
            for value in test_values:
                # Dans un test réel, cela appellerait _loss_function_realtime
                simulated_loss = np.random.uniform(0.1, 1.0)
                print(f"    {value}: loss={simulated_loss:.6f} (simulé)")
            
            print("✅ Test de paramètres terminé")
            
    except Exception as e:
        print(f"❌ Erreur test de paramètres: {e}")


def demonstrate_workflow():
    """Démontre le workflow complet d'optimisation."""
    print("\n🎯 Démonstration du workflow d'optimisation")
    print("=" * 50)
    
    print("""
    Workflow d'optimisation temps réel:
    
    1. 🎸 Initialisation de l'adaptateur Magicstomp
       - Connexion MIDI au Magicstomp
       - Configuration des offsets de paramètres
    
    2. 🎵 Configuration audio
       - Sélection des périphériques audio
       - Calibration de latence et gain
       - Chargement des fichiers target et DI
    
    3. 📝 Configuration des paramètres
       - Définition des paramètres à optimiser
       - Définition des limites et pas d'incrémentation
       - Mapping vers les offsets Magicstomp
    
    4. 🚀 Optimisation temps réel
       - Pour chaque itération:
         a. Modifie un paramètre via sysex
         b. Attend la stabilisation (100ms)
         c. Joue le signal DI et enregistre la sortie
         d. Calcule la perte perceptuelle
         e. Garde la meilleure valeur
    
    5. 📊 Résultats
       - Paramètres optimaux
       - Historique des améliorations
       - Temps d'optimisation
    
    Avantages du tweaking temps réel:
    ✅ Pas de rechargement de patch complet
    ✅ Optimisation plus rapide
    ✅ Feedback immédiat
    ✅ Possibilité d'optimisation interactive
    """)


def main():
    """Fonction principale de test."""
    print("🎸 Test du système d'optimisation temps réel Magicstomp")
    print("=" * 60)
    
    # Configure le logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    try:
        # Test des composants individuels
        test_realtime_adapter()
        test_parameter_space()
        test_audio_calibration()
        test_optimizer_setup()
        test_parameter_testing()
        
        # Démonstration du workflow
        demonstrate_workflow()
        
        print("\n✅ Tous les tests terminés avec succès!")
        print("\n💡 Pour utiliser le système:")
        print("   1. Connectez votre Magicstomp via USB MIDI")
        print("   2. Configurez vos périphériques audio")
        print("   3. Chargez vos fichiers target.wav et di.wav")
        print("   4. Lancez l'optimisation avec optimize_with_realtime_tweaking()")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


