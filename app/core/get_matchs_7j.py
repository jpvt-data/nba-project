# ======================================
# 📁 Lecture et transformation des matchs à venir (Scoreboard V3)
# ======================================

import pandas as pd
from datetime import datetime
import locale

# 🇫🇷 Pour afficher les dates en français
locale.setlocale(locale.LC_TIME, "fr_FR")  # ✅

def get_matchs_7j():
    chemin_csv = "data/matchs_a_venir.csv"
    df = pd.read_csv(chemin_csv)

    # 🕒 Transformation de la date pour tri et regroupement
    df["date_obj"] = pd.to_datetime(df["date_paris"], format="%Y-%m-%d")
    df = df.sort_values("date_obj")

    jours = []
    for date_jour, groupe in df.groupby("date_obj"):
        matchs = []

        for _, row in groupe.iterrows():
            match = {
                "date": date_jour.strftime("%A %d %B").capitalize(),
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
            "date": date_jour.strftime("%A %d %B").capitalize(),
            "matchs": matchs
        })

    return jours
