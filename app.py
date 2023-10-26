from dash import Dash
import dash_bootstrap_components as dbc
from flask import Flask

external_scripts = [
    {'src': 'https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js'},
    {'src': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'}
]
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', './custom.css']
external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = Flask(__name__)

app = Dash(
    external_stylesheets = external_stylesheets, 
    external_scripts = external_scripts, 
    suppress_callback_exceptions = True, 
    update_title="Loading ...",
    server = server
)
app.title = 'Clover'