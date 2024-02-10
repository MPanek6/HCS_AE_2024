import pandas as pd 
import datetime
import os 

from dash import html
from dash_extensions.enrich import Input, Output, State, no_update

from src.utils import get_study_form, gen_pin, get_form_data
from src.logger import logger

def get_callbacks(app):
    
    @app.callback(
        Input('start_btn', 'n_clicks'),
        State('participant_id', 'value'),
        Output('study_form', 'children'),
        Output('participant_val', 'children'),
        Output('start_btn', 'style'),
        Output('next_btn', 'style'),
        Output('end_btn', 'style'),
        prevent_initial_call=True
        )
    def start_study(btn, participant):
        if participant:
            pin = gen_pin()
            form = get_study_form(1, pin)
            return form, participant, {'display': 'none'}, {}, {}
        return no_update
    
    @app.callback(
        Input('next_btn', 'n_clicks'),
        State('participant_val', 'children'),
        State('study_df', 'data'),
        State('study_form', 'children'),
        Output('study_form', 'children'),
        Output('study_df', 'data'),
        Output('next_btn', 'n_clicks'),
        prevent_initial_call=True
        )
    def next_level(btn, participant, data, form):
        entered_pins, secure_q, usability_q = get_form_data(form)
        
        # Input validation on form. Ensures everything is filled out
        if entered_pins is False:
            return no_update, no_update, btn-1
        
        pin = gen_pin()
        
        if btn == 1:
            df = pd.DataFrame(data={'Participant ID': [participant], 'Level': ['1'], 'Actual Pins': [[pin]], 'Entered Pins': [entered_pins], 'Secure question': [secure_q], 'Usable question': [usability_q]})
        else:
            data.append({'Participant ID': participant, 'Level': btn, 'Actual Pins': data[-1]['Actual Pins'] + [pin], 'Entered Pins': entered_pins, 'Secure question': secure_q, 'Usable question': usability_q})
            df = pd.DataFrame.from_dict(data)
        form = get_study_form(btn+1, pin)
        return form, df.to_dict('records'), no_update
    
    @app.callback(
        Input('end_btn', 'n_clicks'),
        State('participant_val', 'children'),
        State('study_df', 'data'),
        Output('end_modal', 'opened'),
        prevent_initial_call=True
    )
    def end_study(btn, participant, data):
        if not os.path.isdir("Results\\"):
            os.makedirs('Results')
        df = pd.DataFrame.from_dict(data)
        df.to_csv(f'Results\\{participant} - Case Study - {datetime.datetime.now().strftime("%Y-%m-%d %H;%M;%S")}.csv', index=False)
        return True