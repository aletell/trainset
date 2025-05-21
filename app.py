import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from data_handler import parse_csv
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24) # Needed for session management
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Dash app
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

# Define styles for control groups
control_group_style = {'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'}
control_item_style = {'margin-right': '10px', 'display': 'inline-block', 'vertical-align': 'middle'}
button_style = {'margin-right': '10px', 'display': 'inline-block', 'vertical-align': 'middle'} # For buttons next to inputs

dash_app.layout = html.Div([
    dcc.Store(id='data-store'),
    dcc.Store(id='unique-labels-store', data=[]),
    html.Div(id='data-trigger', style={'display': 'none'}),

    html.H1("Python TRAINSET - Time Series Labeling Tool", style={'text-align': 'center', 'margin-bottom': '20px'}),

    # Instructions Section
    html.Div(id='instructions-section', style=control_group_style, children=[
        html.H4("Instructions"),
        html.Ul([
            html.Li(html.Strong("Load Data: ") ), # Placeholder for upload form which is on a separate page
            html.Li([html.Strong("Access Upload Page: "), html.A("Click here to upload your CSV.", href="/upload")]),
            html.Li(html.Strong("CSV Format: ") + "Ensure columns: 'time' (datetime), 'series' (identifier), 'val' (numeric value). 'label' (string) is optional."),
            html.Li(html.Strong("Select Series: ") + "Choose the 'Active Series' to work on and an optional 'Reference Series' for comparison from the dropdowns below."),
            html.Li(html.Strong("Manage Labels: ") + "Create new labels by typing a name and clicking 'Add Label'. Select an 'Active Label' from the dropdown to apply it. Delete labels using the 'Delete Selected Label' button."),
            html.Li(html.Strong("Label Data: ") + "With an 'Active Label' selected, click on individual points on the 'Active Series' in the main graph to apply the label. Click and drag (box or lasso select) to label multiple points."),
            html.Li(html.Strong("Navigate: ") + "Use the bottom context graph's range slider to pan and zoom the main graph. Standard Plotly graph interactions (pan, zoom, etc.) are also available on the main graph."),
            html.Li(html.Strong("Export Data: ") + "Click 'Export Labeled CSV' to download your work. The 'customdata' column will be removed before export.")
        ])
    ]),

    html.Hr(),

    # Controls Section
    html.Div(id='controls-section', children=[
        html.H4("2. Configure Series & Labels", style={'margin-top':'0px'}), # Combined for now as they are interlinked
        
        html.Div(id='series-selection-group', style=control_group_style, children=[
            html.H5("Series Selection"),
            dcc.Dropdown(
                id='active-series-dropdown',
                placeholder='Select Active Series',
                style={**control_item_style, 'width': '45%'}
            ),
            dcc.Dropdown(
                id='reference-series-dropdown',
                placeholder='Select Reference Series (Optional)',
                clearable=True,
                style={**control_item_style, 'width': '45%'}
            )
        ]),

        html.Div(id='label-management-group', style=control_group_style, children=[
            html.H5("Label Management"),
            html.Div([ # Flex container for better alignment
                dcc.Input(id='new-label-input', type='text', placeholder='Enter new label name', style={**control_item_style, 'width': '200px'}),
                html.Button('Add Label', id='add-label-button', n_clicks=0, style=button_style),
                dcc.Dropdown(
                    id='active-label-dropdown',
                    placeholder='Select Active Label',
                    style={**control_item_style, 'width': '200px'}
                ),
                html.Button('Delete Selected Label', id='delete-label-button', n_clicks=0, style=button_style)
            ], style={'display': 'flex', 'align-items': 'center'})
        ]),
        
        # Note: Graph interaction instructions are part of the main instructions now.
        # Export section can be its own small group
        html.Div(id='export-group', style=control_group_style, children=[
            html.H5("4. Export"),
            html.Button("Export Labeled CSV", id="export-csv-button", n_clicks=0, style=button_style),
            dcc.Download(id="download-dataframe-csv")
        ])
    ]),

    html.Hr(),

    # Graphs Section
    html.Div(id='graphs-section', children=[
        html.H4("Time Series Visualization & Labeling Area", style={'text-align': 'center'}),
        dcc.Graph(id='main-graph'),
        dcc.Graph(id='context-graph')
    ]),

], style={'padding': '20px'})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                df = parse_csv(file_path)
                session['dataframe'] = df.to_json(date_format='iso', orient='split')
                session['original_filename'] = secure_filename(file.filename) # Store filename
                return redirect('/dash/')
            except Exception as e:
                # Consider flashing a message or rendering an error page
                return f"Error parsing CSV: {e}"
    return render_template('upload.html')

