# ======================================
# 🧠 Script d'évaluation enrichie des pronostics
# ======================================

import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# ======================================
# 🔐 Connexion à la base PostgreSQL
# ======================================
load_dotenv()
URL_BDD = os.getenv("DATABASE_URL")

def charger_pronostics():
    try:
        conn = psycopg2.connect(URL_BDD)
        requete = """
            SELECT utilisateur, game_id, equipe_pronostiquee, date_pronostic
            FROM pronostics;
        """
        df = pd.read_sql_query(requete, conn)
        conn.close()
        return df
    except Exception as e:
        print("❌ Erreur chargement pronostics :", e)
        return pd.DataFrame()

# ======================================
# 📥 Chargement des matchs terminés
# ======================================
def charger_matchs_finalises(chemin_matchs="data/processed/matchs.csv"):
    try:
        matchs = pd.read_csv(chemin_matchs)
        matchs = matchs[matchs["gameStatusText"] == "Final"].copy()

        # Détermination du vainqueur réel
        def trouver_vainqueur(row):
            if row["homeTeamScore"] > row["awayTeamScore"]:
                return row["homeTeamTricode"]
            elif row["awayTeamScore"] > row["homeTeamScore"]:
                return row["awayTeamTricode"]
            else:
                return "Égalité"

        matchs["vainqueur_reel"] = matchs.apply(trouver_vainqueur, axis=1)
        return matchs
    except Exception as e:
        print("❌ Erreur chargement matchs :", e)
        return pd.DataFrame()

# ======================================
# 🔄 Fusion et enrichissement
# ======================================
def fusionner_et_enrichir(pronos, matchs):
    pronos["game_id"] = pronos["game_id"].astype(str)
    matchs["gameId"] = matchs["gameId"].astype(str)

    fusion = pronos.merge(matchs, left_on="game_id", right_on="gameId", how="inner")

    fusion["pronostic_correct"] = fusion["equipe_pronostiquee"] == fusion["vainqueur_reel"]

    # 🧾 Réorganisation des colonnes pour analyse complète
    df_final = fusion[[
        "game_id", "dateParis", "heureParis", "utilisateur", "date_pronostic",
        "homeTeamTricode", "homeTeamScore", "awayTeamTricode", "awayTeamScore",
        "equipe_pronostiquee", "vainqueur_reel", "pronostic_correct",
        "gameStatusText", "gameLabel"
    ]].copy()

    df_final.columns = [
        "game_id", "date_match", "heure_match", "utilisateur", "date_pronostic",
        "équipe_domicile", "score_domicile", "équipe_extérieure", "score_extérieur",
        "équipe_pronostiquée", "vainqueur_réel", "pronostic_correct",
        "statut_match", "type_match"
    ]

    df_final.sort_values(by=["date_match", "utilisateur"], inplace=True)
    return df_final

# ======================================
# 💾 Export CSV
# ======================================
def exporter_csv(df, chemin="data/processed/pronostics_eval.csv"):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    df.to_csv(chemin, index=False)
    print(f"✅ Fichier exporté : {chemin}")

# ======================================
# 🚀 Lancement
# ======================================
if __name__ == "__main__":
    print("📊 Lancement génération du CSV pronostics_eval...")
    pronos = charger_pronostics()
    matchs = charger_matchs_finalises()
    if pronos.empty or matchs.empty:
        print("❌ Données insuffisantes, arrêt.")
    else:
        df_eval = fusionner_et_enrichir(pronos, matchs)
        exporter_csv(df_eval)
