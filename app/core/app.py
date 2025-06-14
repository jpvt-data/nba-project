# ======================================
# 🎮 App principale - NBA Dashboard multipage
# ======================================

import sys, dash, os, json, pandas as pd
from pathlib import Path
from dash import Dash, html, dcc, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc

# 🔧 Chemin racine
racine = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(racine))
chemin_assets = os.path.join(racine, "assets")

# 📄 Imports internes
from app.pages.accueil_layout import accueil_layout
from app.pages.statistiques_layout import statistiques_layout
from app.pages.joueurs_layout import joueurs_layout
from app.pages.pronostics_layout import pronostics_layout
from app.pages.classement_layout import classement_layout
from app.pages.palmares_layout import palmares_layout
from app.pages.connexion_layout import connexion_layout
from app.pages.admin_layout import admin_layout
from app.composants.menu import navbar
from app.core.get_matchs_7j import get_matchs_7j
from scripts.db import a_deja_vote, inserer_pronostic, supprimer_pronostic

# ======================================
# 🚀 App
# ======================================
app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.DARKLY],
           assets_folder=chemin_assets,
           title="NBA Dashboard")
server = app.server

# ======================================
# 🖼️ Layout général
# ======================================
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="session_utilisateur", storage_type="session"),
    navbar(),
    html.Div(id="contenu_page", style={"padding": "20px"}),
    html.Div(id="fake_trigger", style={"display": "none"})
])

# ======================================
# 🔁 Routing
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
        "/": accueil_layout(),
        "/statistiques": statistiques_layout(),
        "/joueurs": joueurs_layout(),
        "/pronostics": pronostics_layout(),
        "/classement": classement_layout(),
        "/palmares": palmares_layout(),
        "/connexion": connexion_layout,
        "/admin": admin_layout()
    }
    return routes.get(pathname, html.H1("404 – Page introuvable", style={"color": "white"}))

# ======================================
# 📆 Affichage des matchs + boutons
# ======================================
@app.callback(
    Output("bloc_matchs", "children"),
    Input("url", "pathname"),
    State("session_utilisateur", "data")
)
def afficher_matchs(path, session):
    if path != "/":
        return None

    pseudo = session.get("pseudo") if session else None
    jours = get_matchs_7j()
    cartes = []

    for jour in jours:
        for m in jour["matchs"]:
            ligne_infos = m.get("game_label", "")
            if pd.notnull(m.get("series_game_number")):
                ligne_infos += f" – Match {m['series_game_number'].replace('Game', '').strip()}"
            if str(m.get("if_necessary")).lower() == "true":
                ligne_infos += " – Si Nécessaire"

            game_id = m["game_id"]
            tricode_away = m["away"]
            tricode_home = m["home"]
            vote = a_deja_vote(pseudo, game_id) if pseudo else None

            if vote:
                # 🔒 Affichage après vote
                bloc = html.Div([
                    html.Div([
                        html.Div([html.Img(src=f"https://cdn.nba.com/logos/nba/{m['away_id']}/global/L/logo.svg", className="carte-logo")], className="carte-equipe"),
                        html.Div("VS", className="carte-vs"),
                        html.Div([html.Img(src=f"https://cdn.nba.com/logos/nba/{m['home_id']}/global/L/logo.svg", className="carte-logo")], className="carte-equipe"),
                    ], className="carte-ligne"),
                    html.Div(f"Prono 🔮 : Victoire {vote}", className="carte-vote-label"),
                    html.Button("Modifier mon pronostic", id={"type": "btn_prono", "game_id": game_id, "team": "MODIFIER"}, className="bouton-prono modifiable", n_clicks=0)
                ])
            else:
                # 🟢 Affichage boutons initiaux
                bloc = html.Div([
                    html.Div([
                        html.Img(src=f"https://cdn.nba.com/logos/nba/{m['away_id']}/global/L/logo.svg", className="carte-logo"),
                        html.Button(f"Victoire {tricode_away}", id={"type": "btn_prono", "game_id": game_id, "team": tricode_away}, className="bouton-prono", n_clicks=0)
                    ], className="carte-equipe"),
                    html.Div("VS", className="carte-vs"),
                    html.Div([
                        html.Img(src=f"https://cdn.nba.com/logos/nba/{m['home_id']}/global/L/logo.svg", className="carte-logo"),
                        html.Button(f"Victoire {tricode_home}", id={"type": "btn_prono", "game_id": game_id, "team": tricode_home}, className="bouton-prono", n_clicks=0)
                    ], className="carte-equipe")
                ], className="carte-ligne")

            cartes.append(html.Div([
                html.Div(f"{jour['date']} – {m['heure']}", className="carte-date"),
                html.Div(ligne_infos, className="carte-infos"),
                bloc
            ], className="carte-match"))

    return html.Div(cartes, className="grille-matchs")

# ======================================
# ✅ Callback : vote ou suppression
# ======================================
@app.callback(
    Output("fake_trigger", "children"),
    Input({"type": "btn_prono", "game_id": ALL, "team": ALL}, "n_clicks_timestamp"),
    State("session_utilisateur", "data"),
    prevent_initial_call=True
)
def enregistrer_ou_supprimer_vote(n_clicks_list, session):
    if not session or not session.get("pseudo"):
        return dash.no_update

    index = max([(i, ts) for i, ts in enumerate(n_clicks_list) if ts], key=lambda x: x[1], default=(None, None))[0]
    if index is None:
        return dash.no_update

    ctx_id = ctx.inputs_list[0][index]["id"]
    game_id = ctx_id["game_id"]
    team = ctx_id["team"]
    pseudo = session["pseudo"]

    if team == "MODIFIER":
        print(f"🧼 Suppression vote {pseudo} → {game_id}")
        supprimer_pronostic(pseudo, game_id)
        return f"{pseudo} – suppression {game_id}"

    print(f"✅ Vote {pseudo} → {team} pour {game_id}")
    inserer_pronostic(pseudo, game_id, team)
    return f"{pseudo} – vote {team} pour {game_id}"

# ======================================
# 🔄 Forcer affichage actualisé
# ======================================
@app.callback(
    Output("bloc_matchs", "children", allow_duplicate=True),
    Input("fake_trigger", "children"),
    State("url", "pathname"),
    State("session_utilisateur", "data"),
    prevent_initial_call=True
)
def rafraichir_affichage(_, pathname, session):
    return afficher_matchs(pathname, session)

# ======================================
# 🔐 Connexion utilisateur
# ======================================
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

@app.callback(
    Output("session_utilisateur", "data"),
    Output("url", "pathname"),
    Output("message_connexion", "children"),
    Input("bouton_connexion", "n_clicks"),
    State("champ_pseudo", "value"),
    State("champ_mdp", "value"),
    prevent_initial_call=True
)
def verifier_connexion(n_clicks, pseudo, mdp):
    utilisateurs = os.getenv("USERS_JSON")
    if not utilisateurs:
        return dash.no_update, dash.no_update, "⚠️ Aucun utilisateur défini."

    try:
        users = json.loads(utilisateurs)
    except:
        return dash.no_update, dash.no_update, "⚠️ Format JSON invalide."

    if users.get(pseudo) == mdp:
        return {"connecté": True, "pseudo": pseudo}, "/", ""
    return dash.no_update, dash.no_update, "Identifiants incorrects."

# ======================================
# ▶️ Lancement local
# ======================================
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
