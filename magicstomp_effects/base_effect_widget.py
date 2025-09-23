"""
Base Effect Widget
=================

Widget de base pour tous les effets Magicstomp.
Adapté du code C++/Qt EffectEditBaseWidget.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Callable
import math


class BaseEffectWidget(ttk.Frame):
    """
    Widget de base pour tous les effets Magicstomp.
    
    Fournit les fonctionnalités communes :
    - Mapping des paramètres vers les données Magicstomp
    - Conversion des valeurs (échelles, offsets)
    - Gestion des événements de changement
    """
    
    def __init__(self, parent: Optional[tk.Widget] = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Dictionnaire pour stocker les paramètres actuels
        self.current_params: Dict[str, Any] = {}
        
        # Callbacks pour les changements de paramètres
        self.param_change_callbacks: Dict[str, Callable] = {}
        
        # Configuration des colonnes/grid
        self.grid_columnconfigure(0, weight=1)
        
    def create_parameter_widget(self, 
                               param_name: str,
                               param_type: str = "spinbox",
                               min_val: float = 0,
                               max_val: float = 100,
                               step: float = 1,
                               suffix: str = "",
                               offset: Optional[int] = None,
                               length: int = 1,
                               conversion: Optional[str] = None,
                               values: Optional[list] = None,
                               row: int = 0,
                               column: int = 0) -> tk.Widget:
        """
        Crée un widget de paramètre avec mapping automatique.
        
        Args:
            param_name: Nom du paramètre
            param_type: Type de widget ("spinbox", "double_spinbox", "combobox")
            min_val, max_val: Valeurs min/max
            step: Pas d'incrémentation
            suffix: Suffixe d'affichage (%, ms, dB, etc.)
            offset: Offset dans les données Magicstomp
            length: Longueur en octets
            conversion: Méthode de conversion ("scaleAndAdd", "logScale", etc.)
            row, column: Position dans le grid
        """
        
        # Label
        label = ttk.Label(self, text=param_name)
        label.grid(row=row, column=column, sticky="w", padx=(0, 5))
        
        # Widget de contrôle
        if param_type == "double_spinbox":
            widget = ttk.Spinbox(self, 
                               from_=min_val, 
                               to=max_val, 
                               increment=step,
                               width=10)
        elif param_type == "combobox":
            widget = ttk.Combobox(self, width=12)
            if values is not None:
                widget['values'] = values
            elif isinstance(min_val, list):
                widget['values'] = min_val
            else:
                widget['values'] = list(range(int(min_val), int(max_val) + 1))
        else:  # spinbox par défaut
            widget = ttk.Spinbox(self,
                               from_=int(min_val),
                               to=int(max_val),
                               increment=int(step),
                               width=10)
        
        # Positionnement
        widget.grid(row=row, column=column + 1, sticky="ew", padx=(0, 10))
        
        # Stockage des métadonnées
        widget.param_name = param_name
        widget.param_type = param_type
        widget.min_val = min_val
        widget.max_val = max_val
        widget.step = step
        widget.suffix = suffix
        widget.offset = offset
        widget.length = length
        widget.conversion = conversion
        
        # Bind des événements
        if param_type in ["spinbox", "double_spinbox"]:
            widget.bind('<FocusOut>', lambda e: self._on_parameter_change(widget))
            widget.bind('<Return>', lambda e: self._on_parameter_change(widget))
        else:  # combobox
            widget.bind('<<ComboboxSelected>>', lambda e: self._on_parameter_change(widget))
        
        return widget
    
    def _on_parameter_change(self, widget: tk.Widget):
        """Gère le changement d'un paramètre."""
        try:
            param_name = widget.param_name
            
            # Récupération de la valeur
            if widget.param_type == "double_spinbox":
                value = float(widget.get())
            elif widget.param_type == "combobox":
                value = widget.get()
            else:
                value = int(widget.get())
            
            # Validation des limites
            if hasattr(widget, 'min_val') and hasattr(widget, 'max_val'):
                if isinstance(value, (int, float)):
                    value = max(widget.min_val, min(widget.max_val, value))
            
            # Mise à jour des paramètres
            self.current_params[param_name] = value
            
            # Conversion vers format Magicstomp si nécessaire
            magicstomp_value = self._convert_to_magicstomp(widget, value)
            
            # Callback de changement
            if param_name in self.param_change_callbacks:
                self.param_change_callbacks[param_name](value, magicstomp_value)
                
        except (ValueError, AttributeError) as e:
            print(f"Erreur lors du changement de paramètre: {e}")
    
    def set_parameter_value(self, param_name: str, value: Any):
        """Définit la valeur d'un paramètre par nom."""
        # Trouve le widget correspondant au paramètre
        for child in self.winfo_children():
            if hasattr(child, 'param_name') and child.param_name == param_name:
                # Met à jour la valeur du widget
                if child.param_type == "double_spinbox":
                    child.set(value)
                elif child.param_type == "combobox":
                    child.set(value)
                else:  # spinbox
                    child.set(int(value))
                
                # Met à jour les paramètres internes
                self.current_params[param_name] = value
                return
        
        # Si le widget n'est pas trouvé, met juste à jour les paramètres
        self.current_params[param_name] = value
    
    def get_parameter_value(self, param_name: str) -> Any:
        """Récupère la valeur d'un paramètre par nom."""
        # Cherche d'abord dans les paramètres stockés
        if param_name in self.current_params:
            return self.current_params[param_name]
        
        # Sinon, cherche dans les widgets
        for child in self.winfo_children():
            if hasattr(child, 'param_name') and child.param_name == param_name:
                try:
                    if child.param_type == "double_spinbox":
                        return float(child.get())
                    elif child.param_type == "combobox":
                        return child.get()
                    else:  # spinbox
                        return int(child.get())
                except (ValueError, AttributeError):
                    return 0
        
        return 0  # Valeur par défaut
    
    def _convert_to_magicstomp(self, widget: tk.Widget, value: Any) -> int:
        """
        Convertit une valeur utilisateur vers le format Magicstomp.
        
        Args:
            widget: Widget source
            value: Valeur utilisateur
            
        Returns:
            Valeur au format Magicstomp
        """
        if not hasattr(widget, 'conversion') or not widget.conversion:
            return int(value) if isinstance(value, (int, float)) else 0
        
        conversion = widget.conversion
        
        if conversion.startswith("scaleAndAdd("):
            # Format: "scaleAndAdd(scale, offset)"
            parts = conversion[12:-1].split(",")
            scale = float(parts[0].strip())
            offset = float(parts[1].strip())
            return int((value - offset) / scale)
        
        elif conversion == "logScale":
            # Échelle logarithmique pour les fréquences/temps
            if isinstance(value, (int, float)) and value > 0:
                return int(127 * math.log10(value / widget.min_val) / 
                          math.log10(widget.max_val / widget.min_val))
            return 0
        
        elif conversion == "timeMs":
            # Conversion temps en ms vers format Magicstomp
            return self._ms_to_magicstomp_time(value)
        
        elif conversion == "freqHz":
            # Conversion fréquence Hz vers format Magicstomp
            return self._hz_to_magicstomp_rate(value)
        
        # Conversion par défaut
        return int(value)
    
    def _ms_to_magicstomp_time(self, time_ms: float) -> int:
        """Convertit un temps en ms vers la valeur Magicstomp."""
        if time_ms <= 0:
            return 0
        
        # Mapping approximatif basé sur l'échelle Magicstomp
        if time_ms <= 50:
            return int(time_ms * 2.54)  # 0-127 pour 0-50ms
        elif time_ms <= 500:
            return int(127 + (time_ms - 50) * 0.28)  # 127-255 pour 50-500ms
        else:
            return int(255 + (time_ms - 500) * 0.1)  # 255+ pour >500ms
    
    def _hz_to_magicstomp_rate(self, rate_hz: float) -> int:
        """Convertit une fréquence en Hz vers la valeur Magicstomp."""
        if rate_hz <= 0:
            return 0
        
        # Mapping approximatif: 0.1-20 Hz -> 0-127
        if rate_hz < 0.1:
            return 0
        elif rate_hz <= 20:
            return int(127 * (math.log10(rate_hz / 0.1) / math.log10(200)))
        else:
            return 127
    
    def set_parameter(self, param_name: str, value: Any):
        """Définit la valeur d'un paramètre."""
        # Trouve le widget correspondant
        for child in self.winfo_children():
            if hasattr(child, 'param_name') and child.param_name == param_name:
                # Met à jour la valeur du widget selon son type
                if hasattr(child, 'param_type'):
                    if child.param_type == "double_spinbox":
                        child.set(value)
                    elif child.param_type == "combobox":
                        child.set(value)
                    else:  # spinbox
                        child.set(int(value))
                else:
                    # Fallback: try set method first, then delete/insert
                    try:
                        child.set(value)
                    except AttributeError:
                        # For Entry widgets
                        child.delete(0, tk.END)
                        child.insert(0, str(value))
                
                self.current_params[param_name] = value
                break
    
    def get_parameter(self, param_name: str) -> Any:
        """Récupère la valeur d'un paramètre."""
        return self.current_params.get(param_name, 0)
    
    def set_parameter_callback(self, param_name: str, callback: Callable):
        """Définit un callback pour les changements de paramètre."""
        self.param_change_callbacks[param_name] = callback
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """Récupère tous les paramètres actuels."""
        return self.current_params.copy()
    
    def set_all_parameters(self, params: Dict[str, Any]):
        """Définit tous les paramètres."""
        for param_name, value in params.items():
            self.set_parameter(param_name, value)
