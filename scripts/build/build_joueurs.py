# ======================================
# 📥 Récupération de la liste complète des joueurs NBA (nba_api) avec URL photo
# ======================================
# Ce script extrait tous les joueurs (actuels et historiques) depuis nba_api et exporte en CSV.
# Ajout d'une colonne 'url_photo' pour chaque joueur.

import pandas as pd
import os
from nba_api.stats.static import players
import pathlib

racine = pathlib.Path(__file__).resolve().parents[2]

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
colonnes_existe = {k: v for k, v in noms_colonnes.items() if k in df_joueurs.columns}
df_joueurs = df_joueurs.rename(columns=colonnes_existe)

# ===============================
# 3. Ajout de la colonne URL photo officielle NBA
# ===============================
def generer_url_photo(id_joueur):
    return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{id_joueur}.png"


df_joueurs["url_photo"] = df_joueurs["id_joueur"].apply(generer_url_photo)

# ===============================
# 4. Export en CSV
# ===============================
chemin_export = os.path.join(racine, "data", "processed", "static")
fichier_sortie = os.path.join(chemin_export, "joueurs_liste_nba.csv")
df_joueurs.to_csv(fichier_sortie, index=False, encoding="utf-8")

print(f"✅ {len(df_joueurs)} joueurs exportés dans {chemin_export}")