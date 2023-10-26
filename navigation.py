from dash import html, Input, Output, State
import dash_bootstrap_components as dbc

from app import app

LOGO = "assets/DEGClover_logo.svg"

nav_item = dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/index")),
        dbc.NavItem(dbc.NavLink("Data sources", href="/datasources")),
        dbc.NavItem(dbc.NavLink("Document", href="/document")),
        # dbc.DropdownMenu(
        #     children=[
        #         # dbc.DropdownMenuItem("More pages", header=True),
        #         # dbc.DropdownMenuItem(
        #         #     f"{page['name']}, href={page['relative_path']}"
        #         # )
        #         # for page in dash.page_registry.values()
        #         dbc.DropdownMenuItem("Community forums", href="https://community.okama.io"),
        #         # dbc.DropdownMenuItem("Compare Assets", href="/")
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],className="ml-auto",navbar=True,
)

LAYOUT = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("Clover", className="ms-2", style={"font-size": "200%"})),
                    ],
                    align="center",
                    className="g-0",
                ),
                href=".",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                nav_item,
                navbar=True,
                id="navbar-collapse"
                )
        ],fluid=True,
    ),
    color="dark",
    dark=True,
    style={"font-size": "150%", "padding-left": "10%", "padding-right": "10%"},
    sticky = "top"
)

# we use a callback to toggle the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open