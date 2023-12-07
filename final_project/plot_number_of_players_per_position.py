import pandas as pd


def number_of_players_per_position(df, year):
    df["year"] = [int(date.split("-")[0]) for date in df["date"]]
    df = df[df["year"] == year]
    df = df.drop_duplicates(subset="player_id")
    df = df.sort_values(by="market_value_in_eur", ascending=False).head(500)
    df = df.groupby("sub_position").count()["player_id"]
    df = df.sort_values(ascending=False)
    # create a dictionary with the number of players per position
    position_dict = {}
    for position in df.index:
        position_dict[position] = df[position]
    return position_dict


def number_of_players_per_position_plot(year_from=2010, year_to=2023):
    player_valuations = pd.read_csv("data/player_valuations_with_age.csv")

    positions_per_year = {}
    for year in range(year_from, year_to + 1):
        positions_per_year[year] = number_of_players_per_position(
            player_valuations.copy(), year
        )

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
            r = g = b = (k + 1) / (num_positions + 2)
            color = f"rgba({r}, {g}, {b}, 0)"
            print(color)
            k += 1

        fig.add_trace(
            go.Scatter(
                x=df.columns,
                y=df.loc[position],
                name=position,
                marker=dict(color=color, size=size),
                line=dict(color=color, width=size / 2),
                connectgaps=True,
            )
        )

    fig.update_layout(
        # size of the plot
        width=900,
        height=600,
        title="Do you really want to be a center forward?<br>"
        "<sup>Percentage of centre forwards amongst worlds "
        "best players dropped a lot since 2010</sup>",
        # title size and font
        title_font_size=30,
        title_font_family="Arial",
        xaxis_tickfont_size=14,
        yaxis=dict(
            titlefont_size=16,
            tickfont_size=14,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, 22],
        ),
        xaxis=dict(
            title="Year",
            titlefont_size=16,
            tickfont_size=20,
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            range=[year_from - 1, year_to + 1],
            tickvals=[year_from, year_to],
        ),
        # remove legend
        showlegend=False,
        # plot background color
        plot_bgcolor="white",
        # margin left, bottom, right, top
        margin=dict(l=150, r=50, t=80, b=50),
    )
    print(df)

    annotations = []
    # Adding labels
    for position in colors:
        # labeling the left_side of the plot
        text_left = df[df.index == position][year_from].values[0]
        text_right = df[df.index == position][year_to].values[0]

        annotations.append(
            dict(
                xref="paper",
                x=0.05,
                y=df[df.index == position][year_from].values[0],
                xanchor="right",
                yanchor="middle",
                text=f"{position} {text_left}%",
                font=dict(family="Arial", size=16),
                showarrow=False,
            )
        )
        # labeling the right_side of the plot
        annotations.append(
            dict(
                xref="paper",
                x=0.95,
                y=df[df.index == position][year_to].values[0],
                xanchor="left",
                yanchor="middle",
                text=f"{text_right}%",
                font=dict(family="Arial", size=16),
                showarrow=False,
            )
        )
    fig.update_layout(annotations=annotations)
    return fig


if __name__ == "__main__":
    fig = number_of_players_per_position_plot()
    fig.show()
    fig.write_html("images/plot_value_difference_in_positions.html")
