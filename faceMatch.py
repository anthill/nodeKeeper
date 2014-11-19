# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 11:01:58 2014

@author: babou
"""

import cv2
import pandas as pd
import os
import glob
import time
import datetime
import picamera
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import matplotlib
# Force matplotlib to not use any Xwindows backend.
# to avoid an error : "no display name and no $DISPLAY environment variable"
matplotlib.use('Agg')
import pylab as plt
from pylab import rcParams
from matplotlib.patches import Rectangle


def initFaceRecog():

    # init Cam
    camera = picamera.PiCamera()
    camera.vflip = True

    # Init Model
    node_cascade = cv2.CascadeClassifier('script/cascade.xml')


def cam_photo():
    camera.start_preview()
    time.sleep(5)
    timecam = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
    camera.capture('image_test/' + '%s' %(timecam))
    time.sleep(115)
    camera.stop_preview()
    return(timecam)
    
def analyse_photo(filename):
    img = cv2.imread('image_test/' + filename)
    resized_image = cv2.resize(img, (640, 480))
    nodes = node_cascade.detectMultiScale(resized_image)
    return(len(nodes))

def create_photo_analyse(filename):
    img = cv2.imread('image_test/' + filename)
    resized_image = cv2.resize(img, (640, 480))
    plt.imshow(resized_image)
    currentAxis = plt.gca()
    nodes = node_cascade.detectMultiScale(resized_image)
    xx,yy = [],[]
    for (x,y,w,h) in nodes:
        xx += [x+w/2.]
        yy += [y+h/2.]
        coords = (x, y), w, h
        currentAxis.add_patch(Rectangle(*coords, fill=True, alpha=0.2, color='#00FF00', edgecolor='#00FF00', linewidth=3))
    
    plt.scatter(xx,yy, color="r")
    plt.savefig('image_analyse/' + filename)
    
def snapAndAnalyse():
    filename = cam_photo()
    result = analyse_photo(filename)
    os.remove('image_test/' + filename)
    return result
    
