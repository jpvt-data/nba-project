# ======================================
# 🧪 Page Admin / Test - Layout
# ======================================

from dash import html

def admin_layout():
    return html.Div(
        [
            html.H1("Espace admin (dev/test)", className="titre-texte"),
            html.P("Zone de test réservée aux développeurs...", className="texte-secondaire")
        ],
        style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "30px"}
    )
