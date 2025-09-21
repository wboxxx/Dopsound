# 🎸 Assistant Audio → Magicstomp Patch

Pipeline complet pour analyser des fichiers audio de guitare et générer automatiquement des patches compatibles avec le **Magicstomp de Yamaha**.

## 🚀 Fonctionnalités

### Analyse audio dual backend
- **Backend Essentia** : Haute performance, analyse C++ optimisée
- **Backend Librosa** : Pure Python, installation simple
- **Sélection runtime** : CLI, variable d'environnement, ou auto-détection
- **Fallback automatique** : Graceful degradation si backend préféré indisponible

### Hardware-in-the-Loop (HIL) Tone Matching
- **Optimisation automatique** via Magicstomp réel
- **Calibration audio** : latence + gain automatiques
- **Loss perceptuel** : log-mel + MFCC pour comparaison authentique
- **Coordinate search** : optimisation paramètre par paramètre
- **Export complet** : JSON + SYX + WAV + rapport

### Détection et mapping classiques
- **Détection automatique des effets** : delay, reverb, chorus, phaser, distortion avec heuristiques explicites
- **Mapping intelligent** : Conversion des caractéristiques audio vers paramètres Magicstomp
- **Export flexible** : JSON neutre + SysEx Magicstomp + envoi direct USB-MIDI
- **Interface CLI complète** : Pipeline automatisé avec sélection de backend

## 📋 Prérequis

- **Python 3.10+**
- **Magicstomp Yamaha** (ou émulateur)
- **Interface USB-MIDI** (pour envoi direct)

## 🛠️ Installation

### Installation minimale (librosa uniquement)

```bash
# Clone le repository
git clone <repository-url>
cd Dopsound

# Installation de base avec librosa
pip install librosa mido pedalboard soundfile numpy scipy click
```

### Installation complète (avec Essentia)

```bash
# Dépendances de base
pip install librosa mido pedalboard soundfile numpy scipy click

# Essentia (optionnel, pour de meilleures performances)
# Option 1: Via pip (si wheels disponibles)
pip install essentia

# Option 2: Via conda (recommandé)
conda install -c conda-forge essentia

# Option 3: Build from source (Linux/macOS)
# Voir: https://essentia.upf.edu/installing.html
```

### Vérification des backends

```bash
# Vérifier les backends disponibles
python auto_tone_match_magicstomp.py --list-backends
```

### Dépendances principales

- **librosa** : Analyse audio pure Python (toujours disponible)
- **essentia** : Analyse audio C++ optimisée (optionnel, plus rapide)
- **mido** : Communication MIDI et SysEx
- **numpy/scipy** : Calculs scientifiques
- **soundfile** : Lecture/écriture fichiers audio
- **pedalboard** : Traitement audio (optionnel)
- **click** : Interface CLI avancée

## 🎯 Usage

### Nouveau pipeline dual backend (recommandé)

```bash
# Auto-sélection backend (Essentia si disponible, sinon librosa)
python auto_tone_match_magicstomp.py guitar.wav

# Force Essentia backend (plus rapide)
python auto_tone_match_magicstomp.py guitar.wav --backend essentia

# Force librosa backend (pure Python)
python auto_tone_match_magicstomp.py guitar.wav --backend librosa

# Avec envoi direct vers Magicstomp
python auto_tone_match_magicstomp.py guitar.wav --backend auto --send

# Mode verbeux avec backend spécifique
python auto_tone_match_magicstomp.py guitar.wav --backend essentia --verbose
```

### Hardware-in-the-Loop (HIL) Tone Matching

```bash
# Pipeline HIL complet (optimisation automatique)
python cli/auto_match_hil.py target.wav --di-signal dry.wav \
    --calibrate --optimize --send-patch --max-iterations 15

# Calibration système seulement
python cli/auto_match_hil.py --calibrate \
    --in-device "Focusrite" --out-device "Focusrite"

# Envoi patch seulement
python cli/auto_match_hil.py target.wav --di-signal dry.wav \
    --send-patch --patch-number 5

# Liste des dispositifs audio
python cli/auto_match_hil.py --list-devices

# Démonstration (sans hardware)
python demo_hil.py
```

### Sélection de backend

