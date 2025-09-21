# 🔧 Documentation Technique - Pipeline Magicstomp

## Architecture du Pipeline

### Vue d'ensemble
```
Audio File → analyze2json.py → JSON Patch → adapter_magicstomp.py → SysEx → Magicstomp
```

### Modules principaux

#### 1. `analyze2json.py` - Analyseur audio
- **Classe principale** : `AudioAnalyzer`
- **Responsabilités** :
  - Chargement et normalisation audio (librosa)
  - Extraction de features spectrales
  - Détection d'effets (delay, reverb, modulation, distortion)
  - Mapping vers paramètres d'amplificateur
  - Génération de patch JSON neutre

#### 2. `adapter_magicstomp.py` - Convertisseur SysEx
- **Classe principale** : `MagicstompAdapter`
- **Responsabilités** :
  - Conversion des paramètres JSON vers IDs Magicstomp
  - Génération de messages SysEx
  - Calcul de checksums
  - Envoi vers device ou sauvegarde fichier

#### 3. `cli/analyze2stomp.py` - Interface CLI
- **Classe principale** : `MagicstompCLI`
- **Responsabilités** :
  - Orchestration du pipeline complet
  - Gestion des arguments CLI
  - Interface utilisateur

## Algorithmes de Détection

### Détection Delay
```python
# Auto-corrélation pour trouver des répétitions
autocorr = np.correlate(y, y, mode='full')
peaks, properties = signal.find_peaks(search_window, height=0.3, distance=100)
```

**Heuristique** :
- Recherche de pics dans l'auto-corrélation
- Seuil minimum : 0.3 (configurable)
- Distance minimum : 100 échantillons
- Temps de delay calculé : `(peak_idx + offset) * 1000 / sample_rate`

### Détection Reverb
```python
# Analyse de la queue de réverbération
envelope = np.abs(y)
decay_time_s = last_above / sample_rate

# Densité spectrale haute fréquence
high_freq_ratio = high_freq_energy / total_energy
```

**Heuristique** :
- Décroissance > 0.8s → reverb probable
- Ratio hautes fréquences > 0.1 → coloration reverb
- Classification : ROOM (< 1.5s), PLATE (1.5-2s), HALL (> 2s)

### Détection Modulation
```python
# Filtre passe-bas pour isoler la modulation
mod_envelope = signal.filtfilt(b, a, envelope)

# FFT de la modulation
mod_fft = np.fft.fft(mod_envelope)
mod_spectrum = np.abs(mod_fft[freq_mask])
```

**Heuristique** :
- Bande de fréquence : 0.5-8 Hz
- Force de modulation > 0.1 → effet détecté
- Classification : CHORUS (< 1.5Hz), PHASER (1.5-4Hz), TREMOLO (> 4Hz)

### Détection Distortion
```python
# Analyse du clipping
clipped_samples = np.sum(np.abs(y) > 0.95)
clipping_ratio = clipped_samples / len(y)

# Distorsion harmonique (THD approximatif)
harmonic_energy = sum(harmonics[2:8])
thd_approx = harmonic_energy / fundamental_energy
```

**Heuristique** :
- Clipping > 1% → distortion probable
- THD > 0.1 → saturation harmonique
- Drive level basé sur l'intensité du clipping

## Mapping des Paramètres

### Amplificateurs
```python
# Sélection basée sur les caractéristiques spectrales
if centroid > 3000 and bandwidth > 1500:
    amp_model = "BRIT_TOP_BOOST"  # Bright
elif centroid < 2000 and bandwidth < 1000:
    amp_model = "TWEED_BASSMAN"   # Vintage
else:
    amp_model = "JCM800"          # Équilibré
```

### EQ (Égaliseur)
```python
# Paramètres basés sur le spectre
treble = min(1.0, (centroid - 1000) / 3000)
bass = min(1.0, (1500 - centroid) / 1000)
mid = 0.5 + (bandwidth - 1000) / 2000
```

### Temps et Fréquences
```python
# Mapping logarithmique pour les temps
if time_ms <= 50:
    return int(time_ms * 2.54)  # Linéaire 0-50ms
else:
    return int(127 + (time_ms - 50) * 0.28)  # Log 50-500ms

# Mapping logarithmique pour les fréquences
return int(127 * (math.log10(rate_hz / 0.1) / math.log10(200)))
```

## Format SysEx Magicstomp

