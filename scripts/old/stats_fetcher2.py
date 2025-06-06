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
    Fetches and caches NBA team and player stats by season and playoffs, both aggregate and game-by-game.
    Supports historical seasons from the NBA inception (1946-47) to present.
    Implements retry logic on all NBAStats HTTP calls.
    """
    def __init__(self, cache_dir='data', delay: float = 0.5, retries: int = 3):
        self.cache_dir = cache_dir
        self.delay = delay
        self.retries = retries
        os.makedirs(self.cache_dir, exist_ok=True)

    def _cache_path(self, prefix: str, season: str, suffix: str) -> str:
        return os.path.join(self.cache_dir, f"{prefix}_{season}_{suffix}.csv")

    def _save_df(self, df: pd.DataFrame, path: str) -> pd.DataFrame:
        df.to_csv(path, index=False)
        return df

    def _call_with_retries(self, func, *args, **kwargs) -> pd.DataFrame:
        attempt = 0
        while attempt < self.retries:
            try:
                return func(*args, **kwargs).get_data_frames()[0]
            except Exception as e:
                attempt += 1
                print(f"Retry {attempt}/{self.retries} for {func.__name__}: {e}")
                time.sleep(self.delay)
        print(f"Warning: {func.__name__} failed after {self.retries} attempts.")
        return pd.DataFrame()

    def fetch_team_stats(self, season: str, playoffs: bool = False) -> pd.DataFrame:
        mode = 'Playoffs' if playoffs else 'Regular Season'
        suffix = 'playoffs' if playoffs else 'regular'
        cache = self._cache_path('team_stats', season, suffix)
        if os.path.exists(cache):
            return pd.read_csv(cache)
        df = self._call_with_retries(
            LeagueDashTeamStats,
            season=season,
            season_type_all_star=mode
        )
        if df.empty:
            return self._save_df(df, cache)
        team_map = {t['id']: t['full_name'] for t in teams.get_teams()}
        df['team_name'] = df['TEAM_ID'].map(team_map)
        return self._save_df(df, cache)

    def fetch_player_stats(self, season: str, playoffs: bool = False) -> pd.DataFrame:
        mode = 'Playoffs' if playoffs else 'Regular Season'
        suffix = 'playoffs' if playoffs else 'regular'
        cache = self._cache_path('player_stats', season, suffix)
        if os.path.exists(cache):
            return pd.read_csv(cache)
        df = self._call_with_retries(
            LeagueDashPlayerStats,
            season=season,
            season_type_all_star=mode,
            per_mode_detailed='PerGame'
        )
        if df.empty:
            return self._save_df(df, cache)
        df = df.rename(columns={'PLAYER_NAME': 'player_name'})
        return self._save_df(df, cache)

    def fetch_team_game_logs(self, season: str, playoffs: bool = False) -> pd.DataFrame:
        suffix = 'playoffs' if playoffs else 'regular'
        cache = self._cache_path('team_game_logs', season, suffix)
        if os.path.exists(cache):
            return pd.read_csv(cache)
        frames = []
        for team in teams.get_teams():
            df = self._call_with_retries(
                TeamGameLog,
                team_id=team['id'],
                season=season,
                season_type_all_star=('Playoffs' if playoffs else 'Regular Season')
            )
            if not df.empty:
                df['team_name'] = team['full_name']
                frames.append(df)
            time.sleep(self.delay)
        if not frames:
            return self._save_df(pd.DataFrame(), cache)
        result = pd.concat(frames, ignore_index=True)
        return self._save_df(result, cache)

    def fetch_player_game_logs(self, season: str, playoffs: bool = False) -> pd.DataFrame:
        suffix = 'playoffs' if playoffs else 'regular'
        cache = self._cache_path('player_game_logs', season, suffix)
        if os.path.exists(cache):
            return pd.read_csv(cache)
        stats = self.fetch_player_stats(season, playoffs=playoffs)
        active = stats.loc[stats.get('GP', 0) > 0, 'PLAYER_ID'].unique() if not stats.empty else []
        frames = []
        for pid in active:
            df = self._call_with_retries(
                PlayerGameLog,
                player_id=pid,
                season=season,
                season_type_all_star=('Playoffs' if playoffs else 'Regular Season')
            )
            if not df.empty:
                name = stats.loc[stats['PLAYER_ID'] == pid, 'player_name'].iloc[0]
                df['player_name'] = name
                frames.append(df)
            time.sleep(self.delay)
        if not frames:
            return self._save_df(pd.DataFrame(), cache)
        result = pd.concat(frames, ignore_index=True)
        return self._save_df(result, cache)

    def fetch_historical(self, start_year: int = 1946, end_year: int = None) -> None:
        if end_year is None:
            end_year = pd.Timestamp.now().year
        seasons = [f"{y}-{str(y+1)[-2:]}" for y in range(start_year, end_year)]
        modes = [
            ('team', False), ('team', True),
            ('player', False), ('player', True),
            ('team_game', False), ('team_game', True),
            ('player_game', False), ('player_game', True)
        ]
        funcs = {
            'team': self.fetch_team_stats,
            'player': self.fetch_player_stats,
            'team_game': self.fetch_team_game_logs,
            'player_game': self.fetch_player_game_logs
        }
        for season in seasons:
            for entity, playoffs in modes:
                print(f"Fetching {entity} ({'Playoffs' if playoffs else 'Regular'}) for {season}...")
                funcs[entity](season, playoffs=playoffs)

# Example usage
if __name__ == '__main__':
    sf = StatsFetcher(cache_dir='nba_data', delay=0.5, retries=5)
    sf.fetch_historical()
