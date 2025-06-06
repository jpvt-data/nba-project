# ======================================
# 📁 Lecture et transformation des matchs à venir (Scoreboard V3)
# ======================================

import pandas as pd
from datetime import datetime

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
    chemin_csv = "data/matchs_a_venir.csv"
    df = pd.read_csv(chemin_csv)

    # 🕒 Transformation de la date pour tri et regroupement
    df["date_obj"] = pd.to_datetime(df["date_paris"], format="%Y-%m-%d")
    df = df.sort_values("date_obj")

    jours = []
    for date_jour, groupe in df.groupby("date_obj"):
        nom_jour = jours_fr[date_jour.strftime("%A")]
        nom_mois = mois_fr[date_jour.strftime("%B")]
        date_affichee = f"{nom_jour} {date_jour.day} {nom_mois}"

        matchs = []
        for _, row in groupe.iterrows():
            match = {
                "date": date_affichee,
                "heure": row["heure_paris"],
                "home_id": row["home_team_id"],
                "away_id": row["away_team_id"],
                "home": row["home_team_tricode"],
                "away": row["away_team_tricode"],
                "series_game_number": row["series_game_number"],
                "game_label": row["game_label"],
                "if_necessary": row["if_necessary"]
            }
            matchs.append(match)

        jours.append({
            "date": date_affichee,
            "matchs": matchs
        })

    return jours
