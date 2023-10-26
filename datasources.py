from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app import app
import navigation as nav
import footer

###################################
# Documentation card contents

## FIXME: edd example result


discription = dcc.Markdown('''
## Distribution search
Here, you can plot your intrasting gene in the distribution of DEPrior, Gini index, and publication count.
Please input your gene name.

#### Ugase 
1. choose x axis and y axis for plot from `DE_Prior_Rank`, `gini_norm_rank`, `g2p_rank`. See source of the data at [Data sources](#data-sources) section.
    - `DE_Prior_Rank`: Score of DEG probability from meta-analysis study. Normalized rank of DEPrior.
    - `gini_norm_rank`: Score of tissue specificity. Normalized rank of Gini index.
    - `g2p_rank`: Score of gene popularity. Normalized rank of gene publication count.
2. select plot type form Scatter plot or Density plot.
3. If Scatter plot is selected, user can hightlight intrasting gene by typeing / selecting gene name in input box.
''')

reference_info = dcc.Markdown('''

##### DE prior
- Score of DE prior is downloaded from:
>
> Crow,M. et al. (2019) Predictability of human differential gene expression. 
Proceedings of the National Academy of Sciences, 116, 6491-6500. 
[https://doi.org/10.1073/pnas.1802973116](https://doi.org/10.1073/pnas.1802973116)
>


##### Gini index
- RNA-seq data from Genotype-Tissue Expression GTEx project v8 
(THE GTEX CONSORTIUM, 2020) data in Human protein Atlas 
([https://www.proteinatlas.org/download/rna_tissue_gtex.tsv.zip](https://www.proteinatlas.org/download/rna_tissue_gtex.tsv.zip)).

##### Publication number
- Publication data for each gene is publicly available at 
[https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz](https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz).

''')

padding = {
    "padding-left": "10%", "padding-right": "10%",
    "padding-top": "2%", "padding-bottom": "2%",
    "width": "100%"
    }

figsize=600

###################################
# Plot layout

# Load the CSV files
# This file is merge of the DEPrior, gini index, gene2pubmed count
df1 = pd.read_csv("resources/DEPrior_gini_g2p.txt", sep="\t")

# Size setting
# Left side of the app for selecting features
width = '50%'
vertical_align = 'top'

####################################################
# Callback to update scatter plot
# The scatter plot is updated based on the x and y columns selected by the user
# Also, user can set x and y columns to be log scale or not
# The hover data is the gene name, Entrez ID, and Ensembl ID

@app.callback(
        Output('scatter-plot', 'figure'),
    [
        Input('update-plot-button', 'n_clicks'),
    ],
    [
        State('scatter-x-dropdown', 'value'),
        State('scatter-y-dropdown', 'value'),
        State('input_gene', 'value'),
    ])

def update_scatter_plot(n_clicks, x_col, y_col, input_gene):

    scatter_fig = px.scatter(df1, x=x_col, y=y_col,  hover_name="hgnc_symbol", hover_data=["entrezgene_id", "ensembl_gene_id"])
    # Reduce the opacity of all other points
    scatter_fig.update_traces(marker=dict(opacity=0.3))

    # Set figure title
    scatter_fig.update_layout(
        autosize=True, height=figsize, width=figsize, # size setting
        showlegend=True, # style setting
        template="plotly_white",
        plot_bgcolor = 'white',
        # modebar_orientation="v",
        )


    # Highlighting the input gene
    if input_gene:
        for gene in input_gene:
            if gene in df1['hgnc_symbol'].values:
                gene_row = df1[df1['hgnc_symbol'] == gene]
                hovertext = f"{gene_row['hgnc_symbol'].values[0]}<br>{x_col}: {gene_row[x_col].values[0]}<br>{y_col}: {gene_row[y_col].values[0]}"
                # \n is not work but <br> is
                scatter_fig.add_trace(go.Scatter(x=gene_row[x_col],
                                                y=gene_row[y_col],
                                                mode='markers',
                                                marker=dict(color='red', size=10, line=dict(width=2, color='DarkRed')),
                                                hoverinfo='text',
                                                hovertext=hovertext,
                                                name=gene_row['hgnc_symbol'].values[0] 
                                                ))
    return scatter_fig

@app.callback(
    Output('input_gene', 'value'),
    [Input('submit', 'n_clicks')],
    [State('input', 'value'),
     State('input_gene', 'options')],
    prevent_initial_call=True
)
def update_gene_values(n_clicks, input_value, gene_options):
    # Splitting the genes from input
    genes_from_input = [gene.strip() for gene in input_value.split(',')]
    
    # Filtering genes that are in the dropdown options
    available_genes = [option['value'] for option in gene_options]
    valid_genes = [gene for gene in genes_from_input if gene in available_genes]

    return valid_genes

@app.callback(
        Output('dens-plot', 'figure'),
    [
        Input('scatter-x-dropdown', 'value'),
        Input('scatter-y-dropdown', 'value'),
    ])
