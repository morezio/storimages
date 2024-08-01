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