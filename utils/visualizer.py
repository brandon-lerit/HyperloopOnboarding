from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from widgets.pod import Pod
from widgets import *
import pyqtgraph as pg


class Visualizer(QWidget):
    def __init__(self, *args, **kwargs):
        super(Visualizer, self).__init__()

        hbox = QHBoxLayout(self)
        
        # Assuming you have a Pod widget (replace Pod() with your actual Pod widget)
        pod = Pod()
        hbox.addWidget(pod)

        # Create a PlotWidget for live plotting
        self.plot_widget = pg.PlotWidget()
        hbox.addWidget(self.plot_widget)

        self.setLayout(hbox)

        # Initialize the plot with an empty curve
        self.curve = self.plot_widget.plot()

    def update_plot(self, value):
        # Update the plot with a new data point
        self.curve.setData(y=[value])
