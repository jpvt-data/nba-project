# ======================================
# 📥 Récupération de la liste complète des joueurs NBA (nba_api)
# ======================================
# Ce script extrait tous les joueurs (actuels et historiques) depuis nba_api et exporte en CSV.

import pandas as pd
from nba_api.stats.static import players

# ===============================
# 1. Récupération des joueurs
# ===============================
joueurs = players.get_players()
df_joueurs = pd.DataFrame(joueurs)

# ===============================
# 2. Renommage des colonnes en français
# ===============================
noms_colonnes = {
    'id': 'id_joueur',
    'full_name': 'nom_complet',
    'first_name': 'prenom',
    'last_name': 'nom',
    'is_active': 'actif'
}
# On ne renomme que si la colonne existe (compatibilité toutes versions)
colonnes_existe = {k: v for k, v in noms_colonnes.items() if k in df_joueurs.columns}
df_joueurs = df_joueurs.rename(columns=colonnes_existe)

# ===============================
# 3. Export en CSV
# ===============================
chemin_export = "data/processed/static/joueurs_liste_nba.csv"
df_joueurs.to_csv(chemin_export, index=False, encoding="utf-8")

print(f"✅ {len(df_joueurs)} joueurs exportés dans {chemin_export}")
