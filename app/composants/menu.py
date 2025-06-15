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
                    lien("classement.png", "SwishRank", "/swishrank"),
                    lien("statistiques.png", "Stats NBA", "/statsnba"),
                    lien("connection.png", "Profil", "/profil"),
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

# ======================================
# 🔁 Callback pour le menu hamburger (mobile)
# ======================================

from dash.dependencies import Input, Output, State

def register_navbar_callbacks(app):
    @app.callback(
        Output("navbar-collapse", "is_open"),
        Input("navbar-toggler", "n_clicks"),
        State("navbar-collapse", "is_open")
    )
    def toggle_navbar(n, is_open):
        if n:
            return not is_open
        return is_open

