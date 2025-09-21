# 🎚 Hardware-in-the-Loop (HIL) Tone Matching

## Vue d'ensemble

Le système **Hardware-in-the-Loop (HIL)** permet l'optimisation automatique des paramètres Magicstomp en utilisant le matériel réel. Contrairement aux approches de simulation logicielle, le HIL utilise le Magicstomp physique pour obtenir des résultats authentiques.

## 🎯 Fonctionnalités

### Pipeline HIL Complet
1. **Analyse audio cible** → Génération patch JSON neutre
2. **Mapping JSON** → Paramètres Magicstomp → Envoi SysEx
3. **Ré-amp** signal DI → Magicstomp → Enregistrement retour
4. **Calcul perceptual loss** (log-mel + MFCC) entre cible et retour
5. **Optimisation locale** (coordinate search) via SysEx et ré-enregistrement
6. **Export complet** : patches (JSON + SYX) + WAV (initial/optimisé)

### Audio I/O Temps Réel
- **Sortie carte son** → Boîte de ré-amp → Entrée Magicstomp
- **Sortie Magicstomp** → Entrée carte son
- **Sélection flexible** : `--in-device`, `--out-device`, `--in-ch`, `--out-ch`
- **Modules supportés** : `sounddevice` (recommandé), `pyaudio` (optionnel)

### Calibration Automatique
- **Mesure latence** : Ping/impulsion → calcul round-trip latency
- **Calibration gain** : RMS ratio → compensation niveau (-1 dBFS max)
- **Alignement temporel** : Time-align + level-match automatiques
- **Validation phase** : Mono/stéréo selon configuration

### Optimisation Perceptuelle
- **Loss log-mel** (64 bins, fmax=8kHz) pondérée 0.6
- **Loss MFCC** (20 coefficients) pondérée 0.4
- **Coordinate search** : optimisation paramètre par paramètre
- **Grid search** : recherche exhaustive sur grille fine

## 🏗 Architecture

```
analyzers/          # Analyse audio (dual backend)
├── base.py         # Interface abstraite AudioAnalyzer
├── librosa_backend.py
├── essentia_backend.py
└── factory.py      # Sélection backend runtime

hil/                # Hardware-in-the-Loop
├── io.py          # I/O audio temps réel + calibration
└── __init__.py

optimize/           # Optimisation
├── loss.py        # Loss perceptuel (log-mel + MFCC)
├── search.py      # Coordinate/Grid search
├── constraints.py # Contraintes paramètres
└── __init__.py

cli/
└── auto_match_hil.py  # Orchestration HIL complète

out/               # Sorties générées
├── patch_initial.json
├── patch_opt.json
├── patch_initial.syx
├── patch_opt.syx
├── take_initial.wav
├── take_opt.wav
├── report.txt
└── calibration.json
```

## 🚀 Installation

### Dépendances Core
```bash
pip install sounddevice librosa mido numpy scipy soundfile click
```

### Dépendances Optionnelles
```bash
# Audio I/O alternatif
pip install pyaudio

# Backend haute performance
pip install essentia
# ou
conda install -c conda-forge essentia
```

## 🎛 Utilisation

### 1. Configuration Audio

```bash
# Lister les dispositifs audio
python cli/auto_match_hil.py --list-devices

# Configuration spécifique
python cli/auto_match_hil.py target.wav --di-signal dry.wav \
    --in-device "Focusrite" --out-device "Focusrite" \
    --in-ch 1 --out-ch 1
```

### 2. Calibration Système

```bash
# Calibration automatique
python cli/auto_match_hil.py --calibrate \
    --in-device "Focusrite" --out-device "Focusrite"
```

### 3. Pipeline HIL Complet

```bash
# Analyse + Optimisation + Export
python cli/auto_match_hil.py target.wav --di-signal dry.wav \
    --calibrate --optimize --send-patch \
    --max-iterations 15 --session-name "my_tone"
```

### 4. Opérations Individuelles

```bash
# Envoi patch seulement
python cli/auto_match_hil.py target.wav --di-signal dry.wav \
    --send-patch --patch-number 5

# Optimisation sans calibration
python cli/auto_match_hil.py target.wav --di-signal dry.wav \
    --optimize --optimize-params delay_mix reverb_mix treble
```

## 🔧 Paramètres d'Optimisation

### Paramètres Disponibles
- **Delay** : `mix` (±0.08), `feedback` (±0.10), `time_ms` (±25/±50)
- **Reverb** : `mix` (±0.06), `decay_s` (±0.4)
- **Amp** : `treble` (±0.10), `presence` (±0.10), `gain` (±0.08)
- **Modulation** : `depth` (±0.10), `rate_hz` (±0.2), `mix` (±0.08)

