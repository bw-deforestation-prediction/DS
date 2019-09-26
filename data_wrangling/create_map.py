import plotly
import pandas as pd
from data import df0, predictionDF

slider = []
for year in df0['Year'].unique():
    dfYearX = df0[df0['Year'] == year]
    yearPlot = dict(
        type='choropleth',
        locations=dfYearX['Country Code'],
        z=dfYearX['Forest Land Percent'],
        colorscale=[[0, 'yellow'], [1, 'green']],
        colorbar={'title': '%'},
        zmin=0,
        zmax=100
    )
    slider.append(yearPlot)

steps = []
for i in range(len(slider)):
    step = dict(method='restyle',
                args=['visible', [False] * len(slider)],
                label='Year ' + str(i + 1990))
    step['args'][1][i] = True
    steps.append(step)

sliders = [dict(steps=steps)]

layout = dict(
    sliders=sliders,
    geo=dict(showlakes=True,
             lakecolor='blue',
             showocean=True,
             oceancolor='#1A1AFF',
             projection=dict(type='natural earth')
             ),
)

fig = dict(data=slider, layout=layout)

plotly.offline.iplot(fig)
plotly.offline.plot(fig, filename='map.html', auto_open=False)


slider2 = []
for year in predictionDF['Year'].unique():
    dfYearX = predictionDF[predictionDF['Year'] == year]
    yearPlot = dict(
        type='choropleth',
        locations=dfYearX['Country Code'],
        z=dfYearX['Forest Land Percent'],
        colorscale=[[0, 'yellow'], [1, 'green']],
        colorbar={'title': '%'},
        zmin=0,
        zmax=100
    )
    slider2.append(yearPlot)

steps2 = []
for i in range(len(slider2)):
    step = dict(method='restyle',
                args=['visible', [False] * len(slider2)],
                label='Year ' + str(i + 2017))
    step['args'][1][i] = True
    steps2.append(step)

sliders2 = [dict(steps=steps2)]

layout2 = dict(
    sliders=sliders2,
    geo=dict(showlakes=True,
             lakecolor='blue',
             showocean=True,
             oceancolor='#1A1AFF',
             projection=dict(type='natural earth')
             ),
)

fig2 = dict(data=slider2, layout=layout2)

plotly.offline.iplot(fig2)
plotly.offline.plot(fig2, filename='prediction_map.html', auto_open=False)
