from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from widgets.plot_buttons import PlotButtons
from widgets.proximity_sensors import ProximitySensor
from widgets import *
from constants import *
import pyqtgraph as pg


class Body(QWidget):
    def __init__(self, *args, **kwargs):
        super(Body, self).__init__()
        self.width = args[0]
        self.height = args[1]
        hbox = QHBoxLayout(self)

        sshFile = "utils/body.css"
        with open(sshFile, "r") as fh:
            qstr = str(fh.read())

        home = QSplitter(Qt.Vertical)

        # Create temperature and distance widgets

        temperature = QLabel("Temperature Widget")
        distance = QLabel("Distance Widget")

        # Temporary graph setup
        self.temporary_graph = pg.PlotWidget()
        self.temporary_graph.resize(int(self.width), int(self.height / 4))

        # Add widgets to the layout
        home.addWidget(self.temporary_graph)
        home.addWidget(temperature)
        home.addWidget(distance)

        hbox.addWidget(home)
        self.setLayout(hbox)
        self.setStyleSheet(qstr)

        self.timer = QTimer(self, timeout=self.update)
        self.timer.start(1000)

    def update(self):
        current_plot = self.plot_buttons.getCurrentPlot()
        pen = pg.mkPen(width=10)

        if (self.plot_buttons.getRescaleAxesFlag()):
            self.plot_buttons.setRescaleAxesFlag(False)
            x_axes = self.plot_buttons.getXAxesLimits()
            y_axes = self.plot_buttons.getYAxesLimits()
            self.temporary_graph.setXRange(x_axes[0], x_axes[1])
            self.temporary_graph.setYRange(y_axes[0], y_axes[1])

        if (self.plot_buttons.getPlotResetFlag()):
            # Reset the current plot
            self.current_plot_values[current_plot][0] = 0
            self.current_plot_values[current_plot][1] = 0
            self.current_plot_indices[current_plot] = 0
            self.x_data[current_plot] = [0]
            self.y_data[current_plot] = [0]
            self.plot_buttons.setPlotResetFlag(False)

        elif (self.plot_buttons.getChangedPlot()):
            # Reset the plot
            
            self.currentPlotIndex = self.plot_buttons.getCurrentPlot
            self.currentPlotName = self.plot_buttons.getCurrentPlotName
            
            self.temporary_graph.clear()
            # add another getter in plot_buttons to get index of new graph 
            # add another getter to get the name of the chaged graph 
            # add another getter to get the x and y axes (units) of the changed graph

            # Plot all the data for the new plot
            for i in range(len(self.x_data[current_plot])):
                self.temporary_graph.plot([self.x_data[current_plot][i]], [self.y_data[current_plot][i]],
                                          pen=pen, symbol='x', symbolSize=30)

            # Reset the changed plot flag
            self.plot_buttons.setChangedPlot(False)

        else:
            # Updated variables for the next data
            for i in range(NUM_PLOTS):
                # if statement for amount of time left
                self.x_data[i].append(self.current_plot_values[i][0])
                self.y_data[i].append(self.current_plot_values[i][1])
                self.current_plot_values[i][0] += PLOT_INCREMENTS[i]
                self.current_plot_values[i][1] += PLOT_INCREMENTS[i]

            # Get the current index
            currentIndex = self.current_plot_indices[current_plot]

            # Plot the current data point
            self.temporary_graph.plot([self.x_data[current_plot][currentIndex]], [self.y_data[current_plot][currentIndex]],
                                      pen=pen, symbol='x', symbolSize=30)

            # Update the indices for the next datapoint
            self.current_plot_indices[0] += 1
            self.current_plot_indices[1] += 1

    def dimensions(self):
        return self.width, self.height
