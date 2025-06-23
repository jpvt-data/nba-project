# ======================================
# 🏀 App NBA Dashboard
# ======================================

# ======================================
# 📁 Chemins de travail (racine + assets)
# ======================================

import sys
import os
import json
import pandas as pd
from pathlib import Path

racine = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(racine))
chemin_assets = os.path.join(racine, "assets")

# ======================================
# 📦 Dash & composants
# ======================================

import dash
from dash import dcc, html, Input, Output, State, Dash, ctx, ALL
import dash_bootstrap_components as dbc

# ======================================
# 📄 Imports internes – pages
# ======================================

from app.pages.accueil_layout import accueil_layout
from app.pages.swishrank_layout import swishrank_layout
from app.pages.statsnba_layout import statsnba_layout
from app.pages.profil_layout import profil_layout
from app.pages.connexion_layout import connexion_layout

# ======================================
# 🧩 Composants – menus & callbacks
# ======================================

from app.composants.menu import navbar

# ======================================
# 📊 Données & logique – fonctions de base
# ======================================

from app.core.get_matchs_7j import get_matchs_7j
from scripts.db import a_deja_vote, inserer_pronostic, supprimer_pronostic


# ======================================
# 🚀 Initialisation de l'app Dash
# ======================================

app = Dash(
    __name__,
    use_pages=False,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY],
    assets_folder=chemin_assets,       # 🔧 Chemin assets forcé
    title="NBA Dashboard"              # 🏀 Titre de l'onglet
)

server = app.server


## ===============================
# 🖼️ Layout général de l'application
# ===============================

app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="session_utilisateur", storage_type="session"),
    navbar(),  # ✅ affichée pour tous, même sans être connecté

    # 📄 Contenu principal des pages
    html.Div(id="contenu_page", style={"padding": "20px"}),

    # ⚠️ Élément fantôme (utile pour certains callbacks invisibles)
    html.Div(id="fake_trigger", style={"display": "none"}),

    # 📜 Footer permanent
    html.Footer([
        html.Hr(),
        html.Div([
            html.P([
                "© 2025 JPVT – Appli NBA non commerciale entre amis. "
                "Code sous licence MIT. Logos NBA affichés à titre privé. ",
                html.A("Voir licence complète", href="https://github.com/jpvt-data/nba-project/blob/main/LICENSE.md", target="_blank")
            ])
        ], style={
            "textAlign": "center",
            "fontSize": "0.8rem",
            "color": "#aaa",
            "padding": "10px 20px",
            "margin": "0 auto"
        })
    ], style={"marginTop": "40px"})
])


# ===============================
# 🔁 Routing + Sécurité connexion
# ===============================

@app.callback(
    Output("contenu_page", "children"),
    Input("url", "pathname"),
    State("session_utilisateur", "data")
)
def afficher_page(pathname, session):
    # 🔐 Blocage si non connecté
    if not session:
        return connexion_layout

    # ✅ Routage si connecté
    if pathname == "/":
        pseudo = session.get("pseudo", "")
        return accueil_layout(pseudo, get_bio_phrase(pseudo))
    elif pathname == "/profil":
        return profil_layout()
    elif pathname == "/statsnba":
        return statsnba_layout()
    elif pathname == "/swishrank":
        pseudo = session.get("pseudo", "")
        return swishrank_layout(pseudo)
    else:
        return html.Div("Page introuvable", style={"padding": "2rem", "color": "red"})

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
                        html.Div("@", className="carte-vs"),
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
                    html.Div("@", className="carte-vs"),
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
# 📊 Callback – Affichage Classement NBA par filtres
# ======================================

from nba_api.stats.static import teams
from dash import callback, Output, Input, html
import pandas as pd

# ✅ Chargement des infos équipes depuis nba_api
dict_equipes = {team["id"]: team for team in teams.get_teams()}

