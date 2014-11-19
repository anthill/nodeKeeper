# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 17:56:17 2014

@author: babou
"""

import numpy as np
import cv2
import pylab as plt
from pylab import rcParams
from matplotlib.patches import Rectangle

# run prepare.py to create the training set


# to create a vec file from a bunch of samples:
# opencv_createsamples -info info.dat -num 200 -w 24 -h 24 -vec cars.vec

# bg.dat contains the path to negative sample (background only)
# to train:
# opencv_traincascade -data models -vec cars.vec -bg bg.dat -numStages 15 -nsplits 2 -minhitrate 0.999 -maxfalsealarm 0.5 -numPos 200 -numNeg 900 -w 24 -h 24

node_cascade = cv2.CascadeClassifier('model/test29/cascade.xml')
rcParams['figure.figsize'] = 12, 8
img = cv2.imread('Image/Node_normal13-2.jpg')
resized_image = cv2.resize(img, (640, 480))

plt.imshow(resized_image)
currentAxis = plt.gca()

xx,yy = [],[]
nodes = node_cascade.detectMultiScale(resized_image)
for (x,y,w,h) in nodes:
	xx += [x+w/2.]
	yy += [y+h/2.]
	print ((x,y),(x+w,y+h))
	coords = (x, y), w, h
	currentAxis.add_patch(Rectangle(*coords, fill=True, alpha=0.2, color='#00FF00', edgecolor='#00FF00', linewidth=3))

plt.scatter(xx,yy, color="r")
plt.savefig('temp.jpg')
plt.show()
print "Nbr de positif :" + str(len(nodes))