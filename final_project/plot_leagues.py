import pandas as pd
import geopandas as gpd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go


def main():
    # Read in the data
    df = pd.read_csv('data/league_value_increase_all.csv')


    geojson = gpd.read_file('data/europe.geojson')

    print(geojson.head())

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations='country',
        color='value_increase',
        locationmode='ISO-3'
    )

    fig.update_geos(
        visible=True
    )

    fig.update_layout(
        title=dict(
            text='Go to France, not to Italy<br>'
                 '<sub>France, Denmark and England increase the '
                 'median value of young players most</sub>',
            x=0.05,
            font_size=22,
            xanchor='left',
        ),
        geo=dict(
            bgcolor='#8ad6ff',
            lakecolor='#8ad6ff',
            projection_type='miller',
            scope='europe',
            # more zoom in
            lonaxis_range=[-15, 45],
            lataxis_range=[35, 62]
        ),
        margin=dict(l=0, r=0, t=70, b=0),
        width=900,
        height=600,
        coloraxis=dict(
            colorscale='viridis',
            cmin=df['value_increase'].min(),
            cmax=df['value_increase'].max()
        )
    )

    # fig.show()
    return fig


if __name__ == '__main__':
    main()