# Dash Callbacks
@dash_app.callback(
    Output('data-store', 'data'),
    [Input('data-trigger', 'children')] # This input is just to trigger the callback on page load
)
def load_data_to_store(_): # The input argument is not used
    data = session.get('dataframe', None)
    if data:
        session.pop('dataframe', None) # Clear data from session after loading
    return data

@dash_app.callback(
    [Output('active-series-dropdown', 'options'),
     Output('active-series-dropdown', 'value'),
     Output('reference-series-dropdown', 'options'),
     Output('reference-series-dropdown', 'value')],
    [Input('data-store', 'data')]
)
def populate_series_dropdowns(json_data):
    if json_data is None:
        return [], None, [], None # No data, so no options or values

    try:
        df = pd.read_json(json_data, orient='split')
    except Exception as e:
        print(f"Error parsing data for dropdowns: {e}")
        return [], None, [], None

    if 'series' not in df.columns or df['series'].empty:
        return [], None, [], None # No 'series' column or no series data

    series_names = df['series'].unique()
    options = [{'label': s, 'value': s} for s in series_names]
    
    # Set default for active series, none for reference
    default_active_series = series_names[0] if len(series_names) > 0 else None
    
    return options, default_active_series, options, None

# Callback 1: Update unique-labels-store
@dash_app.callback(
    Output('unique-labels-store', 'data'),
    [Input('data-store', 'data'),
     Input('add-label-button', 'n_clicks')],
    [dash.dependencies.State('new-label-input', 'value'),
     dash.dependencies.State('unique-labels-store', 'data')]
)
def update_unique_labels(json_data, add_label_clicks, new_label_value, existing_labels):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    labels_from_file = set()
    if json_data: # Check if data-store has data (e.g., on new file load)
        try:
            df = pd.read_json(json_data, orient='split')
            if 'label' in df.columns:
                labels_from_file.update(df['label'].dropna().unique())
                labels_from_file = {l for l in labels_from_file if l} # Remove empty strings
        except Exception as e:
            print(f"Error reading dataframe for labels: {e}")
            # Potentially keep existing_labels or handle error
            pass # Keep existing_labels if df parsing fails for labels

    current_labels = set(existing_labels if existing_labels else [])
    
    if triggered_id == 'add-label-button' and new_label_value:
        current_labels.add(new_label_value.strip())

    # Merge labels from file with current (potentially newly added) labels
    combined_labels = current_labels.union(labels_from_file)
    
    return sorted(list(combined_labels))


# Callback 2: Populate active-label-dropdown
@dash_app.callback(
    [Output('active-label-dropdown', 'options'),
     Output('active-label-dropdown', 'value'),
     Output('new-label-input', 'value')], # Clear input after adding
    [Input('unique-labels-store', 'data')],
    [dash.dependencies.State('add-label-button', 'n_clicks'), # To check if it was an add action
     dash.dependencies.State('new-label-input', 'value')]     # To clear input
)
def populate_active_label_dropdown(unique_labels, add_label_clicks, new_label_value_state):
    options = [{'label': label, 'value': label} for label in unique_labels]
    
    # Determine the value for the dropdown
    # If a new label was just added, make it the active one. Otherwise, default to first or None.
    ctx = dash.callback_context
    # Check if the trigger for this callback was an update to unique_labels_store
    # And if the original trigger for THAT update was the add-label-button
    # This is a bit indirect. A more robust way would be to have a separate store for "last added label"
    # or to handle the 'value' update more carefully.
    
    # For now, let's default to the first label, or None if empty.
    # And clear the input field if a label was just added.
    
    value = unique_labels[0] if unique_labels else None
    
    # Clear new-label-input if a label was just added.
    # We infer this by checking if unique_labels contains the new_label_value_state
    # (this is an approximation of "was just added")
    input_value_to_clear = ''
    if new_label_value_state and new_label_value_state.strip() in unique_labels:
         input_value_to_clear = '' # Clear the input
    else:
        input_value_to_clear = new_label_value_state # Keep it if not added

    # A simpler logic for clearing input: if add_label_button was the trigger for the previous callback
    # This is hard to determine directly here. The current logic clears if the label is now in the list.

    return options, value, input_value_to_clear


