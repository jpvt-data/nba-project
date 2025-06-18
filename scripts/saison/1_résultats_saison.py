# ===========================================================
# 📦 Téléchargement du tableau des playoffs via nba_api
# Permet de spécifier un ou plusieurs SeasonID et LeagueID
# Données sauvegardées dans data/raw/playoffs/
# ===========================================================

from nba_api.stats.endpoints import playoffpicture
import pandas as pd
import os

# 🔢 Liste des SeasonID (exemples : 2024-25 → "2024" = 22024)
saison_debut = 1970
saison_fin = 2026

# La formule : season_id = 20000 + année de fin de saison
season_ids = [str(20000 + annee) for annee in range(saison_debut, saison_fin)]
league_ids = ["00"]     # "00" = NBA, "10" = WNBA, "20" = G-League
league_id = ""
season_id = ""

# 📁 Dossier de sauvegarde
dossier_sortie = f"data/raw/saison/{season_id}"
os.makedirs(dossier_sortie, exist_ok=True)

# 🔁 Boucle sur chaque combinaison SeasonID × LeagueID
for season_id in season_ids:
    for league_id in league_ids:
        print(f"🔄 Récupération standings : SeasonID = {season_id}, LeagueID = {league_id}")

        try:
            # 📥 Appel API PlayoffPicture
            pp = playoffpicture.PlayoffPicture(season_id=season_id, league_id=league_id)

            # 📊 Récupération des 2 standings
            df_east = pp.east_conf_standings.get_data_frame()
            df_west = pp.west_conf_standings.get_data_frame()

            # 💾 Sauvegarde
            fichier_est = f"EastConfStandings_{season_id}_{league_id}.csv"
            fichier_ouest = f"WestConfStandings_{season_id}_{league_id}.csv"

            df_east.to_csv(os.path.join(dossier_sortie, fichier_est), index=False, encoding="utf-8")
            df_west.to_csv(os.path.join(dossier_sortie, fichier_ouest), index=False, encoding="utf-8")

            print(f"✅ Sauvegardé : {fichier_est} + {fichier_ouest}")

        except Exception as e:
            print(f"❌ Erreur SeasonID {season_id}, LeagueID {league_id} : {e}")