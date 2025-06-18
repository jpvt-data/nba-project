# ===========================================================
# 📄 Script : concatener_classement_conferences.py
# 🎯 Objectif : Fusionner tous les fichiers de classement
#              dans data/processed/saison/ en un seul CSV
# 📦 Résultat : data/processed/saison/classement_conf_saisons.csv
# ===========================================================

import os
import pandas as pd

# 📁 Dossier contenant les fichiers à concaténer
dossier_source = "data/processed/saison"
fichier_sortie = os.path.join(dossier_source, "classement_conf_saisons.csv")

# 🔍 Tous les fichiers CSV sauf le fichier final
fichiers_csv = [f for f in os.listdir(dossier_source)
                if f.endswith(".csv") and f != "classement_conf_saisons.csv"]

# 🧱 Chargement et concaténation
df_concat = pd.concat(
    [pd.read_csv(os.path.join(dossier_source, fichier)) for fichier in fichiers_csv],
    ignore_index=True
)

# 💾 Enregistrement du fichier final
df_concat.to_csv(fichier_sortie, index=False, encoding="utf-8")
print(f"✅ Fichier concaténé sauvegardé : {fichier_sortie}")
