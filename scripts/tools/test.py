# ======================================
# 🧪 Script de test pour l'API NBA Scoreboard
# ======================================

import requests
from datetime import datetime
import time

# 📅 Date à tester
date_test = "2025-06-27"
url = f"https://stats.nba.com/stats/scoreboardv3?GameDate={date_test}&LeagueID=00"

# 📬 Headers obligatoires pour l'API NBA
headers = {
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

# 🔁 Tentatives de connexion
max_tentatives = 3
for tentative in range(1, max_tentatives + 1):
    print(f"🔄 Tentative {tentative} de connexion à l'API...")
    try:
        reponse = requests.get(url, headers=headers, timeout=40)
        reponse.raise_for_status()
        json_data = reponse.json()
        matchs = json_data.get("scoreboard", {}).get("games", [])
        print(f"✅ Réponse OK : {len(matchs)} match(s) trouvé(s) pour le {date_test}")
        break
    except Exception as e:
        print(f"⚠️ Erreur : {e}")
        if tentative < max_tentatives:
            print("⏳ Nouvelle tentative dans 5 secondes...\n")
            time.sleep(5)
        else:
            print(f"❌ Échec de l'appel API après {max_tentatives} tentatives.")
