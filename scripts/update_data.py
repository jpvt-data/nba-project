# scripts/update_all.py
"""
Script d’orchestration du pipeline NBA.
Lance les modules de récupération de données, un par un.
"""

import subprocess

print("🔄 Mise à jour des données NBA en cours...")

try:
    subprocess.run(["python", "./scripts/build_joueurs.py"], check=True)
    print("✅ Mise à jour des joueurs terminée.")
except subprocess.CalledProcessError:
    print("❌ Erreur lors de la mise à jour des joueurs.")

try:
    subprocess.run(["python", "./scripts/build_equipes.py"], check=True)
    print("✅ Mise à jour des équipes terminée.")
except subprocess.CalledProcessError:
    print("❌ Erreur lors de la mise à jour des équipes.")

print("📦 Pipeline terminé.")
