# ======================================
# 📥 Récupération de la liste complète des équipes NBA (nba_api)
# ======================================
# Ce script extrait toutes les équipes (actuelles et historiques) depuis nba_api et exporte en CSV.
# Les noms des colonnes sont traduits en français, le chemin d’export respecte la structure du projet.

import os
import pandas as pd
from nba_api.stats.static import teams

# ===============================
# 1. Variables de chemin
# ===============================
import pathlib
racine = pathlib.Path(__file__).resolve().parents[2]
chemin_export = os.path.join(racine, "data", "processed", "static")
os.makedirs(chemin_export, exist_ok=True)
fichier_sortie = os.path.join(chemin_export, "equipes_liste_nba.csv")

# ===============================
# 2. Récupération des équipes
# ===============================
equipes = teams.get_teams()
df_equipes = pd.DataFrame(equipes)

# ===============================
# 3. Renommage des colonnes en français
# ===============================
noms_colonnes = {
    'id': 'id_equipe',
    'full_name': 'nom_complet',
    'abbreviation': 'abbreviation',
    'nickname': 'surnom',
    'city': 'ville',
    'state': 'etat',
    'year_founded': 'annee_fondation'
}
colonnes_existe = {k: v for k, v in noms_colonnes.items() if k in df_equipes.columns}
df_equipes = df_equipes.rename(columns=colonnes_existe)

# ===============================
# 4. Génération de l'URL du logo officiel NBA
# ===============================
def generer_url_logo(id_equipe):
    return f"https://cdn.nba.com/logos/nba/{id_equipe}/global/L/logo.svg"


df_equipes["url_logo"] = df_equipes["id_equipe"].apply(generer_url_logo)

# ===============================
# 5. Export en CSV
# ===============================
df_equipes.to_csv(fichier_sortie, index=False, encoding="utf-8")
print(f"✅ {len(df_equipes)} équipes exportées dans {fichier_sortie} (avec url_logo)")