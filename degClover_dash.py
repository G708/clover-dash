
from dash import dash_table, html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn import preprocessing
import plotly.graph_objs as go
from wordcloud import WordCloud
import numpy as np

import base64
import io

from app import app
import navigation as nav
import footer

import Clover.src.scores as scores
from gen_test_data import main


###################################
# Documentation card contents
Header = dcc.Markdown('''
## Find your Clover gene
Clover prioritise the gene with Rerity.
For the detail of the this tool, please visit [document](/document) page or 
[manuscript](.)
''')

discription = dcc.Markdown('''
#### Ugase 
##### [Ranking Table](#ranking)
1. Upload your DEG list
2. Select gene column name
3. Select gene ID format
4. Select the FDR column
5. `Run Clover`

Your will get Ranking Table with the scores.

##### [Visualization](#vis)
After `Run Clover`, you can visualize the top ranked DEG by WordCloud.

1. Select the ranking score to create the WordCloud
2. Select the word number plotted in the WordCloud
3. Select ascending
4. `Draw WordCloud`

''')

overview_fig = "assets/Fig1.jpg"

####################################################
# Load the CSV files
# This file is merge of the DEPrior, gini index, gene2pubmed count
df1 = pd.read_csv("resources/DEPrior_gini_g2p.txt", sep="\t")


####################################################
# Size setting
# Left side of the app for selecting features
width = '50%'
display = 'inline-block'
vertical_align = 'top'
padding = {
    "padding-left": "10%", "padding-right": "10%",
    "padding-top": "2%", "padding-bottom": "2%",
    "width": "100%"
    }

# FIXME: Upload to WEB
# FIXME: Match the version of the Clover package

####################################################
# Function for uploading the user table
# https://dash.plotly.com/dash-core-components/upload

def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            return pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'tsv' in filename:
            # Assume that the user uploaded a TSV file
            return pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), sep = "\t")
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            return pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["ERROR: File format. Allow csv or xls."],id='error-message')


####################################################
# Callback for updating the dropdown menu
# https://dash.plotly.com/dash-core-components/dropdown
# define fdr column name, gene name
# FDR: Defualt value is the last column of the user table
# GENE: Default value is the first column of the user table
# @app.callback(
#     [
#         Output("fdr-column-dropdown", "options"),
#         Output("fdr-column-dropdown", "value"),
#         Output("gene-column-dropdown", "options"),
#         Output("gene-column-dropdown", "value"),
#         Output("user_table", "data"),
#         Output('filename-output', 'children'),
#     ],
#     [Input("upload-data", "contents")],
#     [State("upload-data", "filename")],
#     prevent_initial_call=True,
# )
# def update_dropdown(contents,filename):
#     load_df = parse_contents(contents, filename)
#     if len(load_df.columns) > 30:
#         return (
#             [],
#             None,
#             [],
#             None,
#             {},
#             'Error: Uploaded file has too many columns.'
#         )

#     elif len(load_df) > 1000:
#         return (
#             [],
#             None,
#             [],
#             None,
#             {},
#             'Error: Uploaded file has too many rows.'
#         )

#     else:
#         return (
#             [{'label': i, 'value': i} for i in load_df.columns],
#             load_df.columns[-1],
#             [{'label': i, 'value': i} for i in load_df.columns],
#             load_df.columns[0],
#             load_df.to_dict('records'),
#             'Selected file: {}'.format(filename),
#         )


@app.callback(
    [
        Output("fdr-column-dropdown", "options"),
        Output("fdr-column-dropdown", "value"),
        Output("gene-column-dropdown", "options"),
        Output("gene-column-dropdown", "value"),
        Output("user_table", "data"),
        Output('filename-output', 'children'),
    ],
    [Input("upload-data", "contents"),
     Input('button-test-data', 'n_clicks')],
    [State("upload-data", "filename")],
    prevent_initial_call=True,
)
def combined_callback(contents, n_clicks, filename):
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "upload-data":
        # The same logic as update_dropdown function
        load_df = parse_contents(contents, filename)
        if len(load_df.columns) > 30:
            return (
                [],
                None,
                [],
                None,
                {},
                'Error: Uploaded file has too many columns.'
            )

        elif len(load_df) > 1000:
            return (
                [],
                None,
                [],
                None,
                {},
                'Error: Uploaded file has too many rows.'
            )

        else:
            return (
                [{'label': i, 'value': i} for i in load_df.columns],
                load_df.columns[-1],
                [{'label': i, 'value': i} for i in load_df.columns],
                load_df.columns[0],
                load_df.to_dict('records'),
                'Selected file: {}'.format(filename),
            )
    
    elif trigger_id == 'button-test-data':
        if n_clicks > 0:
            # generate random seed 
            seed = np.random.randint(100000)
            load_df = main(seed)
            return (
                [{'label': i, 'value': i} for i in load_df.columns],
                load_df.columns[-1],
                [{'label': i, 'value': i} for i in load_df.columns],
                load_df.columns[0],
                load_df.to_dict('records'),
                f'Selected file: test_data: seed = {seed}',
            )
    return ([], None, [], None, {}, None)


