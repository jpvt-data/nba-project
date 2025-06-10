# === 🧩 IMPORTS DASH ET BOOTSTRAP ===
from dash import html, dcc
import dash_bootstrap_components as dbc

# === 🖥️ LAYOUT DE LA PAGE DE CONNEXION ===
connexion_layout = html.Div([
    
    # ✅ Titre principal
    html.H2("Accès à Swish League 🏀 !", className="titre-texte", style={"textAlign": "center", "marginTop": "50px"}),

    # 💬 Texte d’accueil sympa
    html.P("Salut les copains ! Saisissez votre identifiant et votre mot de passe pour accéder à l'aplication !",
           className="texte-accueil", style={"textAlign": "center", "marginBottom": "40px", "marginTop": "10px"}),

    # 🔐 Formulaire de connexion centré
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
])