### Contraintes
- **Mix/Depth/Treble/Presence** : [0, 1]
- **Time_ms** : [30, 1500]
- **Feedback** : [0, 0.95] (éviter oscillation)
- **Rate_hz** : [0.1, 10.0]

## 📊 Critères de Loss

### Loss Perceptuel
```python
total_loss = 0.6 * mel_loss + 0.4 * mfcc_loss
```

### Alignement Temporel
- **Cross-correlation** pour alignement automatique
- **Compensation latence** basée sur calibration
- **Fenêtrage** pour comparaison cohérente

### Métriques Additionnelles
- **Spectral centroid loss** : différence centre de masse
- **Spectral rolloff loss** : différence rolloff
- **Zero crossing rate loss** : différence ZCR

## 🎵 Analyse Initiale

### Heuristiques de Génération
- **Treble booster** si tilt(1.5-6kHz) > 3dB & centroid > 2.2kHz
- **Gain** ≈ `1 - spectral_flatness`
- **Delay** via autocorr enveloppe attaque (lag→ms, pic→feedback)
- **Reverb** via ratio Late/Early (0.08-0.6s / 0-0.08s) → mix/decay
- **Mod** via pic FFT 0.2-6Hz sur enveloppe → rate/depth
- **Tempo** optionnel → tag `dotted_8th` si delay ≈ 0.75*beat

## 📁 Format de Sortie

### Fichiers Générés
```
out/my_session/
├── my_session_initial.json     # Patch initial
├── my_session_optimized.json   # Patch optimisé
├── my_session_initial.syx      # SysEx initial
├── my_session_optimized.syx    # SysEx optimisé
├── my_session_target.wav       # Audio cible
├── my_session_di.wav          # Signal DI
├── my_session_report.txt      # Rapport optimisation
└── calibration.json           # Données calibration
```

### Rapport d'Optimisation
```
Hardware-in-the-Loop Optimization Report
==================================================

Session: my_session
Timestamp: 2024-01-15 14:30:25

Iterations: 12
Initial Loss: 4.481285
Final Loss: 2.061038
Improvement: 2.420246

Best Parameters:
  delay_mix: 0.2800
  reverb_mix: 0.5100
  treble: 1.0000
  presence: 1.0000
  gain: 0.6166
```

## 🔬 Démonstration

### Test avec Signaux Synthétiques
```bash
# Démonstration complète (sans hardware)
python demo_hil.py
```

### Résultats Attendus
- **Initial Loss** : ~4.5 (signal brut)
- **Final Loss** : ~2.1 (après optimisation)
- **Improvement** : ~2.4 (réduction 54%)
- **Fichiers** : target.wav, di.wav, processed.wav, patch.json

## ⚠️ Limitations

### Hardware Requis
- **Carte son** avec entrées/sorties séparées
- **Boîte de ré-amp** pour isolation
- **Magicstomp** avec interface MIDI
- **Câbles** : sortie carte son → ré-amp → Magicstomp → entrée carte son

### Performance
- **Latence** : ~50-150ms par itération (hardware + audio)
- **Temps total** : ~5-15 minutes pour 10-20 itérations
- **Stabilité** : dépend de la qualité des connexions

### Précision
- **Calibration** : critique pour résultats cohérents
- **Environnement** : bruit ambiant peut affecter les mesures
- **Hardware** : variations entre unités Magicstomp

## 🐛 Débogage

### Mode Verbose
```bash
python cli/auto_match_hil.py target.wav --di-signal dry.wav \
    --optimize --verbose
```

### Problèmes Courants
1. **Device not found** : Vérifier `--list-devices`
2. **Calibration failed** : Vérifier connexions audio
3. **MIDI timeout** : Vérifier port Magicstomp
4. **Loss not improving** : Ajuster paramètres ou contraintes

### Logs Détaillés
- **Backend selection** : `INFO` level
- **Parameter updates** : `DEBUG` level
- **Loss computation** : `DEBUG` level
- **SysEx communication** : `INFO` level

## 🔮 Extensions Futures

### Améliorations Possibles
- **Multi-objective optimization** : Pareto front
- **Bayesian optimization** : Gaussian processes
- **Real-time monitoring** : Visualisation live
- **Batch processing** : Multiple targets
- **Cloud deployment** : Remote optimization

### Intégrations
- **VST plugins** : Extension aux plugins
- **Other hardware** : Support autres processeurs
- **Machine learning** : Apprentissage automatique
- **Web interface** : Interface graphique

---

## 📞 Support

Pour questions ou problèmes avec le système HIL :
1. Vérifier la calibration audio
2. Tester avec `demo_hil.py`
3. Activer le mode `--verbose`
4. Consulter les logs détaillés

Le système HIL représente l'état de l'art en optimisation de tone matching hardware ! 🎸✨
