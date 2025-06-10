# ======================================
# 🔐 Page de Connexion - NBA Dashboard
# ======================================

from dash import html, dcc
import dash_bootstrap_components as dbc

# 🧱 Layout simple : pseudo + mdp + bouton
connexion_layout = html.Div([
    html.H2("Connexion à NBA Dashboard", className="titre-texte", style={"textAlign": "center", "marginTop": "50px"}),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Input(id="champ_pseudo", placeholder="Votre pseudo", type="text", className="mb-3"),
                dbc.Input(id="champ_mdp", placeholder="Mot de passe", type="password", className="mb-3"),
                dbc.Button("Connexion", id="bouton_connexion", color="primary", className="w-100"),
                html.Div(id="message_connexion", style={"marginTop": "15px", "color": "red", "textAlign": "center"})
            ], width=6)
        ], justify="center")
    ]),

    dcc.Location(id="redir_connexion", refresh=True)
])
