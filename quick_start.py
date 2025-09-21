#!/usr/bin/env python3
"""
Quick Start - Magicstomp Pipeline
================================

Script de démarrage rapide pour tester le pipeline avec des fichiers audio.
"""

import sys
import argparse
from pathlib import Path

# Ajoute le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from cli.analyze2stomp import MagicstompCLI


def main():
    """Point d'entrée pour démarrage rapide."""
    parser = argparse.ArgumentParser(
        description="Démarrage rapide du pipeline Magicstomp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python quick_start.py audio.wav
  python quick_start.py audio.wav --send
  python quick_start.py audio.wav --patch 5 --verbose
        """
    )
    
    parser.add_argument('audio_file', help='Fichier audio à analyser')
    parser.add_argument('--send', action='store_true', help='Envoyer vers Magicstomp')
    parser.add_argument('--patch', '-p', type=int, default=0, help='Numéro de patch')
    parser.add_argument('--verbose', '-v', action='store_true', help='Mode verbeux')
    
    args = parser.parse_args()
    
    # Vérifie que le fichier existe
    if not Path(args.audio_file).exists():
        print(f"❌ Fichier non trouvé: {args.audio_file}")
        sys.exit(1)
    
    print("🚀 Démarrage rapide - Pipeline Magicstomp")
    print("=" * 50)
    
    # Lance le pipeline
    cli = MagicstompCLI()
    success = cli.run_pipeline(
        audio_file=args.audio_file,
        patch_number=args.patch,
        send_to_device=args.send,
        verbose=args.verbose
    )
    
    if success:
        print("\n✅ Pipeline terminé avec succès!")
        if args.send:
            print(f"🎸 Patch envoyé vers Magicstomp (slot #{args.patch})")
        else:
            print("📁 Fichiers générés automatiquement")
    else:
        print("\n❌ Erreur dans le pipeline")
        sys.exit(1)


if __name__ == "__main__":
    main()
