# ==========================================
# 🗓️ Script d’extraction final du calendrier NBA
# Utilise uniquement les colonnes présentes dans ScheduleLeagueV2
# ==========================================

import os
import pandas as pd
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2
from dateutil import parser
from time import sleep
import pytz

# 📅 Saison à saisir manuellement
# saison = input("👉 Entrez la saison NBA au format 'YYYY-YY' (ex : 2024-25) : ").strip()
league_id = "00"

print(f"⏳ Récupération du calendrier pour la saison ...")
try:
    sleep(1)
    calendrier = ScheduleLeagueV2(season="2024-25", league_id=league_id)
    df = calendrier.get_data_frames()[0]
except Exception as e:
    print("❌ Erreur lors de l’appel à l’API :", e)
    exit()

# 🕒 Conversion UTC vers date/heure Paris
def convertir_heure_paris(utc_string):
    try:
        if not utc_string or pd.isna(utc_string):
            return "", ""
        dt_utc = parser.isoparse(utc_string)  # gère le Z
        dt_paris = dt_utc.astimezone(pytz.timezone("Europe/Paris"))
        date = dt_paris.strftime("%d/%m/%y")   # JJ/MM/AA
        heure = dt_paris.strftime("%H:%M")     # 24h
        return date, heure
    except Exception:
        return "", ""


# Conversion UTC → heure Paris
df["date_paris"], df["heure_paris"] = zip(*df["gameDateTimeUTC"].map(convertir_heure_paris))


# ✅ Sélection + renommage des colonnes utiles uniquement
colonnes_utiles = {
    "seasonYear": "Saison",
    "date_paris": "Date",
    "heure_paris": "Heure",
    "gameStatusText": "Statut Match",
    "gameId": "gameId",
    "gameLabel": "Compétition ",
    "gameSubLabel": "Détail Compétition",
    "seriesGameNumber": "# Match Série",
    "seriesText": "Détail Série",
    "ifNecessary": "Si Nécessaire",
    "arenaName": "Salle",
    "arenaCity": "Ville_salle",
    "arenaState": "Etat_salle",
    "gameSubtype": "évènement",
    "homeTeam_teamId": "id_team_domicile",
    "awayTeam_teamId": "id_team_extérieure",
    "homeTeam_teamName": "équipe_domicile",
    "awayTeam_teamName": "équipe_extérieure",
    "homeTeam_teamCity": "ville_domicile",
    "awayTeam_teamCity": "ville_extérieure",
    "homeTeam_teamTricode": "tricode_domicile",
    "awayTeam_teamTricode": "tricode_exterieur",
    "homeTeam_score": "score_domicile",
    "awayTeam_score": "score_exterieur",
    "gameDateTimeUTC": "horodatage_utc",
}

# 🧼 Sélection robuste (ignore les colonnes manquantes si jamais)
colonnes_presentes = [col for col in colonnes_utiles.keys() if col in df.columns or col in ["date_paris", "heure_paris"]]
df_clean = df[colonnes_presentes].rename(columns=colonnes_utiles)

# 💾 Export final
dossier_export = "data/processed/calendrier"
os.makedirs(dossier_export, exist_ok=True)
chemin_export = os.path.join(dossier_export, f"calendrier_saison.csv")
df_clean.to_csv(chemin_export, index=False)
# df.to_csv(chemin_export, index=False)

print(f"✅ Calendrier exporté : {chemin_export}")
