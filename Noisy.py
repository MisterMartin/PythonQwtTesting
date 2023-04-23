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

def doPlot():
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

def sliderChanged(val:int)->None:
    global noiseAmp
    # will be 0.0 - 1.0
    noiseAmp = val/100.0
    noiseLabel.setText(f'Noise: {noiseAmp: 0.2f}')
    plot.setAxisScale(QwtPlot.yLeft, -1-noiseAmp, 1+noiseAmp)

def timeout():
    doPlot()

app = QtWidgets.QApplication([])

# Create main window
mainWindow = QtWidgets.QWidget()
vlayout = QtWidgets.QVBoxLayout(mainWindow)
mainWindow.setLayout(vlayout)
mainWindow.resize(1000, 300)
mainWindow.show()

# Top widgets
hlayout = QtWidgets.QHBoxLayout()

slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
slider.setMinimum(0)
slider.setMaximum(100)
slider.setTickInterval(1)
slider.valueChanged.connect(sliderChanged)
hlayout.addWidget(slider)

noiseLabel = QtWidgets.QLabel('0.00')
hlayout.addWidget(noiseLabel)

itLabel = QtWidgets.QLabel('Iteration: 0')
hlayout.addWidget(itLabel)

spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
hlayout.addItem(spacer)

# Plot widget
plot = QwtPlot("Noisy I&Q", mainWindow)
plot.insertLegend(QwtLegend(), QwtPlot.BottomLegend)
plot.setAxisScale(QwtPlot.yLeft, -1-noiseAmp, 1+noiseAmp)
plot.setAxisScale(QwtPlot.xBottom, -nPeriods*math.pi, nPeriods*math.pi)

vlayout.addLayout(hlayout)
vlayout.addWidget(plot)

# Set imnitial noise value
sliderChanged(0)

# Add timer
timer = QtCore.QTimer()
timer.timeout.connect(timeout)
timer.start(1)

# Run the event loop
app.exec_()
