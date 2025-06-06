# ======================================
# 📊 Page Statistiques - Layout
# ======================================

from dash import html

def statistiques_layout():
    return html.Div(
        [
            html.H1("Statistiques NBA", className="titre-texte"),
            html.P("Analyse des statistiques à venir...", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
