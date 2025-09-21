# Live DI Capture et Auto-Génération de Patch - Guide

## 🎯 Nouvelles Fonctionnalités Ajoutées

### ✅ **1. Live DI Capture**
- **🎤 Live DI Capture** : Capture en temps réel du signal DI de votre guitare
- **Status en temps réel** : Indicateur "Live DI: ON/OFF" toujours visible
- **Alternative au fichier DI** : Plus besoin de fichier DI, capturez directement votre guitare

### ✅ **2. Auto-Génération de Patch Intelligente**
- **🤖 Analyse automatique** : L'analyse du fichier target déclenche automatiquement une proposition de patch
- **Paramètres intelligents** : Génération basée sur l'analyse audio (fréquence, niveau, durée)
- **Adaptation par effet** : Paramètres optimisés selon le type d'effet Magicstomp

## 🎸 **Utilisation du Live DI Capture**

### 📍 **Localisation**
- **Onglet Files** → Section "DI Audio"
- **Bouton** : "🎤 Live DI Capture"

### 🔄 **Workflow Live DI**
```
1. Sélectionner Target Audio (fichier à reproduire)
2. Cliquer "🎤 Live DI Capture"
3. Jouer de la guitare (le signal DI est capturé)
4. Aller à l'onglet Effects pour charger un effet
5. Générer le patch avec le signal live
```

### 📊 **Status Live DI**
- **Live DI: OFF** → Capture inactive
- **Live DI: ON** → Capture active, jouez votre guitare !
- **Files: Target + Live DI** → Prêt pour la génération de patch

## 🤖 **Auto-Génération de Patch Intelligente**

### 🎯 **Déclenchement Automatique**
L'auto-génération se déclenche quand :
1. ✅ **Fichier target analysé** avec succès
2. ✅ **Effet Magicstomp chargé** dans l'onglet Effects
3. ✅ **Analyse complète** du fichier audio

### 📊 **Analyse Intelligente**
L'analyse extrait :
- **Peak Frequency** : Fréquence dominante
- **RMS Level** : Niveau moyen du signal
- **Duration** : Durée du fichier
- **Max Amplitude** : Amplitude maximale

### 🎛️ **Paramètres Intelligents par Effet**

#### **Mono Delay (0x0D)**
```python
# Basé sur la durée et le niveau RMS
delay_time = min(duration * 0.25, 500)  # Quarter note delay
mix = min(50 + int(rms_level * 30), 80)  # Mix basé sur le niveau
fb_gain = min(30 + int(rms_level * 20), 60)  # Feedback basé sur le niveau
```

#### **Chorus (0x12)**
```python
# Basé sur la fréquence dominante
rate = max(0.5, min(peak_freq / 1000, 3.0))  # Rate basé sur la fréquence
depth = min(30 + int(rms_level * 40), 70)  # Depth basé sur le niveau
mix = min(40 + int(rms_level * 25), 65)  # Mix basé sur le niveau
```

#### **Reverb (0x09)**
```python
# Basé sur la durée du fichier
reverb_time = min(duration * 0.5, 3.0)  # Reverb time basé sur la durée
mix = min(40 + int(rms_level * 35), 75)  # Mix basé sur le niveau
high_ratio = min(0.6 + rms_level * 0.3, 1.0)  # High ratio basé sur le niveau
```

#### **Autres Effets (Générique)**
```python
# Ajustement intelligent selon le type de paramètre
if "gain" in param_name.lower():
    value *= (0.8 + rms_level * 0.4)  # Gain basé sur RMS
elif "time" in param_name.lower():
    value *= (0.5 + duration * 0.1)  # Time basé sur durée
elif "rate" in param_name.lower():
    value *= (0.5 + peak_freq / 2000)  # Rate basé sur fréquence
```

## 🚀 **Nouveau Workflow Complet**

### **Option A : Fichier DI**
```
1. 📁 Files → Select Target Audio
2. 📁 Files → Select DI Audio
3. 📁 Files → Analyze Target (auto-génère les paramètres)
4. 🎛️ Effects → Load Effect
5. 📁 Files → Generate Patch
6. 📊 Analysis → Voir l'impact des paramètres
```

