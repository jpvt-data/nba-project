# ======================================
# 🏠 Page Accueil - Layout
# ======================================

from dash import html, dcc

def accueil_layout():
    return html.Div(
        style={"backgroundColor": "#121212", "minHeight": "100vh"},
        children=[

            # Conteneur principal aligné (hors navbar)
            html.Div([

                # 🏠 Titre principal
                html.H1("Bienvenue dans Swish League 🏀 !", className="titre-texte"),

                # 👋 Introduction générale
                html.P([
                    "Une appli pour suivre la saison NBA, faire des pronos entre potes et briller sur les stats !",
                    html.Br(),
                    "Résultats, classements, actus NBA et défis quotidiens – Enjoy !"
                ], className="texte-intro"),


                # 📆 Bloc 1 – Matchs à pronostiquer
                html.Div([
                    html.H2("Matchs à pronostiquer", className="titre-bloc"),
                    html.P([
                        "Voici les matchs des 7 prochains jours à ne surtout pas rater.",
                        html.Br(),
                        "Pronostique vite avant qu'ils ne soient verrouillés – chaque point compte pour grimper au classement 🏆",
                    ], className="texte-description"
                    ),
                    html.Div(id="bloc_matchs")
                ], className="section-bloc"),

                # 🔜 Autres blocs prévus (non encore activés)
                html.Div([
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
                    html.Div(id="bloc_classement")
                ], className="section-bloc"),

                html.Div([
                    html.H2("Dernières infos NBA", className="titre-bloc"),
                    html.Ul(id="bloc_actu", className="liste-actus")
                ], className="section-bloc"),

            ], className="container-site")  # ← tout contenu aligné ici

        ]
    )
