# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 16:55:10 2014

@author: babou
"""

import Adafruit_DHT

sensor = Adafruit_DHT.DHT11

# connected to pin 23
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
else:
        print 'Failed to get reading. Try again!'