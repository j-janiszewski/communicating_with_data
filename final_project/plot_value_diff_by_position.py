import pandas as pd
import plotly.graph_objects as go


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


def main():
    player_valuations = pd.read_csv('data/player_valuations_with_age.csv')

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
        "Central Midfield": (0, 2.4)
    }

    colors = {
        "Attacking Midfield": "#ff7f0e",
        "Second Striker": "#2ca02c",
        "Centre-Back": "#1f77b4",
        "Right Winger": "#2ca02c",
        "Right Midfield": "#ff7f0e",
        "Left-Back": "#1f77b4",
        "Centre-Forward": "#2ca02c",
        "Left Midfield": "#ff7f0e",
        "Defensive Midfield": "#ff7f0e",
        "Left Winger": "#2ca02c",
        "Goalkeeper": "#d62728",
        "Right-Back": "#1f77b4",
        "Central Midfield": "#ff7f0e"
    }

    fig = go.Figure()

    for position in coordinates:
        print(position)

        fig.add_trace(go.Scatter(
            x=[coordinates[position][0]],
            y=[coordinates[position][1]],
            mode="markers",
            marker=dict(
                size=values[position] / 600000,
                color=colors[position],
                opacity=0.5
            ),
            name=position,
            text=position,
            hoverinfo="text"
        ))

    # add annotations for the increase_per_position
    annotations = []
    for position in coordinates:
        # get the radius of the circle
        # r = 0.25
        r = (values[position] / (600000 * 3.14)) ** 0.5
        y = coordinates[position][1] - r / 10 + 0.07
        annotations.append(dict(xref='x', yref='y',
                                x=coordinates[position][0], y=y,
                                text=position,
                                font=dict(family='Arial', size=14,
                                          color=colors[position]),
                                showarrow=False))
        annotations.append(dict(xref='x', yref='y',
                                x=coordinates[position][0], y=coordinates[position][1],
                                text=f"{round(values[position] / 1000000, 1)}M",
                                font=dict(family='Arial', size=14,
                                          color=colors[position]),
                                showarrow=False))
    fig.update_layout(annotations=annotations)

    fig.update_layout(
        width=700,
        height=700,
        margin=dict(l=100, r=50, t=50, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        title="Average market value of the increase_per_position group_by the top 500 players 2023",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        showlegend=False
    )

    fig.show()
    fig.write_html("images/average_market_value.html")


if __name__ == "__main__":
    main()
