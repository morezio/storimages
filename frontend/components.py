## Right now both layout and components live here to not make a mess of files
from dash import html, dcc
import dash_bootstrap_components as dbc

src_logo = '/storimages/frontend/assets/storimages_logo_by_morezio_white.svg'

# the contents of a file with instructions; a markdown file
user_instructions = None
with open('/storimages/frontend/assets/instructions.md') as hh:
    user_instructions = hh.read()

# holder for contents
instructions = dcc.Markdown(
    id='instructions_markdown',
    className='markdown_text',
    children=[user_instructions]
    # style={"display": "none"}
)

# div separated because I felt it unreadable rn, might re-int
instructions_division = html.Div(
    id='instructions_division', children=[instructions]
)

# toggle on-off display of instructions
instructions_button = dbc.Col(
    children=[
        html.Button('Instructions', id='instructions_button', className='action-button')
    ]
)

submit_button_div = html.Div(id='submit_button_div',children=[])

submit_button = [dbc.Col(
    children=[html.Button('Submit', id='submit_button', className='action-button')])]

# must appear only when processing is done
download_button = dbc.Col(
    children=[
        html.Button('Download results', id='download_button', style={'display':'none'})
    ]
)

# to make sure the user wants to proceed
submit_button = html.Button('Submit', id='submit_button', n_clicks=0)

# area where the upload display should be
upload_column = dbc.Col(align='center',children=[
    html.Div(
        children=[
            # either zip or a directory of pictures or a selection of them
            dcc.Upload( 
                id='upload_area',
                className='highlight',
                children=[
                    html.Div([
                        html.H2(
                            "Drag & drop or click here to select your pictures",
                            className='context-text'
                        )
                    ])
                ]#, multiple=False # allowing for multiple risk;; mind how to handle it 
            )
        ]
    )
], width=6)

logo = html.Div(
    children=[
        html.Img(src=src_logo, className='svg-image')
    ],
    style={
        'position': 'relative',
        'height': '100vh',
        'width': '100vw'
    }
)

preset_dimensions_div = dbc.Col(
    align='center',
    children=[html.Div(id='preset_dimensions_div')], width=6)

preset_dimensions = dcc.Dropdown(
            id='thumbnail_sizes_dropdown',
        options=[
            'Photo galleries = 120x90',
            'Video = 160x120',
            'Social media profile picture = 100x100',
            'Online store - small = 80x80',
            'Online store - large = 150x150',
            'Icons = 96x96'
        ],
        placeholder='Please, select 1 option to proceed')

preview_div = html.Div(id='preview_list', className='list-container', children=[])

error_markdown = dcc.Markdown('## Please refresh the webpage. Your input was \
                              not valid. Only upload .zip or pics of supported format', style={'color':'red'})

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
                        dbc.Row([upload_column, 
                                 html.Br(),
                                 preview_div, 
                                 html.Br(),
                                 preset_dimensions_div,
                                 html.Br(),
                                 submit_button_div
                                 ]),
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
        # dbc.Row([dbc.Col([preview_div])]),
        # dbc.Row([dbc.Col([submit_button_div],className='action-button-column')]),
        dbc.Row([html.Br()]),
        dbc.Row([html.Br()]),
        dbc.Row([dbc.Col([download_button])]),
        dbc.Row([html.Br()]),
        dbc.Row([html.Br()]),
        # dbc.Row([dbc.Col([instructions_button],className='action-button-column')]),
        dbc.Row([instructions_division])
    ], fluid=True
)