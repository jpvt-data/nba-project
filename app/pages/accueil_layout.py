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
                html.H1("Bienvenue dans Swish League !", className="titre-texte"),

                # 👋 Introduction générale
                html.P([
                    "Une appli pour suivre la saison NBA, faire des pronos entre potes et briller sur les stats !",
                    html.Br(),
                    "Résultats, classements, actus NBA et défis quotidiens – Enjoy !"
                ], className="texte-intro"),


                # 📆 Bloc 1 – Matchs à pronostiquer
                html.Div([
                    html.Div([
                        html.Hr(className="ligne-separatrice")
                    ], className="container-site"),

                    html.H2("Matchs à pronostiquer", className="titre-bloc"),
                    html.Div([
                        html.P("Voici les matchs des 7 prochains jours à ne surtout pas rater."),
                        html.P([
                            "Avant de faire ton choix, tu peux consulter les pages ",
                            html.Strong("Statistiques, Joueurs ou Classement"),
                            " pour affiner ton analyse."
                        ]),
                        html.P([
                            "👉 ",
                            html.Strong("Clique sur le bouton sous l'équipe que tu vois gagnante.")
                        ]),
                        html.P([
                            "🚨 ",
                            html.Strong("Attention : une fois ton choix validé, il sera définitif."),
                            " Impossible de revenir en arrière !"
                        ]),
                        html.P([
                            "⏳ Tu peux pronostiquer jusqu’à l’heure de début du match.",
                            " Ensuite, c’est verrouillé automatiquement !"
                        ])
                    ], className="texte-description"),

                    html.Div(id="bloc_matchs")
                ], className="section-bloc"),

                # 🔜 Autres blocs prévus (non encore activés)
                html.Div([
                    html.Div([
                        html.Hr(className="ligne-separatrice")
                    ], className="container-site"),
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
                    html.Hr(className="ligne-separatrice")
                ], className="container-site"),
                html.Div([
                    html.H2("Dernières infos NBA", className="titre-bloc"),
                    html.Ul(id="bloc_actu", className="liste-actus")
                ], className="section-bloc"),

            ], className="container-site")  # ← tout contenu aligné ici

        ]
    )
