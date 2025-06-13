# ==========================================
# 📦 Connexion PostgreSQL & création table
# ==========================================

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# 🔐 Chargement des variables d'environnement (.env)
load_dotenv()
URL_BDD = os.getenv("DATABASE_URL")

# 🔌 Connexion à la base PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(URL_BDD)
        return conn
    except Exception as e:
        print("❌ Erreur de connexion à la base :", e)
        return None

# 🧱 Création de la table `pronostics` si elle n'existe pas
def create_table_pronostics():
    conn = connect_db()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pronostics (
                    id SERIAL PRIMARY KEY,
                    utilisateur TEXT NOT NULL,
                    game_id TEXT NOT NULL,
                    equipe_pronostiquee TEXT NOT NULL,
                    date_pronostic TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (utilisateur, game_id)
                );
            """)
            conn.commit()
            print("✅ Table `pronostics` prête.")
    except Exception as e:
        print("❌ Erreur lors de la création de la table :", e)
    finally:
        conn.close()

# ==========================================
# ✅ Insertion d’un pronostic utilisateur
# ==========================================

def inserer_pronostic(utilisateur, game_id, equipe_pronostiquee):
    conn = connect_db()
    if conn is None:
        return False

    try:
        with conn.cursor() as cur:
            print("👤 Insertion en base :", utilisateur, game_id, equipe_pronostiquee)
            cur.execute("""
                INSERT INTO pronostics (utilisateur, game_id, equipe_pronostiquee)
                VALUES (%s, %s, %s)
                ON CONFLICT (utilisateur, game_id) DO NOTHING;
            """, (utilisateur, game_id, equipe_pronostiquee))
            conn.commit()
            return cur.rowcount > 0  # True si insertion réussie, False si déjà existant
    except Exception as e:
        print("❌ Erreur lors de l'insertion du pronostic :", e)
        return False
    finally:
        conn.close()

# ================================================
# 🔍 Vérifie si un utilisateur a déjà voté ce match
# ================================================
def a_deja_vote(utilisateur, game_id):
    conn = connect_db()
    if conn is None:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT equipe_pronostiquee FROM pronostics
                WHERE utilisateur = %s AND game_id = %s;
            """, (utilisateur, str(game_id)))
            result = cur.fetchone()
            return result[0] if result else None
    except Exception as e:
        print("❌ Erreur lors de la vérification de vote :", e)
        return None
    finally:
        conn.close()


if __name__ == "__main__":
    create_table_pronostics()
