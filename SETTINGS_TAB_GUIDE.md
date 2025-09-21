# Onglet Settings - Guide Complet

## 🎯 Nouvel Onglet Settings Ajouté

J'ai ajouté un **onglet Settings complet** avec toutes les options audio et MIDI nécessaires pour le live DI capture et la communication avec le Magicstomp.

## ⚙️ **Structure de l'Onglet Settings**

### 🎤 **Section Audio Settings**

#### **Audio Input Device**
- **Sélection** : Liste déroulante des périphériques d'entrée audio
- **Refresh** : Bouton pour actualiser la liste des périphériques
- **Format** : "Nom du périphérique (ID: X)"
- **Utilisation** : Pour la capture live DI de votre guitare

#### **Audio Output Device**
- **Sélection** : Liste déroulante des périphériques de sortie audio
- **Utilisation** : Pour la sortie audio du système

#### **Paramètres Audio**
- **Sample Rate** : 22050, 44100, 48000, 88200, 96000 Hz
- **Buffer Size** : 256, 512, 1024, 2048, 4096 samples
- **Channels** : 1, 2, 4, 6, 8 canaux

### 🎹 **Section MIDI Settings**

#### **MIDI Input Device**
- **Sélection** : Liste déroulante des périphériques MIDI d'entrée
- **Refresh** : Bouton pour actualiser la liste des périphériques
- **Utilisation** : Pour recevoir les commandes MIDI du Magicstomp

#### **MIDI Output Device**
- **Sélection** : Liste déroulante des périphériques MIDI de sortie
- **Utilisation** : Pour envoyer les commandes MIDI au Magicstomp

#### **MIDI Channels**
- **Sélection** : Cases à cocher pour les canaux 1-16
- **Par défaut** : Canal 1 sélectionné
- **Multi-canal** : Possibilité de sélectionner plusieurs canaux
- **Utilisation** : Canaux MIDI pour la communication avec le Magicstomp

### 🎧 **Section Test Audio**
- **Test Button** : "🎵 Test Audio Setup"
- **Test Tone** : Génère un ton de 440Hz pendant 1 seconde
- **Status Display** : Affiche le statut du test
- **Utilisation** : Vérifier que votre configuration audio fonctionne

## 🔧 **Fonctionnalités Techniques**

### 📱 **Détection Automatique des Périphériques**

#### **Audio Devices**
```python
import sounddevice as sd

devices = sd.query_devices()
for i, device in enumerate(devices):
    device_name = f"{device['name']} (ID: {i})"
    if device['max_input_channels'] > 0:
        input_devices.append(device_name)
    if device['max_output_channels'] > 0:
        output_devices.append(device_name)
```

#### **MIDI Devices**
```python
import mido

input_names = mido.get_input_names()
output_names = mido.get_output_names()
```

### 🎤 **Live DI Capture Intégré**

#### **Configuration Audio**
```python
def start_live_di_capture(self):
    # Get audio settings from Settings tab
    sample_rate = int(self.sample_rate_var.get())
    buffer_size = int(self.buffer_size_var.get())
    channels = int(self.audio_channels_var.get())
    input_device = self.audio_input_var.get()
    
    # Start audio stream with configured settings
    self.start_audio_capture(sample_rate, buffer_size, channels)
```

#### **Stream Audio Réel**
```python
def start_audio_capture(self, sample_rate, buffer_size, channels):
    self.live_di_stream = sd.InputStream(
        samplerate=sample_rate,
        blocksize=buffer_size,
        channels=channels,
        callback=audio_callback,
        dtype='float32'
    )
    self.live_di_stream.start()
```

### 🎹 **Gestion MIDI**

#### **Sélection Multi-Canal**
```python
def update_midi_channels(self, channel):
    self.midi_channels = []
    for ch, var in self.midi_channel_vars.items():
        if var.get():
            self.midi_channels.append(ch)
```

## 🚀 **Workflow avec Settings**

### **1. Configuration Initiale**
```
1. ⚙️ Settings → Refresh Audio Devices
2. ⚙️ Settings → Select Audio Input (votre interface audio)
3. ⚙️ Settings → Select Audio Output (vos haut-parleurs/casque)
4. ⚙️ Settings → Configure Sample Rate (44100 Hz recommandé)
5. ⚙️ Settings → Configure Buffer Size (1024 recommandé)
6. ⚙️ Settings → Test Audio Setup
```

