# ======================================
# 🎮 App principale - NBA Dashboard multipage
# ======================================

import sys
import pandas as pd
import os
import json
from pathlib import Path

# 🔧 Ajout du chemin racine au PYTHONPATH pour les imports
racine = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(racine))

# 📦 Dash
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# 📄 Layouts des pages
from app.pages.accueil_layout import accueil_layout
from app.pages.statistiques_layout import statistiques_layout
from app.pages.joueurs_layout import joueurs_layout
from app.pages.pronostics_layout import pronostics_layout
from app.pages.classement_layout import classement_layout
from app.pages.palmares_layout import palmares_layout
from app.pages.connexion_layout import connexion_layout
from app.pages.admin_layout import admin_layout

# 🔧 Scripts internes
from app.core.get_matchs_7j import get_matchs_7j
from app.composants.menu import navbar

# 🚀 Initialisation app Dash
chemin_assets = os.path.join(racine, "assets")
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY],
    assets_folder=chemin_assets,
    title="NBA Dashboard"
)

server = app.server

# 🖼️ Layout global
app.layout = html.Div([
    dcc.Store(id="session_utilisateur", storage_type="session"),
    dcc.Location(id="url"),
    navbar(),
    html.Div(id="contenu_page", style={"padding": "20px"})
])

# 🔁 Routing avec vérification de session
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


# 📆 Affichage des matchs (Accueil)
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
            ligne_infos = m["game_label"] or ""
            if pd.notnull(m.get("series_game_number")) and isinstance(m["series_game_number"], str) and m["series_game_number"].strip():
                ligne_infos += f" – Match {m['series_game_number'].replace('Game', '').strip()}"
            if str(m.get("if_necessary")).lower() == "true":
                ligne_infos += " – Si Nécessaire"

            carte = html.Div([
                html.Div(f"{jour['date']} – {m['heure']}", className="carte-date"),
                html.Div(ligne_infos, className="carte-infos"),
                html.Div([
                    html.Div([
                        html.Img(src=f"https://cdn.nba.com/logos/nba/{m['away_id']}/global/L/logo.svg", className="carte-logo"),
                        html.Div(m["away"], className="carte-abbr")
                    ], className="carte-equipe"),
                    html.Div("VS", className="carte-vs"),
                    html.Div([
                        html.Img(src=f"https://cdn.nba.com/logos/nba/{m['home_id']}/global/L/logo.svg", className="carte-logo"),
                        html.Div(m["home"], className="carte-abbr")
                    ], className="carte-equipe")
                ], className="carte-ligne"),
                html.Button("🌮 Prono", className="bouton-prono", n_clicks=0)
            ], className="carte-match")

            cartes.append(carte)

    return html.Div(cartes, className="grille-matchs")


# 🔐 Authentification - Callback de connexion
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


# ▶️ Lancement local
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
