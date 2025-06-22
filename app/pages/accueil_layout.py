# ======================================
# 🏠 Page Accueil - Layout
# ======================================

from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd


def accueil_layout(pseudo, bio_phrase):
    # Chargement une seule fois au début du fichier ou via cache
    df_stats = pd.read_csv("data/processed/vue_ensemble_stats_prono_par_utilisateur.csv")
    df_stats = df_stats[df_stats["utilisateur"] != "admin33"]
    stats = df_stats[df_stats["utilisateur"] == pseudo]

    # 🧾 Valeurs par défaut si non trouvé
    total = int(stats["total_pronostics"].values[0]) if not stats.empty else 0
    reussite = f"{stats['taux_reussite (%)'].values[0]}%" if not stats.empty else ""
    equipe = stats["équipe_favorite"].values[0] if not stats.empty else "?"

    # Bloc de gauche : avatar utilisateur
    bloc_avatar = html.Div([
        html.Div([
            # 🧍 Avatar du joueur
            html.Div([
                html.Img(src=f"/assets/avatars/{pseudo}.png", className="bloc-avatar-img"),
                html.H3(pseudo, className="bloc-avatar-nom")
            ], className="bloc-avatar-gauche"),

            # 📈 Statistiques
            html.Div([
                html.Div([
                    html.Span("Total pronostics", className="bloc-label"),
                    html.Span(f"{total}", className="bloc-valeur")
                ], className="bloc-stat"),

                html.Div([
                    html.Span("Pronos réussis", className="bloc-label"),
                    html.Span(f"{reussite}", className="bloc-valeur")
                ], className="bloc-stat"),

                html.Div([
                    html.Span("Équipe favorite", className="bloc-label"),
                    html.Span(f"{equipe}", className="bloc-valeur equipe-valeur")
                ], className="bloc-stat"),

                # 💬 Phrase personnalisée
                html.Div([
                    html.Hr(style={"borderColor": "#777", "margin": "36px auto 30px auto", "width": "80%"}),
                    html.Em(bio_phrase)
                ], style={"fontSize": "0.9rem", "color": "#ccc", "textAlign": "center"})
            ], className="bloc-avatar-stats")
        ], className="bloc-avatar-ligne")
    ], className="bloc-avatar-wrapper")

    # Bloc de droite : top 3 + bouton
    # Tri décroissant et sélection du top 3
    top_actifs = df_stats.sort_values(by="total_pronostics", ascending=False).head(10)
    top3 = top_actifs.sort_values(by="taux_reussite (%)", ascending=False).head(3).reset_index(drop=True)
    
    bloc_ranking = html.Div([
        html.H4("Top 3 Swish League", className="titre-bloc-droit"),
        html.Img(
            src="/assets/logos/swish_league_logo.png",  # adapte le chemin
            style={
                "height": "160px",
                "marginBottom": "20px",
                "display": "block",
                "marginLeft": "auto",
                "marginRight": "auto"
            },
            alt="Badge Swish League"
        ),
        html.Table([
            html.Thead(html.Tr([
                html.Th("Swisher"), html.Th("Nb Pronos"), html.Th("% Réussite") 
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(top3.loc[0, "utilisateur"]),
                    html.Td(f"{top3.loc[0, 'total_pronostics']}"),
                    html.Td(f"{top3.loc[0, 'taux_reussite (%)']:.1f}%")
                ]),
                html.Tr([
                    html.Td(top3.loc[1, "utilisateur"]),
                    html.Td(f"{top3.loc[1, 'total_pronostics']}"),
                    html.Td(f"{top3.loc[1, 'taux_reussite (%)']:.1f}%")
                ]),
                html.Tr([
                    html.Td(top3.loc[2, "utilisateur"]),
                    html.Td(f"{top3.loc[2, 'total_pronostics']}"),
                    html.Td(f"{top3.loc[2, 'taux_reussite (%)']:.1f}%")
                ]),
            ])
        ], className="tableau-ranking", style={"textAlign": "center"}),
        html.Br(),
        html.Div(
            dcc.Link("Détails Swish League", href="/swishrank", className="bouton-sw"),
            style={"textAlign": "center"}
        )
    ], className="bloc-ranking-wrapper")

    # image_centrale
    image_centrale = html.Div(
        html.Img(
            src="/assets/images/affiche_accueil.png",
            alt="Affiche accueil",
            style={
                "width": "100%",
                "height": "auto",
                "objectFit": "cover",
                "borderRadius": "12px"
            },
            className="d-none d-lg-block"
        ),
        style={
            "height": "100%",         # 👈 oblige le conteneur à suivre les autres blocs
            "display": "flex", 
            "alignItems": "stretch"
        }
    )

    return html.Div(
        style={"backgroundColor": "#121212", "minHeight": "100vh"},
        children=[
            html.Div([
                html.H2("Swish Score", className="titre-bloc section-bienvenue"),

                dbc.Row(
                    [
                        dbc.Col(bloc_avatar, sm=12, lg=4, className="mb-4"),
                        dbc.Col(image_centrale, sm=12, lg=4, className="mb-4 d-none d-lg-block"),
                        dbc.Col(bloc_ranking, sm=12, lg=4, className="mb-4")
                    ],
                    className="gx-4 gy-0 align-items-stretch"
                ),

                html.Hr(className="ligne-separatrice"),


                # Bloc Pronostics en cours – Texte à gauche / Bouton à droite
                # html.H2("Pronostics en cours", className="titre-bloc"),

                dbc.Row(
                    [
                        # 📋 Texte d’instructions (2/3 gauche)
                        dbc.Col([
                            html.H2("Pronostics en cours", className="titre-bloc"),
                            html.P("Voici les prochains matchs à ne pas manquer."),
                            html.P([
                                "👉 ",
                                html.Strong("Clique sur l’équipe que tu vois gagnante pour pronostiquer.")
                            ]),
                            html.P([
                                "📊 ",
                                "Besoin d'infos pour affiner ton choix ? ",
                                html.Span("Consulte les stats NBA à droite."),
                            ]),
                            html.P([
                                "⏳ ",
                                "Tu peux modifier ton vote jusqu’au début du match. Ensuite, c’est verrouillé!"
                            ])
                        ], lg=8, sm=12, className="texte-description"),


                        # 🎯 Colonne droite : logo centré + bouton, tous deux alignés verticalement
                        dbc.Col(
                            html.Div([
                                html.Img(
                                    src="/assets/logos/swish_stats_logo.png",  # 🖼️ adapte le chemin si besoin
                                    style={
                                        "height": "120px",
                                        "marginBottom": "5px"
                                    },
                                    alt="Logo stats NBA"
                                ),
                                dcc.Link("Accès aux Stats NBA", href="/statsnba", className="bouton-sw")
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "justifyContent": "center"
                            }),
                            lg=4,
                            sm=12,
                            className="d-flex align-items-center justify-content-center"
                        )
                    ],
                    className="gy-0 align-items-stretch",
                    style={"marginLeft": "0", "marginRight": "0", "width": "100%"}
                    ),

                # 🎮 Bloc des cartes de pronostics (pleine largeur)
                html.Div(id="bloc_matchs"),

                # 🔽 Bloc des cartes de pronostics (pleine largeur)
                html.Div(id="bloc_matchs"),

                html.Hr(className="ligne-separatrice"),

                afficher_calendrier(),

                html.Hr(className="ligne-separatrice"),
                html.H2("Dernières infos NBA", className="titre-bloc"),
                html.Ul(id="bloc_actu", className="liste-actus")
            ], className="container-site")
        ]
    )

