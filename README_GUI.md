# 🖥️ Magicstomp HIL GUI - Guide d'Utilisation

## 🚀 Lancement du GUI

### Démarrage Standard
```bash
python run_gui.py
```

### Démarrage Grandes Polices (Recommandé)
```bash
python run_gui_large_fonts.py
```

### Démarrage Plein Écran
```bash
python run_gui_fullscreen.py
```

### Démarrage Direct
```bash
python gui/main_window.py
```

### Options de Taille et Polices
- **Standard** : 1200x800, polices normales
- **Large Fonts** : 1600x1000, **polices ÉNORMES** (recommandé)
- **Plein écran** : Taille écran complète, polices géantes

### Tailles de Polices (Large Fonts) - MAXIMUM VISIBILITY
- **Titre principal** : 48px bold (ÉNORME!)
- **En-têtes de section** : 28px bold  
- **Texte info** : 20px
- **Boutons** : 20px-24px bold
- **Graphiques** : 28px titres, 22px labels
- **Étiquettes graphiques** : 18px

## 🎯 Workflow Complet dans le GUI

### **📁 Étape 1: Sélection des Fichiers**

#### **Fichiers Audio**
1. **Target Audio** : Sélectionnez votre fichier audio cible (le son que vous voulez reproduire)
   - Formats supportés : WAV, MP3, FLAC, M4A
   - Durée recommandée : 5-10 secondes pour de meilleures performances

2. **DI Signal** : Sélectionnez votre signal DI (guitare sèche, même extrait)
   - Doit correspondre au même extrait que le target
   - Signal direct de la guitare sans effets

#### **Configuration Audio**
1. **Input Device** : Sélectionnez votre entrée audio (où arrive le retour Magicstomp)
2. **Output Device** : Sélectionnez votre sortie audio (vers la boîte de ré-amp)
3. **Refresh Devices** : Actualisez la liste des périphériques disponibles

### **⚙️ Étape 2: Génération de Patch**

#### **Analyse et Génération**
1. Cliquez sur **"🎵 Analyze Target & Generate Patch"**
2. Sélectionnez le backend :
   - **auto** : Sélection automatique (Essentia si disponible, sinon librosa)
   - **librosa** : Backend Python pur
   - **essentia** : Backend haute performance (si installé)

#### **Affichage du Patch**
Le patch généré s'affiche avec tous les paramètres :
- **AMP** : Modèle, gain, bass, mid, treble, presence, cab
- **BOOSTER** : Type et niveau
- **DELAY** : État et paramètres
- **REVERB** : État et paramètres  
- **MOD** : Type, rate, depth, mix

#### **Actions sur le Patch**
- **📤 Send to Magicstomp** : Envoie le patch au Magicstomp via SysEx
- **💾 Save Patch** : Sauvegarde le patch en fichier JSON

### **🎤 Étape 3: Monitoring Audio**

#### **Calibration Système**
1. Cliquez sur **"🔧 Calibrate System"**
   - Mesure automatique de la latence
   - Calibration du gain
   - Alignement temporel

#### **Visualisation Audio**
- **Target Audio** : Affichage de la forme d'onde du fichier cible
- **Processed Audio** : Affichage du retour Magicstomp (après optimisation)

#### **Contrôles de Monitoring**
- **▶️ Start Monitoring** : Démarre l'enregistrement en temps réel
- **⏹️ Stop Monitoring** : Arrête l'enregistrement

### **🔄 Étape 4: Boucle d'Optimisation**

#### **Configuration d'Optimisation**
- **Max Iterations** : Nombre maximum d'itérations (défaut: 20)
- **Session Name** : Nom pour les fichiers de sortie

#### **Contrôles d'Optimisation**
- **🚀 Start HIL Optimization** : Lance l'optimisation complète
- **⏸️ Pause Optimization** : Met en pause l'optimisation
- **⏹️ Stop Optimization** : Arrête l'optimisation

#### **Affichage des Résultats**
- **Progress Bar** : Progression de l'optimisation
- **Initial Loss** : Loss initial (avant optimisation)
- **Current Loss** : Loss actuel (pendant optimisation)
- **Improvement** : Amélioration obtenue

## 🎛️ Fonctionnalités Avancées

