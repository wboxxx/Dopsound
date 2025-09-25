#!/usr/bin/env python3
"""Debug logger pour écrire les logs dans un fichier texte."""

import os
from datetime import datetime

class DebugLogger:
    def __init__(self, log_file="debug.log"):
        self.log_file = log_file
        # Nettoyer le fichier de log au démarrage
        if os.path.exists(log_file):
            os.remove(log_file)
    
    def log(self, message):
        """Écrit un message dans le fichier de log."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)  # Afficher aussi dans la console
    
    def log_sysex_data(self, data, name="SYSEX"):
        """Écrit les données SYSEX de manière lisible."""
        if isinstance(data, (list, tuple)):
            data_str = " ".join(f"{b:02X}" for b in data[:20])
            if len(data) > 20:
                data_str += f"... (total {len(data)} bytes)"
        else:
            data_str = str(data)
        self.log(f"{name}: {data_str}")

# Instance globale
debug_logger = DebugLogger()
