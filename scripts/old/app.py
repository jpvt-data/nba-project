# app.py
"""
Application principale Dash avec routage multi-pages et thème sombre.
"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import sys
import os
sys.path.append(os.path.dirname(__file__))


# Initialisation de l'app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "NBA Dashboard"
server = app.server  # utile pour le déploiement Render

# Layout principal avec détection d'URL
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')  # zone où la page sélectionnée est affichée
])

# Routing selon URL
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def afficher_page(pathname):
    if pathname == '/' or pathname == '/accueil':
        from pages.accueil_layout import accueil_layout
        return accueil_layout()
    elif pathname == '/statistiques':
        from pages.statistiques_layout import statistiques_layout
        return statistiques_layout()
    elif pathname == '/joueurs':
        from pages.joueurs_layout import joueurs_layout
        return joueurs_layout()
    elif pathname == '/pronostics':
        from pages.pronostics_layout import pronostics_layout
        return pronostics_layout()
    elif pathname == '/classement':
        from pages.classement_layout import classement_layout
        return classement_layout()
    elif pathname == '/palmares':
        from pages.palmares_layout import palmares_layout
        return palmares_layout()
    elif pathname == '/connexion':
        from pages.connexion_layout import connexion_layout
        return connexion_layout()
    else:
        return html.Div("404 - Page non trouvée", style={"color": "red", "padding": "2rem"})

# Lancement de l'app
if __name__ == '__main__':
    app.run(debug=True)
