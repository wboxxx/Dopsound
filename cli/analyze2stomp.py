#!/usr/bin/env python3
"""
CLI Magicstomp - Audio to Patch Pipeline
=======================================

Interface en ligne de commande complète pour le pipeline :
Audio → Analyse → JSON → SysEx → Magicstomp

Usage:
    python cli/analyze2stomp.py audio.wav --send
    python cli/analyze2stomp.py audio.wav --output patch.syx --patch 5
    python cli/analyze2stomp.py audio.wav --json-only --verbose

Fonctionnalités:
- Analyse audio complète avec features guitare
- Génération de patch JSON neutre
- Conversion vers SysEx Magicstomp
- Envoi direct vers device USB-MIDI
- Export de fichiers .syx
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Optional

# Ajoute le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyze2json import AudioAnalyzer
from adapter_magicstomp import MagicstompAdapter


class MagicstompCLI:
    """Interface CLI pour le pipeline Audio → Magicstomp."""
    
    def __init__(self):
        """Initialise la CLI."""
        self.analyzer = AudioAnalyzer()
        self.adapter = MagicstompAdapter()
    
    def analyze_audio(self, audio_file: str, verbose: bool = False) -> dict:
        """
        Analyse un fichier audio et génère un patch JSON.
        
        Args:
            audio_file: Chemin vers le fichier audio
            verbose: Mode verbeux
            
        Returns:
            Patch JSON généré
        """
        if verbose:
            print(f"🎵 Analyse de {audio_file}...")
        
        return self.analyzer.analyze(audio_file)
    
    def save_json(self, patch: dict, output_file: str, verbose: bool = False) -> None:
        """
        Sauvegarde le patch JSON.
        
        Args:
            patch: Patch JSON
            output_file: Fichier de sortie
            verbose: Mode verbeux
        """
        if verbose:
            print(f"💾 Sauvegarde JSON vers {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(patch, f, indent=2, ensure_ascii=False)
        
        if verbose:
            print(f"✅ JSON sauvegardé: {output_file}")
    
    def convert_to_syx(self, patch: dict, patch_number: int = 0, 
                      verbose: bool = False) -> list:
        """
        Convertit le patch JSON vers SysEx.
        
        Args:
            patch: Patch JSON
            patch_number: Numéro de patch
            verbose: Mode verbeux
            
        Returns:
            Données SysEx
        """
        if verbose:
            print(f"🔄 Conversion vers SysEx (patch #{patch_number})...")
        
        return self.adapter.json_to_syx(patch, patch_number)
    
    def save_syx(self, syx_data: list, output_file: str, verbose: bool = False) -> None:
        """
        Sauvegarde les données SysEx.
        
        Args:
            syx_data: Données SysEx
            output_file: Fichier de sortie
            verbose: Mode verbeux
        """
        if verbose:
            print(f"💾 Sauvegarde SysEx vers {output_file}...")
        
        self.adapter.save_to_file(syx_data, output_file)
    
    def send_to_device(self, syx_data: list, verbose: bool = False) -> bool:
        """
        Envoie le patch vers le device Magicstomp.
        
        Args:
            syx_data: Données SysEx
            verbose: Mode verbeux
            
        Returns:
            True si l'envoi a réussi
        """
        if verbose:
            print("📤 Envoi vers device Magicstomp...")
        
        return self.adapter.send_to_device(syx_data)
    
    def list_ports(self) -> None:
        """Liste les ports MIDI disponibles."""
        print("🔌 Ports MIDI disponibles:")
        self.adapter.list_midi_ports()
    
    def run_pipeline(self, audio_file: str, 
                    json_output: Optional[str] = None,
                    syx_output: Optional[str] = None,
                    patch_number: int = 0,
                    send_to_device: bool = False,
                    json_only: bool = False,
                    verbose: bool = False) -> bool:
        """
        Exécute le pipeline complet.
        
        Args:
            audio_file: Fichier audio à analyser
            json_output: Fichier JSON de sortie (optionnel)
            syx_output: Fichier SysEx de sortie (optionnel)
            patch_number: Numéro de patch Magicstomp
            send_to_device: Envoyer vers le device
            json_only: Arrêter après la génération JSON
            verbose: Mode verbeux
            
        Returns:
            True si le pipeline s'est exécuté avec succès
        """
        print("🚀 Pipeline Audio → Magicstomp")
        print("=" * 40)
        
        try:
            # Étape 1: Analyse audio
            patch = self.analyze_audio(audio_file, verbose)
            
            # Sauvegarde JSON si demandé
            if json_output:
                self.save_json(patch, json_output, verbose)
            elif json_only:
                # Sauvegarde automatique si json_only
                auto_json = Path(audio_file).with_suffix('.json')
                self.save_json(patch, str(auto_json), verbose)
                return True
            
            # Arrêt si json_only
            if json_only:
                return True
            
            # Étape 2: Conversion vers SysEx
            syx_data = self.convert_to_syx(patch, patch_number, verbose)
            
            # Sauvegarde SysEx si demandé
            if syx_output:
                self.save_syx(syx_data, syx_output, verbose)
            
            # Envoi vers device si demandé
            if send_to_device:
                success = self.send_to_device(syx_data, verbose)
                if not success:
                    print("⚠️  Envoi vers device échoué, mais le patch SysEx est prêt")
                    return False
            
            print("\n✅ Pipeline terminé avec succès!")
            return True
            
        except Exception as e:
            print(f"\n❌ Erreur dans le pipeline: {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            return False


def main():
    """Point d'entrée principal de la CLI."""
    parser = argparse.ArgumentParser(
        description="Pipeline Audio → Magicstomp Patch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'usage:

  # Analyse complète avec envoi vers device
  python cli/analyze2stomp.py guitar.wav --send

  # Génération de fichiers JSON et SysEx
  python cli/analyze2stomp.py guitar.wav --json patch.json --syx patch.syx

  # Analyse JSON seulement (pour debugging)
  python cli/analyze2stomp.py guitar.wav --json-only --verbose

  # Patch personnalisé sur slot 5
  python cli/analyze2stomp.py guitar.wav --send --patch 5

  # Lister les ports MIDI disponibles
  python cli/analyze2stomp.py --list-ports
        """
    )
    
    # Arguments principaux
    parser.add_argument('audio_file', nargs='?', help='Fichier audio à analyser')
    
    # Options de sortie
    parser.add_argument('--json', '-j', help='Fichier JSON de sortie')
    parser.add_argument('--syx', '-s', help='Fichier SysEx de sortie')
    parser.add_argument('--json-only', action='store_true', 
                       help='Arrêter après la génération JSON')
    
    # Options Magicstomp
    parser.add_argument('--patch', '-p', type=int, default=0,
                       help='Numéro de patch Magicstomp (0-99, défaut: 0)')
    parser.add_argument('--send', action='store_true',
                       help='Envoyer directement vers le device Magicstomp')
    
    # Options utilitaires
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Mode verbeux avec détails d\'analyse')
    parser.add_argument('--list-ports', action='store_true',
                       help='Lister les ports MIDI disponibles')
    
    args = parser.parse_args()
    
    # Lister les ports si demandé
    if args.list_ports:
        cli = MagicstompCLI()
        cli.list_ports()
        return
    
    # Vérifie qu'un fichier audio est fourni
    if not args.audio_file:
        parser.error("Un fichier audio est requis (ou utilisez --list-ports)")
    
    # Vérifie que le fichier existe
    if not Path(args.audio_file).exists():
        print(f"❌ Erreur: Le fichier {args.audio_file} n'existe pas")
        sys.exit(1)
    
    # Valide le numéro de patch
    if not 0 <= args.patch <= 99:
        print(f"❌ Erreur: Le numéro de patch doit être entre 0 et 99")
        sys.exit(1)
    
    # Détermine les fichiers de sortie automatiques
    json_output = args.json
    syx_output = args.syx
    
    if not json_output and not args.json_only:
        # Génère un nom de fichier JSON automatique
        json_output = str(Path(args.audio_file).with_suffix('.json'))
    
    if not syx_output and not args.json_only and not args.send:
        # Génère un nom de fichier SysEx automatique
        syx_output = str(Path(args.audio_file).with_suffix('.syx'))
    
    # Exécute le pipeline
    cli = MagicstompCLI()
    success = cli.run_pipeline(
        audio_file=args.audio_file,
        json_output=json_output,
        syx_output=syx_output,
        patch_number=args.patch,
        send_to_device=args.send,
        json_only=args.json_only,
        verbose=args.verbose
    )
    
    if success:
        print("\n🎸 Patch Magicstomp prêt!")
        
        # Affiche les fichiers générés
        if json_output and Path(json_output).exists():
            print(f"   📄 JSON: {json_output}")
        if syx_output and Path(syx_output).exists():
            print(f"   🎛️  SysEx: {syx_output}")
        if args.send:
            print(f"   📤 Envoyé vers device (patch #{args.patch})")
    else:
        print("\n❌ Pipeline échoué")
        sys.exit(1)


if __name__ == "__main__":
    main()
