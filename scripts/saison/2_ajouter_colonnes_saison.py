# ===========================================================
# 📄 Script : ajouter_colonnes_saison_playoffs.py
# 🎯 Objectif : Ajouter "Saison" (ex : 2014-2015) et "Année" (ex : 2015)
#              à tous les fichiers CSV dans data/raw/saison/
# 📦 Sauvegarde dans data/processed/saison/
# ===========================================================

import os
import pandas as pd
import re

# 📁 Dossiers
dossier_source = "data/raw/saison"
dossier_sortie = "data/processed/saison"
os.makedirs(dossier_sortie, exist_ok=True)

# 🔁 Parcours des fichiers CSV dans le dossier source
for nom_fichier in os.listdir(dossier_source):
    if nom_fichier.endswith(".csv"):
        # 🎯 Recherche du SeasonID (5 chiffres), puis extraction des 4 derniers pour obtenir l'année
        match = re.search(r"_(\d{5})_", nom_fichier)
        if match:
            season_id = match.group(1)
            annee = int(season_id[-4:])  # ex : "21983" → 1983, "22014" → 2014
            saison_label = f"{annee}-{annee + 1}"
            annee_fin = annee + 1

            # 📄 Chargement
            chemin_fichier = os.path.join(dossier_source, nom_fichier)
            df = pd.read_csv(chemin_fichier)

            # ➕ Insertion des colonnes
            df.insert(0, "Saison", saison_label)
            df.insert(1, "Année", annee_fin)

            # 💾 Sauvegarde
            chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
            df.to_csv(chemin_sortie, index=False, encoding="utf-8")

            print(f"✅ {nom_fichier} → {chemin_sortie}")
        else:
            print(f"⚠️ Aucun SeasonID trouvé dans : {nom_fichier}")
