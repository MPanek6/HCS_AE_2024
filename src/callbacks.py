import pandas as pd 
import datetime
import os 

from dash import html
from dash_extensions.enrich import Input, Output, State, no_update

from src.utils import get_study_form, gen_pin, get_form_data, get_end_form_data

def get_callbacks(app):
    
    @app.callback(
        Input('start_btn', 'n_clicks'),
        State('participant_id', 'value'),
        Output('study_form', 'children'),
        Output('participant_val', 'children'),
        Output('start_btn', 'style'),
        Output('next_btn', 'style'),
        Output('actual_pin_div', 'children'),
        prevent_initial_call=True
        )
    def start_study(btn, participant):
        if participant:
            pin = gen_pin()
            form = get_study_form(1, pin)
            return form, participant, {'display': 'none'}, {}, pin
        return no_update
    
    @app.callback(
        Input('next_btn', 'n_clicks'),
        State('participant_val', 'children'),
        State('study_df', 'data'),
        State('study_form', 'children'),
        State('lives_val', 'children'),
        State('actual_pin_div', 'children'),
        Output('study_form', 'children'),
        Output('study_df', 'data'),
        Output('next_btn', 'n_clicks'),
        Output('lives_val', 'children'),
        Output('actual_pin_div', 'children'),
        Output('end_modal', 'opened'),
        prevent_initial_call=True
        )
    def next_level(btn, participant, data, form, lives, actual_pin):
        entered_pins, secure_q, usability_q = get_form_data(form)
        
        # Input validation on form. Ensures everything is filled out
        if entered_pins is False:
            return no_update, no_update, btn-1, no_update, no_update, no_update
        
        new_pin = gen_pin()
         
        if btn == 1:
            if actual_pin != entered_pins[0]:
                '''
                lives = lives-1
                if lives==0:
                    return no_update, no_update, no_update, lives, no_update, True
                '''
                return no_update, no_update, btn-1, no_update, no_update, no_update
            df = pd.DataFrame(data={'Participant ID': [participant], 'Level': ['1'], 'Actual Pins': [[actual_pin]], 'Entered Pins': [entered_pins], 'Secure question': [secure_q], 'Usable question': [usability_q]})
        else:
            actual_pins = data[-1]['Actual Pins'] + [actual_pin]
            print('actual=', actual_pins, 'entered=', entered_pins)
            
            if actual_pins != entered_pins:
                lives = lives-1
                if lives==0:
                    data.append({'Participant ID': participant, 'Level': btn, 'Actual Pins': actual_pins, 'Entered Pins': entered_pins, 'Secure question': secure_q, 'Usable question': usability_q})
                    df = pd.DataFrame.from_dict(data)
                    return no_update, df.to_dict('records'), no_update, lives, no_update, True
                return no_update, no_update, btn-1, lives, no_update, no_update
            data.append({'Participant ID': participant, 'Level': btn, 'Actual Pins': actual_pins, 'Entered Pins': entered_pins, 'Secure question': secure_q, 'Usable question': usability_q})
            df = pd.DataFrame.from_dict(data)
        return get_study_form(btn+1, new_pin), df.to_dict('records'), no_update, lives, new_pin, no_update
    
    @app.callback(
        Input('end_btn', 'n_clicks'),
        State('participant_val', 'children'),
        State('study_df', 'data'),
        State('end_form', 'children'),
        Output('end_modal', 'opened'),
        Output('ty_modal', 'opened'),
        prevent_initial_call=True
    )
    def end_study(btn, participant, data, form):
        ans = get_end_form_data(form)
        
        if ans is False:
            return no_update
        
        if not os.path.isdir("Results\\"):
            os.makedirs('Results')
        df = pd.DataFrame.from_dict(data)
        df['Day to day'] = ans[0]
        df['Apps'] = str(ans[1])
        df.to_csv(f'Results\\{participant} - Case Study - {datetime.datetime.now().strftime("%Y-%m-%d %H;%M;%S")}.csv', index=False)
        return False, True