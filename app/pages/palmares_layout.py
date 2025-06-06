# ======================================
# 🥇 Page Palmarès - Layout
# ======================================

from dash import html

def palmares_layout():
    return html.Div(
        [
            html.H1("Palmarès NBA (Champions & MVP)", className="titre-texte"),
            html.P("Historique des saisons à venir...", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
