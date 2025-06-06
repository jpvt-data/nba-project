# ======================================
# 🔐 Page Connexion - Layout
# ======================================

from dash import html

def connexion_layout():
    return html.Div(
        [
            html.H1("Connexion / Choix du pseudo", className="titre-texte"),
            html.P("Interface de session MVP à implémenter...", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