####################################################
# Callback of running the ranking score
@app.callback(
        Output('ranking-table', 'children'),
        Output('ranking-table_data', 'data'),
        Output("wordcloud-dropdown", "options"),
    [
        Input('run_Clover', 'n_clicks'),
    ],
    [
        State('user_table', 'data'),
        State('gene-column-dropdown', 'value'),
        State('id-type-dropdown', 'value'),
        State('fdr-column-dropdown', 'value'),
    ],
    prevent_initial_call=True,
    )
def run_ranking(b1,user_df, gene_column, id_type, fdr_value):
    triggered_id = ctx.triggered_id
    if triggered_id == 'run_Clover':
         return show_table(user_df, gene_column, id_type, fdr_value)

def show_table(user_df, gene_column, id_type, fdr_value):
    user_df = pd.DataFrame(user_df)
    df_merge = pd.DataFrame()

    try:  
        df_merge = pd.merge(user_df, df1[["hgnc_symbol", "ensembl_gene_id", "entrezgene_id", "DE_Prior_Rank", "g2p_rank", "N", "gini_norm", "gini_norm_rank"]], 
            left_on = gene_column, right_on = id_type, how="left")
        df_merge["Glint"] = scores.glint(df_merge["DE_Prior_Rank"], df_merge["gini_norm"])
        df_merge["Dowsing"] = scores.dowsing(df_merge["DE_Prior_Rank"], df_merge["gini_norm"], df_merge[fdr_value] )
        df_merge["Treasure_Hunt"] = scores.treasure_hunt(df_merge["g2p_rank"], df_merge["Dowsing"])
        df_merge["Ropeway"] = scores.ropeway(df_merge["g2p_rank"], df_merge["Dowsing"])

        df_merge = df_merge.reindex(columns=[gene_column, "hgnc_symbol", "ensembl_gene_id", "entrezgene_id",fdr_value, "Glint", "Dowsing", "Treasure_Hunt", "Ropeway", "DE_Prior_Rank", "g2p_rank", "N", "gini_norm_rank", "gini_norm"])

        ranking_children = [
            dash_table.DataTable(
                data=df_merge.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df_merge.columns],
                id='ranking-table',
                style_table={'minWidth': '100%'},
                fixed_columns={'headers': True, 'data': 1},
                fixed_rows={'headers':True}, 
                sort_action='native', # sort by clicking on the column name
                sort_mode='multi', # sort by multiple columns
                page_action='native', # all data is passed to the table up-front
                style_cell={
                    # all three widths are needed
                    'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                export_format='csv', # export as csv
                export_headers='display',
                )
            ]

        return (
            html.Div(ranking_children),
            df_merge.to_dict('records'),
            ["Glint", "Dowsing", "Treasure_Hunt", "Ropeway", fdr_value,"DE_Prior_Rank", "g2p_rank","gini_norm_rank", ],
        )
    except Exception as e:
        return (html.Div([html.P("ERROR: Please check Settings of: "),
                          html.P("Gene column name or gene id format"),
                          ],id='error-message'),
                {},
                [])

####################################################
# Callback to update word cloud
# The word cloud is updated based on the column selected by the user

@app.callback(   
        Output('word-cloud', 'children'),
    [
        Input('Draw_wordcloud', 'n_clicks'),
    ],
    [
        State('ranking-table_data', 'data'),
        State('wordcloud-dropdown', 'value'),
        State('input_range', 'value'),
        State('word_ascending', 'value'),
    ],
    prevent_initial_call=True,
    )

