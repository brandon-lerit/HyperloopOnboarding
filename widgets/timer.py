from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QTime, Qt, QSize
import sys


class Timer(QWidget):
    def __init__(self, *args, parent=None):
        super(Timer, self).__init__(parent)
        self.width = int(args[0] / 10)
        self.height = int(args[1] / 30)
        self.initUI()

    def initUI(self):
        self.count = 0
        self.start = True
        self.label = QLabel("         Time         ", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "font-family: Helvetica; font-size: 20px; background-color: lightcoral; color: black; border: 3px solid black; padding: 10px")
        self.label.resize(int(self.width), int(self.height))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(100)

    def showTime(self):
        self.count += 1
        text = f'Time: {self.count / 10} s'
        self.label.setText(text)
        self.label.update()

    def sizeHint(self):
        return QSize(int(self.width), int(self.height))
