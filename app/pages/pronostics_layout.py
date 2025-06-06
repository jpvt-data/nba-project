# ======================================
# 🧠 Page Pronostics - Layout
# ======================================

from dash import html

def pronostics_layout():
    return html.Div(
        [
            html.H1("Pronostics entre amis", className="titre-texte"),
            html.P("Interface de jeu à venir...", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
