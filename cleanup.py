#!/usr/bin/env python3
"""
Script de nettoyage pour le pipeline Magicstomp
==============================================

Supprime les fichiers temporaires et de test générés.
"""

import os
from pathlib import Path


def cleanup_files():
    """Nettoie les fichiers temporaires et de test."""
    print("🧹 Nettoyage des fichiers temporaires...")
    
    # Fichiers à supprimer
    cleanup_patterns = [
        "*.wav",           # Fichiers audio de test
        "*.json",          # Fichiers JSON de test
        "*.syx",           # Fichiers SysEx de test
        "__pycache__",     # Cache Python
        "*.pyc",           # Bytecode Python
        "*.pyo",           # Bytecode optimisé
    ]
    
    # Dossiers à nettoyer
    cleanup_dirs = [
        "__pycache__",
        "cli/__pycache__",
    ]
    
    removed_files = []
    removed_dirs = []
    
    # Supprime les fichiers selon les patterns
    for pattern in cleanup_patterns:
        if "*" in pattern:
            # Pattern avec wildcard
            import glob
            for file_path in glob.glob(pattern):
                if Path(file_path).is_file():
                    try:
                        Path(file_path).unlink()
                        removed_files.append(file_path)
                    except Exception as e:
                        print(f"⚠️  Impossible de supprimer {file_path}: {e}")
        else:
            # Fichier spécifique
            if Path(pattern).exists():
                try:
                    Path(pattern).unlink()
                    removed_files.append(pattern)
                except Exception as e:
                    print(f"⚠️  Impossible de supprimer {pattern}: {e}")
    
    # Supprime les dossiers
    for dir_path in cleanup_dirs:
        if Path(dir_path).exists():
            try:
                import shutil
                shutil.rmtree(dir_path)
                removed_dirs.append(dir_path)
            except Exception as e:
                print(f"⚠️  Impossible de supprimer {dir_path}: {e}")
    
    # Affiche le résumé
    if removed_files or removed_dirs:
        print("✅ Nettoyage terminé:")
        if removed_files:
            print(f"   📄 Fichiers supprimés: {len(removed_files)}")
            for file in removed_files:
                print(f"      - {file}")
        if removed_dirs:
            print(f"   📁 Dossiers supprimés: {len(removed_dirs)}")
            for dir in removed_dirs:
                print(f"      - {dir}")
    else:
        print("✅ Aucun fichier à nettoyer")


def show_project_structure():
    """Affiche la structure du projet après nettoyage."""
    print("\n📁 Structure du projet:")
    print("=" * 30)
    
    project_files = [
        "analyze2json.py",
        "adapter_magicstomp.py", 
        "cli/analyze2stomp.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "TECHNICAL.md",
        "setup.py",
        "quick_start.py",
        "example_usage.py",
        "test_pipeline.py",
        "cleanup.py"
    ]
    
    for file_path in project_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"   ✅ {file_path} ({size} bytes)")
        else:
            print(f"   ❌ {file_path} (manquant)")


def main():
    """Point d'entrée principal."""
    print("🧹 Script de nettoyage - Pipeline Magicstomp")
    print("=" * 50)
    
    # Demande confirmation
    try:
        response = input("Supprimer les fichiers temporaires? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            cleanup_files()
        else:
            print("❌ Nettoyage annulé")
    except KeyboardInterrupt:
        print("\n❌ Nettoyage annulé")
        return
    
    # Affiche la structure
    show_project_structure()
    
    print("\n📋 Prochaines étapes:")
    print("   1. Installez les dépendances: pip install -r requirements.txt")
    print("   2. Testez avec: python quick_start.py your_audio.wav")
    print("   3. Consultez README.md pour plus d'informations")


if __name__ == "__main__":
    main()