def update_word_cloud(b1, ranking_table, wordcloud_col, input_range, word_ascending):
    triggered_id = ctx.triggered_id
    if triggered_id == 'Draw_wordcloud':
         return show_cloud( ranking_table, wordcloud_col,  input_range, word_ascending)
    
def show_cloud(ranking_table, wordcloud_col, input_range, word_ascending): 

    gene_col = "hgnc_symbol"

    word_width = 800
    word_height = 800

    # Rank the data based on the FDR score column selected by the user
    ranking_table_df = pd.DataFrame(ranking_table)
    s = ranking_table_df[wordcloud_col].astype(float)

    if word_ascending == "ascending":
        ranking_table_df["size"] = preprocessing.minmax_scale(s, feature_range=(0.01,0.99))
        ranking_table_df["size"] = abs(1 - ranking_table_df["size"])
    else:
        ranking_table_df["size"] = preprocessing.minmax_scale(s, feature_range=(0.01,0.99)) # 0.01 to 0.99 scale
    # if 0 - 1, 0 value will be removed from the word cloud

    try:
        # Create the word cloud
        # posseble issue for the wordcloud plotting: https://github.com/amueller/word_cloud/issues/285
        # set max_font_size and min_font_size to avoid the issue
        cloud = WordCloud(background_color="white", width=word_width, height=word_height, max_font_size=10*input_range, min_font_size=10)
        word_df = ranking_table_df[[gene_col, 'size']].dropna().sort_values('size', ascending=False)

        if len(word_df) > input_range:
            word_dict = word_df[0:input_range].set_index(gene_col).to_dict()['size']
        else:
            word_dict = word_df.set_index(gene_col).to_dict()['size']

        cloud.generate_from_frequencies(word_dict)

    except Exception as e:
        
        return html.Div([f"ERROR: {e}"],id='error-message')

    # stored_cloud = cloud.to_svg()

    cloud_img = cloud.to_array()
    flipped_cloud_img = np.flipud(cloud_img)
    # Plotly's go.Image treats the origin (0,0) of the image as the top-left corner, 
    # while many imaging libraries (including the one used by WordCloud) may treat 
    # the origin as the bottom-left corner.

    fig_cld = go.Figure(go.Image(z=flipped_cloud_img))
    fig_cld.update_layout(
                            showlegend=False,
                            xaxis=dict(visible=False, range=[0, word_width]),
                            yaxis=dict(visible=False, range=[0, word_height], scaleanchor="x"),
                            margin=dict(t=0, b=0, l=0, r=0)
                        )

    return html.Div([f"{len(word_dict)} gene in the word cloud: {word_dict.keys()}",
                     dcc.Graph(figure=fig_cld),
                    ])


####################################################
# Web page settings

def discription_layout():
    layout = html.Div(
            children = [
                Header,

                html.Div(
                    className = "flexbox",
                    children = [
                        html.Div(
                            className="textbox",
                            children=[discription]
                        ),
                        html.Div(
                            className="image-box",
                            children=[
                            html.Img(src=overview_fig, className="responsive-img"),
                        ]),
                    ]
                )
            ], style=padding,
    )
    return layout


def Setting_layout():
    layout = html.Div(children=[
                
                # Accordion Sections
                dbc.Accordion(
                    [
                        accordion_item("1. Upload your data", [
                            html.H6("File size limit:"),
                            html.P("< 30 columns, < 1000 rows"),
                            upload_section(), # upload button
                            # test data selection
                            html.H6("Test data:"),
                            html.A(dbc.Button("random test data", id='button-test-data', n_clicks=0, outline=True, color="secondary", className="me-2")),
                            html.P(id='filename-output'),
                            dcc.Store(id="user_table"),
                        ]),
                        accordion_item("2. Select the gene column", [
                            dcc.Dropdown(id='gene-column-dropdown'),
                        ]),
                        accordion_item("3. Select gene name / ID format", [
                            dcc.RadioItems(
                                options=[
                                    {'label': 'HGNC Symbol', 'value': 'hgnc_symbol'},
                                    {'label': 'Entrez Gene ID', 'value': 'entrezgene_id'},
                                    {'label': 'Ensembl Gene ID', 'value': 'ensembl_gene_id'}
                                ],
                                value='hgnc_symbol',
                                id='id-type-dropdown',
                            ),
                        ]),
                        accordion_item("4. Select the FDR column", [
                            dcc.Dropdown(id='fdr-column-dropdown'),
                        ]),
                        accordion_item("5. Run Clover",[
                            dbc.Button("Run Clover", id='run_Clover', n_clicks=0, color="primary", className="me-1"),
                            html.A(dbc.Button("Reload page", id='Reset_data', n_clicks=0, outline=True, color="secondary", className="me-2"), href="/"),
                            html.P('Reload page to reset the data.'),
                        ]),
                    ],
                    always_open=True,
                ),     
            ])

    return layout

