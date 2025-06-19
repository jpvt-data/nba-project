# === 🧩 IMPORTS DASH ET BOOTSTRAP ===
from dash import html, dcc
import dash_bootstrap_components as dbc

# === 🖥️ LAYOUT DE LA PAGE DE CONNEXION ===
connexion_layout = html.Div(
    style={"backgroundColor": "#121212", "minHeight": "100vh"},
    children=[
        # 🏀 Logo NBA centré
        html.Div([
            html.Img(
                src="/assets/logos/swish_league_logo.png",
                style={
                    "height": "100px",
                    "margin": "20px auto 10px auto",
                    "display": "block"
                }
            )
        ]),

        # 🔝 Titre principal stylisé façon accueil
        html.Div([
            html.H2("Bienvenue dans Swish League !", className="titre-texte", style={"textAlign": "center", "marginTop": "20px"}),

            html.P(
                "Une appli pour suivre la saison NBA, faire des pronos entre potes et briller sur les stats !", 
                className="texte-intro", style={"textAlign": "center", "maxWidth": "700px", "margin": "10px auto 10px auto"}),
        
            html.P(
                "Saisissez votre identifiant et votre mot de passe pour accéder à l'application.",
                className="texte-accueil", style={"textAlign": "center", "marginBottom": "40px", "marginTop": "2px"}),
        ]),

        # 🛠️ Bloc connexion
        

        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Input(id="champ_pseudo", placeholder="Votre pseudo", type="text", className="champ-connexion mb-3"),
                    dbc.Input(id="champ_mdp", placeholder="Mot de passe", type="password", className="champ-connexion mb-3"),
                    dbc.Button("Connexion", id="bouton_connexion", color="primary", className="bouton-connexion"),
                    html.Div(id="message_connexion", className="message-erreur")
                ], width=12, lg=4)
            ], justify="center")
        ]),

        # 🔁 Redirection automatique si déjà connecté
        dcc.Location(id="redir_connexion", refresh=True)
    ]
)

