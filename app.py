import dash_bootstrap_components as dbc

from flask import Flask
from dash_extensions.enrich import DashProxy, MultiplexerTransform

from src.layout import layout
from src.callbacks import get_callbacks

flask_app = Flask(__name__)
flask_app.secret_key = 'HCS_AE_2024'

app = DashProxy(__name__, server=flask_app, external_stylesheets=[dbc.themes.BOOTSTRAP], transforms=[MultiplexerTransform()])

app.title = 'HCS AE Case Study'

app.layout = layout

get_callbacks(app)

if __name__ == '__main__':
    flask_app.run(debug=True)