from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import (
    LeagueDashTeamStats,
    LeagueDashPlayerStats,
    TeamGameLog,
    PlayerGameLog
)
import pandas as pd
import os
import time

class StatsFetcher:
    """
    Fetches and caches NBA team and player stats by season and by game.
    Uses per-entity game log endpoints with retry and throttling to handle rate limits.
    For player game logs, only fetches for players who appeared in the season.
    Historical data can be fetched in bulk and stored locally.
    """
    def __init__(self, cache_dir='data', delay: float = 0.5, retries: int = 3):
        self.cache_dir = cache_dir
        self.delay = delay
        self.retries = retries
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_team_stats(self, season: str) -> pd.DataFrame:
        cache_path = os.path.join(self.cache_dir, f'team_stats_{season}.csv')
        if os.path.exists(cache_path):
            return pd.read_csv(cache_path)

        df = LeagueDashTeamStats(
            season=season,
            season_type_all_star='Regular Season'
        ).get_data_frames()[0]
        # Map team IDs to names
        team_map = {t['id']: t['full_name'] for t in teams.get_teams()}
        df['team_name'] = df['TEAM_ID'].map(team_map)
        df.to_csv(cache_path, index=False)
        return df

    def fetch_player_stats(self, season: str) -> pd.DataFrame:
        cache_path = os.path.join(self.cache_dir, f'player_stats_{season}.csv')
        if os.path.exists(cache_path):
            return pd.read_csv(cache_path)

        df = LeagueDashPlayerStats(
            season=season,
            season_type_all_star='Regular Season',
            per_mode_detailed='PerGame'
        ).get_data_frames()[0]
        df.rename(columns={'PLAYER_NAME': 'player_name'}, inplace=True)
        df.to_csv(cache_path, index=False)
        return df

    def fetch_team_game_logs(self, season: str) -> pd.DataFrame:
        cache_path = os.path.join(self.cache_dir, f'team_game_logs_{season}.csv')
        if os.path.exists(cache_path):
            return pd.read_csv(cache_path)

        frames = []
        for team in teams.get_teams():
            attempt = 0
            while attempt < self.retries:
                try:
                    df = TeamGameLog(
                        team_id=team['id'],
                        season=season,
                        season_type_all_star='Regular Season'
                    ).get_data_frames()[0]
                    df['team_name'] = team['full_name']
                    frames.append(df)
                    time.sleep(self.delay)
                    break
                except Exception as e:
                    attempt += 1
                    print(f"Retry {attempt}/{self.retries} for team {team['full_name']}: {e}")
                    time.sleep(self.delay)
            else:
                print(f"Warning: no game logs for team {team['full_name']} after {self.retries} attempts.")

        result = pd.concat(frames, ignore_index=True)
        result.to_csv(cache_path, index=False)
        return result

    def fetch_player_game_logs(self, season: str) -> pd.DataFrame:
        cache_path = os.path.join(self.cache_dir, f'player_game_logs_{season}.csv')
        if os.path.exists(cache_path):
            return pd.read_csv(cache_path)

        # 1) Get list of players who actually played (GP > 0) from season stats
        stats_df = self.fetch_player_stats(season)
        active_ids = stats_df.loc[stats_df['GP'] > 0, 'PLAYER_ID'].unique()

        frames = []
        for pid in active_ids:
            player_name = stats_df.loc[stats_df['PLAYER_ID'] == pid, 'player_name'].iloc[0]
            attempt = 0
            while attempt < self.retries:
                try:
                    df = PlayerGameLog(
                        player_id=pid,
                        season=season,
                        season_type_all_star='Regular Season'
                    ).get_data_frames()[0]
                    df['player_name'] = player_name
                    frames.append(df)
                    time.sleep(self.delay)
                    break
                except Exception as e:
                    attempt += 1
                    print(f"Retry {attempt}/{self.retries} for player {player_name}: {e}")
                    time.sleep(self.delay)
            else:
                print(f"Warning: no game logs for player {player_name} (ID {pid}) after {self.retries} attempts.")

        result = pd.concat(frames, ignore_index=True)
        result.to_csv(cache_path, index=False)
        return result

    def fetch_historical(self, seasons: list[str], entity: str='team') -> None:
        funcs = {
            'team': self.fetch_team_stats,
            'player': self.fetch_player_stats,
            'team_game': self.fetch_team_game_logs,
            'player_game': self.fetch_player_game_logs
        }
        if entity not in funcs:
            raise ValueError(f"Unknown entity: {entity}")

        for season in seasons:
            print(f"Fetching {entity} for {season}...")
            funcs[entity](season)

# Example usage
if __name__ == '__main__':
    sf = StatsFetcher(cache_dir='nba_data', delay=0.5, retries=3)
    seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(2014, 2025)]
    sf.fetch_historical(seasons, entity='team')
    sf.fetch_historical(seasons, entity='player')
    sf.fetch_historical(seasons, entity='team_game')
    # sf.fetch_historical(seasons, entity='player_game')
