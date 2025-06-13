# ======================================
# 🎮 App principale - NBA Dashboard multipage
# ======================================

# 📦 Import des librairies système
import sys
import pandas as pd
import os
from pathlib import Path

# 🔧 Ajout du chemin racine au PYTHONPATH pour les imports
racine = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(racine))

# 📦 Import Dash
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# 📄 Import des layouts de pages
from app.pages.accueil_layout import accueil_layout
from app.pages.statistiques_layout import statistiques_layout
from app.pages.joueurs_layout import joueurs_layout
from app.pages.pronostics_layout import pronostics_layout
from app.pages.classement_layout import classement_layout
from app.pages.palmares_layout import palmares_layout
from app.pages.connexion_layout import connexion_layout
from app.pages.admin_layout import admin_layout

# Import des scripts connexes
from app.core.get_matchs_7j import get_matchs_7j

# 📋 Import de la navbar
from app.composants.menu import navbar

# ======================================
# 🚀 Initialisation de l'app Dash
# ======================================
chemin_assets = os.path.join(racine, "assets")  # ⬅️ on force le chemin assets
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY],
    assets_folder=chemin_assets,
    title="NBA Dashboard"
)

# 👇 Forcer la validation de tous les IDs utilisés dans les callbacks
app.validation_layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="session_utilisateur", storage_type="session"),
    dcc.Location(id="forcage_url", refresh=True),
    dcc.Input(id="champ_pseudo"),
    dcc.Input(id="champ_mdp"),
    html.Button(id="bouton_connexion"),
    html.Div(id="message_connexion"),
    html.Div(id="fake_trigger")  # <<< C’EST CELUI QUI MANQUE AU VALIDATION_LAYOUT !
])

server = app.server  # utile pour déploiement Render

# ======================================
# 🖼️ Layout principal
# ======================================
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Location(id="forcage_url", refresh=True),  # nouveau redirecteur
    dcc.Store(id="session_utilisateur", storage_type="session"),
    navbar(),
    html.Div(id="contenu_page", style={"padding": "20px"}),
    html.Div(id="fake_trigger", style={"display": "none"})
])


# ======================================
# 🔁 Routing dynamique entre les pages
# ======================================
@app.callback(
    Output("contenu_page", "children"),
    Input("url", "pathname"),
    Input("session_utilisateur", "data")
)
def afficher_page(pathname, session):
    if not session or not session.get("connecté"):
        return connexion_layout

    routes = {
        "/": accueil_layout,
        "/statistiques": statistiques_layout,
        "/joueurs": joueurs_layout,
        "/pronostics": pronostics_layout,
        "/classement": classement_layout,
        "/palmares": palmares_layout,
        "/connexion": connexion_layout,
        "/admin": admin_layout
    }

    return routes.get(pathname, lambda: html.H1("404 – Page introuvable", style={"color": "white", "textAlign": "center"}))()

# ======================================
# 📆 Callback affichage des matchs des 7 prochains jours (Accueil)
# ======================================

@app.callback(
    Output("bloc_matchs", "children"),
    Input("url", "pathname")
)
def afficher_matchs(path):
    if path != "/":
        return None

    jours = get_matchs_7j()
    cartes = []

    for jour in jours:
        for m in jour["matchs"]:
            # Ligne d'infos contextuelle
            ligne_infos = m["game_label"] or ""

            if pd.notnull(m.get("series_game_number")) and isinstance(m["series_game_number"], str):
                ligne_infos += f" – Match {m['series_game_number'].replace('Game', '').strip()}"

            if str(m.get("if_necessary")).lower() == "true":
                ligne_infos += " – Si Nécessaire"

            # 🔠 Tricodes
            tricode_away = m["away"]
            tricode_home = m["home"]

            carte = html.Div([

                html.Div(f"{jour['date']} – {m['heure']}", className="carte-date"),
                html.Div(ligne_infos, className="carte-infos"),

                html.Div([

                    # Bloc équipe extérieure
                    html.Div([
                        html.Img(
                            src=f"https://cdn.nba.com/logos/nba/{m['away_id']}/global/L/logo.svg",
                            className="carte-logo"
                        ),
                        html.Button(
                            f"Victoire {tricode_away}",
                            id={"type": "btn_prono", "game_id": m["game_id"], "team": tricode_away},
                            className="bouton-prono",
                            n_clicks=0
                        ),
                        # 🔍 Print bouton extérieur
                        html.Div(style={"display": "none"}, children=print("🔍 Bouton créé :", {
                            "type": "btn_prono", 
                            "game_id": m["game_id"], 
                            "team": tricode_away
                        }))
                    ], className="carte-equipe"),

                    html.Div("VS", className="carte-vs"),

                    # Bloc équipe domicile
                    html.Div([
                        html.Img(
                            src=f"https://cdn.nba.com/logos/nba/{m['home_id']}/global/L/logo.svg",
                            className="carte-logo"
                        ),
                        html.Button(
                            f"Victoire {tricode_home}",
                            id={"type": "btn_prono", "game_id": m["game_id"], "team": tricode_home},
                            className="bouton-prono",
                            n_clicks=0
                        ),
                        # 🔍 Print bouton domicile
                        html.Div(style={"display": "none"}, children=print("🔍 Bouton créé :", {
                            "type": "btn_prono", 
                            "game_id": m["game_id"], 
                            "team": tricode_home
                        }))
                    ], className="carte-equipe"),

                ], className="carte-ligne"),

            ], className="carte-match")

            cartes.append(carte)

    return html.Div(cartes, className="grille-matchs")

