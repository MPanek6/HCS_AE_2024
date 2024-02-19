import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd

from dash import html, dash_table
from dash_iconify import DashIconify

header = html.Div(html.Img(src='assets/uog logo.png'), className='header')

layout = html.Div(children=[
    header,
    dmc.LoadingOverlay(html.Div(children=[
        html.H1('Case study'),
        html.H3('Lives left: ', style={'display': 'inline'}),
        html.H3(3, id='lives_val', style={'display': 'inline'}),
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
            "Submit",
            leftIcon=DashIconify(icon="ic:baseline-navigate-next"),
            id='next_btn',
            n_clicks=0,
            fullWidth=True,
            style={'display': 'none'},
            ), span=3, offset=9)])
    ]), className='main_content'),
    html.Div([], id='participant_val', style={'display': 'none'}),
    html.Div([], id='actual_pin_div', style={'display': 'none'}),
    html.Div([dash_table.DataTable(pd.DataFrame().to_records(), id='study_df')], style={'display': 'none'}),
    dmc.Modal(
        title="Thank You",
        id="ty_modal",
        zIndex=10001,
        children=[dmc.Text("Thank you for participating in our case study!")],
        withCloseButton=False,
        closeOnClickOutside=False,
        closeOnEscape=False,
    ),
    dmc.Modal(
        title="End Questionnaire",
        id="end_modal",
        zIndex=10000,
        children=[dbc.Form(dmc.Grid([
            dmc.Col(dmc.RadioGroup(
                [dmc.Radio('Yes', 'Yes'), dmc.Radio('No', 'No')],
                label="Would you be willing to use this many passwords day-to-day?",
                orientation='horizontal',
                required=True,
                id="q_daytoday"
                )),
            dmc.Col(
                dmc.MultiSelect(
                    label="What type of apps would you use this security style for?",
                    data=['None', 'Entertainment', 'Finance', 'Food Delivery', 'Games', 'Shopping', 'Social Media', 'Utility'],
                    id='q_apptype',
                    required=True
                ))
            ]), id='end_form'),
                  dmc.Group([
                      dmc.Button(
                          "End study",
                          leftIcon=DashIconify(icon="ic:outline-stop-circle"),
                          id='end_btn',
                          color='red')
                    ],
                    position="right",
                )],
        withCloseButton=False,
        closeOnClickOutside=False,
        closeOnEscape=False,
    )
])
