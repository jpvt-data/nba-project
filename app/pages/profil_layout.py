# ======================================
# 👤 Page Profil utilisateur - Layout
# ======================================

from dash import html

def profil_layout():
    return html.Div(
        [
            html.H1("Mon Profil", className="titre-texte"),
            html.P("Informations personnelles, historique de pronostics, et performances.", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
