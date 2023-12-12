"""
This module contains code used to create plot representing mean value 
of football players playing on certain positions. 
"""
import pandas as pd
import plotly.graph_objects as go
from PIL import Image


def filter_only_players_from_top5(df):
    df2 = pd.read_csv("data/player_valuations_with_age_and_club.csv")
    transfers = pd.read_csv("data/club_transfers.csv")
    transfers = transfers[transfers["league"] != "Arab"]
    clubs = pd.read_csv("data/clubs.csv")
    top5_league_club_ids = clubs[clubs["name"].isin(transfers["Club"].unique())][
        "club_id"
    ].unique()
    df = df.merge(
        df2[["player_id", "date", "player_club_id"]], on=["player_id", "date"]
    )
    return df[df["player_club_id"].isin(top5_league_club_ids)]


def number_of_players_per_position(df, year):
    df["year"] = [int(date.split("-")[0]) for date in df["date"]]
    df = df[df["year"] == year]
    df = df.drop_duplicates(subset="player_id")
    df = df.sort_values(by="market_value_in_eur", ascending=False).head(500)
    df = df.groupby("sub_position").mean("market_value_in_eur")

    position_dict = {}
    for position in df.index:
        position_dict[position] = df.loc[position, "market_value_in_eur"]
    return position_dict


def create_plot_value_per_position():
    player_valuations = pd.read_csv("data/player_valuations_with_age.csv")
    player_valuations = filter_only_players_from_top5(player_valuations)
    values = number_of_players_per_position(player_valuations.copy(), 2023)
    coordinates = {
        "Attacking Midfield": (0, 3.15),
        "Second Striker": (0, 3.9),
        "Centre-Back": (0, 0.8),
        "Right Winger": (0.8, 4),
        "Right Midfield": (1, 2.4),
        "Left-Back": (-0.8, 1),
        "Centre-Forward": (0, 4.6),
        "Left Midfield": (-1, 2.4),
        "Defensive Midfield": (0, 1.65),
        "Left Winger": (-0.8, 4),
        "Goalkeeper": (0, 0),
        "Right-Back": (0.8, 1),
        "Central Midfield": (0, 2.4),
    }
    colors = {
        "Goalkeeper": "#CCE47E",
        "Defender": "#A9D78E",
        "Midfielder": "#9DC3C2",
        "Attacker": "#6B97C3",
    }
    position_groups = {
        "Attacking Midfield": "Midfielder",
        "Second Striker": "Attacker",
        "Centre-Back": "Defender",
        "Right Winger": "Attacker",
        "Right Midfield": "Midfielder",
        "Left-Back": "Defender",
        "Centre-Forward": "Attacker",
        "Left Midfield": "Midfielder",
        "Defensive Midfield": "Midfielder",
        "Left Winger": "Attacker",
        "Goalkeeper": "Goalkeeper",
        "Right-Back": "Defender",
        "Central Midfield": "Midfielder",
    }

    fig = go.Figure()

    for position in coordinates:
        # print(position)

        fig.add_trace(
            go.Scatter(
                x=[coordinates[position][0]],
                y=[coordinates[position][1]],
                mode="markers",
                marker=dict(
                    size=values[position] / 600000,
                    color=colors[position_groups[position]],
                    opacity=1,
                ),
                name=position,
                text=position,
                hoverinfo="text",
            )
        )

        # add annotations for the increase_per_position
    annotations = []
    for position in coordinates:
        # get the radius of the circle
        # r = 0.25
        r = (values[position] / (600000 * 3.14)) ** 0.5
        y = coordinates[position][1] - r / 10 + 0.07
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=coordinates[position][0],
                y=y,
                text=position,
                font=dict(
                    family="Arial", size=14, color=colors[position_groups[position]]
                ),
                showarrow=False,
            )
        )
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=coordinates[position][0],
                y=coordinates[position][1],
                text=f"{round(values[position] / 1000000, 1)}M",
                font=dict(family="Arial", size=14, color="black"),
                showarrow=False,
            )
        )
    fig.update_layout(annotations=annotations)

    # add black lines that represent the field
    fig.add_shape(
        type="line",
        x0=-1.3,
        y0=-0.4,
        x1=1.3,
        y1=-0.4,
        line=dict(color="Black", width=2),
    )
    fig.add_shape(
        type="line",
        x0=-1.3,
        y0=5.2,
        x1=1.3,
        y1=5.2,
        line=dict(color="Black", width=2),
    )
    fig.add_shape(
        type="line",
        x0=-1.3,
        y0=-0.4,
        x1=-1.3,
        y1=5.2,
        line=dict(color="Black", width=2),
    )
    fig.add_shape(
        type="line", x0=1.3, y0=-0.4, x1=1.3, y1=5.2, line=dict(color="Black", width=2)
    )
    # line in the middle
    fig.add_shape(
        type="line", x0=-1.3, y0=2.5, x1=1.3, y1=2.5, line=dict(color="Black", width=2)
    )
    # circle in the middle
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-0.41,
        y0=1.75,
        x1=0.41,
        y1=3.25,
        line_color="Black",
        line_width=2,
    )
    # goalkeepers area
    fig.add_shape(
        type="line", x0=-0.7, y0=0.6, x1=0.7, y1=0.6, line=dict(color="Black", width=2)
    )
    fig.add_shape(
        type="line",
        x0=-0.7,
        y0=-0.4,
        x1=-0.7,
        y1=0.6,
        line=dict(color="Black", width=2),
    )
    fig.add_shape(
        type="line", x0=0.7, y0=-0.4, x1=0.7, y1=0.6, line=dict(color="Black", width=2)
    )
    # goalkeepers area on the other side
    fig.add_shape(
        type="line", x0=-0.7, y0=4.4, x1=0.7, y1=4.4, line=dict(color="Black", width=2)
    )
    fig.add_shape(
        type="line",
        x0=-0.7,
        y0=5.20,
        x1=-0.7,
        y1=4.4,
        line=dict(color="Black", width=2),
    )
    fig.add_shape(
        type="line", x0=0.7, y0=5.20, x1=0.7, y1=4.4, line=dict(color="Black", width=2)
    )

    fig.update_layout(
        width=700,
        height=700,
        margin=dict(l=100, r=50, t=50, b=50),
        plot_bgcolor="rgba(0,0,0,0)",
        title="You are fast and shoot good? Go for left wing<br><sup>If not avoid being left mid or right mid</sup>",
        title_font_size=30,
        title_font_family="Arial",
        title_x=0.05,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
    )
    return fig


if __name__ == "__main__":
    fig = create_plot_value_per_position()
    fig.show()
    fig.write_html("images/average_market_value.html")
