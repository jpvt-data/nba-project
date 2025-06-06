# ======================================
# 🏆 Page Classement - Layout
# ======================================

from dash import html

def classement_layout():
    return html.Div(
        [
            html.H1("Classement des utilisateurs", className="titre-texte"),
            html.P("Classement en cours de mise en place...", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
