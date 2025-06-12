# ==========================================
# 💾 Export des pronostics en CSV
# ==========================================

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

# 🔐 Chargement de l'URL depuis .env
load_dotenv()
url_bdd = os.getenv("DATABASE_URL")

# 📦 Création du moteur SQLAlchemy
engine = create_engine(url_bdd)

# 📁 Nom du fichier avec date automatique
date_str = datetime.today().strftime("%Y-%m-%d")
nom_fichier = f"data/export/pronostics_{date_str}.csv"

# 🔄 Lecture de la table SQL et export CSV
try:
    df = pd.read_sql("SELECT * FROM pronostics", con=engine)
    df.to_csv(nom_fichier, index=False, encoding="utf-8")
    print(f"✅ Export réussi : {nom_fichier}")
except Exception as e:
    print("❌ Erreur lors de l’export :", e)
