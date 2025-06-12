# ✅ To-Do Mensuelle — Changement de base PostgreSQL (Render)

### 📅 Quand : chaque mois, avant l’expiration de la base Render gratuite

---

## 🧾 1. **Sauvegarder les données existantes**

✔️ Lancer manuellement ton script d’export :

```bash
python scripts/export_pronostics.py
```

✅ Vérifie que le fichier `data/export/pronostics_YYYY-MM-DD.csv` est bien créé et contient les données.

👉 Tu peux aussi le **committer sur GitHub** pour avoir une trace versionnée.

---

## 🗑️ 2. **Supprimer l’ancienne base sur Render**

* Va sur [Render](https://dashboard.render.com/)
* Clique sur ta base expirée (`nba-pronostics`)
* Bouton **Delete Database**

🧘 Aucune donnée perdue si l’export CSV a bien été fait.

---

## 🆕 3. **Créer une nouvelle base PostgreSQL Render**

* `New +` > **PostgreSQL**
* Nom : `nba-pronostics-XXXX`
* Plan : **Free**

📌 Patiente quelques secondes que Render crée la base

---

## 🔑 4. **Récupérer la nouvelle `DATABASE_URL`**

* Dans la nouvelle base : onglet **Connections**
* Copier l’URL **External Database URL**

---

## ✏️ 5. **Mettre à jour la variable d’environnement**

### En local (`.env`) :

```env
DATABASE_URL=postgres://...
```

### Sur GitHub (`Settings` > Secrets > Actions) :

* Modifier le secret `DATABASE_URL`
* Coller la nouvelle URL

---

## 🔁 6. **(Optionnel) Restaurer les données depuis le dernier CSV**

> Si tu veux réimporter les anciens pronostics dans la nouvelle base :
> Je peux te générer un script `import_pronostics_csv.py` pour faire ça proprement.

---

## 🧪 7. **Tester que tout fonctionne**

```bash
python scripts/db.py        # pour vérifier que la table est bien là
python scripts/export_pronostics.py  # pour tester l’accès
```

---

## ✅ Résumé rapide

| Étape                                | À faire ?    |
| ------------------------------------ | ------------ |
| Export CSV                           | ✅            |
| Supprimer base Render                | ✅            |
| Créer nouvelle base                  | ✅            |
| Mettre à jour `.env` + GitHub secret | ✅            |
| (Réimporter CSV si besoin)           | 🔁 optionnel |
| Tester export                        | ✅            |

---
