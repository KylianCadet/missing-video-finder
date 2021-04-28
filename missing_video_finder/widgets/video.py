from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from missing_video_finder.utils import get_id_from_videos
from missing_video_finder.wayback_machine_api import WaybackMachineAPI
from missing_video_finder.thread import Thread

wayback_machine_api = WaybackMachineAPI()

class VideoWidget(QWidget):
    copy_clipboard = pyqtSignal(str)

    def fetch_callback(self, data):
        name = data['data']
        self.resolved_label.setText(name)
        self.resolved_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.btn.setEnabled(True)
        self.copy_btn = QPushButton('Copy')
        self.copy_btn.clicked.connect(lambda: self.copy_clipboard.emit(self.resolved_label.text()))
        self.resolve_layout.addWidget(self.copy_btn, alignment=Qt.AlignRight)

    def fetch_resolved_video_name(self):
        self.btn.setEnabled(False)
        self.thread = Thread(lambda: wayback_machine_api.resolve_videoname_from_snapshot(wayback_machine_api.get_youtube_snapshot(self.video_id)), self.fetch_callback)
        self.thread.start()

    def __init__(self, video, parent=None):
        super(VideoWidget, self).__init__(parent)
        self.video_id = str(get_id_from_videos([video])[0])
        self.main_layout = QHBoxLayout()
        label = QLabel()
        self.resolved_label = QLabel()
        label.setText(self.video_id)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.btn = QPushButton("Resolve")
        self.btn.clicked.connect(self.fetch_resolved_video_name)
        self.main_layout.addWidget(label, stretch=10)
        self.main_layout.addWidget(self.btn, stretch=10)
        self.main_layout.addStretch()
        self.resolve_layout = QHBoxLayout()
        self.resolve_layout.addWidget(self.resolved_label, stretch=100, alignment=Qt.AlignRight)
        self.main_layout.addLayout(self.resolve_layout, stretch=20)
        self.setLayout(self.main_layout)
