# 🎸 Assistant Audio → Magicstomp Patch

Pipeline complet pour analyser des fichiers audio de guitare et générer automatiquement des patches compatibles avec le **Magicstomp de Yamaha**.

## 🚀 Fonctionnalités

- **Analyse audio intelligente** : Détection automatique des effets (delay, reverb, chorus, phaser, distortion)
- **Mapping intelligent** : Conversion des caractéristiques audio vers paramètres Magicstomp
- **Export flexible** : JSON neutre + SysEx Magicstomp + envoi direct USB-MIDI
- **Heuristiques explicites** : Logs détaillés avec scores de confiance
- **Interface CLI complète** : Pipeline automatisé en une commande

## 📋 Prérequis

- **Python 3.10+**
- **Magicstomp Yamaha** (ou émulateur)
- **Interface USB-MIDI** (pour envoi direct)

## 🛠️ Installation

```bash
# Clone le repository
git clone <repository-url>
cd Dopsound

# Installe les dépendances
pip install -r requirements.txt
```

### Dépendances principales

- `librosa` : Analyse audio et extraction de features
- `mido` : Communication MIDI et SysEx
- `numpy` / `scipy` : Calculs scientifiques
- `pedalboard` : Traitement audio (optionnel, pour boucle A/B future)

## 🎯 Usage

### Pipeline complet (recommandé)

```bash
# Analyse + génération + envoi vers Magicstomp
python cli/analyze2stomp.py guitar.wav --send

# Avec numéro de patch personnalisé
python cli/analyze2stomp.py guitar.wav --send --patch 5
```

### Génération de fichiers

```bash
# Génère JSON + SysEx
python cli/analyze2stomp.py guitar.wav --json patch.json --syx patch.syx

# JSON seulement (pour debugging)
python cli/analyze2stomp.py guitar.wav --json-only --verbose
```

### Modules individuels

```bash
# Analyse audio vers JSON
python analyze2json.py guitar.wav --output patch.json

# Conversion JSON vers SysEx
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
    "global_confidence": 0.75,
    "analysis_version": "1.0",
    "input_file": "guitar.wav"
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
├── analyze2json.py          # Analyse audio → JSON
├── adapter_magicstomp.py    # JSON → SysEx Magicstomp
├── cli/
│   └── analyze2stomp.py     # Interface CLI complète
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

## 🐛 Debugging

### Mode verbose

```bash
python cli/analyze2stomp.py guitar.wav --verbose
```

### Analyse JSON seulement

```bash
python cli/analyze2stomp.py guitar.wav --json-only --verbose
```

### Vérification SysEx

```bash
python adapter_magicstomp.py patch.json --output patch.syx
```

## ⚠️ Limitations connues

- **Mappings Magicstomp** : Basés sur MagicstompFrenzy, peuvent nécessiter ajustements
- **Détection d'effets** : Heuristiques approximatives, résultats dépendants du contenu audio
- **Confiance** : Scores indicatifs, toujours valider manuellement
- **Formats audio** : Optimisé pour WAV/MP3, autres formats non testés

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
