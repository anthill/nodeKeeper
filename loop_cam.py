# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 17:55:13 2014

@author: Babou
"""

import time
import picamera


camera = picamera.PiCamera()
camera.vflip = True
i = 0

while i < 15:
    camera.start_preview()
    time.sleep(5)
    timecam = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
    camera.capture('/home/pi/keeper_of_node/image/' + '%s' %(timecam))
    time.sleep(1800)
    camera.stop_preview()
    i+=1