# Callback 3: Delete Label
@dash_app.callback(
    [Output('unique-labels-store', 'data', allow_duplicate=True), # Allow duplicate for unique-labels-store
     Output('data-store', 'data', allow_duplicate=True)], # Allow duplicate for data-store
    [Input('delete-label-button', 'n_clicks')],
    [dash.dependencies.State('active-label-dropdown', 'value'),
     dash.dependencies.State('unique-labels-store', 'data'),
     dash.dependencies.State('data-store', 'data')],
    prevent_initial_call=True
)
def delete_label(n_clicks, label_to_delete, current_unique_labels, json_data):
    if not n_clicks or not label_to_delete:
        return dash.no_update, dash.no_update

    updated_unique_labels = [l for l in current_unique_labels if l != label_to_delete]
    
    new_json_data = dash.no_update
    if json_data:
        try:
            df = pd.read_json(json_data, orient='split')
            if 'label' in df.columns:
                # Update labels in DataFrame
                df['label'] = df['label'].apply(lambda x: '' if x == label_to_delete else x)
                new_json_data = df.to_json(date_format='iso', orient='split')
        except Exception as e:
            print(f"Error processing DataFrame for label deletion: {e}")
            # Decide if we should still update unique_labels or halt
            return dash.no_update, dash.no_update # Or updated_unique_labels, dash.no_update

    return updated_unique_labels, new_json_data


@dash_app.callback(
    [Output('main-graph', 'figure'),
     Output('context-graph', 'figure')],
    [Input('data-store', 'data'),
     Input('active-series-dropdown', 'value'),
     Input('reference-series-dropdown', 'value'),
     Input('unique-labels-store', 'data')] # To update colors if labels change
)
def update_graphs(json_data, active_series, reference_series, unique_labels):
    if json_data is None or active_series is None:
        return {}, {} # Return empty figures if no data or no active series selected
    
    try:
        df = pd.read_json(json_data, orient='split')
        df['time'] = pd.to_datetime(df['time'])
        # Ensure customdata is based on the original index if df is reset for each load
        # If df is appended, a more robust unique ID is needed. Assuming reset for now.
        df['customdata'] = df.index 
    except Exception as e:
        print(f"Error processing JSON data for graphs: {e}")
        return {}, {}

    if df.empty:
        return {}, {}

    # Filter for active series
    df_active = df[df['series'] == active_series].copy() # Use .copy() to avoid SettingWithCopyWarning
    if df_active.empty or 'val' not in df_active.columns or 'time' not in df_active.columns:
        return {}, {}

    # Ensure 'label' column exists and fill NaN with empty string for coloring
    if 'label' not in df_active.columns:
        df_active['label'] = ''
    df_active['label'] = df_active['label'].fillna('')
        
    # Create a color map for labels
    # Ensure '' (unlabeled) is mapped to a default color, e.g., blue
    color_discrete_map = {label: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] 
                          for i, label in enumerate(l for l in unique_labels if l)}
    color_discrete_map[''] = '#1f77b4' # Default Plotly blue for unlabeled points

    # Main graph: scatter plot with points colored by label
    # Using customdata for point identification
    main_fig = px.scatter(df_active, x='time', y='val', title=f'Main View: {active_series}',
                          color='label', custom_data=['customdata'],
                          color_discrete_map=color_discrete_map)
    main_fig.update_traces(marker=dict(size=8), selector=dict(mode='markers'))


    # Add reference series if selected and different from active series
    if reference_series and reference_series != active_series:
        df_reference = df[df['series'] == reference_series]
        if not df_reference.empty and 'val' in df_reference.columns:
            main_fig.add_scatter(x=df_reference['time'], y=df_reference['val'], mode='lines',
                                 name=f'Reference: {reference_series}', line=dict(dash='dash', color='grey'),
                                 marker=None) # No markers for reference line

    # Context graph shows only the active series line (no individual point colors for simplicity)
    context_fig = px.line(df_active, x='time', y='val', title=f'Context: {active_series}')
    
    context_fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    main_fig.update_layout(xaxis_type="date")
    
    return main_fig, context_fig

@dash_app.callback(
    Output('main-graph', 'figure'),
    [Input('context-graph', 'relayoutData'),
     Input('data-store', 'data'), # Re-plot if main data changes
     Input('active-series-dropdown', 'value'),
     Input('reference-series-dropdown', 'value'),
     Input('active-label-dropdown', 'value'), # Potentially to update styling based on active label
     Input('unique-labels-store', 'data')], # To update colors if labels change
    prevent_initial_call=True
)
def update_main_graph_range(relayout_data, json_data, active_series, 
                            reference_series, active_label, unique_labels):
    if json_data is None or active_series is None:
        return {}
        
    try:
        df = pd.read_json(json_data, orient='split')
        df['time'] = pd.to_datetime(df['time'])
        df['customdata'] = df.index # Ensure customdata is available
    except Exception:
        return {} # Error parsing data

    if df.empty:
        return {}

    df_active = df[df['series'] == active_series].copy()
    if df_active.empty or 'val' not in df_active.columns:
        return {}
        
    if 'label' not in df_active.columns:
        df_active['label'] = ''
    df_active['label'] = df_active['label'].fillna('')

    color_discrete_map = {label: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] 
                          for i, label in enumerate(l for l in unique_labels if l)}
    color_discrete_map[''] = '#1f77b4' # Default Plotly blue

    fig = px.scatter(df_active, x='time', y='val', title=f'Main View: {active_series}',
                     color='label', custom_data=['customdata'],
                     color_discrete_map=color_discrete_map)
    fig.update_traces(marker=dict(size=8), selector=dict(mode='markers'))
    
    if reference_series and reference_series != active_series:
        df_reference = df[df['series'] == reference_series]
        if not df_reference.empty and 'val' in df_reference.columns:
            fig.add_scatter(x=df_reference['time'], y=df_reference['val'], mode='lines',
                            name=f'Reference: {reference_series}', line=dict(dash='dash',color='grey'),
                            marker=None)

    fig.update_layout(xaxis_type="date")

    # Apply zoom from context graph if present
    if relayout_data and 'xaxis.range[0]' in relayout_data and 'xaxis.range[1]' in relayout_data:
        fig.update_xaxes(range=[relayout_data['xaxis.range[0]'], relayout_data['xaxis.range[1]']])
    elif relayout_data and 'xaxis.autorange' in relayout_data:
         fig.update_xaxes(autorange=True)
    
    return fig


