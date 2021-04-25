import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from functools import partial
import random


class Window(QWindow):
    def __init__(self):
        QWindow.__init__(self)
        # QWidget.__init__(self) # Define this class as a QWindow
        # self.setTitle("kek")
        self.setTitle("Hello")
        layout = QGridLayout()
        # self.setLayout(layout)
        label = QLabel("Hello, World!")
        layout.addWidget(label, 0, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
