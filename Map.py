# https://pythonqwt.readthedocs.io
#
# # pip install PyQt6
# pip install PythonQwt

from PyQt6 import QtCore, QtGui, QtWidgets
from qwt import *
import sys
import json

def getData(filePath:str)->None:
    """Return a tupple: (x[], y[], alt[], time[])"""
    allData = json.load(open(filePath, 'r'))
    xraw = [v['iridium']['lon'] for v in allData]
    yraw = [v['iridium']['lat'] for v in allData]
    altraw = [v['iridium']['alt'] for v in allData]
    timeraw = [v['dateSent'] for v in allData]

    x = []
    y = []
    alt = []
    time = []
    for i in range(len(xraw)):
        if xraw[i] != 0 and yraw[i] != 0:
            x.append(xraw[i])
            y.append(yraw[i])
            alt.append(altraw[i])
            time.append(timeraw[i])
        else:
            print(f'Bad data in record {i}: {timeraw[i]} {xraw[i]}, {yraw[i]}, {altraw[i]}')

    return (x, y, alt, time)

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} data_file')
    sys.exit(1)

# read the data
(x, y, alt, time) = getData(sys.argv[1])

# create app and main window
app = QtWidgets.QApplication([])
mainWindow = QtWidgets.QWidget()
vlayout = QtWidgets.QVBoxLayout(mainWindow)
mainWindow.setLayout(vlayout)
mainWindow.resize(800, 800)
mainWindow.show()

# Add x-y plot
plot = QwtPlot("Map", mainWindow)
plot.insertLegend(QwtLegend(), QwtPlot.BottomLegend)
QwtPlotCurve.make(x, y, "Path", plot, linecolor="red", linewidth=3, antialiased=True)
vlayout.addWidget(plot)

# Run the event loop
app.exec_()
