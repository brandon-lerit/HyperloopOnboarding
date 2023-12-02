from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from widgets.emergency_button import EmergencyButton
from widgets.fsm import FSM
from widgets.help_pupup import HelpPopup
from widgets.quit import Quit
from widgets.timer import Timer
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject, pyqtSignal
import time
from widgets import progressBar
import constants as cons


class Header(QWidget):
    def __init__(self, w=1000, h=500, *args, **kwargs):
        super(Header, self).__init__()
        hbox = QHBoxLayout(self)
        sshFile = "utils/header.css"
        with open(sshFile, "r") as fh:
            qstr = str(fh.read())
        self.width = w
        self.height = h
        hbox.setContentsMargins(0, 0, 0, 0)

        grid1 = QGridLayout(self)

        quit = Quit(w, h)
        grid1.addWidget(quit, 0, 0, alignment=Qt.AlignCenter)

        timer = Timer(self.width, self.height)
        grid1.addWidget(timer, 0, 2, alignment=Qt.AlignCenter)

        help = HelpPopup(int(self.width), int(self.height))
        grid1.addWidget(help, 0, 3, alignment=Qt.AlignCenter)

        fsm = FSM()

        emergency_button = EmergencyButton(fsm, self.width, self.height)
        grid1.addWidget(emergency_button, 0, 4,
                        alignment=Qt.AlignCenter)

        grid2 = QGridLayout(self)
        self.b4 = QPushButton("Temperature")
        self.b4.clicked.connect(lambda: self.navbar(self.b4))
        self.b4.resize(int(self.width / 5), int(self.height / 20))
        self.b5 = QPushButton("Distance")
        self.b5.clicked.connect(lambda: self.navbar(self.b5))
        self.b5.resize(int(self.width / 5), int(self.height / 20))
        grid2.addWidget(self.b4, 0, 3)
        grid2.addWidget(self.b5, 0, 4)

        vbox = QVBoxLayout(self)

        vbox.addLayout(grid1)
        vbox.addLayout(grid2)

        hbox.addLayout(vbox)
        self.setStyleSheet(qstr)

        splitter4 = QSplitter(Qt.Horizontal)
        self.pBarContainer = progressBar.ProgressBar()
        splitter4.addWidget(self.pBarContainer.label)

        # PROGRESS BAR
        splitter4.addWidget(self.pBarContainer.pBar)
        splitter4.setSizes([int(self.height / 30), int(self.height / 30)])





        hyperloop = QPixmap('state_icons/logo.png')
        hyperloop = hyperloop.scaled(200, 100)
        label = QLabel()
        label.setStyleSheet("border: 1px grey")
        label.setFixedWidth(200)
        label.setFixedHeight(100)
        label.setPixmap(hyperloop)

        splitter4.addWidget(label)           

        hbox.addWidget(splitter4)






        self.timer = QTimer(self, timeout=self.update)
        self.timer.start(1000)

        self.show()

    def update(self):  # PROGRESS BAR
        self.pBarContainer.pBar.setValue(self.pBarContainer.pBar.value()+5)

        if int(self.pBarContainer.pBar.value()) < 50:
            self.pBarContainer.pBar.setStyleSheet(cons.PBAR_LOW_PROGRESS)
        elif int(self.pBarContainer.pBar.value()) > 50:
            self.pBarContainer.pBar.setStyleSheet(cons.PBAR_MED_PROGRESS)
        elif int(self.pBarContainer.pBar.value()) == 100:
            self.pBarContainer.pBar.setStyleSheet(cons.PBAR_HIGH_PROGRESS)

    def navbar(self, b):
        buttons = [self.b1, self.b2, self.b3, self.b4, self.b5]
        # only temperature page is not implemented
        if buttons.index(b) == 3:
            return 0
        else:
            return buttons.index(b)