# ======================================
# 🧠 Callback : Enregistrement d'un pronostic
# ======================================

from dash import ctx, ALL
from scripts.db import inserer_pronostic

@app.callback(
    Output("fake_trigger", "children"),  # Ne sert qu'à déclencher le callback
    Input({"type": "btn_prono", "game_id": ALL, "team": ALL}, "n_clicks_timestamp"),
    State("session_utilisateur", "data"),
    prevent_initial_call=True
)
def enregistrer_pronostic(n_clicks_list, session):
    # Vérification utilisateur connecté
    if not session or not session.get("pseudo"):
        return dash.no_update

    pseudo = session["pseudo"]

    # 🔒 Aucun bouton cliqué
    if not any(n_clicks_list):
        return dash.no_update

    # 🔍 Trouver l'index du bouton cliqué le plus récemment
    index_clique = max(
        [(i, ts) for i, ts in enumerate(n_clicks_list) if ts],
        key=lambda x: x[1],
        default=(None, None)
    )[0]

    if index_clique is None:
        return dash.no_update

    # Récupérer l’ID du bouton cliqué
    ctx_id = ctx.inputs_list[0][index_clique]["id"]
    game_id = ctx_id.get("game_id")
    team = ctx_id.get("team")

    if not game_id or not team:
        return dash.no_update

    # ✅ Enregistrement en base
    print(f"👤 Insertion en base : {pseudo} {game_id} {team}")
    success = inserer_pronostic(pseudo, game_id, team)

    if success:
        print(f"✅ Pronostic ajouté : {pseudo} → {team} pour {game_id}")
    else:
        print(f"🔁 Pronostic déjà existant pour {pseudo} sur {game_id}")

    return f"{pseudo} → {team} pour {game_id} (clic enregistré)"


# ======================================
# 🔁 Authentification simple (pseudo/mdp)
# ======================================

import json
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass  # Sur Render, dotenv est inutile

USERS = json.loads(os.getenv("USERS_JSON", "{}"))

@app.callback(
    Output("session_utilisateur", "data"),
    Output("redir_connexion", "pathname"),
    Output("message_connexion", "children"),
    Input("bouton_connexion", "n_clicks"),
    State("champ_pseudo", "value"),
    State("champ_mdp", "value"),
    prevent_initial_call=True
)
def verifier_connexion(n_clicks, pseudo, motdepasse):
    utilisateurs_json = os.environ.get("USERS_JSON")

    if not utilisateurs_json:
        return dash.no_update, dash.no_update, "⚠️ Aucun utilisateur défini."

    try:
        utilisateurs = json.loads(utilisateurs_json)
    except:
        return dash.no_update, dash.no_update, "⚠️ Format JSON invalide pour USERS_JSON."

    if not pseudo or not motdepasse:
        return dash.no_update, dash.no_update, "Veuillez entrer un identifiant et un mot de passe."

    if utilisateurs.get(pseudo) == motdepasse:
        return {"connecté": True, "pseudo": pseudo}, "/", ""
    else:
        return dash.no_update, dash.no_update, "Identifiants incorrects."



# ======================================
# ▶️ Lancement local
# ======================================
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