```bash
# Variables d'environnement
export AUDIO_BACKEND=essentia  # Force Essentia
export AUDIO_BACKEND=librosa   # Force librosa
export AUDIO_BACKEND=auto      # Auto-sélection (défaut)

# Vérifier les backends disponibles
python auto_tone_match_magicstomp.py --list-backends
```

### Génération de fichiers

```bash
# Génère JSON + SysEx avec backend auto
python auto_tone_match_magicstomp.py guitar.wav --output patch.json --syx patch.syx

# Patch personnalisé sur slot 5
python auto_tone_match_magicstomp.py guitar.wav --syx patch.syx --patch 5
```

### Pipeline legacy (compatible)

```bash
# Interface CLI originale (utilise librosa)
python cli/analyze2stomp.py guitar.wav --send

# Modules individuels
python analyze2json.py guitar.wav --output patch.json
python adapter_magicstomp.py patch.json --output patch.syx
```

## 📊 Format JSON

Le pipeline génère un JSON neutre avec cette structure :

```json
{
  "amp": {
    "model": "BRIT_TOP_BOOST",
    "gain": 0.4,
    "bass": 0.5,
    "mid": 0.5,
    "treble": 0.75,
    "presence": 0.7,
    "cab": "2x12_ALNICO"
  },
  "booster": {
    "type": "TREBLE",
    "level": 0.55
  },
  "delay": {
    "enabled": true,
    "time_ms": 370,
    "feedback": 0.3,
    "mix": 0.2
  },
  "reverb": {
    "enabled": true,
    "type": "PLATE",
    "decay_s": 1.5,
    "mix": 0.15
  },
  "mod": {
    "enabled": true,
    "type": "CHORUS",
    "rate_hz": 0.8,
    "depth": 0.35,
    "mix": 0.18
  },
  "meta": {
    "backend": "essentia",
    "analysis_version": "2.0",
    "features": {
      "spectral_tilt_db": 3.2,
      "spectral_centroid_mean": 2450.5,
      "thd_proxy": 0.15,
      "onset_delay_ms": [370.0, 0.3],
      "reverb_estimate": [1.5, 0.15],
      "lfo_rate_hz": [0.8, 0.35],
      "tempo_bpm": 120.0
    }
  }
}
```

## 🔍 Heuristiques d'analyse

### Détection Delay
- **Méthode** : Auto-corrélation pour trouver des répétitions périodiques
- **Seuils** : Pic > 0.3, distance minimum 100 échantillons
- **Log** : `"delay détecté via autocorr pic à 370 ms"`

### Détection Reverb
- **Méthode** : Analyse de la queue de réverbération + densité spectrale haute fréquence
- **Seuils** : Décroissance > 0.8s, ratio hautes fréquences > 0.1
- **Types** : ROOM (< 1.5s), PLATE (1.5-2s), HALL (> 2s)

### Détection Modulation
- **Méthode** : FFT de l'enveloppe pour isoler la modulation
- **Bande** : 0.5-8 Hz (modulation typique)
- **Types** : CHORUS (< 1.5Hz), PHASER (1.5-4Hz), TREMOLO (> 4Hz)

### Détection Distortion
- **Méthode** : Analyse du clipping + distorsion harmonique (THD approximatif)
- **Seuils** : Clipping > 1%, THD > 0.1
- **Mapping** : Drive level basé sur l'intensité du clipping

## 🎛️ Mapping Magicstomp

### Amplificateurs supportés
- `BRIT_TOP_BOOST` : Bright, clair (centroid > 3kHz)
- `TWEED_BASSMAN` : Chaleureux, vintage (centroid < 2kHz)
- `JCM800` : Équilibré, rock (par défaut)

### Effets supportés
- **Delay** : Temps logarithmique (0-50ms → 0-127, 50-500ms → 127-255)
- **Reverb** : Types ROOM/PLATE/HALL, decay normalisé sur 3s max
- **Modulation** : Rate logarithmique (0.1-20Hz → 0-127)

## 🔌 Configuration MIDI

### Ports disponibles

```bash
# Lister les ports MIDI
python cli/analyze2stomp.py --list-ports
```

### Envoi vers device

