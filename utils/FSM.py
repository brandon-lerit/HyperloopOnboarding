from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from widgets import *
from PyQt5.QtGui import *
import constants
from numpy import random
import numpy as np
import math


class FSM(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = args[0]
        self.height = args[1]
        self.currstate = constants.CURRENT_STATE
        self.initUI()
        self.color()

    def initUI(self):
        def create(state):
            im = QPixmap((constants.STATES[state]))
            im = im.scaled(
                100, 100, Qt.KeepAspectRatio, Qt.FastTransformation)
            label = QLabel()
            label.setPixmap(im)
            label.setFixedWidth(100)
            label.setFixedHeight(100)

            # set stylesheet later to whole layout ?
            label.setStyleSheet(
                "font-family: Helvetica; font-size: 14px; background-color : #2B26c1")
            label.setAutoFillBackground(True)
            return label

        def arrow(start, end):
            startx, starty, endx, endy = start.pos().x(
            ), start.pos().y(), end.pos().x(), end.pos().y()
            orig = ((startx + endx) / 2, (starty + endy) / 2)
            arr = QPixmap(('state_icons/arrow.png'))
            length = np.sqrt((startx - endx) ** 2 + (starty-endy)**2)
            arr = arr.scaled(int(length - 110), 50)
            if endx != orig[0] and endy != orig[1]:
                tan_theta = (endy - orig[1]) / (endx - orig[0])
                theta = math.degrees(np.arctan(tan_theta))
            elif endx == orig[0]:
                if endy > orig[1]:
                    theta = 90
                else:
                    theta = 270
            else:
                if endx > orig[0]:
                    theta = 0
                else:
                    theta = 180

            final = QTransform()
            final.rotate(theta)
            if (endy - orig[1]) > 0 and endx != orig[0]:
                final.rotate(180)
            if (endx > orig[0] and endy > orig[1]) or (endx < orig[0] and endy < orig[1]):
                final.rotate(180)
            arr = arr.transformed(final)
            label = QLabel()
            label.setPixmap(arr)
            label.setStyleSheet("background-color: transparent;")
            finalx, finaly = (startx + endx - arr.size().width() + 100) / \
                2, (starty + endy - arr.size().height() + 100) / 2
            label.move(int(finalx), int(finaly))
            return label

        self.states = {i: create(i) for i in ["Temperature", "Distance"]}

        layout = QGridLayout()
        
        scene = QGraphicsScene(self.left, self.top, self.width * 1.07, self.height * 0.81)
        xi = self.height * 0.81 / 5
        yi = self.width * 1.07 / 7
        self.states["Temperature"].move(int(2 * xi), int(0*yi))
        scene.addWidget(self.states["Temperature"])
        self.states["Distance"].move(int(4 * xi), int(yi))
        scene.addWidget(self.states["Distance"])

        view = QGraphicsView(scene)
        layout.addWidget(view)

        self.setLayout(layout)

        # Use a timer to randomly change state for testing purposes
        self.timerFSMRand = QTimer(self, timeout=self.update)
        self.timerFSMRand.start(2000)

    def update(self):
        self.undocolor()
        self.currstate = random.choice(list(self.states.keys()))
        self.color()

    def color(self):
        self.states[self.currstate].setStyleSheet(
            "font-family: Helvetica; font-size: 14px; background-color : #8c88f8")
        self.states[self.currstate].update()

    def undocolor(self):
        self.states[self.currstate].setStyleSheet(
            "font-family: Helvetica; font-size: 14px; background-color : #2B26c1")
        self.states[self.currstate].update()
