import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
from app import app

# Function to create the layout of the Dash app
def create_layout():
    return html.Div([
        html.H1("TRAINSET: Time Series Labeling Tool"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-data-upload'),
        dcc.Graph(id='time-series-plot'),
        html.Div(id='hover-data'),
        html.Button('Add Label', id='add-label-button', n_clicks=0),
        html.Button('Delete Label', id='delete-label-button', n_clicks=0),
        html.Div(id='label-output')
    ])

# Function to parse uploaded CSV file
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df
        else:
            return None
    except Exception as e:
        print(e)
        return None

# Callback to handle file upload and update the plot
@app.callback(
    [Output('output-data-upload', 'children'),
     Output('time-series-plot', 'figure')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is not None:
        df = parse_contents(contents, filename)
        if df is not None:
            fig = px.line(df, x='timestamp', y='value', color='series')
            return html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns]
                )
            ]), fig
        else:
            return html.Div(['There was an error processing this file.']), {}
    else:
        return html.Div(['No file uploaded.']), {}

# Callback to handle hover data
@app.callback(
    Output('hover-data', 'children'),
    [Input('time-series-plot', 'hoverData')]
)
def display_hover_data(hoverData):
    if hoverData is not None:
        point = hoverData['points'][0]
        return html.Div([
            html.H6(f"Time: {point['x']}"),
            html.H6(f"Value: {point['y']}"),
            html.H6(f"Series: {point['curveNumber']}")
        ])
    else:
        return html.Div(['Hover over a point to see details.'])

# Callback to handle adding labels
@app.callback(
    Output('label-output', 'children'),
    [Input('add-label-button', 'n_clicks')],
    [State('time-series-plot', 'selectedData')]
)
def add_label(n_clicks, selectedData):
    if n_clicks > 0 and selectedData is not None:
        points = selectedData['points']
        for point in points:
            # Add label logic here
            pass
        return html.Div(['Labels added.'])
    else:
        return html.Div(['No labels added.'])

# Callback to handle deleting labels
@app.callback(
    Output('label-output', 'children'),
    [Input('delete-label-button', 'n_clicks')],
    [State('time-series-plot', 'selectedData')]
)
def delete_label(n_clicks, selectedData):
    if n_clicks > 0 and selectedData is not None:
        points = selectedData['points']
        for point in points:
            # Delete label logic here
            pass
        return html.Div(['Labels deleted.'])
    else:
        return html.Div(['No labels deleted.'])
