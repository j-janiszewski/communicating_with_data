import pandas as pd
import plotly.graph_objects as go
from PIL import Image


def plot_best_managers():
    df = pd.read_csv('data/manager_value_increase_all.csv')
    managers_list = [
        'Pep Guardiola',
        'Carlo Ancelotti',
        'Unai Emery',
        'Arsène Wenger',
        # 'Jürgen Klopp',
        'José Mourinho',
        'Frank de Boer'
    ]
    df = df[df['manager'].isin(managers_list)]
    df = df.sort_values(by='value_increase', ascending=False)
    print(df.head(10))

    fig = go.Figure()
    # add each manager as a bar plot to the figure
    for i, manager in enumerate(df['manager']):
        print(manager)
        # instead of a bar plot, show an image of the manager
        img = Image.open(f"managers/{manager}.png")
        fig.add_layout_image(
            source=img,
            xref="x",
            yref="y",
            x=i,
            y=df.loc[df['manager'] == manager, 'value_increase'].values[0],
            sizex=0.8,
            sizey=df.loc[df['manager'] == manager, 'value_increase'].values[0],
            sizing="stretch"
        )

    fig.update_layout(
        # no x axis
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        # no y axis
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        # white background
        plot_bgcolor='rgba(0,0,0,0)',
        # title
        title="Wait for the right moment to join the superstar manager<br>"
              "<sup>Comparing three managers with highest value increase, "
              "with three of the most famous managers</sup>",
        title_font_size=30,
        title_font_family="Arial",
        title_font_color="black",
        xaxis_range=[-0.5, len(df['manager']) + 0.5],
        margin=dict(l=30, r=30, t=80, b=50),
    )
    x_text_positions = [
        0.35,
        1.38,
        2.55,
        3.45,
        4.4,
        5.35,
    ]

    # add annotations for each manager
    annotations = []
    for i, manager in enumerate(df['manager']):
        text = f"{manager.split(' ')[0]}<br>{manager.split(' ')[1]}" \
            if len(manager.split(' ')) == 2 \
            else f"{manager.split(' ')[0]} {manager.split(' ')[1]}<br>{manager.split(' ')[2]}"
        annotations.append(dict(xref='x', yref='y',
                                x=x_text_positions[i], y=-0.4,
                                text=text,
                                font=dict(family='Arial', size=16, color='black'),
                                xanchor='center',
                                showarrow=False))

        annotations.append(dict(xref='x', yref='y',
                                x=x_text_positions[i], y=df.loc[df['manager'] == manager, 'value_increase'].values[0] + 0.2,
                                text=f"{round(df.loc[df['manager'] == manager, 'value_increase'].values[0], 2)}",
                                font=dict(family='Arial', size=16, color='black'),
                                showarrow=False))

    # add another annotation for the top 3 managers
    annotations.append(dict(xref='x', yref='y',
                            x=1.5, y=-1,
                            text='Managers with the highest value increase',
                            font=dict(family='Arial', size=20, color='black'),
                            xanchor='center',
                            showarrow=False))
    # add another annotation for the most famous four managers
    annotations.append(dict(xref='x', yref='y',
                            x=4.5, y=-1,
                            text='Most famous and successful managers',
                            font=dict(family='Arial', size=20, color='black'),
                            xanchor='center',
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    # fig.show()
    return fig


if __name__ == '__main__':
    plot_best_managers()
