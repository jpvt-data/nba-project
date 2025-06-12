# ======================================
# 📋 Barre de navigation responsive stylisée avec logos
# ======================================

from dash import html, dcc
import dash_bootstrap_components as dbc

def navbar():
    def lien(img, texte, href):
        return dbc.NavItem(
            dbc.NavLink(
                children=[
                    html.Img(src=f"/assets/logos/{img}", className="nav-logo"),
                    html.Span(texte, className="nav-text")
                ],
                href=href,
                active="exact",
                className="nav-link-custom"
            )
        )

    return dbc.Navbar(
        children=[
            dbc.NavbarBrand(
                html.Div([
                    html.Img(src="/assets/logos/nba_logo.png", className="navbar-logo"),
                    html.Span("Swish League", className="nav-titre")
                ], className="d-flex align-items-center navbar-brand-wrapper"),
                href="/"
            ),

            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(
                dbc.Nav([
                    lien("accueil.png", "Accueil", "/"),
                    lien("statistiques.png", "Statistiques", "/statistiques"),
                    lien("joueurs.png", "Joueurs", "/joueurs"),
                    lien("pronostics.png", "Pronostics", "/pronostics"),
                    lien("classement.png", "Classement", "/classement"),
                    lien("palmares.png", "Palmarès", "/palmares"),
                    lien("connection.png", "Connexion", "/connexion"),
                    lien("admin.png", "Admin", "/admin")
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                is_open=False,
                navbar=True
            ),
        ],
        color="dark",
        dark=True,
        sticky="top",
        className="navbar-custom"
    )

