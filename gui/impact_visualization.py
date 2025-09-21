"""
Impact Visualization for Magicstomp Effects
==========================================

Visualisation des éléments impactés par l'analyse de target et la génération de patch.
Montre visuellement quels paramètres sont modifiés et dans quelle mesure.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from typing import Dict, List, Tuple, Optional
import colorsys
from dataclasses import dataclass
from enum import Enum


class ImpactLevel(Enum):
    """Niveaux d'impact des modifications."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ParameterImpact:
    """Représente l'impact d'un paramètre."""
    name: str
    original_value: float
    target_value: float
    current_value: float
    impact_level: ImpactLevel
    description: str = ""
    unit: str = ""


class ImpactVisualizer:
    """
    Visualiseur d'impact pour les paramètres Magicstomp.
    """
    
    def __init__(self, parent_frame: tk.Widget):
        self.parent_frame = parent_frame
        self.impacts: Dict[str, ParameterImpact] = {}
        self.current_effect_widget = None
        
        self._create_interface()
        
    def _create_interface(self):
        """Crée l'interface de visualisation."""
        # Frame principal
        main_frame = ttk.Frame(self.parent_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title = ttk.Label(main_frame, text="📊 Impact Analysis", 
                         font=("Arial", 12, "bold"))
        title.pack(pady=(0, 10))
        
        # Frame pour les contrôles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Boutons de contrôle
        self.analyze_btn = ttk.Button(
            controls_frame,
            text="Analyze Current Parameters",
            command=self._analyze_current_parameters
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.compare_btn = ttk.Button(
            controls_frame,
            text="Compare with Target",
            command=self._compare_with_target
        )
        self.compare_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.reset_btn = ttk.Button(
            controls_frame,
            text="Reset Analysis",
            command=self._reset_analysis
        )
        self.reset_btn.pack(side=tk.LEFT)
        
        # Frame pour la visualisation
        self.viz_frame = ttk.LabelFrame(main_frame, text="Impact Visualization", padding=10)
        self.viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas pour le graphique
        self._create_impact_chart()
        
        # Frame pour la liste détaillée
        self.details_frame = ttk.LabelFrame(main_frame, text="Parameter Details", padding=10)
        self.details_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Treeview pour les détails
        self._create_details_tree()
        
    def _create_impact_chart(self):
        """Crée le graphique d'impact."""
        # Figure matplotlib
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Canvas Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialisation
        self._update_chart()
        
    def _create_details_tree(self):
        """Crée l'arbre de détails des paramètres."""
        columns = ("Parameter", "Original", "Current", "Target", "Impact", "Change")
        self.tree = ttk.Treeview(self.details_frame, columns=columns, show="headings", height=8)
        
        # Configuration des colonnes
        self.tree.heading("Parameter", text="Parameter")
        self.tree.heading("Original", text="Original")
        self.tree.heading("Current", text="Current")
        self.tree.heading("Target", text="Target")
        self.tree.heading("Impact", text="Impact")
        self.tree.heading("Change", text="Change %")
        
        self.tree.column("Parameter", width=150)
        self.tree.column("Original", width=80)
        self.tree.column("Current", width=80)
        self.tree.column("Target", width=80)
        self.tree.column("Impact", width=100)
        self.tree.column("Change", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.details_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def set_effect_widget(self, effect_widget):
        """Définit le widget d'effet à analyser."""
        self.current_effect_widget = effect_widget
        
    def set_target_parameters(self, target_params: Dict[str, float]):
        """Définit les paramètres cibles."""
        if not self.current_effect_widget:
            return
            
        # Récupère les paramètres actuels comme origine
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Crée les impacts
        self.impacts.clear()
        for param_name, target_value in target_params.items():
            original_value = current_params.get(param_name, 0)
            
            # Calcule le niveau d'impact
            impact_level = self._calculate_impact_level(original_value, target_value)
            
            impact = ParameterImpact(
                name=param_name,
                original_value=original_value,
                target_value=target_value,
                current_value=original_value,
                impact_level=impact_level,
                unit=self._get_parameter_unit(param_name)
            )
            
            self.impacts[param_name] = impact
        
        self._update_visualization()
        
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
    
    def _update_chart(self):
        """Met à jour le graphique d'impact."""
        self.ax.clear()
        
        if not self.impacts:
            self.ax.text(0.5, 0.5, "No impact data available", 
                        ha='center', va='center', transform=self.ax.transAxes,
                        fontsize=14, style='italic')
            self.canvas.draw()
            return
        
        # Préparation des données
        param_names = list(self.impacts.keys())
        impact_levels = [impact.impact_level.value for impact in self.impacts.values()]
        change_percentages = [
            abs((impact.target_value - impact.original_value) / impact.original_value * 100)
            if impact.original_value != 0 else 0
            for impact in self.impacts.values()
        ]
        
        # Couleurs basées sur le niveau d'impact
        colors = [self._get_impact_color(level) for level in impact_levels]
        
        # Graphique en barres
        bars = self.ax.bar(param_names, change_percentages, color=colors, alpha=0.7)
        
        # Configuration du graphique
        self.ax.set_ylabel('Change Percentage (%)')
        self.ax.set_title('Parameter Impact Analysis')
        self.ax.tick_params(axis='x', rotation=45)
        
        # Légende des couleurs
        legend_elements = [
            plt.Rectangle((0,0),1,1, color=self._get_impact_color(ImpactLevel.LOW), alpha=0.7, label='Low'),
            plt.Rectangle((0,0),1,1, color=self._get_impact_color(ImpactLevel.MEDIUM), alpha=0.7, label='Medium'),
            plt.Rectangle((0,0),1,1, color=self._get_impact_color(ImpactLevel.HIGH), alpha=0.7, label='High'),
            plt.Rectangle((0,0),1,1, color=self._get_impact_color(ImpactLevel.CRITICAL), alpha=0.7, label='Critical')
        ]
        self.ax.legend(handles=legend_elements, loc='upper right')
        
        # Ajustement automatique
        self.fig.tight_layout()
        self.canvas.draw()
        
    def _get_impact_color(self, impact_level: ImpactLevel) -> str:
        """Retourne la couleur correspondant au niveau d'impact."""
        colors = {
            ImpactLevel.NONE: '#90EE90',      # Vert clair
            ImpactLevel.LOW: '#FFE135',       # Jaune
            ImpactLevel.MEDIUM: '#FFA500',    # Orange
            ImpactLevel.HIGH: '#FF6347',      # Rouge-orange
            ImpactLevel.CRITICAL: '#DC143C'   # Rouge
        }
        return colors.get(impact_level, '#CCCCCC')
    
    def _update_details_tree(self):
        """Met à jour l'arbre de détails."""
        # Efface les éléments existants
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ajoute les nouveaux éléments
        for impact in self.impacts.values():
            change_percent = abs((impact.target_value - impact.original_value) / impact.original_value * 100) \
                           if impact.original_value != 0 else 0
            
            impact_text = impact.impact_level.name
            
            self.tree.insert('', 'end', values=(
                impact.name,
                f"{impact.original_value:.2f}{impact.unit}",
                f"{impact.current_value:.2f}{impact.unit}",
                f"{impact.target_value:.2f}{impact.unit}",
                impact_text,
                f"{change_percent:.1f}%"
            ))
    
    def _update_visualization(self):
        """Met à jour toute la visualisation."""
        self._update_chart()
        self._update_details_tree()
        
    def _analyze_current_parameters(self):
        """Analyse les paramètres actuels."""
        if not self.current_effect_widget:
            return
            
        current_params = self.current_effect_widget.get_all_parameters()
        
        # Crée des impacts avec les valeurs actuelles comme cibles
        self.impacts.clear()
        for param_name, value in current_params.items():
            impact = ParameterImpact(
                name=param_name,
                original_value=0,  # Valeur par défaut
                target_value=value,
                current_value=value,
                impact_level=ImpactLevel.MEDIUM,
                unit=self._get_parameter_unit(param_name)
            )
            self.impacts[param_name] = impact
        
        self._update_visualization()
        
    def _compare_with_target(self):
        """Compare avec les paramètres cibles."""
        if not self.impacts:
            return
            
        # Met à jour les valeurs courantes
        if self.current_effect_widget:
            current_params = self.current_effect_widget.get_all_parameters()
            for param_name, impact in self.impacts.items():
                if param_name in current_params:
                    impact.current_value = current_params[param_name]
        
        self._update_visualization()
        
    def _reset_analysis(self):
        """Remet à zéro l'analyse."""
        self.impacts.clear()
        self._update_visualization()
        
    def get_impact_summary(self) -> Dict:
        """Retourne un résumé de l'impact."""
        if not self.impacts:
            return {}
            
        summary = {
            'total_parameters': len(self.impacts),
            'impact_levels': {},
            'average_change': 0,
            'critical_changes': []
        }
        
        # Compte les niveaux d'impact
        for impact in self.impacts.values():
            level = impact.impact_level.name
            summary['impact_levels'][level] = summary['impact_levels'].get(level, 0) + 1
            
            # Calcule le changement moyen
            change_percent = abs((impact.target_value - impact.original_value) / impact.original_value * 100) \
                           if impact.original_value != 0 else 0
            summary['average_change'] += change_percent
            
            # Identifie les changements critiques
            if impact.impact_level == ImpactLevel.CRITICAL:
                summary['critical_changes'].append(impact.name)
        
        summary['average_change'] /= len(self.impacts)
        
        return summary


class ImpactComparisonWindow:
    """Fenêtre de comparaison d'impact avant/après."""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Impact Comparison")
        self.window.geometry("800x600")
        
        self.before_impacts = {}
        self.after_impacts = {}
        
        self._create_interface()
        
    def _create_interface(self):
        """Crée l'interface de comparaison."""
        # Titre
        title = ttk.Label(self.window, text="🔄 Before/After Impact Comparison", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Graphique de comparaison
        self._create_comparison_chart(main_frame)
        
        # Tableau de comparaison
        self._create_comparison_table(main_frame)
        
    def _create_comparison_chart(self, parent):
        """Crée le graphique de comparaison."""
        chart_frame = ttk.LabelFrame(parent, text="Impact Comparison Chart", padding=10)
        chart_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Figure matplotlib
        self.fig = Figure(figsize=(12, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.X)
        
    def _create_comparison_table(self, parent):
        """Crée le tableau de comparaison."""
        table_frame = ttk.LabelFrame(parent, text="Parameter Comparison", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Parameter", "Before", "After", "Change", "Impact")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def set_before_after_impacts(self, before: Dict[str, ParameterImpact], 
                                after: Dict[str, ParameterImpact]):
        """Définit les impacts avant et après."""
        self.before_impacts = before
        self.after_impacts = after
        self._update_comparison()
        
    def _update_comparison(self):
        """Met à jour la comparaison."""
        if not self.before_impacts or not self.after_impacts:
            return
            
        # Met à jour le graphique
        self._update_comparison_chart()
        
        # Met à jour le tableau
        self._update_comparison_table()
        
    def _update_comparison_chart(self):
        """Met à jour le graphique de comparaison."""
        self.ax.clear()
        
        param_names = list(self.before_impacts.keys())
        before_values = [impact.current_value for impact in self.before_impacts.values()]
        after_values = [impact.current_value for impact in self.after_impacts.values()]
        
        x = np.arange(len(param_names))
        width = 0.35
        
        bars1 = self.ax.bar(x - width/2, before_values, width, label='Before', alpha=0.7, color='lightblue')
        bars2 = self.ax.bar(x + width/2, after_values, width, label='After', alpha=0.7, color='lightcoral')
        
        self.ax.set_xlabel('Parameters')
        self.ax.set_ylabel('Values')
        self.ax.set_title('Before/After Comparison')
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(param_names, rotation=45)
        self.ax.legend()
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def _update_comparison_table(self):
        """Met à jour le tableau de comparaison."""
        # Efface les éléments existants
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ajoute les comparaisons
        for param_name in self.before_impacts.keys():
            if param_name in self.after_impacts:
                before = self.before_impacts[param_name]
                after = self.after_impacts[param_name]
                
                change = after.current_value - before.current_value
                change_percent = (change / before.current_value * 100) if before.current_value != 0 else 0
                
                impact_level = after.impact_level.name
                
                self.tree.insert('', 'end', values=(
                    param_name,
                    f"{before.current_value:.2f}",
                    f"{after.current_value:.2f}",
                    f"{change_percent:+.1f}%",
                    impact_level
                ))


# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Impact Visualization Demo")
    root.geometry("1000x800")
    
    # Créer le visualiseur d'impact
    viz = ImpactVisualizer(root)
    
    # Simuler des données d'impact
    mock_impacts = {
        "Time": ParameterImpact("Time", 100, 250, 100, ImpactLevel.HIGH, unit="ms"),
        "Mix": ParameterImpact("Mix", 50, 75, 50, ImpactLevel.MEDIUM, unit="%"),
        "Feedback": ParameterImpact("Feedback", 30, 45, 30, ImpactLevel.MEDIUM, unit="%"),
        "Rate": ParameterImpact("Rate", 1.0, 2.5, 1.0, ImpactLevel.HIGH, unit="Hz"),
        "Depth": ParameterImpact("Depth", 25, 80, 25, ImpactLevel.CRITICAL, unit="%"),
    }
    
    viz.impacts = mock_impacts
    viz._update_visualization()
    
    root.mainloop()
