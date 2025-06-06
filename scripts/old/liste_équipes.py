# 📌 Ce script récupère l'historique complet des franchises NBA (actives et anciennes)
import pandas as pd
from nba_api.stats.endpoints import FranchiseHistory

# Récupération des données
franchises = FranchiseHistory().get_data_frames()[0]

# Sélection et renommage des colonnes utiles
df_equipes = franchises[["TEAM_ID", "TEAM_NAME", "ABBREVIATION"]].drop_duplicates()
df_equipes.columns = ["id", "nom", "abréviation"]

# Tri pour lisibilité
df_equipes = df_equipes.sort_values(by="nom")

# Export CSV
df_equipes.to_csv("../nba_data/brut/teams.csv", index=False, encoding='utf-8')

print("✅ teams.csv généré avec succès !")