### **Option B : Live DI Capture**
```
1. 📁 Files → Select Target Audio
2. 📁 Files → 🎤 Live DI Capture (joue ta guitare !)
3. 📁 Files → Analyze Target (auto-génère les paramètres)
4. 🎛️ Effects → Load Effect
5. 📁 Files → Generate Patch
6. 📊 Analysis → Voir l'impact des paramètres
```

## 📊 **Messages de Feedback**

### ✅ **Live DI Capture**
- `🎤 Starting live DI capture...`
- `✅ Live DI capture started - play your guitar!`
- `⏹️ Live DI capture stopped`

### 🤖 **Auto-Génération de Patch**
- `🤖 Auto-generating patch proposal based on analysis...`
- `🤖 Auto-generated 3 parameters: Time, Mix, FB Gain`
- `💡 Go to Analysis tab to see the parameter impacts!`

### 📊 **Status Panel**
- `Files: Ready (Live DI)` → Prêt avec capture live
- `Files: Target + Live DI` → Target + capture active
- `Live DI: ON` → Capture active
- `Live DI: OFF` → Capture inactive

## 🎯 **Avantages du Live DI Capture**

### 🎸 **Flexibilité**
- **Pas de fichier DI requis** : Jouez directement votre guitare
- **Test en temps réel** : Ajustez et testez instantanément
- **Workflow fluide** : Pas besoin de préparer des fichiers

### 🎛️ **Intégration Parfaite**
- **Même interface** : Utilise la même logique que les fichiers DI
- **Status unifié** : Intégré dans le système de status
- **Génération de patch** : Compatible avec la génération de patch

## 🤖 **Avantages de l'Auto-Génération**

### 🧠 **Intelligence Audio**
- **Analyse spectrale** : Utilise la fréquence dominante
- **Analyse temporelle** : Utilise la durée du fichier
- **Analyse d'amplitude** : Utilise les niveaux RMS et max

### 🎛️ **Adaptation par Effet**
- **Mono Delay** : Paramètres basés sur durée et niveau
- **Chorus** : Paramètres basés sur fréquence et niveau
- **Reverb** : Paramètres basés sur durée et niveau
- **Autres** : Ajustement intelligent selon le type de paramètre

### ⚡ **Workflow Accéléré**
- **Génération automatique** : Plus besoin de deviner les paramètres
- **Base intelligente** : Point de départ optimisé
- **Ajustement facile** : Modifiez ensuite selon vos préférences

## 🔧 **Configuration Technique**

### 🎤 **Live DI Capture**
```python
# Variables d'état
self.is_live_di_capturing = False
self.live_di_stream = None

# Interface
self.live_di_btn = ttk.Button(text="🎤 Live DI Capture")
self.live_di_var = tk.StringVar(value="Live DI: OFF")
```

### 🤖 **Auto-Génération**
```python
# Données d'analyse stockées
self.analysis_data = {
    'target': {
        'duration': duration,
        'sample_rate': sample_rate,
        'peak_frequency': peak_frequency,
        'rms_level': rms_level,
        # ...
    }
}

# Génération intelligente
proposed_params = self.generate_smart_parameters_from_analysis(target_data)
```

## 🎸 **Exemple d'Utilisation**

### **Scénario : Reproduire un son de delay**
```
1. 📁 Files → Select Target: "guitar_with_delay.wav"
2. 📁 Files → 🎤 Live DI Capture → ON
3. 🎸 Jouer votre guitare (signal DI capturé)
4. 📁 Files → 📊 Analyze Target
   → Peak Frequency: 1200 Hz
   → RMS Level: 0.6
   → Duration: 2.5s
5. 🤖 Auto-génération déclenchée :
   → Time: 625ms (basé sur durée)
   → Mix: 68% (basé sur RMS)
   → FB Gain: 42% (basé sur RMS)
6. 🎛️ Effects → Load Effect: Mono Delay
7. 📁 Files → Generate Patch
8. ✅ Patch généré avec paramètres optimisés !
```

## 🎯 **Résultat**

Vous avez maintenant :
- ✅ **Live DI Capture** : Jouez directement votre guitare
- ✅ **Auto-génération intelligente** : Paramètres optimisés automatiquement
- ✅ **Workflow fluide** : Plus besoin de fichiers DI préparés
- ✅ **Feedback en temps réel** : Status toujours visible
- ✅ **Intégration parfaite** : Compatible avec toutes les fonctionnalités existantes

L'interface est maintenant **complètement autonome** et **intelligente** ! 🎸✨
