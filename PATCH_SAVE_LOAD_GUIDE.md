# Sauvegarde et Chargement de Patches - Guide

## 💾 **Nouveaux Boutons Ajoutés**

J'ai ajouté **4 boutons** à côté du bouton "Generate Patch" dans l'onglet Files :

```
[🎯 Generate Patch] [💾 Save Patch] [📂 Load Patch] [📤 Send to Magicstomp]
```

### ✅ **Fonctionnalités**

#### **1. 💾 Save Patch**
- **Sauvegarde** le patch actuel en format JSON
- **Métadonnées complètes** : date, fichiers source, effet, version GUI
- **Nom automatique** : `patch_[nom_fichier].json`
- **Format JSON** lisible et éditable

#### **2. 📂 Load Patch**
- **Charge** un patch depuis un fichier JSON
- **Affiche les métadonnées** : date de création, effet, fichier source
- **Applique automatiquement** les paramètres si un effet est chargé
- **Validation** du format de fichier

#### **3. 📤 Send to Magicstomp**
- **Envoie** le patch directement au Magicstomp
- **Utilise** les paramètres MIDI de l'onglet Settings
- **Conversion SysEx** automatique
- **Debug complet** du processus d'envoi

## 🔧 **Format de Fichier Patch**

### **Structure JSON**
```json
{
  "metadata": {
    "created_date": "2024-01-15 16:12:24",
    "target_file": "C:/Users/Vincent/Downloads/wwry.wav",
    "di_file": null,
    "effect_type": 13,
    "effect_name": "Mono Delay",
    "gui_version": "split_vertical"
  },
  "patch": {
    "meta": {
      "name": "Basic Patch - wwry",
      "created_from": "fallback_analysis",
      "target_file": "C:/Users/Vincent/Downloads/wwry.wav"
    },
    "compressor": {
      "enabled": true,
      "threshold": 0.722,
      "ratio": 2.0,
      "attack": 10.0,
      "release": 100.0,
      "makeup_gain": 3.61
    },
    "eq": {
      "enabled": true,
      "low_gain": 0.0,
      "mid_gain": 2.0,
      "high_gain": 0.0,
      "low_freq": 100.0,
      "mid_freq": 1000.0,
      "high_freq": 5000.0
    },
    "delay": {
      "enabled": true,
      "time": 500,
      "feedback": 0.3,
      "mix": 0.2,
      "low_cut": 100.0,
      "high_cut": 8000.0
    }
  }
}
```

## 🔄 **Workflow Complet**

### **1. Génération de Patch**
```
1. Sélectionnez un fichier target
2. Cliquez "Analyze Target"
3. ✅ Basic patch generated from fallback analysis
4. Le patch est affiché dans l'interface
```

### **2. Sauvegarde de Patch**
```
1. Cliquez "💾 Save Patch"
2. Choisissez l'emplacement et le nom
3. ✅ Patch saved to: patch_wwry.json
4. Le fichier contient toutes les métadonnées
```

### **3. Chargement de Patch**
```
1. Cliquez "📂 Load Patch"
2. Sélectionnez un fichier .json
3. ✅ Patch loaded: patch_wwry.json
4. 📅 Created: 2024-01-15 16:12:24
5. 🎛️ Effect: Mono Delay
6. 🎵 Target: wwry.wav
7. Si un effet est chargé → 🎛️ Parameters applied to current effect
```

### **4. Envoi au Magicstomp**
```
1. Configurez MIDI dans l'onglet Settings
2. Cliquez "📤 Send to Magicstomp"
3. 📤 Sending patch to Magicstomp...
4. ✅ Patch sent to Magicstomp successfully!
```

## 🔍 **Debug Complet**

### **Sauvegarde**
```
🔍 DEBUG: Starting save_patch()
🔍 DEBUG: Saving patch to: C:/Users/Vincent/Desktop/patch_wwry.json
🔍 DEBUG: Patch saved successfully to C:/Users/Vincent/Desktop/patch_wwry.json
```

### **Chargement**
```
🔍 DEBUG: Starting load_patch()
🔍 DEBUG: Loading patch from: C:/Users/Vincent/Desktop/patch_wwry.json
🔍 DEBUG: Loaded patch: {...}
🔍 DEBUG: Metadata: {...}
🔍 DEBUG: Starting convert_patch_to_widget_params()
🔍 DEBUG: Converted widget params: {...}
🔍 DEBUG: Applied parameters to effect: {...}
```

### **Envoi Magicstomp**
```
🔍 DEBUG: Starting send_patch_to_magicstomp()
🔍 DEBUG: Current patch: {...}
🔍 DEBUG: Listing MIDI ports...
🔍 DEBUG: Converting patch to SysEx...
🔍 DEBUG: SysEx data length: 256 bytes
🔍 DEBUG: SysEx header: [240, 43, 112, 0, 1, 0, 0, 0, 0, 0]...
🔍 DEBUG: Sending to MIDI port: Magicstomp MIDI Out
🔍 DEBUG: Patch sent successfully
```

## 📊 **Messages de Status**

### **Succès**
```
✅ Patch saved to: patch_wwry.json
✅ Patch loaded: patch_wwry.json
📅 Created: 2024-01-15 16:12:24
🎛️ Effect: Mono Delay
🎵 Target: wwry.wav
🎛️ Parameters applied to current effect
✅ Patch sent to Magicstomp successfully!
```

### **Erreurs**
```
⚠️ No patch to save
⚠️ No patch to load
⚠️ Invalid patch file format
⚠️ No MIDI output device selected
❌ Error saving patch: [details]
❌ Error loading patch: [details]
❌ Error sending patch: [details]
```

## 🎯 **Avantages**

### ✅ **Persistance Complète**
- **Sauvegarde** de tous les paramètres générés
- **Métadonnées** pour traçabilité complète
- **Rechargement** instantané des patches

### ✅ **Intégration Seamless**
- **Application automatique** aux widgets d'effet
- **Validation** des paramètres
- **Conversion** entre formats

### ✅ **Envoi Direct**
- **Magicstomp** : Envoi direct via MIDI
- **Configuration** via onglet Settings
- **Debug complet** du processus

### ✅ **Workflow Optimisé**
```
Analyse → Génération → Sauvegarde → Rechargement → Envoi
```

## 🚀 **Utilisation Pratique**

### **Scénario 1: Sauvegarde de Patches**
```
1. Analysez plusieurs fichiers target
2. Générez des patches pour chacun
3. Sauvegardez chaque patch avec un nom descriptif
4. Créez une bibliothèque de patches
```

### **Scénario 2: Rechargement Rapide**
```
1. Chargez un patch sauvegardé
2. Les paramètres sont automatiquement appliqués
3. Ajustez si nécessaire
4. Envoyez au Magicstomp
```

### **Scénario 3: Partage de Patches**
```
1. Générez un patch sur un système
2. Sauvegardez le fichier JSON
3. Partagez le fichier
4. Chargez sur un autre système
```

## 🎸 **Résultat Final**

Vous pouvez maintenant :
- ✅ **Générer** des patches intelligents
- ✅ **Sauvegarder** avec métadonnées complètes
- ✅ **Recharger** instantanément
- ✅ **Appliquer** automatiquement aux effets
- ✅ **Envoyer** directement au Magicstomp
- ✅ **Partager** les patches entre systèmes

Le workflow complet d'analyse → génération → sauvegarde → rechargement → envoi est maintenant opérationnel ! 🎸✨
