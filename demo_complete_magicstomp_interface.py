#!/usr/bin/env python3
"""
Complete Magicstomp Interface Demo
================================

Démonstration complète de l'interface Magicstomp avec visualisation d'impact
pour l'analyse de target et la génération de patch.

Fonctionnalités démontrées :
- Widgets d'effets Magicstomp spécialisés
- Visualisation d'impact des paramètres
- Analyse de target et génération de patch
- Comparaison avant/après
- Sauvegarde/chargement de patches
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Ajoute le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from magicstomp_effects import EffectRegistry
from adapter_magicstomp import MagicstompAdapter
from gui.impact_visualization import ImpactVisualizer, ParameterImpact, ImpactLevel


class CompleteMagicstompDemo:
    """
    Démonstration complète de l'interface Magicstomp avec toutes les fonctionnalités.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎸 Complete Magicstomp Interface Demo - Dopsound")
        self.root.geometry("1600x1000")
        
        # Composants
        self.magicstomp_adapter = MagicstompAdapter()
        self.current_effect_widget = None
        self.current_effect_type = None
        self.impact_visualizer = None
        
        # État
        self.original_parameters = {}
        self.target_parameters = {}
        self.current_parameters = {}
        self.is_demo_mode = False
        
        self._create_interface()
        self._setup_demo_data()
        
    def _create_interface(self):
        """Crée l'interface complète."""
        # Menu principal
        self._create_menu()
        
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
        
    def _create_menu(self):
        """Crée le menu principal."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Effect", command=self._new_effect)
        file_menu.add_command(label="Save Patch", command=self._save_patch)
        file_menu.add_command(label="Load Patch", command=self._load_patch)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Menu Demo
        demo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Demo", menu=demo_menu)
        demo_menu.add_command(label="Start Auto Demo", command=self._start_auto_demo)
        demo_menu.add_command(label="Stop Demo", command=self._stop_demo)
        demo_menu.add_separator()
        demo_menu.add_command(label="Demo: Delay Impact", command=self._demo_delay_impact)
        demo_menu.add_command(label="Demo: Chorus Evolution", command=self._demo_chorus_evolution)
        demo_menu.add_command(label="Demo: Reverb Comparison", command=self._demo_reverb_comparison)
        
        # Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="User Guide", command=self._show_user_guide)
        
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
        
        # Bouton de démo
        demo_btn = ttk.Button(
            selection_frame,
            text="🎬 Demo",
            command=self._start_quick_demo
        )
        demo_btn.pack(side=tk.LEFT)
        
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
                original_value=value,
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
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Génère des variations basées sur le type d'effet
        target_params = self._generate_smart_target_parameters(current_params)
        
        # Définit les paramètres cibles
        self.target_parameters = target_params
        
        # Met à jour la visualisation d'impact
        self._update_impact_visualization()
        
        print(f"Generated {len(target_params)} target parameters")
    
    def _generate_smart_target_parameters(self, current_params: dict) -> dict:
        """Génère des paramètres cibles intelligents basés sur le type d'effet."""
        target_params = {}
        
        if self.current_effect_type == 0x0D:  # Mono Delay
            target_params = {
                "Time": current_params.get("Time", 100) * 1.5,  # Augmente le delay
                "Mix": min(100, current_params.get("Mix", 50) + 20),  # Augmente le mix
                "FB Gain": min(99, current_params.get("FB Gain", 30) + 15)  # Augmente le feedback
            }
        elif self.current_effect_type == 0x12:  # Chorus
            target_params = {
                "Rate": current_params.get("Rate", 1.0) * 2.0,  # Double la vitesse
                "Depth": min(100, current_params.get("Depth", 50) + 30),  # Augmente la profondeur
                "Mix": min(100, current_params.get("Mix", 50) + 25)  # Augmente le mix
            }
        elif self.current_effect_type == 0x09:  # Reverb
            target_params = {
                "Time": current_params.get("Time", 1.0) * 2.0,  # Double le temps
                "Mix": min(100, current_params.get("Mix", 50) + 30),  # Augmente le mix
                "High Ratio": min(1.0, current_params.get("High Ratio", 0.5) + 0.2)  # Augmente les aigus
            }
        else:
            # Génération générique
            for param_name, value in current_params.items():
                if isinstance(value, (int, float)):
                    variation = np.random.uniform(0.8, 1.3)
                    target_params[param_name] = value * variation
        
        # Applique des limites
        for param_name, value in target_params.items():
            target_params[param_name] = self._apply_parameter_limits(param_name, value)
        
        return target_params
    
    def _apply_parameter_limits(self, param_name: str, value: float) -> float:
        """Applique les limites appropriées à un paramètre."""
        limits = {
            "Time": (0.1, 2730.0),
            "Mix": (0, 100),
            "Rate": (0.1, 20.0),
            "Depth": (0, 100),
            "Feedback": (0, 99),
            "FB Gain": (0, 99),
            "Gain": (-12, 12),
            "Level": (0, 100),
            "Frequency": (20, 20000),
            "High Ratio": (0.1, 1.0),
            "Low Ratio": (0.1, 1.0)
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
            "Release": "ms",
            "FB Gain": "%",
            "High Ratio": "",
            "Low Ratio": ""
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
    
    def _start_quick_demo(self):
        """Démarre une démo rapide."""
        if not self.current_effect_widget:
            self._load_effect()
        
        if self.current_effect_widget:
            self._demo_delay_impact()
    
    def _start_auto_demo(self):
        """Démarre la démo automatique."""
        self.is_demo_mode = True
        self._auto_demo_loop()
    
    def _stop_demo(self):
        """Arrête la démo automatique."""
        self.is_demo_mode = False
    
    def _auto_demo_loop(self):
        """Boucle de démo automatique."""
        if not self.is_demo_mode:
            return
        
        # Cycle à travers différents effets
        effects = list(EffectRegistry.get_supported_effects().keys())
        current_idx = effects.index(self.current_effect_type) if self.current_effect_type in effects else 0
        
        # Charge le prochain effet
        next_effect = effects[(current_idx + 1) % len(effects)]
        effect_name = EffectRegistry.get_effect_name(next_effect)
        
        # Met à jour la sélection
        self.effect_var.set(f"{effect_name} (0x{next_effect:02X})")
        self._load_effect()
        
        # Génère des paramètres cibles
        time.sleep(1)
        self._generate_target_parameters()
        
        # Applique les changements
        time.sleep(2)
        self._apply_changes()
        
        # Attend avant le prochain cycle
        time.sleep(3)
        
        # Continue la boucle
        self.root.after(100, self._auto_demo_loop)
    
    def _demo_delay_impact(self):
        """Démo de l'impact sur un delay."""
        if self.current_effect_type != 0x0D:  # Mono Delay
            self.effect_var.set("Mono Delay (0x0D)")
            self._load_effect()
        
        # Génère des paramètres cibles spécifiques
        self.target_parameters = {
            "Time": 500,  # 500ms
            "Mix": 75,    # 75%
            "FB Gain": 60  # 60%
        }
        
        self._update_impact_visualization()
        messagebox.showinfo("Demo", "Delay impact demo loaded. Click 'Apply Changes' to see the effect.")
    
    def _demo_chorus_evolution(self):
        """Démo de l'évolution d'un chorus."""
        if self.current_effect_type != 0x12:  # Chorus
            self.effect_var.set("Chorus (0x12)")
            self._load_effect()
        
        # Génère des paramètres cibles spécifiques
        self.target_parameters = {
            "Rate": 3.0,   # 3 Hz
            "Depth": 80,   # 80%
            "Mix": 65      # 65%
        }
        
        self._update_impact_visualization()
        messagebox.showinfo("Demo", "Chorus evolution demo loaded. Click 'Apply Changes' to see the effect.")
    
    def _demo_reverb_comparison(self):
        """Démo de comparaison de reverb."""
        if self.current_effect_type != 0x09:  # Reverb
            self.effect_var.set("Reverb (0x09)")
            self._load_effect()
        
        # Génère des paramètres cibles spécifiques
        self.target_parameters = {
            "Time": 3.5,      # 3.5s
            "Mix": 60,        # 60%
            "High Ratio": 0.8  # 80%
        }
        
        self._update_impact_visualization()
        messagebox.showinfo("Demo", "Reverb comparison demo loaded. Click 'Apply Changes' to see the effect.")
    
    def _new_effect(self):
        """Crée un nouvel effet."""
        self._load_effect()
    
    def _save_patch(self):
        """Sauvegarde le patch actuel."""
        if not self.current_effect_widget:
            messagebox.showwarning("Warning", "No effect loaded")
            return
        
        # Simulation de sauvegarde
        patch_data = {
            "effect_type": self.current_effect_type,
            "parameters": self.current_effect_widget.get_all_parameters(),
            "target_parameters": self.target_parameters
        }
        
        print("Patch saved:", patch_data)
        messagebox.showinfo("Success", "Patch saved successfully!")
    
    def _load_patch(self):
        """Charge un patch sauvegardé."""
        # Simulation de chargement
        messagebox.showinfo("Load Patch", "Patch loading functionality would be implemented here.")
    
    def _show_about(self):
        """Affiche la boîte À propos."""
        messagebox.showinfo(
            "About",
            "Complete Magicstomp Interface Demo\n\n"
            "🎸 Features:\n"
            "• Visual effect parameter editing\n"
            "• Impact analysis and visualization\n"
            "• Target parameter generation\n"
            "• Before/after comparison\n"
            "• Auto-demo mode\n"
            "• Patch save/load functionality\n\n"
            "Based on MagicstompFrenzy (GPL-3.0)\n"
            "Adapted for Dopsound project"
        )
    
    def _show_user_guide(self):
        """Affiche le guide utilisateur."""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("User Guide")
        guide_window.geometry("600x400")
        
        text_widget = tk.Text(guide_window, wrap=tk.WORD, padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        guide_text = """
Complete Magicstomp Interface - User Guide

🎸 Getting Started:
1. Select an effect from the dropdown menu
2. Click "Load Effect" to load the effect widget
3. Adjust parameters using the controls

📊 Impact Analysis:
1. Click "Analyze Current" to analyze current parameters
2. Click "Generate Target" to create target parameters
3. View the impact visualization on the right panel
4. Click "Apply Changes" to apply target parameters

🎬 Demo Mode:
- Use the Demo menu to try pre-configured examples
- "Start Auto Demo" cycles through all effects automatically
- Individual demos show specific impact scenarios

🔄 Parameter Management:
- "Reset to Original" restores initial parameter values
- Save/Load patches to preserve your settings
- The impact visualization shows changes in real-time

📈 Impact Levels:
- NONE: < 5% change
- LOW: 5-15% change  
- MEDIUM: 15-30% change
- HIGH: 30-50% change
- CRITICAL: > 50% change

🎯 Target Generation:
The system generates intelligent target parameters based on:
- Current parameter values
- Effect type characteristics
- Musical context and best practices

This creates realistic parameter variations that enhance
the musical character of your effects.
        """
        
        text_widget.insert(tk.END, guide_text)
        text_widget.config(state=tk.DISABLED)
    
    def _setup_demo_data(self):
        """Configure les données de démo."""
        # Charge automatiquement le premier effet
        self._load_effect()
        
    def run(self):
        """Lance l'application."""
        self.root.mainloop()


def main():
    """Fonction principale."""
    print("🎸 Starting Complete Magicstomp Interface Demo...")
    print("Features:")
    print("  • Visual effect parameter editing")
    print("  • Impact analysis and visualization") 
    print("  • Target parameter generation")
    print("  • Before/after comparison")
    print("  • Auto-demo mode")
    print("  • Patch save/load functionality")
    print()
    
    app = CompleteMagicstompDemo()
    app.run()


if __name__ == "__main__":
    main()
