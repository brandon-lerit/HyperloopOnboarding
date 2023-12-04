from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from widgets.plot_buttons import PlotButtons
from widgets.proximity_sensors import ProximitySensor
from widgets import *
from constants import *
import pyqtgraph as pg
import serial
import json

class Body(QWidget):
    def __init__(self, *args, **kwargs):
        super(Body, self).__init__()
        self.width = args[0]
        self.height = args[1]

        # self.json_data = {}
        self.x = 0
        self.y = 0

        # Create a QStackedWidget to manage the different pages
        self.stacked_widget = QStackedWidget(self)

        # Create four different pages (widgets)
        self.page1 = self.createTemperaturePage("Temperature (C)", "Temperature (C)")
        self.page2 = self.createTemperaturePage("Temperature (F)", "Temperature (F)")
        self.page3 = self.createTemperaturePage("Temperature (K)", "Temperature (K)")
        self.page4 = self.createDistancePage()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)
        self.stacked_widget.addWidget(self.page4)

        # Set up the layout
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.stacked_widget)

        # Add buttons to switch between pages
        self.button_page1 = QPushButton("Temperature (C)", self)
        self.button_page1.clicked.connect(self.switchToPage1)
        vbox.addWidget(self.button_page1)

        self.button_page2 = QPushButton("Temperature (F)", self)
        self.button_page2.clicked.connect(self.switchToPage2)
        vbox.addWidget(self.button_page2)

        self.button_page3 = QPushButton("Temperature (K)", self)
        self.button_page3.clicked.connect(self.switchToPage3)
        vbox.addWidget(self.button_page3)

        self.button_page4 = QPushButton("Distance (cm)", self)
        self.button_page4.clicked.connect(self.switchToPage4)
        vbox.addWidget(self.button_page4)

        self.setLayout(vbox)

        self.button_page1.setStyleSheet("background-color: lightcoral;")
        self.button_page2.setStyleSheet("background-color: lightcoral;")
        self.button_page3.setStyleSheet("background-color: lightcoral;")
        self.button_page4.setStyleSheet("background-color: lightcoral;")

        # Start with the first page
        self.stacked_widget.setCurrentIndex(0)

        # Set up the timer for updating data
        self.timer = QTimer(self, timeout=self.update)
        self.timer.start(1000)

        # Serial communication with Arduino
        try:
            self.arduino = serial.Serial('COM12', 9600)  
        except serial.SerialException as e:
            print(f"Error opening Arduino port: {e}")
            self.arduino = None

        self.current_time = QTime()

    def createTemperaturePage(self, title, temperature):
        page = QWidget()

        # Temperature specific setup
        temperature_label = QLabel(title)
        font = QFont()
        font.setPointSize(18)
        temperature_label.setFont(font)
        temperature_graph = pg.PlotWidget()
        temperature_graph.setBackground('#ffffff')
        temperature_graph.setLabel('left', temperature)
        temperature_graph.setLabel('bottom', 'Time (s)')

        temperature_graph.setRange(xRange=[0, 10], yRange=[0, 10])

        # Add widgets to the layout
        vbox = QVBoxLayout(page)
        vbox.addWidget(temperature_label)
        vbox.addWidget(temperature_graph)

        return page

    def createDistancePage(self):
        page = QWidget()

        # Distance specific setup
        distance_label = QLabel("Distance (cm)")
        font = QFont()
        font.setPointSize(18)
        distance_label.setFont(font)
        distance_graph = pg.PlotWidget()
        distance_graph.setBackground('#ffffff')
        distance_graph.setLabel('left', 'Distance (cm)')
        distance_graph.setLabel('bottom', 'Time (s)')

        distance_graph.setRange(xRange=[0, 10], yRange=[0, 10])

        # Add widgets to the layout
        vbox = QVBoxLayout(page)
        vbox.addWidget(distance_label)
        vbox.addWidget(distance_graph)

        return page

    def switchToPage1(self):
        self.stacked_widget.setCurrentIndex(0)

    def switchToPage2(self):
        self.stacked_widget.setCurrentIndex(1)

    def switchToPage3(self):
        self.stacked_widget.setCurrentIndex(2)

    def switchToPage4(self):
        self.stacked_widget.setCurrentIndex(3)

    def update(self):
        # Read data from Arduino or use dummy data
        if self.arduino and self.arduino.isOpen():
            data = self.arduino.readline().decode().strip()
            if not data:
                return  # Skip processing empty data
            try:
                json_data = json.loads(data)
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return  # Skip processing invalid JSON
        else:
            # Dummy data for testing without Arduino
            json_data = {"temperature_C": 25.0}

        # Calculate elapsed time in seconds
        current_time_seconds = self.current_time.elapsed() / 1000.0

        # Update the temperature graph with the new data
        self.updateGraph(self.stacked_widget.currentWidget(), json_data)

    def updateTemperatureGraph(self, page, value):
        temperature_graph = page.findChild(pg.PlotWidget)

        if temperature_graph:
            # Get the current data on the graph
            x_data, y_data = temperature_graph.listData()

            # Append the new value to the existing data
            x_data.append(x_data[-1] + 1 if x_data else 0)
            y_data.append(value)

            # Update the temperature graph with the new data
            pen = pg.mkPen(color='r', width=2)  # Adjust the color as needed
            temperature_graph.clear()  # Clear the existing plot
            temperature_graph.plot(x_data, y_data, pen=pen, symbol='o', symbolSize=5)

    def updateGraph(self, page, value):
        current_widget = self.stacked_widget.currentWidget()
        graph = current_widget.findChild(pg.PlotWidget)

        if graph:
        # Get the current data on the graph
            x_data, y_data = graph.listData()

        # Calculate elapsed time in seconds
            current_time_seconds = self.current_time.elapsed() / 1000.0

        # Append the new value to the existing data
            x_data.append(current_time_seconds)
            y_data.append(value)

        # Update the graph with the new data
            pen = pg.mkPen(color='r', width=2)  # Adjust the color as needed
            graph.plot(x_data, y_data, pen=pen, symbol='o', symbolSize=5)

    def updateDistanceGraph(self, page, value):
        distance_graph = page.findChild(pg.PlotWidget)

        if distance_graph:
            # Get the current data on the graph
            x_data, y_data = distance_graph.listData()

            # Append the new value to the existing data
            x_data.append(len(x_data))
            y_data.append(value)

            # Update the distance graph with the new data
            pen = pg.mkPen(width=2)
            distance_graph.plot(x_data, y_data, pen=pen, symbol='o', symbolSize=5)
    
    def closeEvent(self, event):
        if self.arduino and self.arduino.isOpen():
            self.arduino.close()
        event.accept()

    def dimensions(self):
        return self.width, self.height