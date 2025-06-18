# ===============================================
# 🏀 Script All-Time Leaders NBA - Regular & Playoffs
# ===============================================

# 📦 Imports
import os
import pandas as pd
from nba_api.stats.endpoints import AllTimeLeadersGrids

# 📁 Dossier de sortie
dossier_sortie = "data/raw/hall_of_fame"
os.makedirs(dossier_sortie, exist_ok=True)

# 🗂️ Types de saison
types_saison = {
    "Regular Season": "regular",
    "Playoffs": "playoffs"
}

# 🗂️ Liste des tableaux à récupérer
noms_tableaux = [
#
]

# 🔁 Boucle sur chaque type de saison
for libelle, suffixe in types_saison.items():
    print(f"📊 Traitement pour : {libelle}")

    # 🔧 Requête
    leaders = AllTimeLeadersGrids(
        league_id="00",
        per_mode_simple="Totals",
        season_type=libelle,
        topx=100
    )

    # 📥 Extraction brute
    datasets = leaders.get_dict()

    # 💾 Export CSVs
    for nom in noms_tableaux:
        df = pd.DataFrame(datasets[nom])
        nom_fichier = f"{nom.lower()}_{suffixe}.csv"
        chemin_csv = os.path.join(dossier_sortie, nom_fichier)
        df.to_csv(chemin_csv, index=False)
        print(f"✅ {nom_fichier} enregistré.")

print("🏁 Fin du script : All-Time Leaders enregistrés pour Regular + Playoffs.")
