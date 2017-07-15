# -*- coding:utf-8 -*-
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderPDF

from urllib import urlopen

URL = 'http://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt'
COMMON_CHARS = '#:'

drawing = Drawing(400, 200)
data = []

for line in urlopen(URL).readlines():
    if not line.isspace() and not line[0] in COMMON_CHARS:
        data.append([float(n) for n in line.split()])

pred = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]
times = [row[0]+row[1]/12.0 for row in data]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.width = 300
lp.height = 150
lp.data = [zip(times, pred), zip(times, high), zip(times, low)]

lp.lines[0].strokeColor = colors.red
lp.lines[1].strokeColor = colors.blue
lp.lines[2].strokeColor = colors.green

drawing.add(lp)
drawing.add(String(250, 170, 'Sunspots', fontSize=14, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'report2.pdf', 'Sunspots')