from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import sys
import serial
import json
from widgets import *
from utils.header import Header
from utils.body import Body
from utils.visualizer import Visualizer
from utils.FSM import FSM


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Hyperloop Onboarding GUI")

        hbox = QHBoxLayout(self)

        width = 1250
        height = 1500

        self.arduino = serial.Serial("COM12", 9600)

        header = Header(w=int(width), h=int(height))

        self.Stack = QStackedWidget(self)

        self.current_time = QTime()

        body = Body(int(width), int(height))
        visualizer = Visualizer()
        fsm = FSM(width, height)

        self.Stack.addWidget(body)
        self.Stack.addWidget(visualizer)
        self.Stack.addWidget(Body(width, height))
        self.Stack.addWidget(fsm)

        splitter4 = QSplitter(Qt.Vertical)
        splitter4.addWidget(header)

        splitter4.addWidget(self.Stack)
        splitter4.setSizes([50, 350])

        hbox.addWidget(splitter4)

        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setStyleSheet("background-color: #D3D3D3;")

        self.setGeometry(300, 300, width, height)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

        self.showFullScreen()

    def renderPage(self, i):
        self.Stack.setCurrentIndex(i)

    def update_plot(self):
        if self.arduino.isOpen():
            data = self.arduino.readline()
            # print(f"Raw data received from Arduino: {data}")

            # Decode the received data
            data_str = data.decode().strip()
            # print(f"Decoded data: {data_str}")

            # Load JSON data
            json_data = json.loads(data_str)
            # print(f"Parsed JSON data: {json_data}")

            # Extract the value you want to plot
            value = json_data.get("temperature_C", 0.0)  # Change "temperature_C" to the key you want
            # print(f"Extracted value for plotting: {value}")

            current_time = self.current_time.elapsed() / 1000.0  # Convert to seconds

            # Assuming you have a plot item in your Visualizer widget
            self.Stack.widget(1).plot_widget.plot([current_time], [value])

    def closeEvent(self, event):
        self.arduino.close()
