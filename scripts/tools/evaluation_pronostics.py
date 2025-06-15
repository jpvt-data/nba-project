# ======================================
# 🧠 Évaluation des pronostics utilisateurs
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

        # Calcul vainqueur
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
# 🔄 Fusion et comparaison
# ======================================
def fusionner_et_evaluer(pronos, matchs):
    # 🩹 Correction des types pour la fusion
    pronos["game_id"] = pronos["game_id"].astype(str)
    matchs["gameId"] = matchs["gameId"].astype(str)
    fusion = pronos.merge(
        matchs,
        left_on="game_id",
        right_on="gameId",
        how="inner"
    )

    fusion["bon_prono"] = fusion["equipe_pronostiquee"] == fusion["vainqueur_reel"]
    fusion["bon_prono"] = fusion["bon_prono"].map({True: "✅", False: "❌"})

    colonnes_utiles = [
        "utilisateur", "game_id", "equipe_pronostiquee", "vainqueur_reel", "bon_prono", "date_pronostic",
        "dateParis", "homeTeamTricode", "homeTeamScore",
        "awayTeamTricode", "awayTeamScore", "gameStatusText"
    ]

    fusion = fusion[colonnes_utiles].sort_values(by=["dateParis", "utilisateur"])
    return fusion

# ======================================
# 💾 Export CSV
# ======================================
def exporter_csv(df, chemin="data/processed/evaluation_pronostics.csv"):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    df.to_csv(chemin, index=False)
    print(f"✅ Fichier exporté : {chemin}")

# ======================================
# 🚀 Lancement
# ======================================
if __name__ == "__main__":
    print("📊 Lancement évaluation des pronostics...")
    pronos = charger_pronostics()
    matchs = charger_matchs_finalises()
    if pronos.empty or matchs.empty:
        print("❌ Données insuffisantes, arrêt.")
    else:
        df_eval = fusionner_et_evaluer(pronos, matchs)
        exporter_csv(df_eval)