@app.callback(
    Output("tableau_classement", "children"),
    Input("filtre_type_saison", "value"),
    Input("filtre_annee", "value"),
    Input("filtre_conference", "value")
)
def afficher_tableau_classement(type_saison, annee, conference):
    # 🚧 Limitation temporaire
    if type_saison != "regular":
        return html.P("⚠️ Seule la saison régulière est disponible pour le moment.",
                      className="texte-secondaire")

    # 📥 Chargement et filtrage
    df = pd.read_csv("data/processed/saison/classement_conf_saisons_total.csv")
    df = df[(df["Année"] == annee) & (df["CONFERENCE"] == conference)]
    df = df.sort_values("RANK")

    # 📋 Colonnes utiles
    colonnes = ["RANK", "TEAM_ID", "WINS", "LOSSES", "PCT", "HOME", "AWAY", "CONF", "GB"]

    if df.empty:
        return html.P("Aucune donnée trouvée pour les filtres sélectionnés.", className="texte-secondaire")

    lignes = []
    for _, row in df[colonnes].iterrows():
        equipe_info = dict_equipes.get(int(row["TEAM_ID"]), {})
        nom_equipe = equipe_info.get("full_name", "Équipe inconnue")
        logo_url = f"https://cdn.nba.com/logos/nba/{int(row['TEAM_ID'])}/global/L/logo.svg"

        equipe_cell = html.Div([
            html.Img(src=logo_url, style={"height": "26px", "marginRight": "10px"}),
            html.Span(nom_equipe)
        ], style={"display": "flex", "alignItems": "center"})

        lignes.append(html.Tr([
            html.Td(row["RANK"]),
            html.Td(equipe_cell),
            html.Td(row["WINS"]),
            html.Td(row["LOSSES"]),
            html.Td(f"{row['PCT']:.3f}"),
            html.Td(row["HOME"]),
            html.Td(row["AWAY"]),
            html.Td(row["CONF"]),
            html.Td(row["GB"])
        ]))

    entetes = ["#", "Équipe", "V", "D", "%", "Domicile", "Extérieur", "Conf", "Écart"]

    return html.Div(
        html.Table([
            html.Thead(html.Tr([html.Th(col) for col in entetes])),
            html.Tbody(lignes)
        ], className="tableau-ranking"),
        className="tableau-ranking-wrapper"
    )

# ===============================
# 📅 Callback Calendrier NBA
# ===============================

