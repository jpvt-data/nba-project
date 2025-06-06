# 🔧 Base officielle Python slim
FROM python:3.11-slim

# 🏗️ Variables d'environnement pour Dash/Render
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000
ENV PYTHONPATH=/app
ENV LANG=fr_FR.UTF-8
ENV LANGUAGE=fr_FR:fr
ENV LC_ALL=fr_FR.UTF-8

# 📁 Dossier de travail
WORKDIR /app

# 🧩 Copie des fichiers
COPY . /app

# 🔧 Installation des dépendances système + Python
RUN apt-get update && \
    apt-get install -y locales && \
    echo "fr_FR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen fr_FR.UTF-8 && \
    pip install --upgrade pip && \
    pip install dash pandas requests nba_api dash-bootstrap-components

# 🚀 Commande par défaut : lancer Dash
CMD ["python", "app/core/app.py"]
