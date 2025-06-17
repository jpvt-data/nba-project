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
date_debut_matchs = (aujourd_hui - timedelta(days=1)).date()
date_fin_matchs = datetime(2025, 8, 31).date()
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
