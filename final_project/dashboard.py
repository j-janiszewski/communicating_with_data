import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback
from plot_value_diff_by_position import create_plot_value_per_position
from plot_number_of_players_per_position import number_of_players_per_position_plot
from bar_plot_clubs import create_plot_club_increasing_value
import plotly.express as px
import dash_bootstrap_components as dbc

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'],
    prevent_initial_callbacks="initial_duplicate",
)

app.layout = html.Div(
    [
        html.H1("Charting Success: How Data visualization Guides a Young Fotballer"),
        dcc.Tabs(
            id="tabs-example-graph",
            value="tab-1-example-graph",
            children=[
                dcc.Tab(
                    label="Wich positions are more valuable",
                    value="tab-1-example-graph",
                ),
                dcc.Tab(label="Value of the positions", value="tab-2-example-graph"),
                dcc.Tab(label="Value of the positions", value="tab-3-example-graph"),
                dcc.Tab(label="Value of the positions", value="tab-4-example-graph"),
            ],
        ),
        dcc.Store(id="graph-storage"),
        dcc.Store(id="graph-tab3-storage"),
        html.Div(id="tabs-content-example-graph"),
    ]
)

@callback(
    [Output("tabs-content-example-graph", "children"), Output("graph-storage", "data")],
    Input("tabs-example-graph", "value"),
    [State("graph-storage", "data")],
)
def render_content(tab, stored_data):
    if stored_data is None:
        stored_data = {}

    if tab == "tab-1-example-graph":
        fig = stored_data.get("fig1") or create_plot_value_per_position()
        stored_data["fig1"] = fig
        return (
            html.Div(
                [
                    html.H3("Wich positions are more valuable"),
                    dcc.Graph(id="positions_field", figure=fig),
                ]
            ),
            stored_data,
        )

    elif tab == "tab-2-example-graph":
        fig2 = stored_data.get("fig2") or number_of_players_per_position_plot()
        stored_data["fig2"] = fig2
        return (
            html.Div(
                [
                    html.H3("Line Graph Positions"),
                    dcc.Graph(id="graph-2-tabs-dcc", figure=fig2),
                ]
            ),
            stored_data,
        )

    elif tab == "tab-3-example-graph":
        return (
            html.Div(
                [
                    html.H3(
                        f"Top 10 clubs that increase the median value of young Defenders",
                        id="plot_3_title",
                    ),
                    dcc.RadioItems(
    [
        {
            "label": html.Div(['Defenders'], style={'color': '#1f77b4', 'font-size': 20,'padding':20}),
            "value": "Defenders",
        },
        {
            "label": html.Div(['Midfielders'], style={'color': '#ff7f0e', 'font-size': 20, 'padding':20}),
            "value": "Midfielders",
        },
        {
            "label": html.Div(['Attackers'], style={'color': '#2ca02c', 'font-size': 20,'padding':20}),
            "value": "Attackers",
        },
    ], value='Defenders', id="radio-items-positions", inline=True
),
                    dcc.Graph(id="graph-3-tabs-dcc"),
                ]
            ),
            stored_data,
        )

    elif tab == "tab-4-example-graph":
        return (
            html.Div(
                [
                    html.H3("Tab content 4"),
                    dcc.Graph(
                        id="graph-4-tabs-dcc",
                        figure={
                            "data": [{"x": [1, 2, 3], "y": [5, 10, 6], "type": "bar"}]
                        },
                    ),
                ]
            ),
            stored_data,
        )

    return html.Div(), stored_data


@callback(
    [
        Output("plot_3_title", "children"),
        Output("graph-3-tabs-dcc", "figure"),
        Output("graph-tab3-storage", "data"),
    ],
    Input(component_id="radio-items-positions", component_property="value"),
    State("graph-tab3-storage", "data"),
)
def render_third_tab(position, stored_data):
    if stored_data is None:
        stored_data = {}
    fig3 = stored_data.get("fig3") or create_plot_club_increasing_value(position)
    stored_data["fig3"] = fig3
    return (
        f"Top 10 clubs that increase the median value of young {position}",
        fig3,
        stored_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
