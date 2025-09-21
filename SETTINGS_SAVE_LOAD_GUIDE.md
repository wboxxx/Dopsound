# Sauvegarde et Chargement des Paramètres - Guide

## 💾 **Sauvegarde Automatique des Paramètres**

J'ai ajouté un **système complet de sauvegarde/chargement des paramètres** qui se déclenche automatiquement à la fermeture de l'application.

### ✅ **Fonctionnalités Ajoutées**

#### **1. Sauvegarde Automatique**
- **À la fermeture** : Tous les paramètres sont automatiquement sauvegardés
- **Fichier JSON** : `magicstomp_gui_settings.json` dans le répertoire de l'application
- **Sauvegarde complète** : Audio, MIDI, fichiers, effet, géométrie de fenêtre

#### **2. Chargement Automatique**
- **Au démarrage** : Les paramètres sont automatiquement chargés
- **Restauration complète** : Tous les paramètres sont restaurés
- **Fallback** : Utilise les valeurs par défaut si aucun fichier de paramètres

#### **3. Gestion Manuelle**
- **Bouton Save** : Sauvegarde manuelle dans l'onglet Settings
- **Bouton Load** : Chargement manuel des paramètres
- **Bouton Reset** : Remise à zéro vers les valeurs par défaut

## 📁 **Paramètres Sauvegardés**

### 🎤 **Paramètres Audio**
```json
{
  "audio_input_device": "Focusrite Scarlett 2i2 (ID: 1)",
  "audio_output_device": "Speakers (Realtek High Definition Audio)",
  "sample_rate": 44100,
  "buffer_size": 1024,
  "audio_channels": 2
}
```

### 🎹 **Paramètres MIDI**
```json
{
  "midi_input_device": "Magicstomp MIDI In",
  "midi_output_device": "Magicstomp MIDI Out",
  "midi_channels": [1, 2, 3]
}
```

### 🪟 **Paramètres de Fenêtre**
```json
{
  "window_geometry": "1400x900+100+100"
}
```

### 📁 **Fichiers Récemment Utilisés**
```json
{
  "last_target_file": "C:/Users/Vincent/Desktop/guitar_solo.wav",
  "last_di_file": "C:/Users/Vincent/Desktop/guitar_di.wav"
}
```

### 🎛️ **Effet Actuel**
```json
{
  "last_effect_type": 13
}
```

## 🔧 **Correction des Erreurs**

### ✅ **Erreur Callback Audio Corrigée**
```python
# AVANT (erreur)
def audio_callback(indata, frames, time, status):
    self._last_audio_time = time.time()  # ❌ 'time' est un paramètre, pas le module

# APRÈS (corrigé)
def audio_callback(indata, frames, callback_time, status):
    current_time = time.time()  # ✅ Utilise le module Python time
    self._last_audio_time = current_time
```

### ✅ **Sauvegarde Robuste**
```python
def save_settings(self):
    try:
        settings = {
            'audio_input_device': self.audio_input_var.get() if hasattr(self, 'audio_input_var') else '',
            'sample_rate': int(self.sample_rate_var.get()) if hasattr(self, 'sample_rate_var') else 44100,
            # ... autres paramètres
        }
        
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
            
        self.log_status("✅ Settings saved successfully")
    except Exception as e:
        self.log_status(f"⚠️ Error saving settings: {e}")
```

## 🚀 **Utilisation**

### **Sauvegarde Automatique**
```
1. Configurez vos paramètres audio/MIDI
2. Sélectionnez vos fichiers
3. Chargez un effet
4. Fermez l'application
5. ✅ Tous les paramètres sont automatiquement sauvegardés
```

### **Chargement Automatique**
```
1. Lancez l'application
2. ✅ Tous vos paramètres sont automatiquement restaurés
3. Vos fichiers récents sont mémorisés
4. Votre effet est rechargé
5. Votre configuration audio/MIDI est restaurée
```

### **Gestion Manuelle**
```
⚙️ Settings → 💾 Settings Management:
├── 💾 Save Settings : Sauvegarde manuelle
├── 📂 Load Settings : Chargement manuel
└── 🔄 Reset to Defaults : Remise à zéro
```

## 📊 **Messages de Feedback**

### **Sauvegarde**
```
✅ Settings saved successfully
👋 Application closing - settings saved
```

### **Chargement**
```
✅ Settings loaded successfully
ℹ️ No settings file found - using defaults
```

### **Erreurs**
```
⚠️ Error saving settings: [details]
⚠️ Error loading settings: [details]
```

## 🔄 **Workflow Complet**

### **Premier Lancement**
```
1. Lancez l'application
2. ℹ️ No settings file found - using defaults
3. Configurez vos paramètres audio/MIDI
4. Testez votre configuration
5. Fermez l'application
6. ✅ Settings saved successfully
```

### **Lancements Suivants**
```
1. Lancez l'application
2. ✅ Settings loaded successfully
3. ✅ Tous vos paramètres sont restaurés
4. ✅ Vos fichiers récents sont mémorisés
5. ✅ Votre effet est rechargé
6. ✅ Prêt à utiliser !
```

## 🎯 **Avantages**

### ✅ **Persistance Complète**
- **Audio/MIDI** : Configuration complète sauvegardée
- **Fichiers** : Derniers fichiers utilisés mémorisés
- **Effets** : Dernier effet chargé restauré
- **Interface** : Géométrie de fenêtre préservée

### ✅ **Workflow Optimisé**
- **Pas de reconfiguration** à chaque lancement
- **Reprise immédiate** du travail
- **Configuration une seule fois**

### ✅ **Gestion d'Erreurs Robuste**
- **Fallback automatique** vers les valeurs par défaut
- **Pas de crash** si problème de sauvegarde
- **Messages d'erreur clairs**

### ✅ **Flexibilité**
- **Sauvegarde manuelle** disponible
- **Reset facile** vers les valeurs par défaut
- **Chargement manuel** possible

## 📁 **Fichier de Paramètres**

### **Localisation**
```
magicstomp_gui_settings.json
```

### **Format JSON**
```json
{
  "audio_input_device": "Focusrite Scarlett 2i2 (ID: 1)",
  "audio_output_device": "Speakers (Realtek High Definition Audio)",
  "sample_rate": 44100,
  "buffer_size": 1024,
  "audio_channels": 2,
  "midi_input_device": "Magicstomp MIDI In",
  "midi_output_device": "Magicstomp MIDI Out",
  "midi_channels": [1],
  "window_geometry": "1400x900+100+100",
  "last_target_file": "C:/Users/Vincent/Desktop/guitar_solo.wav",
  "last_di_file": "C:/Users/Vincent/Desktop/guitar_di.wav",
  "last_effect_type": 13
}
```

## 🎸 **Résultat Final**

L'application sauvegarde maintenant **automatiquement** :
- ✅ **Configuration audio/MIDI complète**
- ✅ **Fichiers récemment utilisés**
- ✅ **Effet actuellement chargé**
- ✅ **Géométrie de la fenêtre**
- ✅ **Tous les paramètres de l'interface**

Plus besoin de reconfigurer à chaque lancement ! L'application se souvient de tout et reprend exactement où vous vous êtes arrêté. 🎸✨
