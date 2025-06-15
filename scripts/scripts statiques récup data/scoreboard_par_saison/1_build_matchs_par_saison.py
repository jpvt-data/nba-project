"""
Script de récupération des matchs NBA (via scoreboardv3)
Stocke les données brutes JSON par saison NBA (ex : saison_2024_2025.json)
Testable sur un intervalle de dates réduit.
"""

import requests
import os
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict

# 📁 Dossier de sortie
DOSSIER_EXPORT = "data/raw"
os.makedirs(DOSSIER_EXPORT, exist_ok=True)

# 📬 Headers requis par stats.nba.com
HEADERS = {
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

# 🧪 À MODIFIER POUR TEST
DATE_DEBUT = "1946-09-01"
DATE_FIN = "1947-08-31"

# 🧠 Convertit une date en saison NBA (format YYYY_YYYY)
def saison_from_date(date_obj):
    annee = date_obj.year
    if date_obj.month >= 9:  # Septembre à Décembre
        return f"{annee}_{annee + 1}"
    else:  # Janvier à Août
        return f"{annee - 1}_{annee}"

# 📅 Génération de la liste de dates à traiter
date_debut = datetime.strptime(DATE_DEBUT, "%Y-%m-%d")
date_fin = datetime.strptime(DATE_FIN, "%Y-%m-%d")
dates = [date_debut + timedelta(days=i) for i in range((date_fin - date_debut).days + 1)]

# 🏗️ Dictionnaire : { saison : [matchs] }
matchs_par_saison = defaultdict(list)

# 🔁 Boucle principale
for date_obj in dates:
    date_str = date_obj.strftime("%Y-%m-%d")
    saison_id = saison_from_date(date_obj)
    url = f"https://stats.nba.com/stats/scoreboardv3?GameDate={date_str}&LeagueID=00"

    try:
        response = requests.get(url, headers=HEADERS, timeout=60)
        response.raise_for_status()
        games = response.json().get("scoreboard", {}).get("games", [])
        if games:
            matchs_par_saison[saison_id].extend(games)
            print(f"✅ {date_str} ({saison_id}) : {len(games)} matchs")
        else:
            print(f"➖ {date_str} : aucun match")
    except Exception as e:
        print(f"⚠️ Erreur pour {date_str} : {e}")

    time.sleep(1.5)

# 💾 Écriture des fichiers JSON par saison
for saison, matchs in matchs_par_saison.items():
    chemin = os.path.join(DOSSIER_EXPORT, f"saison_{saison}.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(matchs, f, indent=2, ensure_ascii=False)
    print(f"📁 Exporté : {chemin} ({len(matchs)} matchs)")

print("✅ Récupération terminée.")
