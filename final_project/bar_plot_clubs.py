import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
    # plot bar plot of top 10 clubs with highest value increase
    import plotly.express as px

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

    fig.show()
    # save as html
    fig.write_html("images/bar_plot_clubs.html")


if __name__ == "__main__":
    main()
