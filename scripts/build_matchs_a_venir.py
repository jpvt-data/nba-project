# ======================================
# 🏗️ Export enrichi des matchs à venir via ScoreboardV3 (NBA Stats)
# ======================================

import requests
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import time

# 📁 Création du dossier d'export
os.makedirs("data", exist_ok=True)

# 📅 Jours à interroger (14 jours)
aujourd_hui = datetime.today()
jours = [aujourd_hui + timedelta(days=i) for i in range(14)]

# 🧱 Configuration de la requête
headers = {
    "Host": "stats.nba.com",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "x-nba-stats-token": "true",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "x-nba-stats-origin": "stats",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}

# 📦 Stockage des données extraites
matchs_extraits = []

for jour in jours:
    date_str = jour.strftime("%Y-%m-%d")
    url = f"https://stats.nba.com/stats/scoreboardv3?GameDate={date_str}&LeagueID=00"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        games = response.json().get("scoreboard", {}).get("games", [])

        for game in games:
            game_et = game.get("gameEt")
            date_paris = "?"
            heure_paris = "?"

            try:
                # 🕒 Interpréter game_et comme ET (UTC−4) et convertir en heure Paris (UTC+2)
                dt_et = datetime.strptime(game_et, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("America/New_York"))
                dt_fr = dt_et.astimezone(ZoneInfo("Europe/Paris"))
                date_paris = dt_fr.strftime("%Y-%m-%d")
                heure_paris = dt_fr.strftime("%H:%M")
            except:
                pass

            match_info = {
                "game_id": game.get("gameId"),
                "game_time_utc": game.get("gameTimeUTC"),
                "game_et": game_et,
                "date_paris": date_paris,
                "heure_paris": heure_paris,
                "game_status_text": game.get("gameStatusText"),
                "series_game_number": game.get("seriesGameNumber"),
                "game_label": game.get("gameLabel"),
                "game_sub_label": game.get("gameSubLabel"),
                "if_necessary": game.get("ifNecessary"),
                "series_conference": game.get("seriesConference"),
                "po_round_desc": game.get("poRoundDesc"),
                "game_subtype": game.get("gameSubtype"),
                "is_neutral": game.get("isNeutralVenue"),
                "home_team_id": game.get("homeTeam", {}).get("teamId"),
                "home_team_tricode": game.get("homeTeam", {}).get("teamTricode"),
                "away_team_id": game.get("awayTeam", {}).get("teamId"),
                "away_team_tricode": game.get("awayTeam", {}).get("teamTricode"),
                "team_leaders": game.get("teamLeaders")
            }
            matchs_extraits.append(match_info)

        print(f"✅ Données récupérées pour {date_str}")

    except Exception as e:
        print(f"❌ Erreur pour {date_str} : {e}")

    time.sleep(1)

# 💾 Export CSV
df = pd.DataFrame(matchs_extraits)
df.to_csv("data/matchs_a_venir.csv", index=False, encoding="utf-8")
print("📁 Export terminé : data/matchs_a_venir.csv")
