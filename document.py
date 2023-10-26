from dash import html, dcc
import dash_bootstrap_components as dbc

import navigation as nav
import footer

###################################
# Documentation card contents

discription = dcc.Markdown('''
## Clover
Clover is a package for prioritising unexpected rare genes in a differentially 
expressed gene (DEG) list. We used this tool to rank DEGs from bulk RNA-seq analysis, 
but any gene list with an FDR value (statistically significant value of differentially 
expressed) is applicable.

Also, please see the GitHub repository for the code:
[https://github.com/G708/Clover](https://github.com/G708/Clover)



''',
link_target="_blank",
)

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

def build_layout():
    layout = html.Div(
        children=[
            nav.LAYOUT,
            html.Div(
                children=[
                    html.H2(children='Document', style={"text-align": "center"}),
                    html.Div(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                [
                                discription
                                ]
                                )
                            ),
                        ]
                    ),
                ],style={"padding-left": "5%", "padding-right": "5%", "width": "100%"},
            ),
            dbc.Row(html.Hr(), style={'height': '3%'}),
            footer.LAYOUT
        ],
        )

    return layout