```bash
# Envoi automatique (détecte le port Magicstomp)
python cli/analyze2stomp.py guitar.wav --send

# Port personnalisé (si nécessaire)
# Modifier adapter_magicstomp.py pour spécifier le port
```

## 📁 Structure du projet

```
Dopsound/
├── auto_tone_match_magicstomp.py  # 🆕 Pipeline dual backend principal
├── analyzers/                     # 🆕 Backends d'analyse audio
│   ├── base.py                   # Interface abstraite
│   ├── librosa_backend.py        # Backend librosa (pure Python)
│   ├── essentia_backend.py       # Backend essentia (C++ optimisé)
│   └── factory.py                # Factory avec sélection runtime
├── hil/                          # 🆕 Hardware-in-the-Loop
│   ├── io.py                     # I/O audio temps réel + calibration
│   └── __init__.py
├── optimize/                     # 🆕 Optimisation HIL
│   ├── loss.py                   # Loss perceptuel (log-mel + MFCC)
│   ├── search.py                 # Coordinate/Grid search
│   ├── constraints.py            # Contraintes paramètres
│   └── __init__.py
├── cli/
│   ├── analyze2stomp.py         # Interface CLI legacy
│   └── auto_match_hil.py        # 🆕 Orchestration HIL complète
├── analyze2json.py              # Pipeline legacy (librosa)
├── adapter_magicstomp.py        # JSON → SysEx Magicstomp
├── tests/                        # 🆕 Tests des backends
├── out/                          # 🆕 Sorties HIL (patches, WAV, rapports)
├── demo_hil.py                   # 🆕 Démonstration HIL (sans hardware)
├── demo_dual_backend.py          # 🆕 Démonstration système dual backend
├── requirements.txt             # Dépendances Python
├── README.md                   # Documentation principale
└── README_HIL.md               # 🆕 Documentation HIL détaillée
```

## 🐛 Debugging

### Mode verbose avec backend spécifique

```bash
# Pipeline dual backend avec logs détaillés
python auto_tone_match_magicstomp.py guitar.wav --backend essentia --verbose

# Vérifier les backends disponibles
python auto_tone_match_magicstomp.py --list-backends
```

### Analyse JSON seulement

```bash
# Pipeline dual backend (JSON auto-généré)
python auto_tone_match_magicstomp.py guitar.wav --output patch.json --verbose

# Pipeline legacy
python cli/analyze2stomp.py guitar.wav --json-only --verbose
```

### Vérification SysEx

```bash
# Génération SysEx avec backend auto
python auto_tone_match_magicstomp.py guitar.wav --syx patch.syx --verbose

# Conversion directe
python adapter_magicstomp.py patch.json --output patch.syx
```

## ⚠️ Limitations connues

- **Backend Essentia** : Installation complexe sur certains systèmes, fallback automatique vers librosa
- **Mappings Magicstomp** : Basés sur MagicstompFrenzy, peuvent nécessiter ajustements
- **Détection d'effets** : Heuristiques approximatives, résultats dépendants du contenu audio
- **Confiance** : Scores indicatifs, toujours valider manuellement
- **Formats audio** : Optimisé pour WAV/MP3, autres formats non testés
- **Performance** : Essentia ~2x plus rapide que librosa, mais installation plus complexe

## 🔮 Roadmap

- [ ] **Étape 4** : Boucle A/B avec `pedalboard` pour auto-tuning
- [ ] **Mappings étendus** : Support de plus d'effets Magicstomp
- [ ] **Machine Learning** : Amélioration des heuristiques par apprentissage
- [ ] **Interface graphique** : GUI pour visualisation des features
- [ ] **Batch processing** : Traitement de plusieurs fichiers

## 🤝 Contribution

1. **Heuristiques** : Améliorer les algorithmes de détection
2. **Mappings** : Affiner les correspondances Magicstomp
3. **Tests** : Valider sur différents styles de guitare
4. **Documentation** : Ajouter des exemples d'usage

## 📜 Licence

Ce projet est fourni à des fins éducatives et de recherche. Respectez les droits d'auteur des fichiers audio analysés.

---

**Note** : Ce pipeline est un prototype. Les résultats peuvent nécessiter des ajustements manuels selon le style musical et les préférences sonores.
