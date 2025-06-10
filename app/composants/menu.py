# ======================================
# 📋 Barre de navigation responsive stylisée avec logos
# ======================================

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback

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

def navbar():
    return html.Div([
        dcc.Store(id="session_utilisateur", storage_type="session"),

        dbc.Navbar(
            dbc.Container([
                dbc.NavbarBrand("NBA Dashboard", href="/", className="ms-2 navbar-title"),

                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

                dbc.Collapse(
                    dbc.Nav(id="menu_nav_items", className="ms-auto", navbar=True),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True
                ),
            ]),
            color="dark",
            dark=True,
            sticky="top",
            className="navbar-custom"
        )
    ])

# 📦 Callback pour afficher menu adapté à l’état connecté
@callback(
    Output("menu_nav_items", "children"),
    Input("session_utilisateur", "data")
)
def afficher_menu(session):
    liens = [
        lien("accueil.png", "Accueil", "/"),
        lien("statistiques.png", "Statistiques", "/statistiques"),
        lien("joueurs.png", "Joueurs", "/joueurs"),
        lien("pronostics.png", "Pronostics", "/pronostics"),
        lien("classement.png", "Classement", "/classement"),
        lien("palmares.png", "Palmarès", "/palmares"),
        lien("admin.png", "Admin", "/admin")
    ]

    if session and session.get("connecté"):
        # Bouton déconnexion
        liens.append(
            dbc.NavItem(
                dbc.Button("Déconnexion", id="bouton_deconnexion", color="danger", className="ms-3", size="sm")
            )
        )

    return liens
