# ======================================
# 🏠 Page Accueil - Layout
# ======================================

from dash import html, dcc
import dash_bootstrap_components as dbc


def accueil_layout(pseudo=""):
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
                    html.Span("128", className="bloc-valeur")
                ], className="bloc-stat"),

                html.Div([
                    html.Span("Pronos réussis", className="bloc-label"),
                    html.Span("65%", className="bloc-valeur")
                ], className="bloc-stat"),

                html.Div([
                    html.Span("Équipe favorite", className="bloc-label"),
                    html.Span("NETS", className="bloc-valeur equipe-valeur")
                ], className="bloc-stat"),
            ], className="bloc-avatar-stats")
        ], className="bloc-avatar-ligne")
    ], className="bloc-avatar-wrapper")

    # Bloc de droite : top 3 + bouton
    bloc_ranking = html.Div([
        html.H4("Top 3 Swish Rank", className="titre-bloc-droit"),
        html.Table([
            html.Thead(html.Tr([
                html.Th("Pseudo"), html.Th("% Réussite")
            ])),
            html.Tbody([
                html.Tr([html.Td("Tout_Sec"), html.Td("65%")]),
                html.Tr([html.Td("Milk_it"), html.Td("61%")]),
                html.Tr([html.Td("Polo"), html.Td("60%")]),
            ])
        ], className="tableau-ranking"),
        html.Br(),
        html.Div(
            dcc.Link("Détails Swish Rank", href="/swishrank", className="bouton-sw"),
            style={"textAlign": "center"}
        )
    ], className="bloc-ranking-wrapper")

        # 🏀 Image centrale entre les deux blocs (affichée uniquement en mode desktop)
    image_centrale = html.Div(
        html.Img(
            src="/assets/images/basketteur.png",
            style={"height": "300px"},
            alt="Basketteur central",
            className="d-none d-lg-block"
        ),
        style={"textAlign": "center", "margin": "auto"}
    )


    return html.Div(
        style={"backgroundColor": "#121212", "minHeight": "100vh"},
        children=[
            html.Div([
                html.H2("Ton Swish Score", className="titre-bloc section-bienvenue"),

                dbc.Row([
                    dbc.Col(bloc_avatar, lg=5, sm=12),
                    dbc.Col(image_centrale, lg=2, sm=0),  # image uniquement visible en desktop
                    dbc.Col(bloc_ranking, lg=5, sm=12)
                ], className="gy-4 align-items-center"),

                html.Hr(className="ligne-separatrice"),

                # 📆 Bloc 1 – Matchs à pronostiquer
                html.H2("Pronostics en cours", className="titre-bloc"),
                html.Div([
                    html.P("Voici les matchs des 7 prochains jours à ne surtout pas rater."),
                    html.P([
                        "👉 ",
                        html.Strong("Clique sur le bouton sous l'équipe que tu vois gagnante.")
                    ]),
                    html.P([
                        "⏳ Tu peux pronostiquer ou modifier ton vote jusqu’à l’heure de début du match.",
                        " Ensuite, c’est verrouillé automatiquement !"
                    ])
                ], className="texte-description"),
                html.Div(id="bloc_matchs"),

                html.Hr(className="ligne-separatrice"),

                html.H2("Classement NBA", className="titre-bloc"),
                dcc.RadioItems(
                    id="type_classement",
                    options=[
                        {"label": "Saison régulière", "value": "saison"},
                        {"label": "Playoffs", "value": "playoffs"},
                    ],
                    value="saison",
                    inline=True,
                    className="toggle-classement"
                ),
                html.Div(id="bloc_classement"),

                html.Hr(className="ligne-separatrice"),
                html.H2("Dernières infos NBA", className="titre-bloc"),
                html.Ul(id="bloc_actu", className="liste-actus")
            ], className="container-site")
        ]
    )
