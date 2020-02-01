# Importing Libraries

import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import dash_html_components as html
import webbrowser as wb
import plotly.plotly as py
import os
import urllib
import dash_dangerously_set_inner_html
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Flask, Response
import main
import pandas as pd
import dash_table

server = Flask(__name__)

# external JS
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js",
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]



colors = {
    'background': '#fff',
    'text': '#0000ff'
}

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    },

    {
        'href': 'https://fonts.googleapis.com/css?family=Varela',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }

    
]



# Making app as an object of dash class. Invoking Dash function.

# Provide your name and content.



app = dash.Dash(__name__,server=server,meta_tags=[
    {
        'name': 'description',
        'content': 'My description'
    },
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    }
],
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets,
                static_folder='assets')



app.scripts.config.serve_locally = True
app.css.config.serve_locally = True


# Your webpage title

app.title = 'Tradex 	&#x1F525;'

app.config['suppress_callback_exceptions']=True




'''

Here to write <div> , <h1>, ,<p>, etc. tags we need to specify them as html.Div, html.H1, html.P (As we are importing this tags from html library)


'''




# Your main layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

PLOTLY_LOGO = "/"



app.config['suppress_callback_exceptions']=True

# Update the index

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':

        # Default path is / . It will render Page_1_layout
        
        return page_1_layout

    else:
        return []
    # You could also return a 404 "URL not found" page here



# Root page

page_1_layout = html.Div([

        # Creating a Navbar

        dash_dangerously_set_inner_html.DangerouslySetInnerHTML(
                                '''
  
        <!-- Image and text -->
<nav class="navbar navbar-light bg-light">
  <a class="navbar-brand" href="#">
    <img src="assets/bootstrap-solid.svg" width="30" height="30" class="d-inline-block align-top" alt="">
    Tradex
  </a>
</nav>

'''),
                            
    html.Div([
    dbc.Card(
    [ dbc.CardBody(  
    dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Heading"),
                        html.P(
                            """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."""
                        ),

                        html.Div([
                        dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Bajaj finance', 'value': 'Bajaj data file'},
            {'label': 'Tata', 'value': 'ta'},
            {'label': 'Trident', 'value': 'tr'}
        ],
        placeholder="Select a stock",
        value=''
    ),],style={"margin-bottom":"10%"}),
                    html.Button('Submit', id='button',style={"margin-bottom":"20%"}),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H2("Graph"),
                        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [date.today() + relativedelta(days=-3),date.today() + relativedelta(days=-2),date.today() + relativedelta(days=-1)], 'y': [1, 4, 9], 'type': 'line', 'name': "Trend", 'marker': {
                   'color': '#00ff00'
               }, 'line': {'width': 2, 'color':'#0000ff'}},
                ],
                'layout': {
                    'title': "Stock Market",
                     'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    
                },
                    'xaxis':{'title':'Date'},
                'yaxis':{'title':'Price in INR'}
            }
            }
        ),
                    ],md=8,
                ),
            ]
        )
    ],
    className="mt-12",
),
)]),],style={'margin-top':'1%'},className='ten columns offset-by-one'),


    
     html.Div([    
     html.Div([


        html.Div([

         # Inside this class we are making dcc.Upload which will upload our image.
         
         html.Div(id='output-image',style={"margin-top":"10px","margin-":"10px"}),


    ],className='ten columns offset-by-one'),
     ]),

])


])


# Each time you give input as image in id ('upload-data') this function app.callback will fire and give you output in id ('output-image')

@app.callback(Output('output-image', 'children'),
              [Input('demo-dropdown','value')],[State('demo-dropdown','options')])
def update_graph_interactive_image(content,label):

    if content=="":
        return []


    elif (len(content)!=0):

       

        #Your code here /// import file function


        # Value is content


        array=main.main(content)
        df=pd.DataFrame(array[0])
        table=dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],

    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
)  

        '''
        price=[]
        file = open('data.txt','r') 
        for line in file:
            try:
            #print(line)
                currentline = line.split(",")
                price.append(currentline [2])
            except:
                pass
                
        
        y=price
        x=[i for i in range(len(y))]
        '''
        y=array[1]
        x=[i for i in range(len(y))]
        card=[]
    

         #Get your heading here

        for i in label:
            if i['value']==content:
                
                Heading=i['label']
                break


        Graph= "Graph"
        
        #Get your detailed version of text here
        text="""\
Donec id elit non mi porta gravida at eget metus.
Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum
nibh, ut fermentum massa justo sit amet risus. Etiam porta sem
malesuada magna mollis euismod. Donec sed odio dui. Donec id elit non
mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus
commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit
amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed
odio dui."""
        
        card=dbc.Card(
    [ dbc.CardBody( dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(Heading),
                        html.P(text),
                        table,
                    ],
                    md=12,
                ),
                dbc.Col(
                    [
                        html.H2(Graph),
                       dcc.Graph(
            id='example-graph-1',
            figure={
                'data': [
                    {'x': x, 'y': y, 'type': 'line', 'name': "Trend", 'marker': {
                   'color': '#00ff00'
               }, 'line': {'width': 2, 'color':'#00ff00'}},
                ],
                'layout': {
                    'title': Heading,
                     'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    
                },
                'yaxis':{'title':'Price in INR'}
            }
            }
        ),
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
))])

        return [card]
    else:
        return []




    




    

wb.open('http://127.0.0.1:8050/')
if __name__ == '__main__':
    app.run_server(debug=True,threaded=True,host ='0.0.0.0',use_reloader=False)

