# === Application principale Dash ===

from dash import Dash, html
import dash_bootstrap_components as dbc

# Initialisation de l'app
application = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = application.server  # pour Render

# Layout principal (peut évoluer avec une navbar + pages)
application.layout = html.Div([
    html.H1("NBA Dashboard", style={"textAlign": "center"}),
    html.Div("Bienvenue sur le tableau de bord NBA interactif.")
])

# Lancement local
if __name__ == "__main__":
    application.run_server(debug=True, host="0.0.0.0", port=8050)
