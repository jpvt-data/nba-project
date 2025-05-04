# Pitch – NBA Dashboard

## Vision

Créer une application NBA communautaire et interactive pour suivre les matchs, stats et faire des pronostics entre amis.  
Un projet construit à la main, en open-source, pour mêler passion NBA, données, fun et apprentissage technique.

## Objectif

- Webapp gratuite pour accéder à toutes les données NBA (scores, classements, historiques)
- Interface de pronostics pour jouer entre amis, avec classement et historique
- Expérience fluide, lisible, sans pub, sans appli mobile lourde
- Lancement opérationnel pour **21 octobre 2025**

## Fonctionnalités prévues pour le MVP

- Authentification par pseudo
- Page Accueil avec les matchs du jour
- Page Pronostics avec liste des matchs à venir
- Page Classement des utilisateurs
- Page Stats NBA (équipes, joueurs)
- Intégration de visuels : logos, photos joueurs
- Backend Python, Dash, fichiers ou DB
- Déploiement sur Render (via Docker)

## Instructions GPT

GPT doit :
- Suivre le projet comme assistant produit + dev
- Respecter le calendrier NBA (octobre 2025)
- Utiliser uniquement des outils gratuits et open-source
- Structurer le projet dans un dépôt GitHub clair
- Proposer chaque semaine une étape clé à avancer
- Ne jamais intégrer de Machine Learning avant la V2
- Ajouter des maquettes visuelles ou wireframes au besoin
- Gérer les APIs avec test, vérification des quotas et fiabilité

## Stack

- Python, Dash, Pandas, Plotly
- API-NBA (via RapidAPI)
- PostgreSQL ou fichiers JSON/CSV
- Docker + Render
- GitHub pour gestion et déploiement

## Inspirations

- Scorecast pour la mécanique sociale
- BallersDash pour la structure stats
- StatMuse pour l’interaction fluide

---

## Prochaine étape

- Mettre en place le dépôt `nba-dashboard`
- Intégrer la structure de base (`/app`, `/data`, `/scripts`)
- Tester l’API-NBA et identifier les endpoints utiles
- Lancer la page de connexion + pseudo
- Créer une maquette visuelle simple de l’interface
