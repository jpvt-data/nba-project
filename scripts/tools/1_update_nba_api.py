# ======================================
# 🔁 Mise à jour quotidienne des données NBA (matchs uniquement)
# ======================================

import requests
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import time

# 📁 Chemin vers le fichier CSV principal
import pathlib
racine = pathlib.Path(__file__).resolve().parents[2]
fichier_matchs_csv = os.path.join(racine, "data", "processed", "matchs.csv")
print(f"📁 Chargement du fichier : {fichier_matchs_csv}")

# 📅 Plage de dates à mettre à jour : de la veille jusqu'au 31 août
aujourd_hui = datetime.now()
date_debut_matchs = (aujourd_hui - timedelta(days=7)).date()
date_fin_matchs = datetime(2025, 12, 31).date()
dates_matchs = pd.date_range(date_debut_matchs, date_fin_matchs)
print(f"📆 Intervalle de dates : {date_debut_matchs} → {date_fin_matchs} ({len(dates_matchs)} jours)")

# 📬 Headers API NBA (obligatoires)
headers_api_nba = {
    "Host": "stats.nba.com",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "x-nba-stats-token": "true",
    "User-Agent": "Mozilla/5.0",
    "x-nba-stats-origin": "stats",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}

# 📥 Chargement ou création du DataFrame
if os.path.exists(fichier_matchs_csv):
    print("📖 Lecture du fichier existant...")
    df_matchs = pd.read_csv(fichier_matchs_csv, dtype={"gameId": str})
else:
    print("⚠️ Aucun fichier trouvé. Création d'un DataFrame vide.")
    df_matchs = pd.DataFrame()

df_matchs["gameId"] = df_matchs["gameId"].astype(str)
matchs_a_inserer = []

# 🔁 Boucle sur chaque jour
for jour in dates_matchs:
    date_str = jour.strftime("%Y-%m-%d")
    print(f"\n🔎 Récupération des matchs pour le {date_str}")
    url = f"https://stats.nba.com/stats/scoreboardv3?GameDate={date_str}&LeagueID=00"

    try:
        reponse_api = requests.get(url, headers=headers_api_nba, timeout=20)
        reponse_api.raise_for_status()
        matchs_du_jour = reponse_api.json().get("scoreboard", {}).get("games", [])
        print(f"   📦 {len(matchs_du_jour)} match(s) trouvé(s)")

        for match in matchs_du_jour:
            game_id = str(match.get("gameId")).zfill(9)
            game_et = match.get("gameEt")
            date_paris = heure_paris = "?"
            if game_et:
                dt_et = datetime.strptime(game_et, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("America/New_York"))
                dt_fr = dt_et.astimezone(ZoneInfo("Europe/Paris"))
                date_paris = dt_fr.strftime("%Y-%m-%d")
                heure_paris = dt_fr.strftime("%H:%M")

            donnees_match = {
                "gameId": game_id,
                "gameCode": match.get("gameCode"),
                "gameStatusText": match.get("gameStatusText"),
                "dateParis": date_paris,
                "heureParis": heure_paris,
                "homeTeamId": match.get("homeTeam", {}).get("teamId"),
                "homeTeamTricode": match.get("homeTeam", {}).get("teamTricode"),
                "homeTeamScore": match.get("homeTeam", {}).get("score"),
                "awayTeamId": match.get("awayTeam", {}).get("teamId"),
                "awayTeamTricode": match.get("awayTeam", {}).get("teamTricode"),
                "awayTeamScore": match.get("awayTeam", {}).get("score"),
                "seriesGameNumber": match.get("seriesGameNumber"),
                "gameLabel": match.get("gameLabel"),
                "poRoundDesc": match.get("poRoundDesc"),
                "ifNecessary": match.get("ifNecessary")
            }

            matchs_a_inserer.append(donnees_match)

        time.sleep(1)

    except Exception as e:
        print(f"❌ Erreur API pour {date_str} : {e}")
        continue

# 🧹 Suppression des doublons à remplacer
ids_a_remplacer = [m["gameId"] for m in matchs_a_inserer]
df_matchs = df_matchs[~df_matchs["gameId"].isin(ids_a_remplacer)]

# ➕ Ajout des matchs mis à jour
if matchs_a_inserer:
    df_matchs_nouveaux = pd.DataFrame(matchs_a_inserer)
    df_matchs = pd.concat([df_matchs, df_matchs_nouveaux], ignore_index=True)
    print(f"\n✅ {len(df_matchs_nouveaux)} match(s) ajouté(s) ou mis à jour.")
else:
    print("\nℹ️ Aucun match à ajouter ou mettre à jour.")

