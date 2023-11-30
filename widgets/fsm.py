from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from utils import stateMachine
import constants
import random


class FSM(QWidget):
    def __init__(self, parent=None):
        super(FSM, self).__init__(parent)
        self.initUI()
        self.fsm = stateMachine.FSM()

    def initUI(self):
        self.im = QPixmap(constants.STATES[constants.CURRENT_STATE])
        self.im = self.im.scaled(
            100, 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label = QLabel()
        self.label.setPixmap(self.im)
        self.label.setFixedWidth(100)
        self.label.setFixedHeight(100)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)

        self.setLayout(vbox)
        self.setStyleSheet(
            "font-family: Helvetica; font-size: 14px; background-color : #2B26c1")

        # Use a timer to randomly change state for testing purposes
        self.timerFSMRand = QTimer(self, timeout=self.update)
        self.timerFSMRand.start(2000)

    def update(self):
        newState = self.fsm.allStates[random.randint(
            0, len(self.fsm.allStates) - 1)]
        self.fsm.setState(newState)
        self.im = QPixmap(constants.STATES[self.fsm.getState()])
        self.im = self.im.scaled(
            100, 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label = QLabel()
        self.label.setPixmap(self.im)
        self.label.setFixedWidth(100)
        self.label.setFixedHeight(100)
