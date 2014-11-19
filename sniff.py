# -*- coding: utf-8 -*-
import subprocess
import plotly.plotly as py  
import plotly.tools as tls   
from plotly.graph_objs import *
import numpy as np
import datetime 
import time
import json
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--interface", required = True, help = "From which interface ar you connected.")
ap.add_argument("-s", "--server", required = True, help = "What server should be used.")
args = vars(ap.parse_args())



def count_devices(interface, server):
	cmd = ["sudo", "arp-scan", "--retry=8", "--ignoredups", "-I", interface, server + "/24"]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

	out, err = p.communicate()

	hosts = out.split("\n")[2:-4]

	devices = map(lambda x: x.split("\t")[-1], hosts)

	to_remove = ["Hewlett Packard", "FREEBOX SA"]

	devices = filter(lambda x: x not in to_remove, devices)
	counts  = {key: devices.count(key) for key in devices}

	return counts

# check for a file with the dump
try:
    with dump as open("data/dump.json", "r"):
        past_data = json.parse(dump.read())
except:
    print "No past data"
    past_data = {"x": [], "y1": [], "y2": [], "y3": []}

# init stream
stream_ids = tls.get_credentials_file()['stream_ids']
trace1 = Scatter(
    x=past_data["x"],
    y=past_data["y1"],
    mode='lines+markers',
    name='Total',
    line=Line(
        shape='hvh'
    ),
    stream=Stream(token=stream_ids[0], maxpoints=80)
)
trace2 = Scatter(
    x=past_data["x"],
    y=past_data["y2"],
    mode='lines+markers',
    name='Apple',
    line=Line(
        shape='hvh'
    ),
    stream=Stream(token=stream_ids[1], maxpoints=80)
)
trace3 = Scatter(
    x=past_data["x"],
    y=past_data["y2"],
    mode='lines+markers',
    name='Other',
    line=Line(
        shape='hvh'
    ),
    stream=Stream(token=stream_ids[2], maxpoints=80)
)
data = Data([trace1, trace2, trace3])
layout = Layout(title='Number of devices')
fig = Figure(data=data, layout=layout)
unique_url = py.plot(fig, filename='LeNode')
s1 = py.Stream(stream_ids[0])
s1.open()
s2 = py.Stream(stream_ids[1])
s2.open()
s3 = py.Stream(stream_ids[2])
s3.open()


 
# stream data

while True:
    
    x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    res = count_devices(args["interface"], args["server"])

    total = sum(res.values())
    apple = sum(map(lambda x: res[x], filter(lambda x: "apple" in x.lower() , res.keys())))
    others = sum(map(lambda x: res[x], filter(lambda x: "apple" not in x.lower() , res.keys())))

    past_data["x"] += x
    past_data["y1"] += apple
    past_data["y2"] += others
    with dump as open("data/dump.json", "w"):
        dump.write(json.dumps(dump))
    
    
    s1.write(dict(x=x, y=total))  
    s2.write(dict(x=x, y=apple))  
    s3.write(dict(x=x, y=others))  

    time.sleep(30)
    print x
    print res    

s.close() 


