import mraa
from time import sleep
from math import log
import numpy

import sys
sys.path.append('/../../pygooglechart')

from pygooglechart import SimpleLineChart
from pygooglechart import Axis

tempSensor = mraa.Aio(1)

B = 4275.0
R0 = 100000.0

def get_temp(value):
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

    # Print the chart URL
    print chart.get_url()

    # Download the chart
    chart.download('tempChart.png')
while (1):
    try:
        temp = get_temp(tempSensor.read())
        data.append(temp)
        make_chart(data)
        sleep(5)

    except KeyboardInterrupt:
        exit
