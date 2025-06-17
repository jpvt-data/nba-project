"""
Script corrigé pour générer equipes.csv sans erreur.
Inclut : team_id, abbreviation, name, city, state, full_name
"""

import pandas as pd
from nba_api.stats.static import teams

# Récupérer les équipes NBA actuelles
liste_equipes = teams.get_teams()
df_equipes = pd.DataFrame(liste_equipes)

# Colonnes disponibles : ['id', 'full_name', 'abbreviation', 'nickname', 'city', 'state', 'year_founded']
df_equipes = df_equipes[['id', 'abbreviation', 'full_name', 'nickname', 'city', 'state']]
df_equipes.columns = ['team_id', 'abbreviation', 'name', 'nickname', 'city', 'state']

# Tri
df_equipes = df_equipes.sort_values(by='name')

# Export
df_equipes.to_csv("./nba_data/brut/equipes.csv", index=False, encoding="utf-8")
print(f"✅ {len(df_equipes)} équipes enregistrées dans ./nba_data/brut/equipes.csv")