### Structure du message
```
F0 43 00 2D 40 PP [128 bytes data] CC F7
│  │  │  │  │  │  │                 │  │
│  │  │  │  │  │  │                 │  └─ SysEx End
│  │  │  │  │  │  │                 └──── Checksum
│  │  │  │  │  │  └────────────────────── Patch Data (128 bytes)
│  │  │  │  │  └───────────────────────── Patch Number
│  │  │  │  └──────────────────────────── Command (0x40 = Write)
│  │  │  └─────────────────────────────── Magicstomp ID
│  │  └────────────────────────────────── Device ID
│  └───────────────────────────────────── Yamaha Manufacturer ID
└──────────────────────────────────────── SysEx Start
```

### Layout des données de patch (128 bytes)
```
Offset  Size  Description
------  ----  -----------
0x00    1     Amp Model
0x01    1     Cab Model  
0x02    1     Gain
0x03    1     Bass
0x04    1     Mid
0x05    1     Treble
0x06    1     Presence
0x07    1     Master
0x08    1     Booster Enabled
0x09    1     Booster Type
0x0A    1     Booster Level
0x0B    1     Delay Enabled
0x0C    1     Delay Type
0x0D    1     Delay Time
0x0E    1     Delay Feedback
0x0F    1     Delay Mix
0x10    1     Delay Tempo Sync
0x11    1     Reverb Enabled
0x12    1     Reverb Type
0x13    1     Reverb Decay
0x14    1     Reverb Mix
0x15    1     Reverb Predelay
0x16    1     Reverb High Cut
0x17    1     Mod Enabled
0x18    1     Mod Type
0x19    1     Mod Rate
0x1A    1     Mod Depth
0x1B    1     Mod Mix
0x1C    1     Mod Tempo Sync
0x1D    95    Reserved/Padding
```

## Configuration et Personnalisation

### Fichier `config.py`
- **Seuils de détection** : Paramètres pour l'analyse d'effets
- **Mappings Magicstomp** : Correspondances nom → ID
- **Paramètres audio** : Sample rate, normalisation, etc.
- **Configuration SysEx** : IDs manufacturer, device, etc.

### Extension des mappings
```python
# Ajouter un nouveau modèle d'amplificateur
AMP_MODELS["NEW_AMP"] = {
    "id": 0x07,
    "description": "Nouvel amplificateur",
    "spectral_centroid_min": 2500
}
```

### Personnalisation des seuils
```python
# Modifier la sensibilité de détection
DETECTION_THRESHOLDS["delay"]["min_peak_height"] = 0.2  # Plus sensible
```

## Optimisations et Performance

### Analyse audio
- **librosa** : Optimisé pour l'analyse musicale
- **Fenêtrage** : 4096 samples (93ms à 44.1kHz)
- **Hop length** : 512 samples (12ms)
- **Normalisation** : RMS à 70% pour éviter la saturation

### Gestion mémoire
- **Chargement** : Audio chargé en entier (optimisé pour fichiers < 10min)
- **Traitement** : Opérations vectorisées NumPy
- **Sortie** : JSON léger (~1KB par patch)

## Debugging et Validation

### Mode verbose
```bash
python cli/analyze2stomp.py audio.wav --verbose
```

### Analyse JSON seulement
```bash
python cli/analyze2stomp.py audio.wav --json-only
```

### Validation SysEx
```python
# Vérifier la structure du message
assert syx_data[0] == 0xF0  # SysEx Start
assert syx_data[-1] == 0xF7  # SysEx End
assert len(syx_data) == 136  # Taille attendue
```

### Tests unitaires
```bash
python example_usage.py  # Test avec signal généré
python test_pipeline.py  # Test pipeline complet
```

## Limitations connues

### Détection d'effets
- **Heuristiques approximatives** : Résultats dépendants du contenu audio
- **Effets complexes** : Distinction difficile entre chorus/phaser
- **Signaux saturés** : Détection moins précise avec forte distortion

### Mappings Magicstomp
- **Documentation limitée** : Basé sur MagicstompFrenzy
- **Variations de firmware** : Peut nécessiter ajustements
- **Paramètres avancés** : Non implémentés (compression, gate, etc.)

### Performance
- **Fichiers longs** : > 10min peuvent être lents
- **Analyse en temps réel** : Non optimisé (batch processing)

## Roadmap Technique

### Court terme
- [ ] Validation sur hardware Magicstomp réel
- [ ] Affinage des mappings SysEx
- [ ] Tests avec différents styles musicaux

### Moyen terme
- [ ] Machine Learning pour améliorer la détection
- [ ] Support de plus d'effets Magicstomp
- [ ] Interface graphique de visualisation

### Long terme
- [ ] Analyse en temps réel
- [ ] Support multi-device (autres multi-effets)
- [ ] Cloud processing pour analyse avancée
