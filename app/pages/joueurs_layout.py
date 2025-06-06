# ======================================
# 👥 Page Joueurs - Layout
# ======================================

from dash import html

def joueurs_layout():
    return html.Div(
        [
            html.H1("Détail des joueurs NBA", className="titre-texte"),
            html.P("Page Joueurs en préparation...", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
