# ======================================
# 📊 Page Stats NBA - Layout
# ======================================

from dash import html

def statsnba_layout():
    return html.Div(
        [
            html.H1("Stats NBA – Données historiques", className="titre-texte"),
            html.P("Ici s’afficheront les stats des joueurs, équipes, palmarès et Hall of Fame.", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
