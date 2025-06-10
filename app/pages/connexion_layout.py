from dash import html, dcc

def connexion_layout():
    return html.Div([
        html.H1("Connexion", className="titre-texte", style={"textAlign": "center"}),

        html.Div([
            dcc.Input(
                id="champ_pseudo",
                type="text",
                placeholder="Identifiant",
                className="input-login",
                style={"marginBottom": "10px", "width": "100%", "padding": "10px"}
            ),
            dcc.Input(
                id="champ_mdp",
                type="password",
                placeholder="Mot de passe",
                className="input-login",
                style={"marginBottom": "10px", "width": "100%", "padding": "10px"}
            ),
            html.Button("Se connecter", id="bouton_connexion", className="bouton-prono", style={"width": "100%"}),
            html.Div(id="message_connexion", style={"color": "red", "marginTop": "15px", "textAlign": "center"}),

            # 🔁 Redirection JS custom
            dcc.Interval(id="redir_forcee", interval=1, n_intervals=0, disabled=True),
            html.Script("""
                const observer = new MutationObserver((mutations) => {
                    mutations.forEach((m) => {
                        if (m.target.textContent === '__REDIR__') {
                            window.location.href = '/';
                        }
                    });
                });
                observer.observe(document.body, { childList: true, subtree: true });
            """),
            html.Div(id="fake_trigger", style={"display": "none"})
        ], style={"maxWidth": "400px", "margin": "0 auto"})
    ],
    style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "40px"})
