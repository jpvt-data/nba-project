from nba_api.stats.endpoints import FranchiseHistory
import pandas as pd

# Charger le fichier palmarès
df_palmares = pd.read_csv("./data/palmares.csv")  # adapte le chemin si besoin

# Récupérer toutes les franchises historiques
df_franchises = FranchiseHistory().get_data_frames()[0]

# Garde uniquement les colonnes valides
df_franchises = df_franchises[['TEAM_ID', 'TEAM_NAME']].drop_duplicates()

# Fusion avec le palmarès
df_enrichi = df_palmares.merge(df_franchises, on='TEAM_ID', how='left')

# Export du fichier enrichi
df_enrichi.to_csv("./data/palmares_enrichi.csv", index=False, encoding="utf-8")
print("✅ Fichier enrichi avec les noms d'équipe généré : 'palmares_enrichi.csv'")
