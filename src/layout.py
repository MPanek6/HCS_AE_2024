import dash_mantine_components as dmc
import pandas as pd

from dash import html, dash_table
from dash_iconify import DashIconify

header = html.Div(html.Img(src='assets/uog logo.png'), className='header')

layout = html.Div(children=[
    header,
    dmc.LoadingOverlay(html.Div(children=[
        html.H1('Case study'),
        html.Div([
            dmc.Grid([dmc.Col(dmc.TextInput(label="Participant ID", id="participant_id"))])
            ], id='study_form'),
        dmc.Grid([
            dmc.Col(dmc.Button(
            "Start",
            leftIcon=DashIconify(icon="ic:outline-not-started"),
            id='start_btn',
            fullWidth=True
            ), span=3, offset=9),
            dmc.Col(dmc.Button(
            "End study",
            leftIcon=DashIconify(icon="ic:outline-stop-circle"),
            id='end_btn',
            n_clicks=1,
            fullWidth=True,
            color='red',
            style={'display': 'none'},
            ), span=3, offset=6),
            dmc.Col(dmc.Button(
            "Next Level",
            leftIcon=DashIconify(icon="ic:baseline-navigate-next"),
            id='next_btn',
            n_clicks=0,
            fullWidth=True,
            style={'display': 'none'},
            ), span=3)])
    ]), className='main_content'),
    html.Div([], id='participant_val', style={'display': 'none'}),
    html.Div([dash_table.DataTable(pd.DataFrame().to_records(), id='study_df')], style={'display': 'none'}),
    dmc.Modal(
        title="Thank You",
        id="end_modal",
        zIndex=10000,
        children=[dmc.Text("Thank you for participating in our case study!")]
    )
])
