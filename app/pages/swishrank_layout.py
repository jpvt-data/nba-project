# ======================================
# 🏆 Page SwishRank - Classement utilisateurs
# ======================================

from dash import html

def swishrank_layout():
    return html.Div(
        [
            html.H1("SwishRank – Classement des pronostiqueurs", className="titre-texte"),
            html.P("Ici s’affichera le classement, les scores, et les stats des joueurs.", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
