## Right now both layout and components live here to not make a mess of files
from dash import html, dcc
import dash_bootstrap_components as dbc

# the contents of a file with instructions; a markdown file
user_instructions = None # instructions

# holder for contents
instructions = dcc.Markdown(
    children=[user_instructions] 
## should come in css, but just a reminder for self
# add style={'fontFamily':'Helvetica, sans-serif', 'color':'#fffff99','width':'87%'}
)

# div separated because I felt it unreadable rn, might re-int
instructions_division = html.Div(
    id='instructions_division', children=[instructions]
)

# toggle on-off display of instructions
instructions_button = dbc.Col(
    children=[
        html.Button('Instructions', id='instructions_button')
    ]
)

# to make sure the user wants to proceed
submit_button = html.Button('Submit', id='submit_button', n_clicks=0)

# area where the upload display should be
upload_column = dbc.Col(align='center',children=[
    html.Div(
        className='',
        children=[
            # either zip or a directory of pictures or a selection of them
            dcc.Upload( 
                id='upload_batch',
                children=[
                    html.Div([
                        html.H2(
                            "Drag & drop or click here to select your pictures"
                        )
                    ])
                ]#, multiple=False # allowing for multiple risk;; mind how to handle it 
            )
        ]
    )
], width=12)

##############
### Layout ###
##############

# all within a major container; might have inner containers
storimages_layout = dbc.Container(
    [
        dbc.Row([html.H1("StorImages", className="text-gradient")]),
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        # upload_column is full grid
                        dbc.Row([upload_column]),
                        dbc.Row([html.Br()]), # placeholder for loading bar
                        dbc.Row([html.Br()]), # spacing
                        # download button and legend
                        # dbc.Row([download_button]),
                        # dbc.Row([update_legend_div]),
                    ], className='container') # highlight box
                ])
            ]
                ),
        dbc.Row([html.Br()]),
        dbc.Row([instructions_button]),
        dbc.Row([instructions_division]),
    ], fluid=True
)