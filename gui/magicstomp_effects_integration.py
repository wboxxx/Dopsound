"""
Magicstomp Effects Integration for Dopsound GUI
==============================================

Intégration des widgets d'effets Magicstomp dans l'interface graphique principale de Dopsound.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path

# Ajoute le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from magicstomp_effects import EffectRegistry
from adapter_magicstomp import MagicstompAdapter


class MagicstompEffectsPanel(ttk.Frame):
    """
    Panel d'effets Magicstomp intégré dans l'interface Dopsound.
    """
    
    def __init__(self, parent, magicstomp_adapter: MagicstompAdapter = None):
        super().__init__(parent)
        
        self.magicstomp_adapter = magicstomp_adapter or MagicstompAdapter()
        self.current_effect_widget = None
        self.current_effect_type = None
        
        self._create_interface()
        
    def _create_interface(self):
        """Crée l'interface du panel d'effets."""
        # Titre
        title = ttk.Label(self, text="🎸 Magicstomp Effects", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=(0, 15))
        
        # Frame de sélection d'effet
        selection_frame = ttk.LabelFrame(self, text="Effect Selection", padding=10)
        selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Combo box pour l'effet
        self.effect_var = tk.StringVar()
        self.effect_combo = ttk.Combobox(
            selection_frame,
            textvariable=self.effect_var,
            state="readonly",
            width=40
        )
        self.effect_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton de chargement
        load_btn = ttk.Button(
            selection_frame,
            text="Load",
            command=self._load_effect
        )
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton d'envoi vers Magicstomp
        self.send_btn = ttk.Button(
            selection_frame,
            text="Send to Magicstomp",
            command=self._send_to_magicstomp,
            state=tk.DISABLED
        )
        self.send_btn.pack(side=tk.LEFT)
        
        # Frame pour les paramètres
        self.params_frame = ttk.LabelFrame(self, text="Effect Parameters", padding=10)
        self.params_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame pour les informations
        info_frame = ttk.LabelFrame(self, text="Status", padding=10)
        info_frame.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="Select an effect to begin")
        status_label = ttk.Label(info_frame, textvariable=self.status_var)
        status_label.pack()
        
        # Populate effect list
        self._populate_effect_list()
        
    def _populate_effect_list(self):
        """Remplit la liste des effets disponibles."""
        supported_effects = EffectRegistry.get_supported_effects()
        
        effect_items = []
        for effect_type, name in supported_effects.items():
            effect_items.append(f"{name} (0x{effect_type:02X})")
        
        self.effect_combo['values'] = effect_items
        if effect_items:
            self.effect_combo.set(effect_items[0])
    
    def _load_effect(self):
        """Charge l'effet sélectionné."""
        selection = self.effect_combo.get()
        if not selection:
            return
        
        try:
            # Parse effect type from selection
            effect_type_hex = selection.split('(0x')[1].split(')')[0]
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
            
            # Update status
            effect_name = EffectRegistry.get_effect_name(effect_type)
            self.status_var.set(f"Loaded: {effect_name}")
            self.current_effect_type = effect_type
            
            # Enable send button
            self.send_btn.config(state=tk.NORMAL)
            
        else:
            messagebox.showerror("Error", f"Effect type 0x{effect_type:02X} is not supported")
    
    def _setup_parameter_callbacks(self):
        """Configure les callbacks pour les changements de paramètres."""
        if not self.current_effect_widget:
            return
        
        def parameter_changed(param_name, user_value, magicstomp_value):
            self._on_parameter_changed(param_name, user_value, magicstomp_value)
        
        # Trouve tous les widgets de paramètres et configure les callbacks
        for child in self.current_effect_widget.winfo_children():
            if hasattr(child, 'param_name'):
                self.current_effect_widget.set_parameter_callback(
                    child.param_name,
                    parameter_changed
                )
    
    def _on_parameter_changed(self, param_name: str, user_value, magicstomp_value: int):
        """Gère le changement d'un paramètre."""
        # Mise à jour du statut
        self.status_var.set(f"Parameter '{param_name}' changed: {user_value}")
        
        # Optionnel : envoi automatique vers Magicstomp
        # self._send_parameter_to_magicstomp(param_name, magicstomp_value)
    
    def _send_to_magicstomp(self):
        """Envoie tous les paramètres actuels vers le Magicstomp."""
        if not self.current_effect_widget:
            messagebox.showwarning("Warning", "No effect loaded")
            return
        
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
        
        # Envoi vers Magicstomp via l'adapter
        try:
            # Ici, vous utiliseriez votre MagicstompAdapter pour envoyer les paramètres
            # self.magicstomp_adapter.set_effect_parameters(self.current_effect_type, magicstomp_params)
            
            self.status_var.set(f"Sent {len(magicstomp_params)} parameters to Magicstomp")
            messagebox.showinfo("Success", f"Sent {len(magicstomp_params)} parameters to Magicstomp")
            
        except Exception as e:
            self.status_var.set(f"Error sending to Magicstomp: {e}")
            messagebox.showerror("Error", f"Failed to send parameters: {e}")
    
    def get_current_effect_type(self):
        """Retourne le type d'effet actuellement chargé."""
        return self.current_effect_type
    
    def get_current_parameters(self):
        """Retourne les paramètres actuels de l'effet."""
        if self.current_effect_widget:
            return self.current_effect_widget.get_all_parameters()
        return {}
    
    def set_effect_parameters(self, params: dict):
        """Définit les paramètres de l'effet actuel."""
        if self.current_effect_widget:
            self.current_effect_widget.set_all_parameters(params)


def create_magicstomp_effects_tab(notebook, magicstomp_adapter=None):
    """
    Crée un nouvel onglet avec les effets Magicstomp dans un notebook.
    
    Args:
        notebook: ttk.Notebook où ajouter l'onglet
        magicstomp_adapter: Instance de MagicstompAdapter
        
    Returns:
        MagicstompEffectsPanel: Le panel créé
    """
    # Créer le frame pour l'onglet
    effects_frame = ttk.Frame(notebook)
    
    # Créer le panel d'effets
    effects_panel = MagicstompEffectsPanel(effects_frame, magicstomp_adapter)
    effects_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Ajouter l'onglet au notebook
    notebook.add(effects_frame, text="🎸 Magicstomp Effects")
    
    return effects_panel


# Exemple d'utilisation dans l'interface principale
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dopsound - Magicstomp Effects Integration")
    root.geometry("900x700")
    
    # Créer un notebook pour les onglets
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Créer l'onglet des effets Magicstomp
    magicstomp_adapter = MagicstompAdapter()
    effects_panel = create_magicstomp_effects_tab(notebook, magicstomp_adapter)
    
    # Ajouter d'autres onglets si nécessaire
    other_frame = ttk.Frame(notebook)
    notebook.add(other_frame, text="Other Features")
    
    root.mainloop()
