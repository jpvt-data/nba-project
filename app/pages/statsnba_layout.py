# ======================================
# 📊 Page Stats NBA - Navigation Tri-Boutons
# ======================================

from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

def statsnba_layout():
    return html.Div(
        style={"backgroundColor": "#121212", "minHeight": "100vh"},
        children=[
            html.Div([
                # === Bloc Titre + Boutons sur la même ligne desktop, empilé mobile
                html.Div(
                    [
                        html.H2("Stats NBA", className="titre-bloc section-bienvenue", id="titre-statsnba"),
                        html.Div(
                            id="bloc_boutons_statsnba",
                            children=[
                                dbc.Button("Résultats", id="btn-resultats", n_clicks=1, className="bouton-sw bouton-statsnba"),
                                dbc.Button("Joueurs", id="btn-joueurs", n_clicks=0, className="bouton-sw bouton-statsnba"),
                                dbc.Button("Hall of Fame", id="btn-hof", n_clicks=0, className="bouton-sw bouton-statsnba"),
                            ],
                        ),
                    ],
                    id="ligne-titre-boutons",
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between", 
                        "gap": "28px",
                        "flexWrap": "nowrap",
                        "margin": "38px auto 22px auto",
                        "width": "100%",
                        "maxWidth": "950px",
                        "boxSizing": "border-box"
                    }
                ),
                # === Le reste du contenu de la page...
                html.Div(id="bloc_statsnba_contenu", style={"marginTop": "24px"}),
            ], className="container-site")
        ]
    )
