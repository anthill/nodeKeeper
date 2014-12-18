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
from temperature_humidity import meteo_node

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
    with open("/home/pi/nodeKeeper/data/dump.json", "r") as dump:
        past_data = json.loads(dump.read())
except:
    print "No past data"
    past_data = {"x": [], "y1": [], "y2": [], "y3": [], "y4": [], "y5": [], "y6": []}

# Max point for Plotly
nbr_point = 263

#df = pd.DataFrame(past_data)
#df = df.tail(nbr_point)

# init plotly stream
stream_ids = tls.get_credentials_file()['stream_ids']

# TRACING
#########

# Total device
trace1 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    name='Total devices',
    yaxis='y',
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

# Apple device
trace2 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    name='Apple devices',
    yaxis='y',
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

# Others device
trace3 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    name='Other devices',
    yaxis='y',
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

# Face detect
trace4 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    name='Detected faces',
    yaxis='y',
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

# Humidity
trace5 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    name='Humidity',
    yaxis='y2',
    stream=Stream(token=stream_ids[4], maxpoints=nbr_point),
    marker=Marker(
        line=Line(
            color='rgb(255, 255, 255)',
            width=1
        )
    ),
    line=Line(
        color='rgba(148, 103, 189, 0.5)',
        shape='spline',
        smoothing=1
    ),
    opacity=1
)

# Temperature
trace6 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    name='Temperature',
    yaxis='y3',
    stream=Stream(token=stream_ids[5], maxpoints=nbr_point),
    marker=Marker(
        line=Line(
            color='rgb(255, 255, 255)',
            width=1
        )
    ),
    line=Line(
        color='rgba(23, 190, 207, 0.5)',
        shape='spline',
        smoothing=1
    ),
    opacity=1
)


data = Data([trace1, trace2, trace3, trace4, trace5, trace6])

layout = Layout(title='Affluence',
                yaxis=YAxis(
                    domain=[0.4, 1]),
                yaxis2=YAxis(
                    domain=[0, 0.3],
                    title='Humidity %RH',
                    titlefont=Font(
                        color='rgba(148, 103, 189, 0.9)'),
                    tickfont=Font(
                        color='rgba(148, 103, 189, 0.9)')
                        ),
                yaxis3=YAxis(
                    domain=[0, 0.3],
                    title='Temperature °C',
                    overlaying='y2',
                    anchor='x',
                    side='right',
                    titlefont=Font(
                        color='rgba(23, 190, 207, 0.9)'),
                    tickfont=Font(
                        color='rgba(23, 190, 207, 0.9)')
                        )
)


fig = Figure(data=data, layout=layout)
unique_url = py.plot(fig, filename='LeNode', fileopt="extend")

s1 = py.Stream(stream_ids[0]) # Total
s1.open()
s2 = py.Stream(stream_ids[1]) # Apple 
s2.open()
s3 = py.Stream(stream_ids[2]) # Others
s3.open()
s4 = py.Stream(stream_ids[3]) # Faces
s4.open()
s5 = py.Stream(stream_ids[4]) # Faces
s5.open()
s6 = py.Stream(stream_ids[5]) # Faces
s6.open()

# stream data
    
x = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S.%f')
humidity, temperature = meteo_node()

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
try:
    past_data["y5"]
    past_data["y6"]
except:
    past_data["y5"] = []
    past_data["y6"] = []
    
past_data["y5"] += [humidity]
past_data["y6"] += [temperature]

# Testing
#print str(x) + ' ' + str(total) + ' ' + str(apple) + ' ' + str(others)  + ' ' + str(faces) + ' ' + str(humidity) + ' ' + str(temperature)

s1.write(dict(x=x, y=total))  
s2.write(dict(x=x, y=apple))  
s3.write(dict(x=x, y=others))  
s4.write(dict(x=x, y=faces))
s5.write(dict(x=x, y=humidity))
s6.write(dict(x=x, y=temperature))  

with open("/home/pi/nodeKeeper/data/dump.json", "w") as dump:
    dump.write(json.dumps(past_data))
    
s1.close() # Total
s2.close() # Apple
s3.close() # Others
s4.close() # Faces
s5.close() # Humididy
s6.close() # Temperature