# ======================================
# 📊 Script – Vue d'ensemble des stats pronostics PAR UTILISATEUR
# ======================================

import pandas as pd
import os

# 📁 Chemins vers les fichiers
chemin_pronos = "data/processed/pronostics_eval.csv"
chemin_matchs = "data/processed/matchs.csv"
chemin_export = "data/processed/vue_ensemble_stats_prono_par_utilisateur.csv"

def generer_resume_par_utilisateur():
    # 📥 Chargement des fichiers
    df_eval = pd.read_csv(chemin_pronos)
    df_matchs = pd.read_csv(chemin_matchs)

    # 🎯 Nombre total de matchs joués (terminés)
    total_matchs_joues = df_matchs[df_matchs["gameStatusText"] == "Final"]["gameId"].nunique()

    # 📊 Regroupement principal
    stats = (
        df_eval.groupby("utilisateur")
        .agg(
            total_pronostics=("game_id", "count"),
            matchs_distincts=("game_id", "nunique"),
            bons_pronostics=("pronostic_correct", "sum"),
        )
        .reset_index()
    )

    # 🏀 Détermination de l'équipe la plus votée par utilisateur
    equipe_fav = (
        df_eval.groupby(["utilisateur", "équipe_pronostiquée"])
        .size()
        .reset_index(name="nb_votes")
        .sort_values(["utilisateur", "nb_votes"], ascending=[True, False])
        .drop_duplicates("utilisateur")
        .set_index("utilisateur")
    )

    stats = stats.set_index("utilisateur")
    stats["équipe_favorite"] = equipe_fav["équipe_pronostiquée"]
    stats = stats.reset_index()

    # 🧮 Calcul des métriques complémentaires
    stats["taux_reussite (%)"] = round(100 * stats["bons_pronostics"] / stats["total_pronostics"], 1)
    stats["couverture_matchs (%)"] = round(100 * stats["matchs_distincts"] / total_matchs_joues, 1)

    # 🎯 Colonnes finales
    stats = stats[[
        "utilisateur",
        "total_pronostics",
        "bons_pronostics",
        "taux_reussite (%)",
        "matchs_distincts",
        "couverture_matchs (%)",
        "équipe_favorite"
    ]]

    # 💾 Export
    os.makedirs(os.path.dirname(chemin_export), exist_ok=True)
    stats.to_csv(chemin_export, index=False)
    print(f"✅ Vue d'ensemble PAR UTILISATEUR générée : {chemin_export}")

if __name__ == "__main__":
    generer_resume_par_utilisateur()
