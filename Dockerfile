# 🔧 Base officielle Python slim
FROM python:3.11-slim

# 🏗️ Variables d'environnement pour Dash/Render
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000
ENV PYTHONPATH=/app

# 📁 Dossier de travail
WORKDIR /app

# 🧩 Copie des fichiers
COPY . /app

# 🔧 Installation des dépendances
RUN pip install --upgrade pip && \
    pip install dash pandas requests nba_api dash-bootstrap-components

# 🚀 Commande par défaut : lancer Dash
CMD ["python", "app/core/app.py"]

