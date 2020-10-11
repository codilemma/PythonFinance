import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

# Initialize empty DUT Configuration Data Frame
df_vs_config = pd.DataFrame({})
# ------------------------------------------------------------------------------
# Tab1 Contents
def build_dut_config_tab(vs_data_dict,is_data_dict,gpi_data_dict,
                         gpo_data_dict,temp_data_dict):
    dut_config_dfs = {
        'vs_config_df'   : pd.DataFrame.from_dict(vs_data_dict),
        'is_config_df'   : pd.DataFrame.from_dict(is_data_dict),
        'gpi_config_df'  : pd.DataFrame.from_dict(gpi_data_dict),
        'gpo_config_df'  : pd.DataFrame.from_dict(gpo_data_dict),
        'temp_config_df' : pd.DataFrame.from_dict(temp_data_dict)
    }

    # Initialize DUT tables on Startup, or Load User entered data from callback.
    dut_init_dicts = {
        'vs_init_dict'   : {},
        'is_init_dict'   : {},
        'gpi_init_dict'  : {},
        'gpo_init_dict'  : {},
        'temp_init_dict' : {}
    }
    # Prevent data from being overwritten when tabs are changed.
    for i,j in zip(dut_config_dfs,dut_init_dicts):
        if dut_config_dfs[i] is not None:
            dut_init_dicts[j] = dut_config_dfs[i].to_dict('records')
        else:
            dut_init_dicts[j] = []

    dut_config_tab = dbc.Card(
        dbc.CardBody(
            [
                # Add Voltage Source Input and Button
                html.H6("Configure DUT Voltage Sources", className="card-text"),
                dash_table.DataTable(
                    id='voltage-source-table',
                    columns=(
                        [{'id': 'vs', 'name': 'Voltage Source Name'}] +
                        [{'id': 'vmax', 'name': 'Max Voltage'}] +
                        [{'id': 'vmin', 'name': 'Min Voltage'}] +
                        [{'id': 'ton', 'name': 'Ton Delay'}]
                    ),
                    data=dut_init_dicts['vs_init_dict'],
                    editable=True,
                    row_deletable=True,
                ),
                html.Button('Add Voltage Source', id='add-vs-button', n_clicks=0),
                html.Br(),html.Br(),html.Br(),html.Br(),


                # Add Current Source Input and Button
                html.H6("Configure DUT Current Sources", className="card-text"),
                dash_table.DataTable(
                    id='current-source-table',
                    columns=(
                        [{'id': 'is', 'name': 'Current Source Name'}] +
                        [{'id': 'imax', 'name': 'Estimated Max Current'}]
                    ),
                    data=dut_init_dicts['is_init_dict'],
                    editable=True,
                    row_deletable=True,
                ),
                html.Button('Add Current Source', id='add-is-button', n_clicks=0),
                html.Br(),html.Br(),html.Br(),html.Br(),

                # Add Current Source Input and Button
                html.H6("Configure DUT Current Sources", className="card-text"),
                dash_table.DataTable(
                    id='current-source-table',
                    columns=(
                        [{'id': 'is', 'name': 'Current Source Name'}] +
                        [{'id': 'imax', 'name': 'Estimated Max Current'}]
                    ),
                    data=dut_init_dicts['is_init_dict'],
                    editable=True,
                    row_deletable=True,
                ),
                html.Button('Add Current Source', id='add-is-button', n_clicks=0),
                html.Br(),html.Br(),html.Br(),html.Br(),

                # Save Config Button
                dbc.Button("Save Configuration",
                           id="save-config-button", 
                           color="primary",
                           n_clicks = 0),

                #Page Break x4
                html.Br(),html.Br(),html.Br(),html.Br(),
            ]
        ),
        className="mt-3",
    )
    return dut_config_tab

def build_test_config_tab():
    test_config_tab = dbc.Card(
        dbc.CardBody(
            [
                html.P("This is tab 2!", className="card-text"),
                dbc.Button("Don't click here", color="danger"),
            ]
        ),
        className="mt-3",
    )
    return test_config_tab




