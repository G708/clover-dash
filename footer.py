from dash import html
import dash_bootstrap_components as dbc

# LOGO = "logo.png"
# PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
PLOTLY_LOGO = "https://dash.gallery/Manager/portals_data/default/logo_8a3aad42-392d-11ed-becf-0242ac110014.png"
GitHub_LOGO = "assets/github-mark/github-mark.png"
Clover_GitHub_URL = "https://github.com/G708/Dash_demo"

padding = {
    "padding-left": "10%", "padding-right": "10%",
    "padding-top": "2%", "padding-bottom": "2%",
    "width": "100%"
    }

LAYOUT = html.Footer(id="footer",
    children=[
        html.Span([
            dbc.Row([
            dbc.Col(

                    html.A(
                    [
                        html.Img(src=PLOTLY_LOGO, style={'width':'200px'}),
                    ], 
                    href='https://plotly.com',
                    target='_blank'
                    ),
                    xs=12,  # For extra small screen widths
                    md=4,    # For medium (and larger) screen widths
                    ),
            dbc.Col(
                    html.A(
                    [
                        html.Img(src=GitHub_LOGO, id="GH_logo", style={'width':'50px'}),
                    ], 
                    href=Clover_GitHub_URL,
                    target='_blank'
                    ), 
                    xs=12,  # For extra small screen widths
                    md=3,    # For medium (and larger) screen widths
                    ),


                ]),
            ]),
            
            html.P(u"\u00A9" + " 2023", style={'float': 'right', 'margin-right': '10px'})
        ], style=padding)
