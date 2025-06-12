# ======================================
# 📁 Lecture et transformation des matchs à venir (Scoreboard V3)
# Source : data/processed/matchs.csv (complet)
# ======================================

import pandas as pd
from datetime import datetime, timedelta

# 🇫🇷 Traduction manuelle des jours et mois (compatibilité Render)
jours_fr = {
    "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
    "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"
}
mois_fr = {
    "January": "janvier", "February": "février", "March": "mars",
    "April": "avril", "May": "mai", "June": "juin",
    "July": "juillet", "August": "août", "September": "septembre",
    "October": "octobre", "November": "novembre", "December": "décembre"
}

def get_matchs_7j():
    chemin_csv = "data/processed/matchs.csv"
    df = pd.read_csv(chemin_csv)

    # 🕒 Conversion datetime (heure locale Paris)
    df["datetime_paris"] = pd.to_datetime(df["dateParis"] + " " + df["heureParis"], format="%Y-%m-%d %H:%M")

    # 📆 Maintenant (heure locale)
    maintenant = datetime.now()

    # 🔍 Filtrage : uniquement matchs à venir dans les 7 jours
    df = df[(df["datetime_paris"] > maintenant) & 
            (df["datetime_paris"] <= maintenant + timedelta(days=14))]
    
    # Tri par date
    df = df.sort_values("datetime_paris")

    jours = []
    for date_jour, groupe in df.groupby(df["datetime_paris"].dt.date):
        date_obj = pd.to_datetime(date_jour)
        nom_jour = jours_fr[date_obj.strftime("%A")]
        nom_mois = mois_fr[date_obj.strftime("%B")]
        date_affichee = f"{nom_jour} {date_obj.day} {nom_mois}"

        matchs = []
        for _, row in groupe.iterrows():
            match = {
                "game_id": row["gameId"],
                "date": date_affichee,
                "heure": row["heureParis"],
                "home_id": row["homeTeamId"],
                "away_id": row["awayTeamId"],
                "home": row["homeTeamTricode"],
                "away": row["awayTeamTricode"],
                "series_game_number": row["seriesGameNumber"],
                "game_label": row["gameLabel"],
                "if_necessary": row["ifNecessary"]
            }
            matchs.append(match)

        jours.append({
            "date": date_affichee,
            "matchs": matchs
        })

    return jours
