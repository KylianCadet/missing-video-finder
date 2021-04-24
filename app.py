import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from functools import partial

# https://github.com/googleapis/google-api-python-client Good doc
# https://developers.google.com/youtube/v3/docs youtube api doc
# https://developers.google.com/identity/protocols/oauth2/scopes#youtube google api youtube scopes


def window():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setGeometry(100, 100, 200, 50)
    w.setWindowTitle("PyQt5")
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
