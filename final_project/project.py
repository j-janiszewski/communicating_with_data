import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output,State, callback
from plot_value_diff_by_position import create_plot_value_per_position
from plot_number_of_players_per_position import number_of_players_per_position
from plotly.subplots import make_subplots
import plotly.express as px
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__,suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Charting Success: How Data visualization Guides a Young Fotballer'),
    
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Wich positions are more valuable', value='tab-1-example-graph'),
        dcc.Tab(label='Value of the positions', value='tab-2-example-graph'),
        dcc.Tab(label='Value of the positions', value='tab-3-example-graph'),
        dcc.Tab(label='Value of the positions', value='tab-4-example-graph')       
    ]),
     dcc.Store(id='graph-storage'),
    html.Div(id='tabs-content-example-graph')
])

#### Wich positions are more valuable ######
def create_footballer_value_graph():
    fig = create_plot_value_per_position()
    return fig

#### Value of the positions ######
def create_line_graph_positions(year_from=2010, year_to=2023):
   
    player_valuations = pd.read_csv('data/player_valuations_with_age.csv')

    positions_per_year = {}
    for year in range(year_from, year_to+1):
        positions_per_year[year] = number_of_players_per_position(player_valuations.copy(), year)

    # turn the dictionary of dictionaries into a dataframe
    df = pd.DataFrame(positions_per_year)

    df = df / 5


    # plot the difference between the number of players per position in 2023 and 2010
    # on a bar chart using plotly
    import plotly.graph_objects as go

    colors = {
        "Left Winger": "#66B2FF",
        "Right Winger": "#0080FF",
        "Centre-Forward": "#FF6666",
    }



    fig = go.Figure()
    k = 0
    num_positions = len(df.index) - len(colors)

    # randomly shuffle index
    df = df.sample(frac=1)

    for position in df.index:
        print(position)
        color = colors.get(position, "grey")
        if color == "grey":
            size = 5
        else:
            size = 10

        if color == "grey":
            r = g = b = (k+1) / (num_positions + 2)
            color = f"rgb({r}, {g}, {b})"
            k += 1

        fig.add_trace(go.Scatter(
            x=df.columns,
            y=df.loc[position],
            name=position,
            marker=dict(color=color, size=size),
            line=dict(color=color, width=size / 2),
            connectgaps=True
        ))

    fig.update_layout(
        title='Evolution of the game: Teams playing with wingers instead of strikers<br>'
              '<sup>Comparing the number of players in each position '
              'from 500 most valuable players each year</sup>',
        # title size and font
        title_font_size=30,
        title_font_family="Arial",
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Number of players',
            titlefont_size=16,
            tickfont_size=14,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, 22]
        ),
        xaxis=dict(
            title='Year',
            titlefont_size=16,
            tickfont_size=14,
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            range=[year_from-1, year_to+1],
            tickvals=[year_from, year_to]
        ),
        # remove legend
        showlegend=False,
        # plot background color
        plot_bgcolor='white',
        # margin left, bottom, right, top
        margin=dict(l=150, r=50, t=50, b=50)
    )
    print(df)

    annotations = []
    # Adding labels
    for position in colors:
        # labeling the left_side of the plot
        text_left = df[df.index == position][year_from].values[0]
        text_right = df[df.index == position][year_to].values[0]

        annotations.append(dict(xref='paper', x=0.05, y=df[df.index == position][year_from].values[0],
                                xanchor='right', yanchor='middle',
                                text=f"{position} {text_left}%",
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=df[df.index == position][year_to].values[0],
                                xanchor='left', yanchor='middle',
                                text=f"{text_right}%",
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
    fig.update_layout(annotations=annotations)
    return fig

########Clubs##########
def create_clubs(positions):
    df = pd.read_csv('data/club_value_increase.csv')
    df = df.sort_values(by='value_increase', ascending=False)

    df_def = df[df['position'] == 'Defender']
    df_mid = df[df['position'] == 'Midfield']
    df_att = df[df['position'] == 'Attack']


    fig = make_subplots(rows=1, cols=3, specs=[[{}, {}, {}]],
                        shared_yaxes=False, vertical_spacing=0.001)

    fig.add_trace(go.Bar(x=df_def['value_increase'],
                            y=list(range(10, 0, -1)),
                            name='def',
                            marker=dict(
                                color='green',
                                line=dict(
                                    color='green',
                                    width=1),
                            ),
                            orientation='h'
                            ), 1, 1)

    fig.add_trace(go.Bar(x=df_mid['value_increase'],
                            y=list(range(10, 0, -1)),
                            name='mid',
                            marker=dict(
                                color='blue',
                                line=dict(
                                    color='blue',
                                    width=1),
                            ),
                            orientation='h'
                            ), 1, 2)

    fig.add_trace(go.Bar(x=df_att['value_increase'],
                            y=list(range(10, 0, -1)),
                            name='att',
                            marker=dict(
                                color='orange',
                                line=dict(
                                    color='orange',
                                    width=1),
                            ),
                            orientation='h'
                            ), 1, 3)

    fig.update_layout(
        title='Clubs that increase the median value of young players the most',
        title_font_size=30,
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            domain=[0, 0.95],
        ),
        yaxis2=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            domain=[0, 0.95],
        ),
        yaxis3=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            domain=[0, 0.95],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=False,
            showgrid=True,
            domain=[0, 0.3],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=False,
            showgrid=True,
            domain=[0.33, 0.63],
        ),
        xaxis3=dict(
            zeroline=False,
            showline=False,
            showticklabels=False,
            showgrid=True,
            domain=[0.66, 0.96]
        ),
        showlegend=False,
        plot_bgcolor='white',
    )

    # add annotations
    for i in range(0, 10):
        for j, df in enumerate([df_def, df_mid, df_att]):
            idx = 10 - i - 1
            fig.add_annotation(
                dict(
                    xref="x",
                    yref="y",
                    x=0,
                    y=i+1,
                    text=df['club_name'].iloc[idx][:20],
                    font=dict(
                        family="Arial",
                        size=12,
                        color="black"
                    ),
                    showarrow=False,
                    align="right",
                    xanchor="right"
                ),
                row=1, col=j+1
            )
            # add value to each bar
            fig.add_annotation(
                dict(
                    xref="x",
                    yref="y",
                    x=df['value_increase'].iloc[idx],
                    y=i + 1,
                    text=str(round(df['value_increase'].iloc[idx], 2)),
                    font=dict(
                        family="Arial",
                        size=12,
                        color="black"
                    ),
                    showarrow=False,
                    align="left",
                    xanchor="left"
                ),
                row=1, col=j+1
            )

    # add attack, mid, def labels
    fig.add_annotation(
        dict(
            xref="paper",
            yref="paper",
            x=0.1,
            y=11,
            text="Defenders",
            font=dict(
                family="Arial",
                size=20,
                color="green"
            ),
            showarrow=False,
            align="left",
            xanchor="left"
        ),
        row=1, col=1
    )
    fig.add_annotation(
        dict(
            xref="paper",
            yref="paper",
            x=0.1,
            y=11,
            text="Midfielders",
            font=dict(
                family="Arial",
                size=20,
                color="blue"
            ),
            showarrow=False,
            align="left",
            xanchor="left"
        ),
        row=1, col=2
    )
    fig.add_annotation(
        dict(
            xref="paper",
            yref="paper",
            x=0.1,
            y=11,
            text="Attackers",
            font=dict(
                family="Arial",
                size=20,
                color="orange"
            ),
            showarrow=False,
            align="left",
            xanchor="left"
        ),
        row=1, col=3
    )

    return fig
