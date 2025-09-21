"""
Enhanced Magicstomp Interface with Impact Visualization
=====================================================

Interface complète intégrant les widgets d'effets Magicstomp avec la visualisation d'impact
pour l'analyse de target et la génération de patch.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json

# Ajoute le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from magicstomp_effects import EffectRegistry
from adapter_magicstomp import MagicstompAdapter
from gui.impact_visualization import ImpactVisualizer, ParameterImpact, ImpactLevel


class EnhancedMagicstompInterface:
    """
    Interface complète Magicstomp avec visualisation d'impact.
    """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎸 Dopsound - Enhanced Magicstomp Interface")
        self.root.geometry("1400x900")
        
        # Composants
        self.magicstomp_adapter = MagicstompAdapter()
        self.current_effect_widget = None
        self.current_effect_type = None
        self.impact_visualizer = None
        
        # État des paramètres
        self.original_parameters = {}
        self.target_parameters = {}
        self.current_parameters = {}
        
        self._create_interface()
        
    def _create_interface(self):
        """Crée l'interface principale."""
        # Frame principal avec paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel gauche - Contrôles d'effets
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Panel droit - Visualisation d'impact
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        self._create_effects_panel(left_frame)
        self._create_impact_panel(right_frame)
        
    def _create_effects_panel(self, parent):
        """Crée le panel des effets."""
        # Titre
        title = ttk.Label(parent, text="🎸 Magicstomp Effects", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=(0, 15))
        
        # Frame de sélection d'effet
        selection_frame = ttk.LabelFrame(parent, text="Effect Selection", padding=10)
        selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Combo box pour l'effet
        self.effect_var = tk.StringVar()
        self.effect_combo = ttk.Combobox(
            selection_frame,
            textvariable=self.effect_var,
            state="readonly",
            width=35
        )
        self.effect_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton de chargement
        load_btn = ttk.Button(
            selection_frame,
            text="Load Effect",
            command=self._load_effect
        )
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton de sauvegarde
        save_btn = ttk.Button(
            selection_frame,
            text="Save Patch",
            command=self._save_patch
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton de chargement
        load_patch_btn = ttk.Button(
            selection_frame,
            text="Load Patch",
            command=self._load_patch
        )
        load_patch_btn.pack(side=tk.LEFT)
        
        # Frame pour les paramètres d'effet
        self.params_frame = ttk.LabelFrame(parent, text="Effect Parameters", padding=10)
        self.params_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame pour les contrôles d'analyse
        analysis_frame = ttk.LabelFrame(parent, text="Analysis & Generation", padding=10)
        analysis_frame.pack(fill=tk.X)
        
        # Boutons d'analyse
        analyze_btn = ttk.Button(
            analysis_frame,
            text="📊 Analyze Current",
            command=self._analyze_current_parameters
        )
        analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        generate_btn = ttk.Button(
            analysis_frame,
            text="🎯 Generate Target",
            command=self._generate_target_parameters
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        apply_btn = ttk.Button(
            analysis_frame,
            text="✅ Apply Changes",
            command=self._apply_changes
        )
        apply_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        reset_btn = ttk.Button(
            analysis_frame,
            text="🔄 Reset to Original",
            command=self._reset_to_original
        )
        reset_btn.pack(side=tk.LEFT)
        
        # Populate effect list
        self._populate_effect_list()
        
    def _create_impact_panel(self, parent):
        """Crée le panel de visualisation d'impact."""
        # Créer le visualiseur d'impact
        self.impact_visualizer = ImpactVisualizer(parent)
        
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
            
            # Set effect widget in impact visualizer
            self.impact_visualizer.set_effect_widget(self.current_effect_widget)
            
            # Store current effect type
            self.current_effect_type = effect_type
            
            # Store original parameters
            self.original_parameters = self.current_effect_widget.get_all_parameters()
            
            print(f"Loaded effect: {EffectRegistry.get_effect_name(effect_type)}")
            
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
        # Met à jour les paramètres courants
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        
        # Met à jour la visualisation d'impact si on a des paramètres cibles
        if self.target_parameters:
            self._update_impact_visualization()
    
    def _analyze_current_parameters(self):
        """Analyse les paramètres actuels."""
        if not self.current_effect_widget:
            messagebox.showwarning("Warning", "No effect loaded")
            return
        
        # Récupère les paramètres actuels
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Crée les impacts avec les valeurs actuelles comme cibles
        target_impacts = {}
        for param_name, value in current_params.items():
            impact = ParameterImpact(
                name=param_name,
                original_value=value,  # Utilise la valeur actuelle comme référence
                target_value=value,
                current_value=value,
                impact_level=ImpactLevel.NONE,
                unit=self._get_parameter_unit(param_name)
            )
            target_impacts[param_name] = impact
        
        # Met à jour la visualisation
        self.impact_visualizer.impacts = target_impacts
        self.impact_visualizer._update_visualization()
        
        print(f"Analyzed {len(current_params)} parameters")
    
    def _generate_target_parameters(self):
        """Génère des paramètres cibles (simulation)."""
        if not self.current_effect_widget:
            messagebox.showwarning("Warning", "No effect loaded")
            return
        
        # Simulation de génération de paramètres cibles
        # En réalité, ceci viendrait de votre système d'analyse audio
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Génère des variations aléatoires pour la démo
        import random
        target_params = {}
        
        for param_name, value in current_params.items():
            # Variation de ±20% pour la démo
            variation = random.uniform(-0.2, 0.2)
            target_value = value * (1 + variation)
            
            # Applique des limites selon le type de paramètre
            target_value = self._apply_parameter_limits(param_name, target_value)
            
            target_params[param_name] = target_value
        
        # Définit les paramètres cibles
        self.target_parameters = target_params
        
        # Met à jour la visualisation d'impact
        self._update_impact_visualization()
        
        print(f"Generated target parameters with {len(target_params)} variations")
    
    def _apply_parameter_limits(self, param_name: str, value: float) -> float:
        """Applique les limites appropriées à un paramètre."""
        # Limites basées sur le nom du paramètre
        limits = {
            "Time": (0.1, 2730.0),
            "Mix": (0, 100),
            "Rate": (0.1, 20.0),
            "Depth": (0, 100),
            "Feedback": (0, 99),
            "Gain": (-12, 12),
            "Level": (0, 100),
            "Frequency": (20, 20000),
            "Q": (0.1, 10.0)
        }
        
        min_val, max_val = limits.get(param_name, (0, 100))
        return max(min_val, min(max_val, value))
    
    def _update_impact_visualization(self):
        """Met à jour la visualisation d'impact."""
        if not self.target_parameters or not self.current_effect_widget:
            return
        
        # Récupère les paramètres actuels
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Crée les impacts
        impacts = {}
        for param_name, target_value in self.target_parameters.items():
            original_value = self.original_parameters.get(param_name, 0)
            current_value = current_params.get(param_name, original_value)
            
            # Calcule le niveau d'impact
            impact_level = self._calculate_impact_level(original_value, target_value)
            
            impact = ParameterImpact(
                name=param_name,
                original_value=original_value,
                target_value=target_value,
                current_value=current_value,
                impact_level=impact_level,
                unit=self._get_parameter_unit(param_name)
            )
            
            impacts[param_name] = impact
        
        # Met à jour la visualisation
        self.impact_visualizer.impacts = impacts
        self.impact_visualizer._update_visualization()
    
    def _calculate_impact_level(self, original: float, target: float) -> ImpactLevel:
        """Calcule le niveau d'impact basé sur la différence."""
        if original == 0:
            diff_percent = abs(target) * 100 if target != 0 else 0
        else:
            diff_percent = abs((target - original) / original) * 100
        
        if diff_percent < 5:
            return ImpactLevel.NONE
        elif diff_percent < 15:
            return ImpactLevel.LOW
        elif diff_percent < 30:
            return ImpactLevel.MEDIUM
        elif diff_percent < 50:
            return ImpactLevel.HIGH
        else:
            return ImpactLevel.CRITICAL
    
    def _get_parameter_unit(self, param_name: str) -> str:
        """Retourne l'unité d'un paramètre."""
        units = {
            "Time": "ms",
            "Rate": "Hz", 
            "Mix": "%",
            "Depth": "%",
            "Feedback": "%",
            "Gain": "dB",
            "Level": "%",
            "Frequency": "Hz",
            "Q": "",
            "Attack": "ms",
            "Release": "ms"
        }
        return units.get(param_name, "")
    
    def _apply_changes(self):
        """Applique les changements vers les paramètres cibles."""
        if not self.target_parameters or not self.current_effect_widget:
            messagebox.showwarning("Warning", "No target parameters to apply")
            return
        
        # Applique les paramètres cibles au widget
        self.current_effect_widget.set_all_parameters(self.target_parameters)
        
        # Met à jour les paramètres courants
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        
        # Met à jour la visualisation
        self._update_impact_visualization()
        
        print("Applied target parameters to effect widget")
    
    def _reset_to_original(self):
        """Remet les paramètres à leur valeur originale."""
        if not self.original_parameters or not self.current_effect_widget:
            messagebox.showwarning("Warning", "No original parameters to reset to")
            return
        
        # Remet les paramètres originaux
        self.current_effect_widget.set_all_parameters(self.original_parameters)
        
        # Met à jour les paramètres courants
        self.current_parameters = self.current_effect_widget.get_all_parameters()
        
        # Efface les paramètres cibles
        self.target_parameters.clear()
        
        # Met à jour la visualisation
        self.impact_visualizer._reset_analysis()
        
        print("Reset parameters to original values")
    
    def _save_patch(self):
        """Sauvegarde le patch actuel."""
        if not self.current_effect_widget:
            messagebox.showwarning("Warning", "No effect loaded")
            return
        
        # Demande le nom du fichier
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Magicstomp Patch"
        )
        
        if filename:
            patch_data = {
                "effect_type": self.current_effect_type,
                "effect_name": EffectRegistry.get_effect_name(self.current_effect_type),
                "parameters": self.current_effect_widget.get_all_parameters(),
                "original_parameters": self.original_parameters,
                "target_parameters": self.target_parameters
            }
            
            try:
                with open(filename, 'w') as f:
                    json.dump(patch_data, f, indent=2)
                messagebox.showinfo("Success", f"Patch saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save patch: {e}")
    
    def _load_patch(self):
        """Charge un patch sauvegardé."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Magicstomp Patch"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    patch_data = json.load(f)
                
                # Charge l'effet
                effect_type = patch_data["effect_type"]
                self.effect_var.set(f"{patch_data['effect_name']} (0x{effect_type:02X})")
                self._load_effect()
                
                # Applique les paramètres
                if "parameters" in patch_data:
                    self.current_effect_widget.set_all_parameters(patch_data["parameters"])
                
                if "original_parameters" in patch_data:
                    self.original_parameters = patch_data["original_parameters"]
                
                if "target_parameters" in patch_data:
                    self.target_parameters = patch_data["target_parameters"]
                    self._update_impact_visualization()
                
                messagebox.showinfo("Success", f"Patch loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load patch: {e}")


def main():
    """Fonction principale."""
    root = tk.Tk()
    app = EnhancedMagicstompInterface(root)
    
    # Menu
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # Menu File
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Patch", command=app._save_patch)
    file_menu.add_command(label="Load Patch", command=app._load_patch)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Menu Help
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
        "About", "Enhanced Magicstomp Interface for Dopsound\n\n"
        "Features:\n"
        "• Visual effect parameter editing\n"
        "• Impact analysis and visualization\n"
        "• Target parameter generation\n"
        "• Before/after comparison\n"
        "• Patch save/load functionality"
    ))
    
    root.mainloop()


if __name__ == "__main__":
    main()
