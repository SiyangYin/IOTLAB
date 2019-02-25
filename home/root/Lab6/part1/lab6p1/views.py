# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import Image
import mraa
from time import sleep
from math import log
import numpy

import sys
sys.path.append('/../../pygooglechart')

from pygooglechart import SimpleLineChart
from pygooglechart import Axis

from threading import Thread

button_pin = 4
button = mraa.Gpio(button_pin)
button.dir(mraa.DIR_IN)
tempSensor = mraa.Aio(1)

B = 4275.0
R0 = 100000.0

def get_temp(value):
    global B
    global R0

    R = 1023.0/value - 1.0
    R *= R0
    temp = 1.0 / (log(R / R0)/B + 1.0/298.15) - 273.15
    return temp

data = []
def make_chart(data):
    chart = SimpleLineChart(250,100)
    chart.set_legend(['TEMPERATURE'])
    index = chart.set_axis_range(Axis.LEFT, 0, 40)
    chart.set_axis_style(index, colour='202020', font_size = 10)
    #chart.set_axis_positions(index, [50])
    chart.add_data(data)

    return chart.get_url()

def index(request):

    images = make_chart(data)
    return render(request, "index.html", {'images': images})
    

def thread():
    global data
    global tempSensor
    while True:
        temp = get_temp(tempSensor.read())
        data.append(temp)
        sleep(1)

thread = Thread( target=thread )
thread.start()


    
    #return HttpResponse("Hello, world. You're at the polls index.")
