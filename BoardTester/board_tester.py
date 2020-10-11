# Configure_Dut_Tab.py ################################
#   - Contains the following prompts
#       1) Enter Number of Voltage Inputs
#           - Use input to create DataFrame and 
#           - display editabletable delow
#
#       2) Enter Number of Current Inputs
#           - Use input to create DataFrame and 
#           - display editabletable delow
#
#       3) Enter Number of Temperatures
#           - Use input to create DataFrame and 
#           - display editabletable delow
#
#       4) Enter Number of Digital Inputs
#           - Use input to create DataFrame and 
#           - display editabletable delow
#
#       5) Enter Number of Digital Outputs
#           - Use input to create DataFrame and 
#           - display editabletable delow

### TABS
### Configure DUT
### - details above
### - dropdown to select lab device (labjack, SAILY, Digilent)
### Cofigure Test
### Simulation (Expected Results)
### Start Test (Live Updates)

import time
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# App Files
from tab_contents import build_dut_config_tab, build_test_config_tab

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------
# App layout

app.layout = dbc.Container(
    [
        # Memory Storage used to transfer data between callbacks.
        dcc.Store(id='add-vs-click-store'),
        dcc.Store(id='add-is-click-store'),
        dcc.Store(id='add-gpi-click-store'),
        dcc.Store(id='add-gpo-click-store'),
        dcc.Store(id='add-temp-click-store'),
        dcc.Store(id='vs-dut-config-store',storage_type='session'),
        dcc.Store(id='is-dut-config-store',storage_type='session'),
        dcc.Store(id='gpi-dut-config-store',storage_type='session'),
        dcc.Store(id='gpo-dut-config-store',storage_type='session'),
        dcc.Store(id='temp-dut-config-store',storage_type='session'),

        html.H1("PCB Design Verification Testing App"),
        html.H6("PCB P/N:   {pcb_pn}, PCB Name:   {pcb_name}, Test Date:   {date}"),
        html.Hr(),

        # Tabs Layout
        dbc.Tabs(
            children=[
                dbc.Tab(label="1 - Configure DUT", 
                        tab_id="dut-config-tab",
                ),

                dbc.Tab(label="2 - Configure Test", 
                        tab_id="test-config-tab"
                ),

                dbc.Tab(label="3 - Simulate", 
                        tab_id="simulate_tab"
                ),

                dbc.Tab(label="4 - Run Test", 
                        tab_id="run_test_tab"
                ),
            ],
            id="tabs",
            active_tab="dut-config-tab"
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

#  Switching Tabs
@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'active_tab'), 
     Input('add-vs-click-store', 'data'),
     Input('vs-dut-config-store', 'data'),
     Input('is-dut-config-store', 'data'),
     Input('gpi-dut-config-store', 'data'),
     Input('gpo-dut-config-store', 'data'),
     Input('temp-dut-config-store', 'data')]
)
def switch_tab(active_tab, click_data,
               vs_data_dict,is_data_dict,gpi_data_dict,gpo_data_dict,temp_data_dict):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab == 'dut-config-tab':
        return build_dut_config_tab(vs_data_dict,is_data_dict,gpi_data_dict,
                                    gpo_data_dict,temp_data_dict)
    elif active_tab == 'test-config-tab':
        return build_test_config_tab()
    else:
        return 'No tab selected'

# Tab 1 - Add voltage source
@app.callback(
    [Output('vs-dut-config-store', 'data'),
     Output('add-vs-click-store','data')],
    [Input('add-vs-button', 'n_clicks')],
    [State('voltage-source-table', 'data'),
     State('voltage-source-table', 'columns')]
)
def add_voltage_source(vs_n_clicks, rows, columns):
    if vs_n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
        df = pd.DataFrame(rows, columns=[c['id'] for c in columns])
        return [
            df.to_dict('records'),
            vs_n_clicks
        ]
    else:
        df = pd.DataFrame(rows, columns=[c['id'] for c in columns])
        return [
            df.to_dict('records'),
            vs_n_clicks
        ]


# Tab 1 update all tables from memory storage
@app.callback(
    Output('voltage-source-table','data'),
    Input('vs-dut-config-store','data')
)
def on_data_set_table(data):
    if data is None:
        raise PreventUpdate
    return data

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)
    app.run_server(debug=True)
    #app.run_server(degub=True,port=8077,threaded=True)
    #app.run_server(dev_tools_hot_reload=False)
    #app.run_server(mode='inline')

