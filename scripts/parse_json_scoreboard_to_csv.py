"""
Script de transformation du fichier JSON brut scoreboardv3
en CSV global contenant tous les matchs de la saison NBA.
Inclut : horaires en heure Paris, scores, statuts, équipes, etc.
"""

import json
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import os

# 📂 Chemins d'entrée/sortie
chemin_json = "data/raw/saison_2024_2025.json"
chemin_csv = "data/processed/matchs.csv"

# 📥 Chargement du JSON brut
with open(chemin_json, encoding="utf-8") as f:
    data = json.load(f)

# 📦 Stockage des lignes de match
matchs = []

# 🔁 Boucle sur les matchs
for game in data:
    try:
        game_et = game.get("gameEt")
        date_paris, heure_paris = "?", "?"
        if game_et:
            dt_et = datetime.strptime(game_et, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("America/New_York"))
            dt_fr = dt_et.astimezone(ZoneInfo("Europe/Paris"))
            date_paris = dt_fr.strftime("%Y-%m-%d")
            heure_paris = dt_fr.strftime("%H:%M")

        matchs.append({
            "gameId": game.get("gameId"),
            "gameCode": game.get("gameCode"),
            "gameStatusText": game.get("gameStatusText"),
            "dateParis": date_paris,
            "heureParis": heure_paris,
            "homeTeamId": game.get("homeTeam", {}).get("teamId"),
            "homeTeamTricode": game.get("homeTeam", {}).get("teamTricode"),
            "homeTeamScore": game.get("homeTeam", {}).get("score"),
            "awayTeamId": game.get("awayTeam", {}).get("teamId"),
            "awayTeamTricode": game.get("awayTeam", {}).get("teamTricode"),
            "awayTeamScore": game.get("awayTeam", {}).get("score"),
            "seriesGameNumber": game.get("seriesGameNumber"),
            "gameLabel": game.get("gameLabel"),
            "poRoundDesc": game.get("poRoundDesc"),
            "ifNecessary": game.get("ifNecessary")
        })

    except Exception as e:
        print(f"⚠️ Erreur match {game.get('gameId')} : {e}")

# 📄 Conversion en DataFrame
df = pd.DataFrame(matchs)

# 📁 Création du dossier si besoin
os.makedirs(os.path.dirname(chemin_csv), exist_ok=True)

# 💾 Export CSV
df.to_csv(chemin_csv, index=False, encoding="utf-8")
print(f"✅ Fichier CSV généré : {chemin_csv} ({len(df)} matchs)")
