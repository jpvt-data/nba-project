# 📚 Récapitulatif de la doc **nba_api**

## 1. Structure générale
- **nba_api.stats**  
  - `endpoints/` : wrappers pour tous les endpoints officiels de stats NBA (boxscores, classements, totaux carrière, etc.)  
  - `library/` : fonctions utilitaires  
- **nba_api.live.nba**  
  - `endpoints/scoreboard`, `endpoints/playbyplay`, `endpoints/boxscore` pour données live  
- **nba_api.stats.library.parameters** : constantes (saisons, types de stats…)  

## 2. Principaux modules et classes
| Module                              | Usage                                                                                   |
|-------------------------------------|-----------------------------------------------------------------------------------------|
| `LeagueStandings`                   | Classement général des équipes                                                           |
| `LeagueGameFinder`                  | Liste de tous les matchs d’une saison ou d’une équipe                                    |
| `CommonTeamRoster`                  | Liste des joueurs d’une équipe                                                           |
| `BoxScoreTraditionalV2`             | Boxscore détaillé (points, rebonds, passes…)                                            |
| `BoxScoreFourFactorsV2`             | Statistiques avancées (efficacité, tirs…)                                               |
| `PlayerCareerStats`                 | Totaux et moyennes sur la carrière d’un joueur                                          |
| …                                   | (De nombreux autres endpoints pour shooting splits, défense, rebonds, etc.)             |
| **Live** `ScoreBoard`, `PlayByPlay` | Accès aux scores en direct, play-by-play, alignements                                       |

## 3. Formats de sortie
- **JSON brut** via `.get_dict()`
- **Pandas DataFrame** via `.get_data_frames()`

## 4. Bonnes pratiques
1. **Caching** : stocker localement données statiques (liste joueurs/équipes)  
2. **Throttling** : respecter un délai entre requêtes pour éviter les blocages  
3. **Tests de sanity** : créer une routine qui vérifie régulièrement que les endpoints fonctionnent  

## 5. Limitations & alternatives
- **Endpoints non officiels** : peuvent évoluer sans préavis  
- **Quota non garanti** : usage intensif peut provoquer des erreurs  
- **Alternatives** : API-NBA (RapidAPI), sportsipy (ESPN)
