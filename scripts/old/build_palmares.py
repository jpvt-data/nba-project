# File: scripts/build_palmares.py
# Purpose: Infère le champion NBA par saison (1946-47 → présent) depuis les logs Playoffs
#          et génère un CSV data/palmares.csv contenant season, TEAM_ID et champion_abbreviation.

import os
import time
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import TeamGameLog

import requests
from nba_api.stats.library.http import NBAStatsHTTP

# Patch propre du header User-Agent dans la session utilisée par nba_api
class CustomSession(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['User-Agent'] = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        return super().request(*args, **kwargs)

# On remplace la session utilisée par défaut dans nba_api
NBAStatsHTTP._session = CustomSession()



# --- CONFIGURATION ---
START_YEAR   = 1946                     # première saison à couvrir
END_YEAR     = pd.Timestamp.now().year  # ex. 2025 pour la saison 2024-25
OUTPUT_DIR   = "data"
OUTPUT_FILE  = os.path.join(OUTPUT_DIR, "palmares.csv")
THROTTLE_SEC = 0.2                      # pause entre chaque appel pour éviter d'être throttlé

# Crée le dossier de sortie si nécessaire
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_champion_for_season(season: str):
    """
    Récupère tous les logs Playoffs d'une saison (via TeamGameLog pour chaque franchise),
    puis détermine l'équipe victorieuse du dernier match (la finale).
    Retourne (TEAM_ID, team_abbreviation) ou None si pas de playoffs.
    """
    frames = []
    for t in teams.get_teams():
        try:
            df = TeamGameLog(
                team_id=t['id'],
                season=season,
                season_type_all_star='Playoffs'
            ).get_data_frames()[0]
        except Exception:
            continue

        if df.empty:
            continue

        df = df[['GAME_DATE', 'WL']].copy()
        df['TEAM_ID'] = t['id']
        df['ABBREVIATION'] = t.get('abbreviation', t['full_name'])
        frames.append(df)
        time.sleep(THROTTLE_SEC)

    if not frames:
        return None

    # Concatène, parse dates, puis trouve la date la plus tardive (finale)
    df_all = pd.concat(frames, ignore_index=True)
    df_all['GAME_DATE'] = pd.to_datetime(df_all['GAME_DATE'])
    last_date = df_all['GAME_DATE'].max()

    # Sélectionne l'équipe gagnante du (ou des) match(s) à cette date
    final_day = df_all[df_all['GAME_DATE'] == last_date]
    winners = final_day[final_day['WL'] == 'W']
    if winners.empty:
        return None

    winner = winners.iloc[0]
    return int(winner['TEAM_ID']), winner['ABBREVIATION']

def build_palmares():
    """
    Itère chaque saison de START_YEAR à END_YEAR-1,
    construit la liste des champions et sauve en CSV.
    """
    records = []
    for y in range(START_YEAR, END_YEAR):
        season = f"{y}-{str(y+1)[-2:]}"
        print(f"→ Fetching champion for {season}", end=" … ")
        res = fetch_champion_for_season(season)
        if res:
            team_id, abb = res
            records.append({
                'season': season,
                'TEAM_ID': team_id,
                'champion_abbreviation': abb
            })
            print("OK")
        else:
            print("No playoffs")
    # Sauvegarde
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✓ Palmarès généré pour {len(df)} saisons → {OUTPUT_FILE}")

if __name__ == '__main__':
    build_palmares()