### **Affichage en Temps Réel**
- **Barre de statut** : Informations sur l'état du système
- **Informations backend** : Backend utilisé (librosa/essentia)
- **Métriques de performance** : Latence, gain, loss

### **Gestion des Sessions**
- **Export automatique** : Tous les résultats sont sauvegardés dans `out/`
- **Fichiers générés** :
  - `session_initial.json` : Patch initial
  - `session_optimized.json` : Patch optimisé
  - `session_initial.syx` : SysEx initial
  - `session_optimized.syx` : SysEx optimisé
  - `session_target.wav` : Audio cible
  - `session_di.wav` : Signal DI
  - `session_report.txt` : Rapport d'optimisation

### **Threading et Performance**
- **Interface non-bloquante** : Toutes les opérations longues s'exécutent en arrière-plan
- **Mise à jour temps réel** : Interface mise à jour pendant l'optimisation
- **Gestion d'erreurs** : Messages d'erreur clairs et informatifs

## 🔧 Configuration Requise

### **Hardware**
- **Carte son** avec entrées/sorties séparées
- **Boîte de ré-amp** pour isolation
- **Magicstomp** avec interface MIDI
- **Câbles** : sortie carte son → ré-amp → Magicstomp → entrée carte son

### **Software**
- **Python 3.10+**
- **Dépendances** : matplotlib, sounddevice, tkinter (inclus avec Python)

### **Installation**
```bash
# Installation des dépendances
pip install matplotlib sounddevice

# Lancement du GUI
python run_gui.py
```

## 🎯 Exemples d'Usage

### **Test Rapide (Sans Hardware)**
1. Lancez `python demo_hil.py` pour générer des fichiers de test
2. Dans le GUI, sélectionnez `out/demo_target.wav` comme target
3. Sélectionnez `out/demo_di.wav` comme DI
4. Générez et visualisez le patch

### **Optimisation Complète**
1. Enregistrez votre extrait cible (5-10s)
2. Enregistrez le signal DI correspondant
3. Configurez vos périphériques audio
4. Calibrez le système
5. Lancez l'optimisation HIL complète

### **Workflow Professionnel**
1. **Préparation** : Enregistrements de qualité, setup hardware optimal
2. **Analyse** : Génération de patch initial précis
3. **Calibration** : Mesure précise de la latence et du gain
4. **Optimisation** : Boucle HIL avec monitoring visuel
5. **Export** : Sauvegarde de tous les résultats

## 🐛 Dépannage

### **Problèmes Courants**

#### **"Audio devices must be set"**
- Vérifiez que vos périphériques audio sont connectés
- Cliquez sur "Refresh Devices"
- Sélectionnez les bons périphériques

#### **"No file selected"**
- Utilisez les boutons "Browse Target" et "Browse DI"
- Vérifiez que les fichiers sont dans un format supporté

#### **"Calibration failed"**
- Vérifiez les connexions audio
- Assurez-vous que les périphériques sont disponibles
- Testez avec des dispositifs différents

#### **"Optimization failed"**
- Vérifiez que le système est calibré
- Assurez-vous que le Magicstomp est connecté
- Vérifiez les fichiers audio

### **Logs et Debugging**
- **Console** : Messages détaillés dans la console
- **Status Bar** : État actuel du système
- **Error Dialogs** : Messages d'erreur explicites

## 🎸 Conseils d'Utilisation

### **Pour de Meilleurs Résultats**
1. **Qualité audio** : Utilisez des enregistrements de haute qualité
2. **Durée optimale** : 5-10 secondes d'audio cible
3. **Signal DI propre** : Pas de bruit, gain approprié
4. **Calibration précise** : Système audio stable et calibré
5. **Patience** : L'optimisation peut prendre 5-15 minutes

### **Workflow Recommandé**
1. **Test initial** : Commencez avec la démonstration
2. **Setup hardware** : Configurez votre chaine audio
3. **Enregistrements** : Préparez vos fichiers de qualité
4. **Optimisation** : Lancez le processus HIL complet
5. **Validation** : Écoutez et comparez les résultats

Le GUI Magicstomp HIL transforme l'optimisation de tone matching en processus visuel et intuitif ! 🎚🎸✨
