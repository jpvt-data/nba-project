# ======================================
# 🏆 Page SwishRank - Classement utilisateurs
# ======================================

import pandas as pd
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def swishrank_layout(pseudo):
    # Chargement des données
    df_stats = pd.read_csv("data/processed/vue_ensemble_stats_prono_par_utilisateur.csv")
    df_stats = df_stats[df_stats["utilisateur"] != "admin33"]
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

    # ======================================
    # 📋 Tableaux des pronostics & classement utilisateurs
    # ======================================

    # 📥 Chargement des pronostics
    df_pronos = pd.read_csv("data/processed/pronostics_eval.csv")
    df_pronos = df_pronos[df_pronos["utilisateur"] == pseudo]

    df_pronos["date_match"] = pd.to_datetime(df_pronos["date_match"]).dt.strftime("%d/%m/%Y")

    # 🏀 Détermination vainqueur
    df_pronos["victoire"] = df_pronos.apply(
        lambda row: row["équipe_domicile"] if row["score_domicile"] > row["score_extérieur"]
        else row["équipe_extérieure"], axis=1
    )

    # ✅ Emoji pour bon pronostic
    df_pronos["✔"] = df_pronos["pronostic_correct"].apply(lambda x: "✅" if x else "❌")

    # 🔢 Numérotation des pronostics
    df_pronos = df_pronos.sort_values("date_match").reset_index(drop=True)
    df_pronos["#"] = df_pronos.index + 1

    # 🧱 Sélection et réorganisation des colonnes
    colonnes = [
        "#", "type_match", "date_match", "équipe_domicile", "équipe_extérieure",
        "victoire", "équipe_pronostiquée", "✔"
    ]
    df_affiche = df_pronos[colonnes].rename(columns={
        "type_match": "Type",
        "date_match": "Date Match",
        "équipe_domicile": "Domicile",
        "équipe_extérieure": "Extérieur",
        "victoire": "Victoire",
        "équipe_pronostiquée": "Choix"
    })

    # 🧾 Construction tableau HTML
    entetes_pronos = df_affiche.columns.tolist()
    lignes_pronos = []

    for _, row in df_affiche.iterrows():
        cellules = [html.Td(row[col]) for col in entetes_pronos]
        lignes_pronos.append(html.Tr(cellules))

    tableau_pronos = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in entetes_pronos])),
        html.Tbody(lignes_pronos)
    ], className="tableau-ranking")



    # 📥 Chargement stats utilisateurs
    df_stats = pd.read_csv("data/processed/vue_ensemble_stats_prono_par_utilisateur.csv")
    df_stats = df_stats[df_stats["utilisateur"] != "admin33"]

    # 🔢 Tri par % réussite DESC puis total_pronostics DESC
    df_stats = df_stats.sort_values(by=["taux_reussite (%)", "total_pronostics"], ascending=[False, False])


    # 🔢 Ajout du rang (1 à N)
    df_stats = df_stats.reset_index(drop=True)
    df_stats["#"] = df_stats.index + 1

    # 🧱 Construction tableau HTML – Classement global
    colonnes_stats = [
        "#", "utilisateur", "total_pronostics", "bons_pronostics",
        "taux_reussite (%)", "couverture_matchs (%)", "équipe_favorite"
    ]
    entetes_stats = ["#", "Swisher", "Nb Pronos", "Pronos ✅", "% Réussite", "% Implication", "Équipe favorite"]

    lignes_utilisateurs = []

    for _, row in df_stats.iterrows():
        cellules = [html.Td(row[col]) for col in colonnes_stats]
        lignes_utilisateurs.append(html.Tr(cellules))

        tableau_complet = html.Div([
            html.Img(
                src="/assets/logos/swish_league_logo.png",  # adapte le chemin
                style={
                    "height": "130px",
                    "marginBottom": "20px",
                    "display": "block",
                    "marginLeft": "auto",
                    "marginRight": "auto"
                },
                alt="Badge Swish League"
            ),

            html.H4(
                "Classement Swish League",
                className="titre-bloc-droit",
                style={
                    "fontSize": "1.2rem",
                    "marginBottom": "12px",
                    "fontWeight": "bold",
                    "textAlign": "left"
                }
            ),


            html.Table([
                html.Thead(html.Tr([html.Th(col) for col in entetes_stats])),
                html.Tbody(lignes_utilisateurs)
            ], className="tableau-ranking")
        ])



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

    # Layout final harmonisé – version épurée
    return html.Div(
        style={"backgroundColor": "#121212", "minHeight": "100vh"},
        children=[
            html.Div([
                html.H2("Swish League", className="titre-bloc section-bienvenue"),
                html.P("Compare tes performances avec les autres swishers !", className="texte-description"),

                dbc.Row([
                    dbc.Col(bloc_avatar, lg=4, sm=12),
                    dbc.Col([], lg=1),
                    dbc.Col(tableau_complet, lg=7, sm=12)
                ], className="gy-4 align-items-stretch"),


                html.Hr(className="ligne-separatrice"),

                html.H2("Mes pronostics", className="titre-bloc"),

                dbc.Row([
                    dbc.Col(tableau_pronos, lg=7, sm=12),
                    dbc.Col(
                        html.Div(
                            html.Img(
                                src="/assets/images/pronostic_horizontal.jpg",
                                className="img-fondu-vertical",
                                alt="Illustration pronostics"
                            ),
                            style={"height": "100%", "display": "flex", "alignItems": "center", "justifyContent": "center"}
                        ),
                        lg=5,
                        sm=12
                    )
                ], className="gy-3 align-items-stretch"),
                html.Hr(className="ligne-separatrice"),

                # 📈 Graphique analyse
                html.H2("Analyse des profils", className="titre-bloc"),
                html.Div(scatter_plot, style={"marginTop": "20px"})
            ], className="container-site")
        ]
    )
