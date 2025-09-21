"""
Demo Integration
===============

Exemple d'intégration des widgets d'effets Magicstomp avec l'interface Dopsound.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Ajoute le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from magicstomp_effects import (
    EffectRegistry,
    MonoDelayWidget,
    ChorusWidget,
    ReverbWidget,
    DistortionWidget
)
from adapter_magicstomp import MagicstompAdapter


class MagicstompEffectsDemo:
    """Démo d'intégration des widgets d'effets Magicstomp."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Magicstomp Effects Demo - Dopsound Integration")
        self.root.geometry("800x600")
        
        # Adapter Magicstomp
        self.magicstomp_adapter = MagicstompAdapter()
        
        # Widget d'effet actuel
        self.current_effect_widget = None
        
        # Interface
        self._create_interface()
        
    def _create_interface(self):
        """Crée l'interface principale."""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titre
        title = ttk.Label(main_frame, text="🎸 Magicstomp Effects for Dopsound", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Frame de sélection d'effet
        effect_frame = ttk.LabelFrame(main_frame, text="Select Effect", padding=10)
        effect_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Combo box pour sélectionner l'effet
        self.effect_var = tk.StringVar()
        self.effect_combo = ttk.Combobox(
            effect_frame, 
            textvariable=self.effect_var,
            state="readonly",
            width=30
        )
        self.effect_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton pour charger l'effet
        load_button = ttk.Button(
            effect_frame,
            text="Load Effect",
            command=self._load_effect
        )
        load_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton pour envoyer vers Magicstomp
        send_button = ttk.Button(
            effect_frame,
            text="Send to Magicstomp",
            command=self._send_to_magicstomp
        )
        send_button.pack(side=tk.LEFT)
        
        # Populate effect list
        self._populate_effect_list()
        
        # Frame pour les paramètres d'effet
        self.params_frame = ttk.LabelFrame(main_frame, text="Effect Parameters", padding=10)
        self.params_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame pour les informations
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding=10)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, height=4, wrap=tk.WORD)
        self.info_text.pack(fill=tk.X)
        
        # Informations initiales
        self._update_info("Select an effect from the dropdown to start editing parameters.")
        
    def _populate_effect_list(self):
        """Remplit la liste des effets disponibles."""
        supported_effects = EffectRegistry.get_supported_effects()
        
        effect_items = []
        for effect_type, name in supported_effects.items():
            effect_items.append(f"0x{effect_type:02X} - {name}")
        
        self.effect_combo['values'] = effect_items
        if effect_items:
            self.effect_combo.set(effect_items[0])
    
    def _load_effect(self):
        """Charge l'effet sélectionné."""
        selection = self.effect_combo.get()
        if not selection:
            return
        
        # Parse effect type
        try:
            effect_type_hex = selection.split(' - ')[0]
            effect_type = int(effect_type_hex, 16)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid effect selection")
            return
        
        # Clear current effect widget
        if self.current_effect_widget:
            self.current_effect_widget.destroy()
        
        # Create new effect widget
        self.current_effect_widget = EffectRegistry.create_effect_widget(
            effect_type, 
            self.params_frame
        )
        
        if self.current_effect_widget:
            self.current_effect_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Set up parameter callbacks
            self._setup_parameter_callbacks()
            
            # Update info
            effect_name = EffectRegistry.get_effect_name(effect_type)
            self._update_info(f"Loaded effect: {effect_name} (0x{effect_type:02X})\n"
                            f"Adjust parameters and click 'Send to Magicstomp' to apply.")
        else:
            messagebox.showerror("Error", f"Effect type 0x{effect_type:02X} is not supported")
    
    def _setup_parameter_callbacks(self):
        """Configure les callbacks pour les changements de paramètres."""
        if not self.current_effect_widget:
            return
        
        # Callback générique pour tous les paramètres
        def parameter_changed(param_name, user_value, magicstomp_value):
            self._on_parameter_changed(param_name, user_value, magicstomp_value)
        
        # Trouve tous les widgets de paramètres
        for child in self.current_effect_widget.winfo_children():
            if hasattr(child, 'param_name'):
                self.current_effect_widget.set_parameter_callback(
                    child.param_name, 
                    parameter_changed
                )
    
    def _on_parameter_changed(self, param_name: str, user_value, magicstomp_value: int):
        """Gère le changement d'un paramètre."""
        info_text = f"Parameter '{param_name}' changed:\n"
        info_text += f"  User value: {user_value}\n"
        info_text += f"  Magicstomp value: {magicstomp_value}\n"
        self._update_info(info_text)
    
    def _send_to_magicstomp(self):
        """Envoie les paramètres actuels vers le Magicstomp."""
        if not self.current_effect_widget:
            messagebox.showwarning("Warning", "No effect loaded")
            return
        
        # Get all parameters
        params = self.current_effect_widget.get_all_parameters()
        
        if not params:
            messagebox.showwarning("Warning", "No parameters to send")
            return
        
        # Convert to Magicstomp format
        magicstomp_params = {}
        for param_name, value in params.items():
            # Trouve le widget correspondant pour la conversion
            for child in self.current_effect_widget.winfo_children():
                if hasattr(child, 'param_name') and child.param_name == param_name:
                    magicstomp_value = self.current_effect_widget._convert_to_magicstomp(child, value)
                    magicstomp_params[param_name] = magicstomp_value
                    break
        
        # Affiche les paramètres (en réalité, ici on les enverrait au Magicstomp)
        param_text = "Parameters to send to Magicstomp:\n"
        for param_name, value in magicstomp_params.items():
            param_text += f"  {param_name}: {value}\n"
        
        self._update_info(param_text)
        messagebox.showinfo("Parameters", f"Ready to send {len(magicstomp_params)} parameters to Magicstomp")
    
    def _update_info(self, text: str):
        """Met à jour le texte d'information."""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
    
    def run(self):
        """Lance l'application."""
        self.root.mainloop()


if __name__ == "__main__":
    # Test des widgets individuels
    print("Testing Magicstomp Effects Widgets...")
    
    # Test du registre
    print(f"Supported effects: {len(EffectRegistry.get_supported_effects())}")
    for effect_type, name in list(EffectRegistry.get_supported_effects().items())[:5]:
        print(f"  0x{effect_type:02X}: {name}")
    
    # Lance la démo
    app = MagicstompEffectsDemo()
    app.run()
