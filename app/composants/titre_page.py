# ======================================
# 🏀 Composant titre de page avec icône
# ======================================

from dash import html

def titre_page(titre: str, logo: str):
    return html.Div(
        className="titre-page",
        children=[
            html.Img(src=f"/assets/logos/{logo}", className="titre-logo"),
            html.H1(titre, className="titre-texte")
        ]
    )
