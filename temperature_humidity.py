# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 16:55:10 2014

@author: babou
"""

import Adafruit_DHT



def meteo_node():
    
    sensor = Adafruit_DHT.DHT11
    
    # connected to pin 23
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    return (humidity, temperature)