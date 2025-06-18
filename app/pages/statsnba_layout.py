# ======================================
# 📊 Page Stats NBA - Classement Equipes
# ======================================

from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

# 📦 Chargement initial pour les options dynamiques
chemin_csv = "data/processed/saison/classement_conf_saisons_total.csv"
df_classement = pd.read_csv(chemin_csv)

# 📌 Options disponibles pour les menus déroulants
options_saisons = sorted(df_classement["Année"].dropna().unique(), reverse=True)
options_conferences = df_classement["CONFERENCE"].dropna().unique()


def statsnba_layout():
    return html.Div(
        style={"backgroundColor": "#121212", "minHeight": "100vh"},
        children=[
            html.Div([
                html.H2("Classement NBA", className="titre-bloc section-bienvenue"),

                # 🎛️ Filtres interactifs
                dbc.Row([
                    dbc.Col([
                        html.Label("Type de saison", className="label-filtre"),
                        dcc.Dropdown(
                            id="filtre_type_saison",
                            options=[
                                {"label": "Saison régulière", "value": "regular"},
                                {"label": "Playoffs", "value": "playoffs"},
                                {"label": "Finals", "value": "finals"}
                            ],
                            value="regular",
                            className="dropdown-sw"
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Saison (Année)", className="label-filtre"),
                        dcc.Dropdown(
                            id="filtre_annee",
                            options=[{"label": str(annee), "value": annee} for annee in options_saisons],
                            value=options_saisons[0],
                            className="dropdown-sw"
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Conférence", className="label-filtre"),
                        dcc.Dropdown(
                            id="filtre_conference",
                            options=[{"label": conf, "value": conf} for conf in options_conferences],
                            value=options_conferences[0],
                            className="dropdown-sw"
                        )
                    ], md=4)
                ], className="gy-3"),

                html.Hr(className="ligne-separatrice"),

                # 📊 Conteneur tableau classement
                html.Div(id="tableau_classement")
            ], className="container-site")
        ]
    )