def update_density_plot(x_col, y_col):
    dens_fig = px.density_heatmap(df1, x=x_col, y=y_col, hover_name="hgnc_symbol", hover_data=["entrezgene_id", "ensembl_gene_id"], nbinsx=100, nbinsy=100)
    # dens_fig.update_traces(contours_coloring="fill", contours_showlabels = False)
    
    # Set figure title
    dens_fig.update_layout(autosize=True, height=figsize, width=figsize)

    return dens_fig

@app.callback(
    Output('selected_plot', 'children'),
    [Input('plot_selection', 'value')]
)
def switch_plot(plot_choice):
    return [plot_build()[0]] if plot_choice == 'scatter-plot' else [plot_build()[1]]

####################################################
# Settingcard layout
def left_build_layout():
    layout = dbc.Card([
        dbc.CardHeader("Plot settings"),
        dbc.CardBody([
            html.Div([
                # dummy input to avoid google password autocomplete
                dcc.Input(id='fake-username', style={'display': 'none'}),
                dcc.Input(type='password', id='fake-pass', style={'display': 'none'}),

                html.H5("Select x axis for scatter plot"),
                dcc.Dropdown(
                    id='scatter-x-dropdown',
                    options=["DE_Prior_Rank", "gini_norm_rank", "g2p_rank"],
                    placeholder="Select x axis",
                    value="DE_Prior_Rank"
                ),
                html.Hr(),
                html.H5("Select y axis for scatter plot"),
                dcc.Dropdown(
                    id='scatter-y-dropdown',
                    options=["DE_Prior_Rank", "gini_norm_rank", "g2p_rank"],
                    placeholder="Select y axis",
                    value="gini_norm_rank"
                ),
                html.Hr(),
                html.H5("Plot type"),
                dcc.RadioItems(
                    options=[
                        {'label': 'Scatter plot', 'value': 'scatter-plot'},
                        {'label': 'Density plot', 'value': 'dens-plot'},
                    ],
                    value='scatter-plot',
                    id='plot_selection',
                ),
                html.Hr(),
                html.H5("Input gene name to highlight"),
                html.P("Type gene name list with comma separated."),
                html.P("e.g. 'TP53, BRCA1'"),
                dcc.Input(id='input', value='', placeholder='Type gene names', type='text'),
                dbc.Button('Add list', id='submit', outline=True, color="secondary", className="me-1"),
                html.P("or select from the Dropdown"),
                dcc.Dropdown(
                    id='input_gene',
                    options=[{'label': gene, 'value': gene} for gene in df1['hgnc_symbol'].unique()],
                    placeholder="Select gene names",
                    multi=True
                ),
                html.Hr(),
                dbc.Button('Update Plot', id='update-plot-button', n_clicks=0, color="primary", className="me-1"),
            ]),], style= padding),])
    return layout

####################################################
# Plot layout
# FIXME: Gene検索について、listをinputできるようにする。


def plot_build():
    figs = [
            dcc.Graph(id='scatter-plot',
                  figure={
                            'data': [
                                    {'genename': df1['hgnc_symbol'], 'EntrezID': df1['entrezgene_id'], 'EnsemblID': df1['ensembl_gene_id'],'hoverinfo': 'text'},
                                    ],
                            }),

            dcc.Graph(id='dens-plot',
                  figure={
                            'data': [
                                    {'genename': df1['hgnc_symbol'], 'EntrezID': df1['entrezgene_id'], 'EnsemblID': df1['ensembl_gene_id'],'hoverinfo': 'text'},
                                    ],
                            }),
    ]
    return figs

def plot_layout():
    layout = html.Div(
        id = "plot_space",
        children=[
            html.Div(
                dcc.Loading(
                    id="ls-loading-1", 
                    children=[
                        html.Div([plot_build()[0]], id='selected_plot')
                    ], type="default"
                )
            )
        ], style=padding,

    )
    return layout

def discription_layout():
    layout = html.Div(
            children = [
                discription,
            ], style=padding,
    )
    return layout   
                           
def document_build_layout():
    layout = html.Div(
                [
                    html.H1('Data sources',id="data-sources"),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Public Data source", className="card-title"),
                                reference_info
                            ]
                        )
                    ),
                ],
            )
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
            html.H1("Score distribution"),
            dbc.Row([
                # Left column
                dbc.Col(
                    id="left-column", 
                    xs=12,
                    md=3,
                    children=[
                        left_build_layout()
                    ]
                ),
                # Right column
                dbc.Col(
                    id="Right-column", 
                    xs=12,  # For extra small screen widths
                    md=9,    # For medium (and larger) screen widths
                    children=[plot_layout()]
                )
            ]),
            document_build_layout()

        ]
    )
    return layout

def build_layout():

    layout = html.Div(
        children=[
            nav.LAYOUT,

            html.Div(children=[
                body_layout()
            ], style=padding),

            dbc.Row(html.Hr(), style= padding),
            
            footer.LAYOUT,
        ],
        
        className="fullpage"
    )
    return layout