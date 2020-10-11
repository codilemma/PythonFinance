# Cody Holthus - Rip City Robotics

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table


class TabContents:
    def __init__(self):
        self.dut_config_tab = dbc.Card(
            dbc.CardBody(
                [
                    html.P("Configure the DUT", className="card-text"),
                    dbc.Button("Save",
                                id="dut_config_button", 
                                color="primary"),
                    dash_table.DataTable(
                        id='adding-rows-table',
                        columns=[{
                            'name': ['Voltage Source',
                                     'Vmax (Volts)',
                                     'Vmin (Volts',
                                     'Von Delay (ms)'],
                            'id': ['vs','vmax','vmin','von_delay'],
                            'deletable': False,
                            'renamable': True
                        }],
                        editable=True,
                        row_deletable=True
                    ),

                    html.Button('Add Row', id='editing-rows-button', n_clicks=0),
                ]
            ),
            className="mt-3",
        )

        self.test_config_tab = dbc.Card(
            dbc.CardBody(
                [
                    html.P("This is tab 2!", className="card-text"),
                    dbc.Button("Don't click here", color="danger"),
                ]
            ),
            className="mt-3",
        )

        self.tabs = dbc.Tabs(
            [
                dbc.Tab(label="1 - Configure DUT", 
                        tab_id="dut_config_tab"),

                dbc.Tab(label="2 - Configure Test", 
                        tab_id="test_config_tab"),

                dbc.Tab(label="3 - Simulate", 
                        tab_id="simulate_tab"),

                dbc.Tab(label="4 - Run Test", 
                        tab_id="run_test_tab"),
            ],
            id="tabs"
        )

    def get_all_tabs(self):
        return self.tabs

    def render_tab(self,active_tab):
        if active_tab == 'dut_config_tab':
            return self.dut_config_tab

