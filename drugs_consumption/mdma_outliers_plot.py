import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go


df = pd.read_csv('data/ww-data-long-2023-05-02.csv')
# remove rows with NaN values
df = df.dropna()
df = df[df["Daily mean"] != 0]
df = df[df["Year"] == 2022]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
days_norm = [f"{day}_norm" for day in days]
for day in days:
    df[f"{day}_norm"] = np.where(df["Daily mean"] != 0, df[day] / df["Daily mean"], 1)

pd.options.mode.chained_assignment = None  # default='warn'


def plot_top_weird_cities(df, drug, k, add_mean=True):
    drug_df = df[(df["Metabolite"] == drug) & (df["Year"] == 2022)]

    drug_df["Country"] = drug_df["Country"].apply(lambda x: f"({x})")

    drug_df["City2"] = drug_df["City"].str.cat(drug_df["Country"], sep=" ")

    drug_df = drug_df.groupby("City2")[days_norm].sum() / drug_df.groupby("City2")[
        days_norm].count()
    # remove nan
    drug_df = drug_df.dropna()
    drug_df.loc["mean"] = drug_df.mean()

    corr = drug_df.corrwith(drug_df.loc["mean"], axis=1)
    # convert to dataframe
    corr = pd.DataFrame(corr, columns=["corr"])

    corr = corr.sort_values(by="corr", ascending=True)

    # add the correlation as a column

    drug_df = drug_df.join(corr, on="City2")
    drug_df = drug_df.sort_values(by="corr", ascending=True)
    drug_df = drug_df.reset_index()

    if add_mean:
        top_k = drug_df[drug_df["City2"].isin(corr.index[:k]) |
                        drug_df["City2"].isin(corr.index[-1:])]
    else:
        top_k = drug_df[drug_df["City2"].isin(corr.index[:k])]

    # change the "mean" row to "Weekly trend"
    mean_new_name = f"Average weekly trend"
    top_k.loc[top_k["City2"] == "mean", "City2"] = mean_new_name

    # add the mean row also
    top_k = top_k.melt(id_vars="City2",
                       value_vars=["Monday_norm", "Tuesday_norm", "Wednesday_norm", "Thursday_norm",
                                   "Friday_norm", "Saturday_norm", "Sunday_norm"])

    # apply function to variable column
    top_k["variable"] = top_k["variable"].apply(lambda x: x.split("_")[0])

    top_k.rename(columns={"variable": "Day of the week"}, inplace=True)
    top_k.rename(columns={"value": "Normalized usage of drug"}, inplace=True)

    return top_k


def create_plot(df):
    title = "Prague, Zagreb and Tampere - the hipsters of European party scene<br>" \
            "<sup>By measuring daily amount of MDMA in wastewater we can observe " \
            "alternative party cultures in European cities.</sup>"
    labels = df["City2"].unique()
    labels = ["Prague", "Zagreb", "Tampere", "Average trend"]
    # labels = ['Television', 'Newspaper', 'Internet', 'Radio', "mean"]
    colors = ['rgb(153, 204, 255)', 'rgb(255, 153, 255)', 'rgb(255, 204, 153)', 'rgb(30, 30, 30)']

    mode_size = [6, 6, 6, 6]
    line_size = [3, 3, 3, 3]
    line_dash = ['solid', 'solid', 'solid', 'dot']

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    x_data = np.vstack((np.array(days), np.array(days), np.array(days), np.array(days),
                        np.array(days)))
    y_data = np.array([df[df["City2"] == city]["Normalized usage of drug"]
                       for city in df["City2"].unique()])

    fig = go.Figure()
    annotations = []

    for i in range(len(df["City2"].unique())):

        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                                 name=labels[i],
                                 line=dict(color=colors[i], width=line_size[i], dash=line_dash[i]),
                                 connectgaps=True,
                                 ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

        # add annotations for peak days
        if labels[i] in ["Prague", "Zagreb", "Tampere"]:
            # find the max value and its index in the y_data array
            max_value = max(y_data[i])
            max_day = x_data[i][np.argmax(y_data[i])]
            annotations.append(dict(x=max_day, y=max_value, text=f"{round(max_value * 100)}%",
                                    showarrow=False, xshift=10, yshift=10,
                                    font=dict(family='Arial', size=14)))

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
        width=1200,
        height=600,
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=120,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )


    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                xanchor='right', yanchor='middle',
                                text=f"{label} {round(y_trace[0] * 100)}%",
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[-1],
                                xanchor='left', yanchor='middle',
                                text=f"{round(y_trace[-1] * 100)}%",
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            align="left",
                            text=title,
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
    fig.write_html("plot2.html")


if __name__ == "__main__":
    df = plot_top_weird_cities(df, "MDMA", 4)
    # keep only cities: "Prague" and "Zagreb"
    df = df[df["City2"].isin(["Prague (2) (CZ)", "Zagreb (HR)",
                              "Tampere (FI)", "Average weekly trend"])]
    create_plot(df)


