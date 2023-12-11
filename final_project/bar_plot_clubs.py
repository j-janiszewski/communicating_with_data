"""
This module contains code used to create plot with clubs 
that are increasing value of football players most . 
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_plot_club_increasing_value(position: str):
    colors = {"Attackers": "#2ca02c", "Defenders": "#1f77b4", "Midfielders": "#ff7f0e"}

    df = pd.read_csv("data/club_value_increase.csv")
    df = df[df["position"] == position[:-1]]
    df = df.sort_values(by="value_increase", ascending=False)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["value_increase"],
            y=list(range(10, 0, -1)),
            name="att",
            marker=dict(
                color=colors[position],
                line=dict(color=colors[position], width=1),
            ),
            orientation="h",
        )
    )

    fig.update_layout(
        title=dict(
            text="If you have a chance, pick one of this clubs <br><sup>Not all clubs are equally good at increasing value of players in different positions</sup>",
            font_size=30,
            font_family="Arial",
            x=0.05,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            # domain=[0, 1],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=False,
            showgrid=True,
            domain=[0.2, 0.8],
        ),
        showlegend=False,
        plot_bgcolor="white",
    )

    # add annotations
    for i in range(0, 10):
        for j, df in enumerate([df]):
            idx = 10 - i - 1
            fig.add_annotation(
                dict(
                    xref="x",
                    yref="y",
                    x=0,
                    y=i + 1,
                    text=df["club_name"].iloc[idx][:20],
                    font=dict(family="Arial", size=12, color="black"),
                    showarrow=False,
                    align="right",
                    xanchor="right",
                )
            )
            # add value to each bar
            fig.add_annotation(
                dict(
                    xref="x",
                    yref="y",
                    x=df["value_increase"].iloc[idx],
                    y=i + 1,
                    text=str(round(df["value_increase"].iloc[idx], 2)),
                    font=dict(family="Arial", size=12, color="black"),
                    showarrow=False,
                    align="left",
                    xanchor="left",
                )
            )

    return fig


if __name__ == "__main__":
    fig = create_plot_club_increasing_value("Attackers")
    fig.show()
    # save as html
    fig.write_html("images/attacker.html")
