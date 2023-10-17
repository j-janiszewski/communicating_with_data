import plotly.express as px
import pandas as pd
import numpy as np


df = pd.read_csv('ww-data-long-2023-05-02.csv')
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

    print(top_k)
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

    fig = px.line(top_k, x="Day of the week", y="Normalized usage of drug", color='City2',
                  width=1000, height=630)
    if add_mean:
        fig.update_traces(patch={"line": {"width": 2, "dash": 'dot', "color": "black"}},
                          selector={"legendgroup": mean_new_name})

    fig.update_layout(
        title=dict(
            x=0.5,
            y=0.95,
            text=f"Cities with unusual {drug} consumption during the week"
                 f"<br><sup>Compared to the average weekly use of {drug} in 86 European cities</sup>",
            font=dict(size=20)
        ),
        annotations=[dict(
            x=1.2,
            y=-0.15,    #Trying a negative number makes the caption disappear - I'd like the caption to be below the map
            xref='paper',
            yref='paper',
            text='Source:<a href="https://www.emcdda.europa.eu/publications/html/pods/waste-water-analysis_en#wastewaterData">\
                EMCDDA</a>',
            showarrow=False
        )]

    )

    fig.show()


if __name__ == "__main__":
    plot_top_weird_cities(df, "MDMA", 4)
