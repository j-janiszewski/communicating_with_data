import pandas as pd
import geopandas as gpd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go


def plot_leagues():
    # Read in the data
    df = pd.read_csv("data/league_value_increase_all.csv")

    geojson = gpd.read_file("data/europe.geojson")

    # print(geojson.head())

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations="country",
        color="value_increase",
        locationmode="ISO-3",
    )

    fig.update_geos(visible=True)

    fig.update_layout(
        title=dict(
            text="I know you like pasta, but baguettes ain't bad either<br>"
            "<sub>Italy is the worst eu country for value increase of young players, France, Denmark and England are best</sub>",
            x=0.05,
            font_size=26,
            font_family="Arial",
        ),
        geo=dict(
            bgcolor="#8ad6ff",
            lakecolor="#8ad6ff",
            projection_type="miller",
            scope="europe",
            # more zoom in
            lonaxis_range=[-15, 45],
            lataxis_range=[35, 62],
        ),
        margin=dict(l=0, r=0, t=70, b=0),
        width=900,
        height=600,
        coloraxis=dict(
            colorscale="viridis",
            cmin=df["value_increase"].min(),
            cmax=df["value_increase"].max(),
        ),
    )

    # fig.show()
    return fig


if __name__ == "__main__":
    plot_leagues()
