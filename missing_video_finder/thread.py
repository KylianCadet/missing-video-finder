from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Worker(QObject):
    finished = pyqtSignal(dict)

    def __init__(self, fn, parent=None):
        super(Worker, self).__init__(parent)
        self.fn = fn

    def run(self):
        arg = self.fn()
        arg = {'data': arg}
        self.finished.emit(arg)
        return


class Thread():
    def __init__(self, fn, callback):
        self.fn = fn
        self.callback = callback
        self.thread = QThread()
        self.worker = Worker(fn)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.callback)
        self.thread.finished.connect(self.thread.deleteLater)

    def start(self):
        self.thread.start()