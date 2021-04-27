from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from missing_video_finder.utils import filter_deleted_videos, get_id_from_videos
from missing_video_finder.wayback_machine_api import WaybackMachineAPI
from missing_video_finder.thread import Thread

wayback_machine_api = WaybackMachineAPI()

class VideoWidget(QWidget):
    def fetch_callback(self, data):
        name = data['data']
        self.resolved_label.setText(name)
        self.btn.setEnabled(True)

    def fetch_resolved_video_name(self):
        self.btn.setEnabled(False)
        self.thread = Thread(lambda: wayback_machine_api.resolve_videoname_from_snapshot(wayback_machine_api.get_youtube_snapshot(self.video_id)), self.fetch_callback)
        self.thread.start()

    def __init__(self, video, parent=None):
        super(VideoWidget, self).__init__(parent)
        self.video_id = str(get_id_from_videos([video])[0])
        main_layout = QHBoxLayout()
        label = QLabel()
        self.resolved_label = QLabel()
        label.setText(self.video_id)
        self.btn = QPushButton("Resolve")
        self.btn.clicked.connect(self.fetch_resolved_video_name)
        main_layout.addWidget(label, stretch=10)
        main_layout.addWidget(self.btn, stretch=10)
        main_layout.addStretch()
        main_layout.addWidget(self.resolved_label, stretch=20, alignment=Qt.AlignRight)
        self.setLayout(main_layout)
