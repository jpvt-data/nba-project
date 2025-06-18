# =====================================================
# 📂 Script : json_scoreboard_vers_csv_par_saison.py
# 🔧 Objectif : Transformer tous les fichiers JSON
#              scoreboard d'une saison NBA en CSV
#              avec colonnes "Saison" et "Année"
# =====================================================

import os
import json
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# 📁 Dossiers d'entrée et de sortie
dossier_source = "data/raw"
dossier_sortie = "data/processed/scoreboard"
os.makedirs(dossier_sortie, exist_ok=True)

# 🔁 Parcours des fichiers JSON correspondant à une saison
for fichier in os.listdir(dossier_source):
    if fichier.startswith("saison_") and fichier.endswith(".json"):
        try:
            # 🧠 Extraire les années depuis le nom de fichier
            parties = fichier.replace("saison_", "").replace(".json", "").split("_")
            saison_debut, saison_fin = parties[0], parties[1]
            label_saison = f"{saison_debut}-{saison_fin}"
            annee_fin = int(saison_fin)

            # 📥 Charger le JSON
            chemin_json = os.path.join(dossier_source, fichier)
            with open(chemin_json, encoding="utf-8") as f:
                data = json.load(f)

            # 📦 Extraire les matchs
            matchs = []
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
                        "Saison": label_saison,
                        "Année": annee_fin,
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

            # 📄 Création du DataFrame
            df = pd.DataFrame(matchs)

            # 💾 Export du CSV
            nom_csv = f"scoreboard_{label_saison}.csv"
            chemin_sortie = os.path.join(dossier_sortie, nom_csv)
            df.to_csv(chemin_sortie, index=False, encoding="utf-8")
            print(f"✅ {nom_csv} généré avec {len(df)} matchs")

        except Exception as e:
            print(f"❌ Erreur avec le fichier {fichier} : {e}")
