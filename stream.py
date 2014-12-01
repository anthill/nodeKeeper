# -*- coding: utf-8 -*-
import plotly.plotly as py  
import plotly.tools as tls   
from plotly.graph_objs import *
import datetime 
import time
import json
import argparse
import pandas as pd
from sniff import count_devices
from faceMatch import initFaceRecog, snapAndAnalyse

# parse command line args

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--interface", required = True, help = "From which interface ar you connected.")
ap.add_argument("-s", "--server", required = True, help = "What server should be used.")
ap.add_argument("-r", "--remove", default="", required = False, help = "Devices to ignore seaprated by ; eg: 'Hewlett Packard;FREEBOX SA'")
args = vars(ap.parse_args())

# init hardware
[camera, node_cascade] = initFaceRecog()

# check for past data stored in a file
try:
    with open("data/dump.json", "r") as dump:
        past_data = json.loads(dump.read())
except:
    print "No past data"
    past_data = {"x": [], "y1": [], "y2": [], "y3": [], "y4": []}

# Max point for Plotly
nbr_point = 500

#df = pd.DataFrame(past_data)
#df = df.tail(nbr_point)

# init plotly stream
stream_ids = tls.get_credentials_file()['stream_ids']
trace1 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    name='Total devices',
    stream=Stream(token=stream_ids[0], maxpoints=nbr_point),
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
    x=[],
    y=[],
    mode='lines+markers',
    name='Apple devices',
    stream=Stream(token=stream_ids[1], maxpoints=nbr_point),
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
    x=[],
    y=[],
    mode='lines+markers',
    name='Other devices',
    stream=Stream(token=stream_ids[2], maxpoints=nbr_point),
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
    x=[],
    y=[],
    mode='lines+markers',
    name='Detected faces',
    stream=Stream(token=stream_ids[3], maxpoints=nbr_point),
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
layout = Layout(title='Affluence')
fig = Figure(data=data, layout=layout)
unique_url = py.plot(fig, filename='LeNode', fileopt="extend")
s1 = py.Stream(stream_ids[0])
s1.open()
s2 = py.Stream(stream_ids[1])
s2.open()
s3 = py.Stream(stream_ids[2])
s3.open()
s4 = py.Stream(stream_ids[3])
s4.open()

 
# stream data
    
x = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S.%f')
res = count_devices(args["interface"], args["server"], args["remove"].split(";"))
try:
    faces = snapAndAnalyse(camera, node_cascade)
except Exception, e:
    print "Error in snapAndAnalyse"
    print e
    faces = 0

total = sum(res.values())
apple = sum(map(lambda x: res[x], filter(lambda x: "apple" in x.lower() , res.keys())))
others = sum(map(lambda x: res[x], filter(lambda x: "apple" not in x.lower() , res.keys())))

past_data["x"] += [x]
past_data["y1"] += [total]
past_data["y2"] += [apple]
past_data["y3"] += [others]
past_data["y4"] += [faces]

s1.write(dict(x=x, y=total))  
s2.write(dict(x=x, y=apple))  
s3.write(dict(x=x, y=others))  
s4.write(dict(x=x, y=faces))  

with open("data/dump.json", "w") as dump:
    dump.write(json.dumps(past_data))