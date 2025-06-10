# ======================================
# 🏠 Page Accueil - Layout
# ======================================

from dash import html, dcc

def accueil_layout():
    return html.Div(
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"},
        children=[

            # 🏠 Titre principal
            html.H1("Bienvenue dans Swish League 🏀 !", className="titre-texte"),

            # 👋 Introduction
            html.P(
                "Une appli pour suivre la saison NBA, faire des pronos entre potes et briller sur les stats ! "
                "Résultats, classements, actus NBA et défis quotidiens – Enjoy !",
                className="texte-intro",
                style={
                    "color": "#CCCCCC",
                    "fontSize": "1.1rem",
                    "marginTop": "10px",
                    "marginBottom": "40px",
                    "maxWidth": "800px"
                }
            ),

            # 📆 Bloc 1 – Matchs à venir
            html.Div(id="bloc_matchs", className="section-bloc"),

            # 📊 Bloc 2 – Classement Saison / Playoffs
            html.Div([
                html.H2("Classement NBA", className="titre-texte", style={"fontSize": "1.6rem", "marginTop": "40px"}),
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

            # 📰 Bloc 3 – Actus NBA
            html.Div([
                html.H2("Dernières infos NBA", className="titre-texte", style={"fontSize": "1.6rem", "marginTop": "40px"}),
                html.Ul(id="bloc_actu", className="liste-actus")
            ], className="section-bloc")
        ]
    )
