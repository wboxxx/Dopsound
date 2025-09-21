# Magicstomp Effects Widgets for Dopsound

Ce module fournit une adaptation Python des widgets d'effets du Yamaha Magicstomp, basée sur le code C++/Qt original de [MagicstompFrenzy](https://github.com/dulnikovsky/magicstompfrenzy).

## 🎸 Fonctionnalités

- **Widgets d'effets spécialisés** : Delay, Reverb, Chorus, Flanger, Phaser, Distortion, etc.
- **Mapping automatique** : Conversion des paramètres utilisateur vers le format Magicstomp
- **Interface intuitive** : Contrôles avec labels, unités et validation
- **Extensible** : Architecture modulaire pour ajouter de nouveaux effets
- **Intégration facile** : Compatible avec l'interface Tkinter de Dopsound

## 📁 Structure

```
magicstomp_effects/
├── __init__.py                 # Module principal
├── base_effect_widget.py       # Widget de base
├── delay_widgets.py           # Effets de delay
├── modulation_widgets.py      # Effets de modulation
├── reverb_widgets.py          # Effets de reverb
├── distortion_widgets.py      # Effets de distorsion
├── filter_widgets.py          # Effets de filtre
├── pitch_widgets.py           # Effets de pitch
├── effect_registry.py         # Registre central
├── demo_integration.py        # Démo d'intégration
└── README.md                  # Ce fichier
```

## 🚀 Utilisation

### Installation

Le module est déjà intégré dans votre projet Dopsound. Aucune installation supplémentaire n'est requise.

### Utilisation basique

```python
from magicstomp_effects import EffectRegistry, MonoDelayWidget

# Créer un widget d'effet spécifique
delay_widget = MonoDelayWidget(parent_frame)

# Ou créer dynamiquement basé sur le type d'effet
effect_widget = EffectRegistry.create_effect_widget(0x0D, parent_frame)  # Mono Delay
```

### Intégration avec Dopsound

```python
# Dans votre interface Dopsound existante
from magicstomp_effects import EffectRegistry

class DopsoundGUI:
    def __init__(self):
        # ... votre code existant ...
        self.effect_widget = None
    
    def load_effect(self, effect_type):
        """Charge un effet basé sur son type."""
        self.effect_widget = EffectRegistry.create_effect_widget(
            effect_type, 
            self.effects_frame
        )
        
        # Configuration des callbacks
        if self.effect_widget:
            self.effect_widget.set_parameter_callback(
                "Time", 
                self.on_delay_time_changed
            )
    
    def on_delay_time_changed(self, user_value, magicstomp_value):
        """Gère le changement du temps de delay."""
        # Envoyer vers le Magicstomp
        self.magicstomp_adapter.set_delay_time(magicstomp_value)
```

## 🎛️ Effets Supportés

### Delays
- **Mono Delay** (0x0D) : Delay mono avec feedback et filtres
- **Stereo Delay** (0x0E) : Delay stéréo avec contrôle L/R indépendant
- **Modulated Delay** (0x0F) : Delay avec modulation LFO
- **Echo** (0x11) : Echo classique

### Modulation
- **Chorus** (0x12) : Chorus avec contrôle de forme d'onde
- **Flanger** (0x13) : Flanger avec feedback
- **Phaser** (0x15) : Phaser multi-étages
- **Tremolo** (0x17) : Tremolo avec différentes formes d'onde

### Reverb
- **Reverb** (0x09) : Reverb avec différents types de salle
- **Gate Reverb** (0x0B) : Reverb avec gate
- **Spring Reverb** (0x22) : Reverb à ressort

### Distortion
- **Digital Distortion** (0x2F) : Distorsion numérique
- **Amp Simulator** (0x08) : Simulateur d'ampli complet

### Filtres
- **Multi Filter** (0x2D) : Filtres multiples
- **Dynamic Filter** (0x1E) : Filtre dynamique
- **3 Band EQ** (0x21) : Égaliseur 3 bandes

### Pitch
- **HQ Pitch** (0x18) : Pitch haute qualité
- **Dual Pitch** (0x19) : Pitch double voix

## 🔧 Architecture Technique

### BaseEffectWidget

Tous les widgets d'effets héritent de `BaseEffectWidget` qui fournit :

- **Mapping des paramètres** : Conversion automatique vers le format Magicstomp
- **Validation des valeurs** : Respect des limites min/max
- **Callbacks** : Gestion des changements de paramètres
- **Conversion d'unités** : Temps (ms), fréquences (Hz), gains (dB)

### Système de Conversion

```python
# Exemples de conversions automatiques
"timeMs"      # Temps en ms → valeur Magicstomp
"freqHz"      # Fréquence Hz → valeur Magicstomp  
"logScale"    # Échelle logarithmique
"scaleAndAdd(0.1, 0.1)"  # value = (magicstomp * 0.1) + 0.1
```

### EffectRegistry

Le registre central permet :

- **Création dynamique** d'effets basée sur le type
- **Mapping type → widget** automatique
- **Noms d'effets** standardisés
- **Vérification de support** des effets

## 🎯 Exemple Complet

```python
import tkinter as tk
from magicstomp_effects import EffectRegistry

root = tk.Tk()

# Créer un effet delay
delay_widget = EffectRegistry.create_effect_widget(0x0D, root)
delay_widget.pack(fill=tk.BOTH, expand=True)

# Configurer les callbacks
def on_time_changed(user_value, magicstomp_value):
    print(f"Delay time: {user_value}ms → Magicstomp: {magicstomp_value}")

delay_widget.set_parameter_callback("Time", on_time_changed)

# Définir des valeurs par défaut
delay_widget.set_parameter("Time", 250.0)  # 250ms
delay_widget.set_parameter("Mix", 50)      # 50%
delay_widget.set_parameter("FB Gain", 30)  # 30%

# Récupérer tous les paramètres
params = delay_widget.get_all_parameters()
print("Current parameters:", params)

root.mainloop()
```

## 🔗 Intégration avec Magicstomp

Les widgets sont conçus pour fonctionner avec votre `MagicstompAdapter` existant :

```python
from adapter_magicstomp import MagicstompAdapter

adapter = MagicstompAdapter()

# Callback pour envoyer vers le Magicstomp
def send_to_magicstomp(param_name, user_value, magicstomp_value):
    if param_name == "Time":
        adapter.set_delay_time(magicstomp_value)
    elif param_name == "Mix":
        adapter.set_delay_mix(magicstomp_value)

effect_widget.set_parameter_callback("Time", send_to_magicstomp)
```

## 📝 Licence

Ce code est basé sur MagicstompFrenzy qui est sous licence GPL-3.0. 
Respectez cette licence si vous distribuez ou modifiez le code.

## 🤝 Contribution

Pour ajouter un nouvel effet :

1. Créez une classe héritant de `BaseEffectWidget`
2. Implémentez `_create_widgets()` avec les paramètres spécifiques
3. Ajoutez l'effet dans `EffectRegistry.EFFECT_WIDGETS`
4. Testez avec `demo_integration.py`

## 🐛 Débogage

Utilisez `demo_integration.py` pour tester les widgets individuellement :

```bash
python magicstomp_effects/demo_integration.py
```

Cette démo permet de :
- Tester tous les effets disponibles
- Voir les conversions de paramètres en temps réel
- Valider le mapping Magicstomp
