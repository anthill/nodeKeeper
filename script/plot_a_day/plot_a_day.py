# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 15:35:57 2014

@author: babou
"""
import plotly.plotly as py  
import plotly.tools as tls   
from plotly.graph_objs import *
import datetime 
import time
import pandas as pd
import json


try:
    with open("dump.json", "r") as dump:
        past_data = json.loads(dump.read())
except:
    print "No past data"
    past_data = {"x": [], "y1": [], "y2": [], "y3": [], "y4": []}
    
df = pd.DataFrame(past_data)
df = df[df.x >= "2014-11-26 08:30:00.000000"]
df = df[df.x <= "2014-11-26 23:30:00.000000"]
df['x'] = pd.to_datetime(df['x'])
df.set_index('x', inplace=True)
df = df.resample('10min', how='mean', fill_method='bfill')
df.reset_index(inplace=True)

trace1 = Scatter(
    x=df["x"],
    y=df["y1"],
    mode='lines+markers',
    name='Total devices',
    marker=Marker(
        line=Line(
            color='rgb(255, 255, 255)',
            width=1
        )
    ),
    line=Line(
        color='rgba(31, 119, 180, 0.5)',
        shape='spline',
        smoothing=1
    ),
    opacity=1
)

trace2 = Scatter(
    x=df["x"],
    y=df["y2"],
    mode='lines+markers',
    name='Apple devices',
    marker=Marker(
        line=Line(
            color='rgb(255, 255, 255)',
            width=1
        )
    ),
    line=Line(
        color='rgba(255, 127, 14, 0.5)',
        shape='spline',
        smoothing=1
    ),
    opacity=1
)

trace3 = Scatter(
    x=df["x"],
    y=df["y3"],
    mode='lines+markers',
    name='Other devices',
    marker=Marker(
        line=Line(
            color='rgb(255, 255, 255)',
            width=1
        )
    ),
    line=Line(
        color='rgba(44, 160, 44, 0.5)',
        shape='spline',
        smoothing=1
    ),
    opacity=1
)

trace4 = Scatter(
    x=df["x"],
    y=df["y4"],
    mode='lines+markers',
    name='Detected faces',
    marker=Marker(
        line=Line(
            color='rgb(255, 255, 255)',
            width=1
        )
    ),
    line=Line(
        color='rgba(214, 39, 40, 0.5)',
        shape='spline',
        smoothing=1
    ),
    opacity=1
)

data = Data([trace1, trace2, trace3, trace4])
layout = Layout(title="November 26th's affluence")
fig = Figure(data=data, layout=layout)
unique_url = py.plot(fig, filename="November 26th's affluence")
