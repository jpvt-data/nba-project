# ======================================
# 🧹 Script admin – Suppression d’un pronostic ciblé
# ======================================

import sys
from pathlib import Path

# Ajout du chemin racine pour les imports
racine = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(racine))

from scripts.db import connect_db


def supprimer_pronostic(utilisateur, game_id):
    conn = connect_db()
    if conn is None:
        print("❌ Connexion impossible à la base.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM pronostics
                WHERE utilisateur = %s AND game_id = %s;
            """, (utilisateur, str(game_id)))
            conn.commit()
            if cur.rowcount > 0:
                print(f"✅ Pronostic supprimé : {utilisateur} / match {game_id}")
            else:
                print(f"⚠️ Aucun pronostic trouvé pour {utilisateur} sur {game_id}")
    except Exception as e:
        print("❌ Erreur lors de la suppression :", e)
    finally:
        conn.close()

if __name__ == "__main__":
    print("🛠️ Suppression manuelle d’un pronostic")
    utilisateur = input("Pseudo utilisateur : ").strip()
    game_id = input("Game ID à supprimer : ").strip()
    supprimer_pronostic(utilisateur, game_id)
