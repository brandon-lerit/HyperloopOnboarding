from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import sys
import serial
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

        # self.arduino = serial.Serial('COM3', 9600)

        header = Header(w=int(width), h=int(height))

        self.Stack = QStackedWidget(self)

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
            try:
                data = self.arduino.readline().decode().strip()
                value = float(data)
                # Assuming you have a plot item in your Visualizer widget
                self.Stack.widget(1).plot_widget.plot(value)  
            except (ValueError, UnicodeDecodeError):
                print("Error reading data from Arduino")

    def closeEvent(self, event):
        self.arduino.close()