@app.callback(
    Output("conteneur_calendrier", "children"),
    Output("cal_week_idx", "data"),
    Input("select_mois_calendrier", "value"),
    Input("prev_week_btn", "n_clicks"),
    Input("next_week_btn", "n_clicks"),
    State("cal_week_idx", "data")
)
def afficher_calendrier_semaine(valeur_mois, prev_clicks, next_clicks, week_idx):
    import pandas as pd
    from datetime import datetime
    import calendar

    df = pd.read_csv("data/processed/calendrier/calendrier_saison.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%y")
    df["mois"] = df["Date"].dt.month
    df["annee"] = df["Date"].dt.year
    df["jour"] = df["Date"].dt.day

    annee, mois = map(int, valeur_mois.split("-"))
    df_mois = df[(df["mois"] == mois) & (df["annee"] == annee)]

    cal = calendar.Calendar(firstweekday=0)
    semaines = list(cal.monthdayscalendar(annee, mois))

    # Gestion index semaine (callback dash pattern)
    ctx = dash.callback_context
    triggered = [t["prop_id"] for t in ctx.triggered]
    today = datetime.today()

    # Détecte le "no-trigger" Dash, donc ouverture de la page
    if not triggered or triggered[0] == "." or "select_mois_calendrier" in triggered[0]:
        if today.year == annee and today.month == mois:
            for idx, semaine in enumerate(semaines):
                if today.day in semaine:
                    week_idx = idx
                    break
            else:
                week_idx = 0
        else:
            week_idx = 0
    elif "prev_week_btn" in triggered[0]:
        week_idx = max(0, (week_idx or 0) - 1)
    elif "next_week_btn" in triggered[0]:
        week_idx = min(len(semaines) - 1, (week_idx or 0) + 1)

    # Clamp au cas où
    week_idx = max(0, min(week_idx, len(semaines) - 1))

    print(f"TRIGGERED: {triggered}, week_idx: {week_idx}, today: {today}, mois: {mois}, annee: {annee}")

    semaine = semaines[week_idx]
    jours_semaine = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

    ligne = []
    for i, jour in enumerate(semaine):
        if jour == 0:
            ligne.append(html.Td("", className="cellule-jour-vide"))
        else:
            matchs_du_jour = df_mois[df_mois["jour"] == jour]
            if matchs_du_jour.empty:
                ligne.append(html.Td(str(jour), className="cellule-jour-vide"))
            else:
                blocs_matchs = []
                for _, match in matchs_du_jour.iterrows():
                    score = (
                        f"{int(match['score_domicile'])} - {int(match['score_exterieur'])}"
                        if pd.notna(match["score_domicile"]) and pd.notna(match["score_exterieur"])
                        else ""
                    )
                    # LOGOS ET NOMS "AWAY @ HOME"
                    logo_away = html.Img(
                        src=f"https://cdn.nba.com/logos/nba/{match['id_team_extérieure']}/global/L/logo.svg",
                        style={"height": "44px", "marginRight": "10px", "display": "block", "marginLeft": "auto", "marginRight": "auto"}
                    )
                    logo_home = html.Img(
                        src=f"https://cdn.nba.com/logos/nba/{match['id_team_domicile']}/global/L/logo.svg",
                        style={"height": "44px", "marginLeft": "10px", "display": "block", "marginLeft": "auto", "marginRight": "auto"}
                    )
                    # Ligne logos centrés
                    logos_row = html.Div([
                        html.Div(logo_away, style={"display": "inline-block", "width": "48%"}),
                        html.Div(logo_home, style={"display": "inline-block", "width": "48%"})
                    ], style={"width": "100%", "marginBottom": "6px", "textAlign": "center"})
                    # Noms des équipes ("AWAY @ HOME")
                    noms_equipes = html.Div([
                        html.Span(match['équipe_extérieure'], style={"fontWeight": "bold", "color": "#fff", "fontSize": "1em"}),
                        html.Span(" @ ", style={"color": "#ccc", "fontWeight": "bold"}),
                        html.Span(match['équipe_domicile'], style={"fontWeight": "bold", "color": "#fff", "fontSize": "1em"}),
                    ], style={"marginBottom": "2px"})
                    arene = f"{match['Salle']}"
                    heure = match["Heure"]
                    competition = ""
                    if pd.notna(match["Compétition "]):
                        comp_str = str(match["Compétition "]).strip()
                        if comp_str and comp_str != "Saison régulière":
                            competition = comp_str

                    blocs_matchs.append(
                        html.Div([
                            logos_row,
                            noms_equipes,
                            html.Div(score, className="score-nba-cal" if score else "score-nba-cal-vide", style={"fontSize": "1.2em", "fontWeight": "bold", "margin": "2px 0 2px 0"}),
                            html.Div(heure, style={"fontSize": "0.92em", "fontWeight": "normal"}),
                            html.Div(arene, style={"fontSize": "0.78em", "color": "#888"}),
                            html.Div(competition, style={"fontSize": "0.78em", "color": "#c96"}) if competition else None
                        ], className="bloc-match-nba", style={"padding": "10px 2px"})
                    )
                ligne.append(html.Td([
                    html.Div(str(jour), className="cellule-jour-num"),
                    *blocs_matchs
                ], className="cellule-jour-cal"))
    calendrier = html.Table([
        html.Thead(html.Tr([html.Th(j, style={"textAlign": "center"}) for j in jours_semaine])),
        html.Tbody([html.Tr(ligne)])
    ], className="tableau-calendrier-nba", style={
        "width": "100%",
        "margin": "0 auto",
        "backgroundColor": "#181818"
    })

    # Indicateur semaine / X
    indicateur = html.Div(
        f"Semaine {week_idx + 1} sur {len(semaines)}",
        style={"color": "#fff", "fontSize": "1em", "marginBottom": "5px"}
    )

    return html.Div([
        indicateur,
        html.Div(calendrier, className="conteneur-scroll-calendrier")
    ]), week_idx

# ==========================================
# 📊 Callback affichage dynamique Stats NBA
# ==========================================
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

