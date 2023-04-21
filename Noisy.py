# https://pythonqwt.readthedocs.io
#
# We are using PyQt6, even though the examples
# use qtpy (which is just a wrapper for
# PyQt and others)
#
# pip install PyQt6
# pip install PythonQwt

from PyQt6 import QtCore, QtGui, QtWidgets
from qwt import *
import numpy as np
import math

# Global declarations
plot = None
noiseLabel = None
itLabel = None
noiseAmp = 0
nPeriods = 5
nPoints = 1000
iteration = 0

def buttonReleased():
    global noiseAmp
    # will be 0.0 - 1.0
    noiseAmp = np.random.random()
    noiseLabel.setText(f'Noise: {noiseAmp: 0.2f}')
    plot.setAxisScale(QwtPlot.yLeft, -1-noiseAmp, 1+noiseAmp)


def plot_sinus():
    global plot
    global iteration

    # clear the plot
    plot.detachItems()
    
    # Create two curves and attach them to plot
    x = np.linspace(-nPeriods*math.pi, nPeriods*math.pi, nPoints)
    cos = np.cos(x)
    sin = np.sin(x)
    sin = [x + (np.random.random()-0.5)*noiseAmp for x in sin]
    cos = [x + (np.random.random()-0.5)*noiseAmp for x in cos]
    QwtPlotCurve.make(x, cos, "Cos", plot, linecolor="red", antialiased=True)
    QwtPlotCurve.make(x, sin, "Sin", plot, linecolor="blue", antialiased=True)
    plot.replot()

    # Update iteration count
    iteration += 1
    itLabel.setText(f'Iteration: {iteration: 010d}')

def timeout():
    plot_sinus()

app = QtWidgets.QApplication([])

# Create main window
mainWindow = QtWidgets.QWidget()
vlayout = QtWidgets.QVBoxLayout(mainWindow)
mainWindow.setLayout(vlayout)
mainWindow.resize(1000, 300)
mainWindow.show()

# Top widgets
button = QtWidgets.QPushButton('Push Me', mainWindow)
button.released.connect(buttonReleased)

noiseLabel = QtWidgets.QLabel('0.00')
itLabel = QtWidgets.QLabel('Iteration: 0')
spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

hlayout = QtWidgets.QHBoxLayout()
hlayout.addWidget(button)
hlayout.addWidget(noiseLabel)
hlayout.addWidget(itLabel)
hlayout.addItem(spacer)

# Plot widget
plot = QwtPlot("Noisy I&Q", mainWindow)
plot.insertLegend(QwtLegend(), QwtPlot.BottomLegend)
plot.setAxisScale(QwtPlot.yLeft, -1-noiseAmp, 1+noiseAmp)
plot.setAxisScale(QwtPlot.xBottom, -nPeriods*math.pi, nPeriods*math.pi)

vlayout.addLayout(hlayout)
vlayout.addWidget(plot)

# Add timers
timer1 = QtCore.QTimer()
timer1.timeout.connect(timeout)
timer1.start(1)
timer2 = QtCore.QTimer()
timer2.timeout.connect(buttonReleased)
timer2.start(2000)

# Run the event loop
app.exec_()
