import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('ww-data-long-2023-05-02.csv')
cities= pd.read_csv("ww-sites-2023-05-02.csv")
# remove rows with NaN values
df = df.dropna()
df=df[df["Daily mean"]!=0]
df=df[df["Year"]==2022]

df= df.merge(cities,on="City")

# Data normalization
days = ["Monday" ,"Tuesday" , "Wednesday" , "Thursday" , "Friday" , "Saturday" , "Sunday"]
days_norm = [f"{day}_norm" for day in days]
df["Daily mean"]= df["Daily mean"]/df["Population"]
for day in days:
    df[day] =df[day]/df["Population"]

    df[f"{day}_norm"] =np.where(df["Daily mean"]!=0, df[day] / df["Daily mean"],1)



# Creating plot
mean_day = df.groupby(["Metabolite"])[days_norm].mean()


mean_day=mean_day.reset_index()
mean_day= mean_day.rename(columns={col_name:col_name[:-5] for col_name in mean_day.columns[1:]})
mean_day = mean_day.rename(columns={"Metabolite": "Drug"})
mean_day=mean_day.melt(id_vars="Drug", value_vars=mean_day.columns[1:], value_name="Normalized drug consumption", var_name="Day of the week")
fig = px.line(mean_day, x="Day of the week", y="Normalized drug consumption", color='Drug', width=1000, height=630)
fig.update_layout(
    title_text='EU drug consumption over the week in 2022 <br><sup>By analysing traces of metabolites in wastewater of 86 European cities </sup>',
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

fig.show()
fig.write_html("plot_eu_drugs_weekly_trends.html")