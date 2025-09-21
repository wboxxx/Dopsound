"""
Audio Analysis Integration with Magicstomp Effects
================================================

Intégration du système d'analyse audio avec les widgets d'effets Magicstomp
pour la génération automatique de paramètres basée sur l'analyse du signal audio.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path
import numpy as np
from typing import Dict, List, Optional, Tuple
import threading
import time

# Ajoute le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from magicstomp_effects import EffectRegistry
from adapter_magicstomp import MagicstompAdapter
from gui.impact_visualization import ImpactVisualizer, ParameterImpact, ImpactLevel
from gui.enhanced_magicstomp_interface import EnhancedMagicstompInterface


class AudioAnalysisIntegration:
    """
    Intégration de l'analyse audio avec les effets Magicstomp.
    """
    
    def __init__(self, parent_interface: EnhancedMagicstompInterface):
        self.parent_interface = parent_interface
        self.audio_analyzer = None
        self.is_analyzing = False
        self.analysis_thread = None
        
        # Paramètres d'analyse
        self.analysis_settings = {
            "target_frequency": 440.0,  # Hz
            "target_amplitude": 0.7,    # 0-1
            "target_spectral_balance": 0.5,  # 0-1 (bass vs treble)
            "target_dynamics": 0.6,     # 0-1 (compression level)
            "target_spatial_width": 0.4,  # 0-1 (stereo width)
        }
        
        self._create_analysis_interface()
        
    def _create_analysis_interface(self):
        """Crée l'interface d'analyse audio."""
        # Frame pour les contrôles d'analyse
        analysis_frame = ttk.LabelFrame(
            self.parent_interface.params_frame.master,
            text="🎵 Audio Analysis & Target Generation",
            padding=10
        )
        analysis_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Contrôles d'analyse
        self._create_analysis_controls(analysis_frame)
        
        # Progress bar pour l'analyse
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            analysis_frame,
            variable=self.progress_var,
            maximum=100,
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready for analysis")
        status_label = ttk.Label(analysis_frame, textvariable=self.status_var)
        status_label.pack(pady=(5, 0))
        
    def _create_analysis_controls(self, parent):
        """Crée les contrôles d'analyse."""
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Bouton d'analyse en temps réel
        self.analyze_btn = ttk.Button(
            controls_frame,
            text="🎤 Start Real-time Analysis",
            command=self._toggle_real_time_analysis
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton d'analyse ponctuelle
        analyze_once_btn = ttk.Button(
            controls_frame,
            text="📊 Analyze Once",
            command=self._analyze_audio_once
        )
        analyze_once_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton de génération de target
        generate_btn = ttk.Button(
            controls_frame,
            text="🎯 Generate Target Parameters",
            command=self._generate_target_from_analysis
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton de paramètres d'analyse
        settings_btn = ttk.Button(
            controls_frame,
            text="⚙️ Analysis Settings",
            command=self._show_analysis_settings
        )
        settings_btn.pack(side=tk.LEFT)
        
    def _toggle_real_time_analysis(self):
        """Active/désactive l'analyse en temps réel."""
        if not self.is_analyzing:
            self._start_real_time_analysis()
        else:
            self._stop_real_time_analysis()
    
    def _start_real_time_analysis(self):
        """Démarre l'analyse en temps réel."""
        self.is_analyzing = True
        self.analyze_btn.config(text="⏹️ Stop Analysis")
        self.status_var.set("Starting real-time analysis...")
        
        # Démarre le thread d'analyse
        self.analysis_thread = threading.Thread(target=self._real_time_analysis_loop)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
        
    def _stop_real_time_analysis(self):
        """Arrête l'analyse en temps réel."""
        self.is_analyzing = False
        self.analyze_btn.config(text="🎤 Start Real-time Analysis")
        self.status_var.set("Analysis stopped")
        self.progress_var.set(0)
        
    def _real_time_analysis_loop(self):
        """Boucle d'analyse en temps réel."""
        try:
            while self.is_analyzing:
                # Simulation d'analyse audio
                # En réalité, ceci viendrait de votre système d'analyse audio
                audio_features = self._simulate_audio_analysis()
                
                # Met à jour l'interface
                self.root.after(0, self._update_analysis_display, audio_features)
                
                # Génère des paramètres cibles basés sur l'analyse
                if audio_features:
                    target_params = self._generate_target_parameters_from_features(audio_features)
                    self.root.after(0, self._apply_target_parameters, target_params)
                
                time.sleep(0.1)  # 10 Hz update rate
                
        except Exception as e:
            self.root.after(0, lambda: self._handle_analysis_error(e))
    
    def _simulate_audio_analysis(self) -> Dict:
        """Simule l'analyse audio (remplacez par votre vraie analyse)."""
        # Simulation de caractéristiques audio
        features = {
            "frequency_spectrum": np.random.exponential(0.3, 100),
            "amplitude": np.random.uniform(0.3, 0.9),
            "spectral_centroid": np.random.uniform(200, 2000),
            "spectral_rolloff": np.random.uniform(1000, 8000),
            "zero_crossing_rate": np.random.uniform(0.1, 0.4),
            "mfcc": np.random.normal(0, 1, 13),
            "spectral_bandwidth": np.random.uniform(500, 3000),
            "spectral_contrast": np.random.uniform(0.2, 0.8, 7)
        }
        
        return features
    
    def _update_analysis_display(self, features: Dict):
        """Met à jour l'affichage de l'analyse."""
        if not self.is_analyzing:
            return
            
        # Met à jour la barre de progression
        progress = (features["amplitude"] * 100) if "amplitude" in features else 0
        self.progress_var.set(progress)
        
        # Met à jour le statut
        centroid = features.get("spectral_centroid", 0)
        self.status_var.set(f"Analyzing... Centroid: {centroid:.0f} Hz, Amp: {features.get('amplitude', 0):.2f}")
    
    def _generate_target_parameters_from_features(self, features: Dict) -> Dict:
        """Génère des paramètres cibles basés sur les caractéristiques audio."""
        if not self.parent_interface.current_effect_widget:
            return {}
        
        # Récupère les paramètres actuels
        current_params = self.parent_interface.current_effect_widget.get_all_parameters()
        
        # Génère des paramètres cibles basés sur l'analyse
        target_params = {}
        
        # Analyse du spectre fréquentiel
        spectral_centroid = features.get("spectral_centroid", 440)
        spectral_balance = features.get("spectral_contrast", [0.5] * 7)
        
        # Analyse de l'amplitude et des dynamiques
        amplitude = features.get("amplitude", 0.5)
        zero_crossing_rate = features.get("zero_crossing_rate", 0.2)
        
        # Génération de paramètres basée sur l'effet actuel
        effect_type = self.parent_interface.current_effect_type
        
        if effect_type == 0x0D:  # Mono Delay
            # Delay basé sur la fréquence fondamentale
            target_params["Time"] = max(50, min(1000, 1000 / (spectral_centroid / 100)))
            target_params["Mix"] = max(10, min(80, amplitude * 100))
            target_params["FB Gain"] = max(0, min(60, zero_crossing_rate * 200))
            
        elif effect_type == 0x12:  # Chorus
            # Chorus basé sur la largeur spectrale
            target_params["Rate"] = max(0.5, min(10, spectral_centroid / 500))
            target_params["Depth"] = max(20, min(80, amplitude * 100))
            target_params["Mix"] = max(30, min(70, spectral_balance[0] * 100))
            
        elif effect_type == 0x09:  # Reverb
            # Reverb basé sur la réverbération naturelle
            target_params["Time"] = max(0.5, min(5.0, amplitude * 3))
            target_params["Mix"] = max(20, min(60, (1 - zero_crossing_rate) * 80))
            target_params["High Ratio"] = max(0.3, min(1.0, spectral_balance[0]))
            
        # Applique des limites aux paramètres
        for param_name, value in target_params.items():
            target_params[param_name] = self._apply_parameter_limits(param_name, value)
        
        return target_params
    
    def _apply_target_parameters(self, target_params: Dict):
        """Applique les paramètres cibles générés."""
        if not target_params:
            return
            
        # Met à jour les paramètres cibles dans l'interface parent
        self.parent_interface.target_parameters = target_params
        
        # Met à jour la visualisation d'impact
        self.parent_interface._update_impact_visualization()
    
    def _analyze_audio_once(self):
        """Effectue une analyse ponctuelle de l'audio."""
        self.status_var.set("Performing single analysis...")
        
        # Simulation d'analyse
        features = self._simulate_audio_analysis()
        
        # Génère les paramètres cibles
        target_params = self._generate_target_parameters_from_features(features)
        
        if target_params:
            self._apply_target_parameters(target_params)
            self.status_var.set(f"Analysis complete. Generated {len(target_params)} target parameters.")
        else:
            self.status_var.set("Analysis complete. No target parameters generated.")
    
    def _generate_target_from_analysis(self):
        """Génère des paramètres cibles basés sur l'analyse actuelle."""
        if not self.parent_interface.current_effect_widget:
            messagebox.showwarning("Warning", "No effect loaded")
            return
        
        # Effectue une analyse ponctuelle
        self._analyze_audio_once()
        
        # Demande confirmation pour appliquer
        result = messagebox.askyesno(
            "Apply Target Parameters",
            f"Apply {len(self.parent_interface.target_parameters)} generated target parameters?"
        )
        
        if result:
            self.parent_interface._apply_changes()
    
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
    
    def _show_analysis_settings(self):
        """Affiche la fenêtre de paramètres d'analyse."""
        settings_window = tk.Toplevel(self.parent_interface.root)
        settings_window.title("Analysis Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.parent_interface.root)
        settings_window.grab_set()
        
        # Titre
        title = ttk.Label(settings_window, text="Audio Analysis Settings", 
                         font=("Arial", 12, "bold"))
        title.pack(pady=10)
        
        # Frame pour les paramètres
        params_frame = ttk.Frame(settings_window)
        params_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Paramètres d'analyse
        settings = [
            ("Target Frequency (Hz)", "target_frequency", 20, 2000),
            ("Target Amplitude", "target_amplitude", 0, 1),
            ("Spectral Balance", "target_spectral_balance", 0, 1),
            ("Target Dynamics", "target_dynamics", 0, 1),
            ("Spatial Width", "target_spatial_width", 0, 1)
        ]
        
        self.settings_vars = {}
        for i, (label, key, min_val, max_val) in enumerate(settings):
            ttk.Label(params_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            
            var = tk.DoubleVar(value=self.analysis_settings[key])
            scale = ttk.Scale(params_frame, from_=min_val, to=max_val, 
                            variable=var, orient=tk.HORIZONTAL, length=200)
            scale.grid(row=i, column=1, padx=(10, 0), pady=5)
            
            value_label = ttk.Label(params_frame, text=f"{var.get():.2f}")
            value_label.grid(row=i, column=2, padx=(10, 0), pady=5)
            
            # Callback pour mettre à jour le label
            def update_label(v, label=value_label):
                label.config(text=f"{v:.2f}")
            var.trace('w', lambda *args, v=var, l=value_label: l.config(text=f"{v.get():.2f}"))
            
            self.settings_vars[key] = var
        
        # Boutons
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="OK", 
                  command=lambda: self._save_analysis_settings(settings_window)).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", 
                  command=settings_window.destroy).pack(side=tk.RIGHT)
    
    def _save_analysis_settings(self, window):
        """Sauvegarde les paramètres d'analyse."""
        for key, var in self.settings_vars.items():
            self.analysis_settings[key] = var.get()
        
        window.destroy()
        print("Analysis settings saved:", self.analysis_settings)
    
    def _handle_analysis_error(self, error):
        """Gère les erreurs d'analyse."""
        self._stop_real_time_analysis()
        messagebox.showerror("Analysis Error", f"An error occurred during analysis: {error}")
    
    def get_analysis_settings(self) -> Dict:
        """Retourne les paramètres d'analyse actuels."""
        return self.analysis_settings.copy()
    
    def set_analysis_settings(self, settings: Dict):
        """Définit les paramètres d'analyse."""
        self.analysis_settings.update(settings)


class EnhancedMagicstompInterfaceWithAnalysis(EnhancedMagicstompInterface):
    """
    Interface Magicstomp améliorée avec intégration d'analyse audio.
    """
    
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        
        # Ajoute l'intégration d'analyse audio
        self.audio_analysis = AudioAnalysisIntegration(self)


def main():
    """Fonction principale avec analyse audio."""
    root = tk.Tk()
    app = EnhancedMagicstompInterfaceWithAnalysis(root)
    
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
    
    # Menu Analysis
    analysis_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Analysis", menu=analysis_menu)
    analysis_menu.add_command(label="Start Real-time Analysis", 
                            command=app.audio_analysis._start_real_time_analysis)
    analysis_menu.add_command(label="Stop Analysis", 
                            command=app.audio_analysis._stop_real_time_analysis)
    analysis_menu.add_command(label="Analysis Settings", 
                            command=app.audio_analysis._show_analysis_settings)
    
    # Menu Help
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
        "About", "Enhanced Magicstomp Interface with Audio Analysis\n\n"
        "Features:\n"
        "• Visual effect parameter editing\n"
        "• Real-time audio analysis\n"
        "• Automatic target parameter generation\n"
        "• Impact analysis and visualization\n"
        "• Before/after comparison\n"
        "• Patch save/load functionality"
    ))
    
    root.mainloop()


if __name__ == "__main__":
    main()