def accordion_item(title, content):
    return dbc.AccordionItem(
        html.Div(content),
        title=title
    )

def upload_section():
    return dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px',
            'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '0px'
        },
        multiple=False
    )

def ranking_layout():
    layout = html.Div(
        id="ranking-table_data",
        children=[
        html.H4("Table"),
        html.Hr(),
        html.Div(
            dcc.Loading(id="ls-loading-1", children=[
                html.Div(html.Table(id="ranking-table" , style={'width': '100%'}))
                ], type="default")
            ),
        ])
    return layout

def word_cloud_setting_layout():
    layout = html.Div(children=[

                    # Accordion Sections
                    dbc.Accordion(
                        [
                            accordion_item("1. Select the ranking score", [
                                dcc.Dropdown(id='wordcloud-dropdown'),
                            ]),
                            accordion_item("2. Select the word number (min: 1, max: 100)", [
                                dcc.Input(
                                    id="input_range", type="number", placeholder="input with range",
                                    min=1, max=100, step=1,
                                    value=20,
                                ),
                            ]),
                            accordion_item("3. Select ascending", [
                                dcc.RadioItems(
                                    options=[
                                        {"label": "ascending: the smaller the score, the bigger the word.", "value": "ascending"},
                                        {"label": "disascending: the bigger the score, the bigger the word.", "value": "disascending"},
                                    ],
                                    value='ascending',
                                    id='word_ascending',
                                ),
                            ]),                           
                            accordion_item("4. Plot WordCloud",[
                            dbc.Button("Draw WordCloud", id='Draw_wordcloud', n_clicks=0, color="primary", className="me-1"),
                        ]),
                        ],
                        always_open=True,
                    ),
                ])
    return layout

def body_layout():
    layout = html.Div(
        className="contents",
        children=[

            html.Div(
                className="background box",
                children=[
                    discription_layout()
                ]
            ),

            html.H1("Ranking Table", id="ranking"),

            dbc.Row([
                # Ranking
                # Left column
                dbc.Col(
                    id="ranking-left-column",
                    xs=12,  # For extra small screen widths
                    md=4,    # For medium (and larger) screen widths
                    children=[
                        Setting_layout(),
                    ]
                ),

                # Right column
                dbc.Col(
                    id="ranking-right-column",
                    xs=12,  # For extra small screen widths
                    md=8,    # For medium (and larger) screen widths
                    children=[
                        ranking_layout(),
                    ]
                ),
            ]),

            html.Hr(),

            html.H1("Visualization", id="vis"),

            dbc.Row([
                # Word Cloud
                # Left column
                dbc.Col(
                    id="wordcloud-left-column",
                    xs=12,  # For extra small screen widths
                    md=4,    # For medium (and larger) screen widths
                    children=[
                        word_cloud_setting_layout(),
                    ]
                ),

                dbc.Col(
                    id="wordcloud-right-column",
                    xs=12,  # For extra small screen widths
                    md=8,    # For medium (and larger) screen widths
                    children=[
                        # Loading and Output Sections
                        html.H4("WordCloud"),
                        html.Hr(),
                        dcc.Loading(id="ls-loading-1", children=[html.Div([], id='word-cloud')], type="default"),
                        html.Div(id='error-message'),
                    ]
                )
            ])
        ]
    )
    return layout

def build_layout():
    layout = html.Div(children=[
        nav.LAYOUT,

        html.Div(children=[body_layout()], style=padding),

        dbc.Row(html.Hr(), style= padding),
        footer.LAYOUT
    ], className="fullpage")
    return layout

