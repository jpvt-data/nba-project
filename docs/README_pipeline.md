# 🏀 Pipeline NBA Dashboard – Mise à jour des données

Ce dépôt contient les scripts nécessaires à la mise à jour quotidienne des données NBA pour l’application communautaire **Swish League**.  
Chaque script a un rôle précis et s’inscrit dans une logique d’automatisation structurée.

---

## 🔁 Ordre de lancement des scripts

| Ordre | Script | Description | Mode de lancement |
|-------|--------|-------------|-------------------|
| 1️⃣ | `1_update_nba_api.py` | Récupère les données de **matchs NBA** depuis l’API officielle. Convertit les dates/horaires, construit le fichier `matchs.csv`. Ce script sera enrichi avec les appels aux stats joueurs, équipes, etc. | 🖥️ **Planificateur Windows** (exécution locale uniquement) |
| 🔚 | `sync_push.yml` *(GitHub Actions)* | Push automatique de tous les fichiers mis à jour (`data/`) vers GitHub après exécution des scripts locaux. Permet à Render de recharger les données. | ⚙️ **GitHub Actions** (cron + manuel) |

