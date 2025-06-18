# =====================================================
# 📂 Script : ajout_colonnes_saison_annee.py
# 🔧 Objectif : Ajouter les colonnes "Saison" et "Année"
#              à tous les fichiers matchs_XXXX_YYYY.csv
#              et sauvegarder dans processed/scoreboard/
# =====================================================

import os
import pandas as pd

# 📁 Chemins d'accès
dossier_source = "data/raw"
dossier_sortie = "data/processed/scoreboard"

# ✅ Création du dossier de sortie s'il n'existe pas
os.makedirs(dossier_sortie, exist_ok=True)

# 🔍 Boucle sur tous les fichiers CSV correspondants
for nom_fichier in os.listdir(dossier_source):
    if nom_fichier.startswith("matchs_") and nom_fichier.endswith(".csv"):
        try:
            # 🧠 Extraction des années depuis le nom de fichier
            parties = nom_fichier.replace("matchs_", "").replace(".csv", "").split("_")
            saison_debut, saison_fin = parties[0], parties[1]
            label_saison = f"{saison_debut}-{saison_fin}"
            annee_fin = int(saison_fin)

            # 📥 Chargement du fichier
            chemin_fichier = os.path.join(dossier_source, nom_fichier)
            df = pd.read_csv(chemin_fichier)

            # ➕ Insertion des colonnes au début du DataFrame
            df.insert(0, "Saison", label_saison)
            df.insert(1, "Année", annee_fin)

            # 💾 Sauvegarde du nouveau fichier
            nom_sortie = f"scoreboard_{label_saison}.csv"
            chemin_sortie = os.path.join(dossier_sortie, nom_sortie)
            df.to_csv(chemin_sortie, index=False)

            print(f"✅ Fichier traité : {nom_fichier} → {nom_sortie}")

        except Exception as e:
            print(f"❌ Erreur avec le fichier {nom_fichier} : {e}")