# 💾 Enregistrement final
os.makedirs(os.path.dirname(fichier_matchs_csv), exist_ok=True)
df_matchs.to_csv(fichier_matchs_csv, index=False, encoding="utf-8")
print(f"\n📁 Fichier sauvegardé : {fichier_matchs_csv} ({len(df_matchs)} lignes)")

# ===========================================================
# 📦 Téléchargement du tableau des playoffs via nba_api
# Permet de spécifier un ou plusieurs SeasonID et LeagueID
# Données sauvegardées dans data/raw/playoffs/
# ===========================================================

from nba_api.stats.endpoints import playoffpicture
import pandas as pd
import os

# 🔢 Liste des SeasonID (exemples : 2024-25 → "2024" = 22024)
saison_debut = 2025
saison_fin = 2026

# La formule : season_id = 20000 + année de fin de saison
season_ids = [str(20000 + annee) for annee in range(saison_debut, saison_fin)]
league_ids = ["00"]     # "00" = NBA, "10" = WNBA, "20" = G-League
league_id = ""
season_id = ""

# 📁 Dossier de sauvegarde
dossier_sortie = os.path.join(racine, "data", "raw", "saison", season_id)
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

# ===========================================================
# 📄 Script : ajouter_colonnes_saison_playoffs.py
# 🎯 Objectif : Ajouter "Saison" (ex : 2014-2015) et "Année" (ex : 2015)
#              à tous les fichiers CSV dans data/raw/saison/
# 📦 Sauvegarde dans data/processed/saison/
# ===========================================================

import os
import pandas as pd
import re

# 📁 Dossiers
dossier_source = os.path.join(racine, "data", "raw", "saison")
dossier_sortie = os.path.join(racine, "data", "processed", "saison")
os.makedirs(dossier_sortie, exist_ok=True)

# 🔁 Parcours des fichiers CSV dans le dossier source
for nom_fichier in os.listdir(dossier_source):
    if nom_fichier.endswith(".csv"):
        # 🎯 Recherche du SeasonID (5 chiffres), puis extraction des 4 derniers pour obtenir l'année
        match = re.search(r"_(\d{5})_", nom_fichier)
        if match:
            season_id = match.group(1)
            annee = int(season_id[-4:])  # ex : "21983" → 1983, "22014" → 2014
            saison_label = f"{annee}-{annee + 1}"
            annee_fin = annee + 1

            # 📄 Chargement
            chemin_fichier = os.path.join(dossier_source, nom_fichier)
            df = pd.read_csv(chemin_fichier)

            # ➕ Insertion des colonnes
            df.insert(0, "Saison", saison_label)
            df.insert(1, "Année", annee_fin)

            # 💾 Sauvegarde
            chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
            df.to_csv(chemin_sortie, index=False, encoding="utf-8")

            print(f"✅ {nom_fichier} → {chemin_sortie}")
        else:
            print(f"⚠️ Aucun SeasonID trouvé dans : {nom_fichier}")

# ===========================================================
# 📄 Script : concatener_classement_conferences.py
# 🎯 Objectif : Fusionner tous les fichiers de classement
#              dans data/processed/saison/ en un seul CSV
# 📦 Résultat : data/processed/saison/classement_conf_saisons.csv
# ===========================================================

import os
import pandas as pd

# 📁 Dossier contenant les fichiers à concaténer
dossier_source = os.path.join(racine, "data", "processed", "saison")
fichier_sortie = os.path.join(dossier_source, "classement_conf_saisons_total.csv")

# 📥 Chargement du fichier existant (s’il existe)
if os.path.exists(fichier_sortie):
    df_existant = pd.read_csv(fichier_sortie)
    print(f"📄 Ancien fichier chargé : {len(df_existant)} lignes")
else:
    df_existant = pd.DataFrame()
    print("⚠️ Aucun fichier existant trouvé, on crée un nouveau total.")

# 📂 Liste des fichiers à ajouter (tous les CSV sauf le fichier final lui-même)
fichiers_csv = [
    f for f in os.listdir(dossier_source)
    if f.endswith(".csv") and f != os.path.basename(fichier_sortie)
]

# 📥 Chargement des nouveaux fichiers
df_nouveaux = pd.concat(
    [pd.read_csv(os.path.join(dossier_source, f)) for f in fichiers_csv],
    ignore_index=True
)

# 🧹 Suppression des doublons potentiels (sur gameId ou autre critère si pertinent)
df_total = pd.concat([df_existant, df_nouveaux], ignore_index=True).drop_duplicates()

# 💾 Sauvegarde dans le fichier total
df_total.to_csv(fichier_sortie, index=False, encoding="utf-8")
print(f"✅ Fichier concaténé mis à jour : {fichier_sortie} ({len(df_total)} lignes totales)")

