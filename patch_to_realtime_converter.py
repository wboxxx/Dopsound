#!/usr/bin/env python3
"""
Patch to Realtime Converter
===========================

Convertit un patch JSON en série de messages temps réel
au lieu d'uploader un patch complet.
"""

import json
from typing import Dict, Any, List
from realtime_magicstomp import RealtimeMagicstomp

class PatchToRealtimeConverter:
    """Convertit un patch JSON en messages temps réel."""
    
    def __init__(self, realtime_magicstomp=None):
        """
        Initialise le convertisseur.
        
        Args:
            realtime_magicstomp: Instance RealtimeMagicstomp existante (optionnel)
        """
        if realtime_magicstomp:
            self.realtime_magicstomp = realtime_magicstomp
            print(f"✅ Utilisation de l'instance RealtimeMagicstomp existante")
        else:
            self.realtime_magicstomp = None
            self._initialize_midi()
    
    def _initialize_midi(self):
        """Initialise la connexion MIDI."""
        try:
            self.realtime_magicstomp = RealtimeMagicstomp(auto_detect=True)
            if self.realtime_magicstomp.output_port:
                print(f"✅ Connexion temps réel: {self.realtime_magicstomp.midi_port_name}")
            else:
                print("❌ Pas de connexion MIDI temps réel")
        except Exception as e:
            print(f"❌ Erreur initialisation MIDI: {e}")
    
    def patch_to_realtime_messages(self, patch: Dict[str, Any]) -> List[tuple]:
        """
        Convertit un patch JSON en liste de messages temps réel.
        
        Returns:
            List[tuple]: [(offset, value, description), ...]
        """
        messages = []
        
        # Mapping des paramètres vers les offsets temps réel
        # Basé sur les offsets qui marchent (2, 4, 6 pour les contrôles)
        
        # Paramètres de base (section commune) - utiliser des valeurs 0-1 comme le test qui marche
        if 'compressor' in patch:
            comp = patch['compressor']
            if comp.get('enabled', False):
                # Utiliser des valeurs 0-1 pour les contrôles
                messages.append((2, 1 if comp.get('threshold', 0.5) > 0.5 else 0, "Compressor Threshold"))
                messages.append((4, 1 if comp.get('ratio', 2.0) > 2.0 else 0, "Compressor Ratio"))
                messages.append((6, 1 if comp.get('makeup_gain', 3.0) > 1.5 else 0, "Compressor Gain"))
        
        if 'eq' in patch:
            eq = patch['eq']
            if eq.get('enabled', False):
                # EQ sur les contrôles - valeurs 0-1
                messages.append((2, 1 if eq.get('mid_gain', 0.0) > 0.0 else 0, "EQ Mid Gain"))
                messages.append((4, 1 if eq.get('low_gain', 0.0) > 0.0 else 0, "EQ Low Gain"))
                messages.append((6, 1 if eq.get('high_gain', 0.0) > 0.0 else 0, "EQ High Gain"))
        
        if 'delay' in patch:
            delay = patch['delay']
            if delay.get('enabled', False):
                # Delay sur les contrôles - valeurs 0-1
                messages.append((2, 1 if delay.get('time', 300) > 300 else 0, "Delay Time"))
                messages.append((4, 1 if delay.get('feedback', 0.3) > 0.15 else 0, "Delay Feedback"))
                messages.append((6, 1 if delay.get('mix', 0.2) > 0.1 else 0, "Delay Mix"))
        
        return messages
    
    def apply_patch_realtime(self, patch: Dict[str, Any], delay: float = 0.5):
        """
        Applique un patch via des messages temps réel.
        
        Args:
            patch: Patch JSON à appliquer
            delay: Délai entre les messages (secondes)
        """
        if not self.realtime_magicstomp or not self.realtime_magicstomp.output_port:
            print("❌ Pas de connexion MIDI temps réel")
            return False
        
        print("🔄 Conversion patch vers messages temps réel...")
        messages = self.patch_to_realtime_messages(patch)
        
        if not messages:
            print("❌ Aucun message généré")
            return False
        
        print(f"📤 Application de {len(messages)} paramètres via temps réel...")
        
        import time
        success_count = 0
        for i, (offset, value, description) in enumerate(messages):
            try:
                print(f"📤 {i+1}/{len(messages)}: {description} = {value}")
                
                # Envoyer avec timeout
                success = self.realtime_magicstomp.tweak_parameter(offset, value, immediate=True)
                if success is not False:  # None ou True sont OK
                    success_count += 1
                else:
                    print(f"⚠️ Échec envoi paramètre {i+1}: {description}")
                
                if delay > 0:
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"❌ Erreur paramètre {i+1}: {e}")
                import traceback
                traceback.print_exc()
        
        if success_count > 0:
            print(f"✅ Patch appliqué via temps réel ! ({success_count}/{len(messages)} paramètres)")
            return True
        else:
            print("❌ Aucun paramètre n'a pu être envoyé")
            return False

def test_patch_converter():
    """Test du convertisseur patch vers temps réel."""
    print("🧪 Test du convertisseur patch vers temps réel")
    print("=" * 50)
    
    # Patch de test
    test_patch = {
        "meta": {"name": "Test Realtime Patch"},
        "compressor": {"enabled": True, "threshold": 0.6, "ratio": 3.0, "makeup_gain": 4.0},
        "eq": {"enabled": True, "low_gain": 1.0, "mid_gain": 2.0, "high_gain": 1.5},
        "delay": {"enabled": True, "time": 400, "feedback": 0.4, "mix": 0.3}
    }
    
    converter = PatchToRealtimeConverter()
    
    if converter.realtime_magicstomp and converter.realtime_magicstomp.output_port:
        print("✅ Convertisseur initialisé")
        
        # Test de conversion
        messages = converter.patch_to_realtime_messages(test_patch)
        print(f"📊 Messages générés: {len(messages)}")
        
        for offset, value, desc in messages:
            print(f"  - {desc}: offset {offset} = {value}")
        
        # Test d'application
        print("\n📤 Application du patch...")
        success = converter.apply_patch_realtime(test_patch, delay=1.0)
        
        if success:
            print("🎉 Patch appliqué avec succès via temps réel !")
        else:
            print("❌ Échec de l'application du patch")
    else:
        print("❌ Convertisseur non initialisé")

def main():
    """Lance le test."""
    test_patch_converter()

if __name__ == "__main__":
    main()
