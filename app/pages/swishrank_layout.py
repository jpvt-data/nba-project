# ======================================
# 🏆 Page SwishRank - Classement utilisateurs
# ======================================

import pandas as pd
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# Chargement des données
df_stats = pd.read_csv("data/processed/vue_ensemble_stats_prono_par_utilisateur.csv")
df_stats = df_stats[df_stats["utilisateur"] != "admin33"]

def swishrank_layout(pseudo="Polo"):
    stats = df_stats[df_stats["utilisateur"] == pseudo]
    total = int(stats["total_pronostics"].values[0]) if not stats.empty else 0
    reussite = f"{stats['taux_reussite (%)'].values[0]}%" if not stats.empty else ""
    equipe = stats["équipe_favorite"].values[0] if not stats.empty else "?"

    # Bloc avatar utilisateur
    bloc_avatar = html.Div([
        html.Div([
            html.Div([
                html.Img(src=f"/assets/avatars/{pseudo}.png", className="bloc-avatar-img"),
                html.H3(pseudo, className="bloc-avatar-nom")
            ], className="bloc-avatar-gauche"),
            html.Div([
                html.Div([html.Span("Total pronostics", className="bloc-label"), html.Span(f"{total}", className="bloc-valeur")], className="bloc-stat"),
                html.Div([html.Span("Pronos réussis", className="bloc-label"), html.Span(f"{reussite}", className="bloc-valeur")], className="bloc-stat"),
                html.Div([html.Span("Équipe favorite", className="bloc-label"), html.Span(f"{equipe}", className="bloc-valeur equipe-valeur")], className="bloc-stat")
            ], className="bloc-avatar-stats")
        ], className="bloc-avatar-ligne")
    ], className="bloc-avatar-wrapper")

    # Top 3
    top_actifs = df_stats.sort_values(by="total_pronostics", ascending=False).head(10)
    top3 = top_actifs.sort_values(by="taux_reussite (%)", ascending=False).head(3).reset_index(drop=True)

    bloc_ranking = html.Div([
        html.H4("Top 3 Swish Rank", className="titre-bloc-droit"),
        html.Table([
            html.Thead(html.Tr([html.Th("Swisher"), html.Th("Nb Pronostics"), html.Th("% Réussite")])),
            html.Tbody([
                html.Tr([html.Td(top3.loc[i, "utilisateur"]),
                         html.Td(f"{top3.loc[i, 'total_pronostics']}"),
                         html.Td(f"{top3.loc[i, 'taux_reussite (%)']:.1f}%")])
                for i in range(min(3, len(top3)))
            ])
        ], className="tableau-ranking"),
    ], className="bloc-ranking-wrapper")

    # ======================================
    # 📋 Tableau des pronostics effectués
    # ======================================

    # Chargement des pronostics
    df_pronos = pd.read_csv("data/processed/pronostics_eval.csv")
    df_pronos = df_pronos[df_pronos["utilisateur"] == pseudo]

    # Conversion UTC → Heure de Paris
    df_pronos["date_pronostic"] = pd.to_datetime(df_pronos["date_pronostic"], utc=True).dt.tz_convert("Europe/Paris")
    df_pronos["date_pronostic"] = df_pronos["date_pronostic"].dt.strftime("%d/%m/%Y %H:%M")

    # Conversion emoji pour la colonne 'pronostic_correct'
    df_pronos["résultat"] = df_pronos["pronostic_correct"].apply(lambda x: "✅" if x else "❌")

    # Sélection et renommage des colonnes utiles
    df_affiche = df_pronos[[
        "date_pronostic", "date_match", "équipe_domicile", "score_domicile",
        "équipe_extérieure", "score_extérieur", "équipe_pronostiquée",
        "résultat", "type_match"
    ]].rename(columns={
        "date_pronostic": "Date Prono (Paris)",
        "date_match": "Date Match",
        "équipe_domicile": "Domicile",
        "score_domicile": "Score D",
        "équipe_extérieure": "Extérieur",
        "score_extérieur": "Score E",
        "équipe_pronostiquée": "Choix",
        "résultat": "✔",
        "type_match": "Type"
    })

    # Tableau stylisé
    tableau_pronos = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df_affiche.columns],
        data=df_affiche.to_dict("records"),
        style_table={"overflowX": "auto", "marginTop": "20px"},
        style_cell={
            "textAlign": "center",
            "padding": "10px",
            "fontFamily": "Exo 2, sans-serif",
            "backgroundColor": "#121212",
            "color": "white",
            "border": "none"
        },
        style_header={
            "backgroundColor": "#1E1E1E",
            "color": "white",
            "fontWeight": "bold",
            "borderBottom": "2px solid #444"
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#1A1A1A"
            },
            {
                "if": {"column_id": "✔"},
                "fontSize": "1.3rem"
            }
        ],
        sort_action="native",
        page_size=10
    )


    # 📊 Tableau complet des pronostiqueurs – version stylisée
    tableau_complet = dash_table.DataTable(
        columns=[
            {"name": "Pseudo", "id": "utilisateur"},
            {"name": "Total Pronos", "id": "total_pronostics"},
            {"name": "Bons", "id": "bons_pronostics"},
            {"name": "% Réussite", "id": "taux_reussite (%)"},
            {"name": "Couverture", "id": "couverture_matchs (%)"},
            {"name": "Équipe favorite", "id": "équipe_favorite"}
        ],
        data=df_stats.to_dict("records"),
        style_table={"overflowX": "auto", "border": "none", "marginTop": "20px"},
        style_cell={
            "textAlign": "center",
            "padding": "12px",
            "fontFamily": "Exo 2, sans-serif",
            "backgroundColor": "#121212",
            "color": "white",
            "border": "none"
        },
        style_header={
            "backgroundColor": "#1E1E1E",
            "color": "#ffffff",
            "fontWeight": "bold",
            "borderBottom": "2px solid #444"
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#1A1A1A"
            },
            {
                "if": {"column_id": "équipe_favorite"},
                "color": "#FFDE59",  # Accent couleur pour la colonne finale
                "fontWeight": "bold"
            }
        ],
        css=[{
            "selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner",
            "rule": "border: none !important;"
        }],
        sort_action="native",
        page_size=10
    )


    # Graphique Volume vs Précision
    scatter_plot = dcc.Graph(
        figure={
            "data": [{
                "x": df_stats["total_pronostics"],
                "y": df_stats["taux_reussite (%)"],
                "text": df_stats["utilisateur"],
                "mode": "markers",
                "marker": {"size": 12, "color": "#FF4136"},
                "hovertemplate": "%{text}<br>Pronos: %{x}<br>% Réussite: %{y:.1f}%<extra></extra>"
            }],
            "layout": {
                "plot_bgcolor": "#121212",
                "paper_bgcolor": "#121212",
                "font": {"color": "white"},
                "xaxis": {"title": "Total pronostics"},
                "yaxis": {"title": "% Réussite"},
                "title": "Volume vs Précision"
            }
        }
    )

    # Layout final harmonisé
    return html.Div(
        style={"backgroundColor": "#121212", "minHeight": "100vh"},
        children=[
            html.Div([
                html.H2("SwishRank – Classement des pronostiqueurs", className="titre-bloc section-bienvenue"),
                html.P("Compare tes performances avec les autres swishers !", className="texte-description"),

                dbc.Row([
                    dbc.Col(bloc_avatar, lg=5, sm=12),
                    dbc.Col(bloc_ranking, lg=7, sm=12)
                ], className="gy-4 align-items-center"),

                html.Hr(className="ligne-separatrice"),

                html.H2("Historique de tes pronostics", className="titre-bloc"),
                html.Div(tableau_pronos),
                html.Hr(className="ligne-separatrice"),


                html.H2("Classement complet", className="titre-bloc"),
                html.Div(tableau_complet, style={"marginTop": "20px"}),

                html.Hr(className="ligne-separatrice"),

                html.H2("Analyse des profils", className="titre-bloc"),
                html.Div(scatter_plot, style={"marginTop": "20px"})
            ], className="container-site")
        ]
    )