@callback([Output('tabs-content-example-graph', 'children'),
          Output('graph-storage', 'data')],
              Input('tabs-example-graph', 'value'),
              [State('graph-storage', 'data')])
def render_content(tab,stored_data):
    if stored_data is None:
        stored_data = {}

    if tab == 'tab-1-example-graph':
        fig = stored_data.get('fig1') or create_footballer_value_graph()
        stored_data['fig1'] = fig
        return html.Div([
            html.H3('Wich positions are more valuable'),
            dcc.Graph(
                id='positions_field',
                figure= fig
            )
        ]), stored_data
    
    elif tab == 'tab-2-example-graph':
        fig2 = stored_data.get('fig2') or create_line_graph_positions()
        stored_data['fig2'] = fig2
        return html.Div([
            html.H3('Line Graph Positions'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure= fig2
                
            )
        ]), stored_data
    
    elif tab == 'tab-3-example-graph':
        
        # # Use the dropdown value to determine which graph to display
        # if dropdown_value == 'Defenders':
        #     fig3 = stored_data.get('fig3') or create_clubs()
        #     stored_data['fig3'] = fig3
        # elif dropdown_value == 'Midfielders':
        #     fig3 = stored_data.get('fig3') or create_clubs()
        #     stored_data['fig3'] = fig3
        # else:  # 'Attackers'
        #     fig4 = stored_data.get('fig4') or create_line_graph_positions()
        #     stored_data['fig4'] = fig4

        return html.Div([
            html.H3(f'Top 10 clubs that increase the median value of young Defenders',id="plot_3_title"),
                    dcc.Dropdown(['Defenders', 'Midfielders', 'Attackers'],'Defenders', id= 'dropdown_positions'),
            dcc.Graph(id='graph-3-tabs-dcc')
        ]), stored_data
    
    
    elif tab == 'tab-4-example-graph':
        return html.Div([
            html.H3('Tab content 4'),
            dcc.Graph(
                id='graph-4-tabs-dcc',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ]), stored_data
    
    return html.Div(), stored_data

@callback([Output('plot_3_title', 'children'),
          Output('graph-3-tabs-dcc', 'figure'),Output('graph-storage', 'data')],
          Input(component_id='dropdown_positions', component_property='value'),
            State('graph-storage', 'data'))
          
def render_third_tab(position, stored_data):
    if stored_data is None:
        stored_data = {}
    fig3 = stored_data.get('fig3') or create_clubs(position)
    stored_data['fig3'] = fig3
    return f"Top 10 clubs that increase the median value of young {position}", fig3,stored_data




if __name__ == '__main__':
    app.run(debug=True)
