import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale

def main():
    df = pd.read_csv('ww-data-long-2023-05-02.csv')
    cities = pd.read_csv("ww-sites-2023-05-02.csv")
    # remove rows with NaN values
    df = df.dropna()
    df = df[df["Daily mean"] != 0]
    df = df[df["Year"] == 2022]

    df = df.merge(cities, on="City")

    # Data normalization
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_norm = [f"{day}_norm" for day in days]
    df["Daily mean"] = df["Daily mean"] / df["Population"]
    for day in days:
        df[day] = df[day] / df["Population"]

        df[f"{day}_norm"] = np.where(df["Daily mean"] != 0, df[day] / df["Daily mean"], 1)

    # Creating plot
    df = df.groupby(["Metabolite"])[days_norm].mean()

    df = df.reset_index()

    df = df.rename(columns={col_name: col_name[:-5] for col_name in df.columns[1:]})
    df = df.rename(columns={"Metabolite": "Drug"})

    labels = list(df["Drug"])
    print(labels)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    x_data = np.vstack((np.array(days), np.array(days), np.array(days), np.array(days),
                        np.array(days), np.array(days)))
    y_data = np.array(df[days])

    colors = ["#42A5F5", "#BDBDBD", "#66BB6A", "#FFD54F", "#757575", "#424242"]
    line_size = [4, 2, 4, 4, 2, 2]
    mode_size = [8, 4, 8, 8, 4, 4]

    fig = go.Figure()

    for i in range(6):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                                 name=labels[i],
                                 line=dict(color=colors[i], width=line_size[i]),
                                 connectgaps=True,
                                 ))
        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        width=1200,
        height=600,
        margin=dict(
            autoexpand=False,
            l=50,
            r=150,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        if round(y_trace[0] * 100) != 99:
            annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                    xanchor='right', yanchor='middle',
                                    text=f"{round(y_trace[0] * 100)}%",
                                    font=dict(family='Arial',
                                              size=16),
                                    showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[-1],
                                xanchor='left', yanchor='middle',
                                text=f"{round(y_trace[-1] * 100)}% {label}",
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(x="Thursday", y=y_data[0][3],
                            xanchor='left', yanchor='bottom',
                            # yshift=10,
                            text=f"{round(y_data[0][3] * 100)}%",
                            font=dict(family='Arial',
                                      size=16),
                            showarrow=True,
                            arrowhead=2))
    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left',
                            yanchor='bottom',
                            align='left',
                            text='EU drug consumption over the week in 2022 <br><sup>By analysing '
                                 'traces of metabolites in wastewater of 86 European cities </sup>',
                            font=dict(family='Arial',
                                      size=30,
                                      color='rgb(37,37,37)'),
                            showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                            xanchor='center', yanchor='top',
                            text='Source:<a href="https://www.emcdda.europa.eu/publications/html/'
                                 'pods/waste-water-analysis_en#wastewaterData">EMCDDA</a>',
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    fig.show()
    fig.write_html("pplot_weekly_trends.html")


if __name__ == "__main__":
    main()


"""

    fig = px.line(mean_day, x="Day of the week", y="Normalized drug consumption", color='Drug', width=1000, height=630)
    fig.update_layout(
         title=dict(
            text='EU drug consumption over the week in 2022 <br><sup>By analysing traces of metabolites in wastewater of 86 European cities </sup>',
            x=0.5,
            y=0.95,
            font=dict(
                size=26,
            )),
        annotations = [dict(
            x=1.2,
            y=-0.15,    #Trying a negative number makes the caption disappear - I'd like the caption to be below the map
            xref='paper',
            yref='paper',
            text='Source:<a href="https://www.emcdda.europa.eu/publications/html/pods/waste-water-analysis_en#wastewaterData">\
                EMCDDA</a>',
            showarrow = False
        )]
    )
"""