### **2. Configuration MIDI (si connecté au Magicstomp)**
```
1. ⚙️ Settings → Refresh MIDI Devices
2. ⚙️ Settings → Select MIDI Input (Magicstomp)
3. ⚙️ Settings → Select MIDI Output (Magicstomp)
4. ⚙️ Settings → Select MIDI Channels (1 par défaut)
```

### **3. Live DI Capture**
```
1. ⚙️ Settings → Configuration terminée
2. 📁 Files → Select Target Audio
3. 📁 Files → 🎤 Live DI Capture
4. 🎸 Jouer votre guitare (signal capturé avec les paramètres configurés)
```

## 📊 **Messages de Feedback**

### **Détection des Périphériques**
```
🔄 Found 3 input, 2 output audio devices
🔄 Found 1 MIDI input, 1 MIDI output devices
```

### **Configuration Audio**
```
🎤 Audio settings: 44100Hz, 1024 samples, 2 channels
🎤 Input device: Focusrite Scarlett 2i2 (ID: 1)
✅ Audio stream started successfully
```

### **Test Audio**
```
🎵 Testing audio setup...
Playing test tone...
✅ Audio test completed
```

### **MIDI Channels**
```
🎹 MIDI channels updated: [1, 2, 3]
```

## 🔧 **Gestion des Erreurs**

### **Périphériques Non Disponibles**
```
⚠️ sounddevice not available - using default audio
⚠️ mido not available - using default MIDI
```

### **Erreurs de Configuration**
```
⚠️ Please select an audio input device in Settings
❌ Error starting audio capture: [details]
❌ Audio test failed: [details]
```

## 🎯 **Cas d'Usage Typiques**

### **🎸 Setup Guitare Simple**
```
Audio Input: Interface audio (Focusrite, Presonus, etc.)
Audio Output: Casque ou moniteurs
Sample Rate: 44100 Hz
Buffer Size: 1024 samples
Channels: 2 (stéréo)
MIDI: Non configuré (pas de Magicstomp)
```

### **🎛️ Setup Magicstomp Complet**
```
Audio Input: Interface audio
Audio Output: Magicstomp → Ampli/Casque
Sample Rate: 44100 Hz
Buffer Size: 512 samples (latence réduite)
Channels: 2
MIDI Input: Magicstomp
MIDI Output: Magicstomp
MIDI Channels: 1 (ou multiple selon setup)
```

### **🎚️ Setup Professionnel**
```
Audio Input: Interface audio haute qualité
Audio Output: Moniteurs de studio
Sample Rate: 48000 Hz ou 96000 Hz
Buffer Size: 256 samples (latence minimale)
Channels: 2
MIDI: Configuration complète avec multiple canaux
```

## 📱 **Interface Utilisateur**

### **Layout de l'Onglet Settings**
```
⚙️ Settings
├── 🎤 Audio Settings
│   ├── Input Device: [Dropdown + Refresh]
│   ├── Output Device: [Dropdown]
│   ├── Sample Rate: [Dropdown]
│   ├── Buffer Size: [Dropdown]
│   └── Channels: [Dropdown]
├── 🎹 MIDI Settings
│   ├── MIDI Input: [Dropdown + Refresh]
│   ├── MIDI Output: [Dropdown]
│   └── MIDI Channels: [Checkboxes 1-16]
└── 🎧 Test Audio
    ├── Test Button
    └── Status Display
```

### **Intégration avec Live DI**
- **Settings** : Configuration des paramètres audio/MIDI
- **Files** : Utilisation des paramètres pour le live DI capture
- **Status Panel** : Feedback en temps réel de la configuration

## 🎸 **Avantages**

### ✅ **Configuration Complète**
- **Audio** : Tous les paramètres nécessaires
- **MIDI** : Support complet pour Magicstomp
- **Test** : Vérification de la configuration

### ✅ **Intégration Parfaite**
- **Live DI** : Utilise automatiquement les paramètres configurés
- **Status** : Feedback en temps réel
- **Workflow** : Configuration une seule fois

### ✅ **Flexibilité**
- **Multi-périphériques** : Support de tous les périphériques audio/MIDI
- **Multi-canaux** : Support des canaux MIDI multiples
- **Paramètres** : Tous les paramètres audio configurables

## 🎯 **Résultat Final**

L'onglet Settings vous donne maintenant :
- ✅ **Configuration audio complète** pour le live DI capture
- ✅ **Configuration MIDI complète** pour le Magicstomp
- ✅ **Test de configuration** intégré
- ✅ **Détection automatique** des périphériques
- ✅ **Intégration parfaite** avec le live DI capture
- ✅ **Interface intuitive** et organisée

Plus besoin de configuration externe - tout est intégré dans l'interface ! 🎸✨
