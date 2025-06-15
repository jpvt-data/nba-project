"""
Script de récupération des joueurs NBA (historiques et actuels)
Crée ou met à jour joueurs.csv dans le dossier /nba_data/brut
"""

import pandas as pd
from nba_api.stats.static import players

# Récupérer tous les joueurs (actuels + anciens)
joueurs = players.get_players()

# Transformation en DataFrame
df_joueurs = pd.DataFrame(joueurs)

# Ne garder que les colonnes utiles
df_joueurs = df_joueurs[['id', 'first_name', 'last_name']]
df_joueurs.columns = ['joueur_id', 'prenom', 'nom']

# Tri pour lisibilité
df_joueurs = df_joueurs.sort_values(by=['nom', 'prenom'])

# Export CSV
df_joueurs.to_csv("./nba_data/brut/joueurs.csv", index=False, encoding="utf-8")
print("✅ Fichier joueurs.csv généré avec succès.")
