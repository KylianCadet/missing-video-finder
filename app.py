import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from functools import partial
import random

# https://github.com/googleapis/google-api-python-client Good doc
# https://developers.google.com/youtube/v3/docs youtube api doc
# https://developers.google.com/identity/protocols/oauth2/scopes#youtube google api youtube scopes


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.hello = "0"

        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello World", alignment=Qt.AlignCenter)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    def magic(self):
        a = int(self.hello)
        a += 1
        self.hello = str(a)
        self.text.setText(self.hello)


if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec_())
