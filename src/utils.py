import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import random

from dash import html
from dash_iconify import DashIconify


def gen_pin():
    return random.randint(1000, 9999)


def get_study_form(n, pin):
    children = [dmc.Col(html.H3(f'Level {n}'))]
    
    # Append pin input
    for i in range(1, n):
        children.append(dmc.Col(dmc.NumberInput(
            label=f"Pin {i}",
            placeholder=f"Recall pin {i}",
            max=9999,
            min=0,
            hideControls=True,
            required=True,
            id=f'pin_in_{i}'
        ), span=7))
    
    children.append(dmc.Col(dmc.NumberInput(
            label=f"Pin {n}",
            description=f"The pin is {pin}",
            placeholder="Enter the pin as shown above",
            max=9999,
            min=0,
            hideControls=True,
            required=True, 
            id=f'pin_in_{n}'
        ), span=7))
    
    # Append questions
    children.append(dmc.Col(dmc.RadioGroup(
            [dmc.Radio('Yes', 'Yes'), dmc.Radio('No', 'No')],
            label=f"Do you think the app is more secure by having {n} pins as a pose to {n-1}",
            orientation='horizontal',
            required=True,
            id="q_secure"
            )))
    
    children.append(dmc.Col(dmc.RadioGroup(
            [dmc.Radio('Very Poor', 'Very Poor'), dmc.Radio('Poor', 'Poor'), dmc.Radio('Acceptable', 'Acceptable'), dmc.Radio('Good', 'Good'), dmc.Radio('Very Good', 'Very Good')],
            label="How would you rate the app's usability in terms of the number of passwords required?",
            orientation='horizontal',
            required=True,
            id="q_usable"
            )))
    
    form = dbc.Form(dmc.Grid(children=children), id='study_form')
    
    return form


def get_form_data(form):
    pins=[]
    for p in form['props']['children'][1:]:
        val = p['props']['children']['props']['value']
        if not val:
            return False, False, False
        pins.append(val)
    usability_q = pins.pop()  
    secure_q = pins.pop()
    
    return pins, secure_q, usability_q
    