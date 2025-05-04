## **Nom du projet GitHub**

`nba-project`

---

## **Objectif MVP fonctionnel pour octobre 2025**

Créer une application web interactive (via Dash), avec :

* Connexion pseudo simple
* Interface utilisateur personnalisée
* Pronostics sur matchs à venir
* Classement des joueurs entre amis
* Affichage des scores / stats / historiques NBA
* Intégration des logos, photos, images d'équipes et joueurs
* Déploiement gratuit via Docker + Render

---

## **Plan de développement détaillé par étapes**

### **Étape 1 – Initialisation projet**

* [ ] Créer le dépôt GitHub `nba-dashboard`
* [ ] Mettre en place la structure de base du projet (`/app`, `/scripts`, `/data`, etc.)
* [ ] Ajouter `README.md`, `Dockerfile`, `requirements.txt`, `main.py`

---

### **Étape 2 – Exploration des APIs**

* [ ] Rechercher une ou plusieurs **API NBA gratuites**

  * Scores en direct
  * Matchs à venir
  * Données historiques (équipes, saisons, joueurs)
  * **Logos et photos** : à confirmer si disponibles via API ou scraping/images locales
* [ ] Tester les appels dans un script `collecter_données.py`
* [ ] Sauvegarder les données en local (`data/`) ou en base

---

### **Étape 3 – Authentification simple par pseudo**

* [ ] Ajouter un champ pseudo (sans mot de passe pour commencer)
* [ ] Stocker les pseudos et sessions côté serveur (fichier JSON ou PostgreSQL)
* [ ] Afficher une interface utilisateur dédiée après login

---

### **Étape 4 – Affichage et navigation NBA**

* [ ] Page Accueil : derniers scores, navigation rapide
* [ ] Page Joueurs : stats individuelles, image, bio
* [ ] Page Équipes : roster, logos, résultats récents
* [ ] Page Classement : classement live par conférence
* [ ] Page Calendrier : calendrier des matchs à venir

---

### **Étape 5 – Système de pronostics**

* [ ] Afficher la liste des prochains matchs (via API)
* [ ] Permettre à chaque utilisateur de pronostiquer (victoire équipe A ou B)
* [ ] Sauvegarder les choix dans une base ou fichier
* [ ] Afficher les résultats dès que les matchs sont joués

---

### **Étape 6 – Classement & Historique**

* [ ] Calculer le nombre de bons pronostics par utilisateur
* [ ] Créer un tableau de classement
* [ ] Afficher l’historique des choix pour chaque utilisateur

---

### **Étape 7 – Déploiement Render**

* [ ] Dockeriser l'app
* [ ] Lier GitHub + Render pour déploiement automatique
* [ ] Créer une URL publique à partager à tes potes

---

### **Étape 8 – UI & Graphismes**

* [ ] Intégrer les logos des clubs
* [ ] Ajouter photos de joueurs
* [ ] Ajouter style CSS/Bootstrap pour rendre l'app agréable à l’œil

---

### **Étape 9 – Bonus futur**

* [ ] Ajouter un chatbot LLM pour interroger les stats NBA en langage naturel
* [ ] Intégrer un module Machine Learning pour prédire les scores

---

## **Maquette utilisateur (structure écran)**

```
---------------------------------------------------
| NBA DASHBOARD - Bienvenue [Pseudo]              |
|-------------------------------------------------|
| Accueil | Équipes | Joueurs | Pronostics | Stats |
---------------------------------------------------
| Bonjour JP !                                    |
|                                                 |
| >>> Matchs à venir :                            |
| - Lakers vs Celtics [Pronostiquer]              |
| - Warriors vs Bucks  [Pronostiquer]             |
|                                                 |
| >>> Ton classement actuel : 4e                  |
| >>> Derniers résultats :                        |
| - Nuggets 112 - 105 Suns                        |
---------------------------------------------------
```

Chaque utilisateur voit :

* son classement
* son historique de pronos
* les matchs à venir à voter
* un bouton pour modifier son pseudo