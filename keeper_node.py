# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 11:01:58 2014

@author: babou
"""

import cv2
import pandas as pd
import time
import picamera
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

# init Cam
camera = picamera.PiCamera()
camera.vflip = True

# Init Model
node_cascade = cv2.CascadeClassifier('model/cascade.xml')

# Init Steam
stream_ids = tls.get_credentials_file()['stream_ids']


# Fonction
##########

def cam_photo():
    camera.start_preview()
    time.sleep(5)
    timecam = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
    camera.capture('/home/pi/keeper_of_node/image_test/' + '%s' %(timecam))
    time.sleep(115)
    camera.stop_preview()
    
def analyse_photo():
    img = cv2.imread('Image/*.jpg')
    resized_image = cv2.resize(img, (640, 480))
    nodes = node_cascade.detectMultiScale(resized_image)
    return(len(nodes))

# Steam Attribut
################

stream = Stream(
    #token=stream_ids,  # (!) link stream id to 'token' key
    maxpoints=80      # (!) keep a max of 80 pts on screen
)

# Initialize trace of streaming plot by embedding the unique stream_id
trace1 = Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    name='Nbr nodeur',
    line=Line(opacity=0.8),  # reduce opacity
    marker=Marker(size=6),
    stream=Stream(token=stream_ids[0])        # (!) embed stream id, 1 per trace
)

data = Data([trace1])

# Add title to layout object
layout = Layout(title="Node's Keeper")

# Make a figure object
fig = Figure(data=data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename="Node's Keeper")

# (@) Make instance of the Stream link object, 
#     with same stream id as Stream id object
s1 = py.Stream(stream_ids[0])

# (@) Open the stream
s1.open()

i = 0
# Loop
while  i < 10: #true:
    try:
        cam_photo()
        # Current time on x-axis, len of nordeur on y-axis
        x=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        y = analyse_photo()
        i += 1
        s1.write(dict(x=x,y=y))
    
    except Exception, e:
        print "Error..."
        print e
        s1.close()
    