# Callback for point labeling
@dash_app.callback(
    Output('data-store', 'data', allow_duplicate=True),
    [Input('main-graph', 'clickData'),
     Input('main-graph', 'selectedData')],
    [dash.dependencies.State('active-label-dropdown', 'value'),
     dash.dependencies.State('active-series-dropdown', 'value'),
     dash.dependencies.State('data-store', 'data')],
    prevent_initial_call=True
)
def apply_label_to_points(click_data, selected_data, label_to_apply, active_series_name, json_data):
    ctx = dash.callback_context
    if not ctx.triggered or not label_to_apply or not active_series_name or not json_data:
        return dash.no_update

    try:
        df = pd.read_json(json_data, orient='split')
        # Important: Ensure 'time' column is datetime for any potential time-based operations
        # and that the index used for customdata is consistent.
        df['time'] = pd.to_datetime(df['time']) 
    except Exception as e:
        print(f"Error parsing DataFrame for labeling: {e}")
        return dash.no_update

    # Create a mask for the active series.
    # This is important because customdata (df.index) is for the whole DataFrame.
    # We need to ensure we are updating points only within the active series.
    # However, if 'customdata' refers to the original index, we can use it directly.
    
    indices_to_update = []

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[1] # 'clickData' or 'selectedData'

    if triggered_input == 'clickData' and click_data:
        point_custom_data = click_data['points'][0].get('customdata')
        if point_custom_data is not None:
            # Assuming customdata is the DataFrame index
            original_df_index = point_custom_data[0] # custom_data was set as ['customdata_col']
            
            # Check if this point actually belongs to the active series
            if df.loc[original_df_index, 'series'] == active_series_name:
                indices_to_update.append(original_df_index)

    elif triggered_input == 'selectedData' and selected_data:
        for point in selected_data['points']:
            point_custom_data = point.get('customdata')
            if point_custom_data is not None:
                original_df_index = point_custom_data[0]
                if df.loc[original_df_index, 'series'] == active_series_name:
                    indices_to_update.append(original_df_index)
    
    if not indices_to_update:
        return dash.no_update

    # Apply the label
    # Optional toggle logic:
    # current_label = df.loc[indices_to_update[0], 'label'] # Check label of first point
    # if current_label == label_to_apply and triggered_input == 'clickData': # Only toggle for single click
    #     df.loc[indices_to_update, 'label'] = '' # Unlabel
    # else:
    #     df.loc[indices_to_update, 'label'] = label_to_apply
    
    df.loc[indices_to_update, 'label'] = label_to_apply
    
    return df.to_json(date_format='iso', orient='split')

# Callback for exporting data
@dash_app.callback(
    Output('download-dataframe-csv', 'data'),
    [Input('export-csv-button', 'n_clicks')],
    [dash.dependencies.State('data-store', 'data')],
    prevent_initial_call=True
)
def export_labeled_csv(n_clicks, json_data):
    if n_clicks == 0 or json_data is None:
        return dash.no_update

    try:
        df = pd.read_json(json_data, orient='split')
    except Exception as e:
        print(f"Error parsing DataFrame for export: {e}")
        return dash.no_update

    # Remove 'customdata' column if it exists
    if 'customdata' in df.columns:
        df = df.drop(columns=['customdata'])
    
    # Ensure 'time' column is in a standard string format if it's datetime
    if 'time' in df.columns and pd.api.types.is_datetime64_any_dtype(df['time']):
        df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')


    original_filename = session.get('original_filename', 'data.csv')
    base_filename, ext = os.path.splitext(original_filename)
    export_filename = f"{base_filename}-labeled.csv"

    return dcc.send_data_frame(df.to_csv, export_filename, index=False)


if __name__ == '__main__':
    app.run(debug=True)
