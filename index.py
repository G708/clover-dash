from dash import html, dcc, Input, Output
import argparse
import socket

from app import app
import degClover_dash
import datasources
import document

# faviconの定義
favicon = "assets/Favicons.ico/favicon.ico"

# FIXME: use gricon for published app
# https://hogetech.info/network/server/gunicorn



@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/datasources':
        return datasources.build_layout()
    if pathname == '/document':
        return document.build_layout()
    else:
        return degClover_dash.build_layout() # homepage
    
app.layout = html.Div([
    html.Link(rel='icon', href=favicon),
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Clover Dash app')
    parser.add_argument("--port", "-p",
                    type=int,
                    default=8050,
                    help="port number. Check available port before as `lsof -i:8050`")
    args = parser.parse_args()

    app.run_server(host='0.0.0.0', debug=True, port = args.port)