# ======================================
# 📅 Bloc Calendrier NBA – Saison régulière
# ======================================

import calendar
from datetime import datetime
import locale

try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
except locale.Error:
    pass

def afficher_calendrier():
    df = pd.read_csv("data/processed/calendrier/calendrier_saison.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%y")
    df["mois"] = df["Date"].dt.month
    df["annee"] = df["Date"].dt.year

    # Limite la dropdown aux mois effectivement présents
    mois_uniques = df[["annee", "mois"]].drop_duplicates().sort_values(["annee", "mois"]).values.tolist()
    options = []
    
    # Liste manuelle des mois avec accents pour un rendu parfait partout
    mois_fr = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]

    options = []
    for annee, mois in mois_uniques:
        mois_label = f"{mois_fr[mois-1]} {annee}"
        options.append({"label": mois_label, "value": f"{annee}-{mois:02d}"})

    now = datetime.now()
    valeur_defaut = options[0]["value"]
    for opt in options:
        if now.year == int(opt["value"].split("-")[0]) and now.month == int(opt["value"].split("-")[1]):
            valeur_defaut = opt["value"]

    return html.Div([
        html.H2("Calendrier de la Saison", className="titre-bloc"),
        html.Div([
            dcc.Dropdown(
                id="select_mois_calendrier",
                options=options,
                value=valeur_defaut,
                clearable=False,
                className="dropdown-mois-nba",
                style={
                    "width": "260px",
                    "margin": "0 auto",
                    "color": "#222",
                    "backgroundColor": "#eee",
                    "display": "inline-block",
                }
            ),
            # Ajout des boutons semaine
            html.Button("◀", id="prev_week_btn", n_clicks=0, className="cal-btn", style={"marginLeft": "20px"}),
            dcc.Store(id="cal_week_idx", data=0),
            html.Button("▶", id="next_week_btn", n_clicks=0, className="cal-btn", style={"marginLeft": "6px"}),
        ], style={"textAlign": "center", "marginBottom": "20px"}),
        html.Div(id="conteneur_calendrier", style={"marginTop": "10px"})
    ], style={"textAlign": "center", "width": "100%"})



