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
            self.arduino = serial.Serial('COM3', 9600)  
        except serial.SerialException as e:
            print(f"Error opening Arduino port: {e}")
            self.arduino = None

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
        if self.arduino and self.arduino.isOpen():
            try:
                data = self.arduino.readline().decode().strip()
                json_data = json.loads(data)

                current_page_index = self.stacked_widget.currentIndex()
                current_page_widget = self.stacked_widget.currentWidget()

                if "Temperature" in current_page_widget.windowTitle():
                    # Determine the temperature unit based on the current page's title
                    temperature_unit = current_page_widget.windowTitle().split()[-1]

                    if temperature_unit == "(C)":
                        self.updateTemperatureGraph(current_page_widget, json_data["temperature_C"])
                    elif temperature_unit == "(F)":
                        self.updateTemperatureGraph(current_page_widget, json_data["temperature_F"])
                    elif temperature_unit == "(K)":
                        self.updateTemperatureGraph(current_page_widget, json_data["temperature_K"])
                elif "Distance" in current_page_widget.windowTitle():
                    self.updateDistanceGraph(current_page_widget, json_data["distance"])

            except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as e:
                print(f"Error reading data from Arduino: {e}")

    def updateTemperatureGraph(self, page, value):
        temperature_graph = page.findChild(pg.PlotWidget)

        if temperature_graph:
            # Update the temperature graph with the new value
            pen = pg.mkPen(width=2)
            temperature_graph.plot([value], pen=pen, symbol='o', symbolSize=5)

    def updateDistanceGraph(self, page, value):
        distance_graph = page.findChild(pg.PlotWidget)

        if distance_graph:
            # Update the distance graph with the new value
            pen = pg.mkPen(width=2)
            distance_graph.plot([value], pen=pen, symbol='o', symbolSize=5)

    def dimensions(self):
        return self.width, self.height