# 👇 Callback qui gère le switch entre Résultats / Joueurs / Hall of Fame
@app.callback(
    Output("bloc_statsnba_contenu", "children"),
    Input("btn-resultats", "n_clicks"),
    Input("btn-joueurs", "n_clicks"),
    Input("btn-hof", "n_clicks"),
)
def afficher_bloc_statsnba(n_res, n_joueurs, n_hof):
    # Détermine quel bouton a été cliqué le plus récemment
    boutons = {
        "btn-resultats": n_res or 0,
        "btn-joueurs": n_joueurs or 0,
        "btn-hof": n_hof or 0,
    }
    # On prend le bouton avec la valeur la plus élevée (= dernier cliqué)
    bouton_actif = max(boutons, key=boutons.get)

    # === Bloc Résultats (Classement NBA)
    if bouton_actif == "btn-resultats":
        # ---- Filtres interactifs
        chemin_csv = "data/processed/saison/classement_conf_saisons_total.csv"
        df_classement = pd.read_csv(chemin_csv)
        options_saisons = sorted(df_classement["Année"].dropna().unique(), reverse=True)
        options_conferences = df_classement["CONFERENCE"].dropna().unique()

        return dbc.Row([
            # Colonne gauche : bannière, alignée en haut du tableau (masquée sur mobile)
            dbc.Col(
                html.Img(
                    id="img_banniere_saison",
                    src="/assets/images/saison_reguliere.png",
                    className="banniere-verticale-saison"
                ),
                md=3, xs=0,
                style={"display": "flex", "justifyContent": "flex-end", "alignItems": "flex-start"}
            ),
            # Colonne droite : Filtres puis tableau
            dbc.Col(
                html.Div([
                    # Filtres sur 3 colonnes, en ligne
                    dbc.Row([
                        dbc.Col([
                            html.Label("Type de saison", className="label-filtre"),
                            dcc.Dropdown(
                                id="filtre_type_saison",
                                options=[
                                    {"label": "Saison régulière", "value": "regular"},
                                    {"label": "Playoffs", "value": "playoffs"},
                                    {"label": "Finals", "value": "finals"}
                                ],
                                value="regular",
                                className="dropdown-sw"
                            )
                        ], md=4, xs=12),
                        dbc.Col([
                            html.Label("Saison (Année)", className="label-filtre"),
                            dcc.Dropdown(
                                id="filtre_annee",
                                options=[{"label": str(annee), "value": annee} for annee in options_saisons],
                                value=options_saisons[0],
                                className="dropdown-sw"
                            )
                        ], md=4, xs=12),
                        dbc.Col([
                            html.Label("Conférence", className="label-filtre"),
                            dcc.Dropdown(
                                id="filtre_conference",
                                options=[{"label": conf, "value": conf} for conf in options_conferences],
                                value=options_conferences[0],
                                className="dropdown-sw"
                            )
                        ], md=4, xs=12)
                    ], className="gy-3", style={"marginBottom": "0px"}),

                    # HR puis tableau, tous DEJA à droite via tableau-droite
                    html.Hr(className="ligne-separatrice", style={"marginTop": "0px", "marginBottom": "32px"}),
                    html.Div(id="tableau_classement", className="tableau-droite"),
                ], style={"width": "100%"})
            , md=9, xs=12)
        ], className="align-items-start")

    # === Bloc Joueurs
    elif bouton_actif == "btn-joueurs":
        return html.Div([
            html.H3("Stats joueurs (work in progress)", style={"color": "#fff"}),
            html.P("À venir : stats individuelles, top joueurs, etc.", style={"color": "#aaa"}),
        ])
    # === Bloc Hall of Fame
    elif bouton_actif == "btn-hof":
        return html.Div([
            html.H3("Hall of Fame (work in progress)", style={"color": "#fff"}),
            html.P("À venir : records, légendes, distinctions majeures.", style={"color": "#aaa"}),
        ])
    else:
        return html.Div()

# Callback affichacge bannière statsnba > Résultats
@app.callback(
    Output("img_banniere_saison", "src"),
    Input("filtre_type_saison", "value")
)
def maj_banniere(type_saison):
    if type_saison == "regular":
        return "/assets/images/saison_reguliere.png"
    elif type_saison == "playoffs":
        return "/assets/images/playoffs.png"
    elif type_saison == "finals":
        return "/assets/images/finals.png"
    return "/assets/images/saison_reguliere.png"


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
    if not n_clicks:
        return dash.no_update, dash.no_update, ""

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

# ===============================
# ▶️ Avatar
# ===============================

@app.callback(
    Output("menu-profil", "children"),
    Input("session_utilisateur", "data"),
    Input("url", "pathname")
)
def afficher_avatar_utilisateur(session, pathname):
    # 🛑 Si non connecté OU sur page connexion → rien à afficher
    if not session or not session.get("connecté") or pathname == "/connexion":
        return html.Div()

    pseudo = session.get("pseudo")

    return dbc.NavLink(
        href="/profil",
        className="nav-link-custom d-flex flex-column align-items-center",
        children=[
            html.Img(src=f"/assets/avatars/{pseudo}_S.png", className="avatar-navbar"),
            html.Div(pseudo, className="pseudo-navbar")
        ]
    )

# ===============================
# Bio-Phrases
# ===============================


# Chargement et parsing du dictionnaire depuis l'environnement
bio_phrases = json.loads(os.getenv("BIO_PHRASES", "{}"))


# 🔍 Récupérer la phrase associée à un pseudo
def get_bio_phrase(pseudo):
    return bio_phrases.get(pseudo, "")

# ===============================
# ▶️ Lancement local
# ===============================

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
