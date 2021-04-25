import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from credentials import Credentials
from wayback_machine_api import WaybackMachineAPI
from youtube_api import YoutubeAPI
from utils import filter_deleted_videos, get_id_from_videos
from exception import *


credentials = Credentials()
youtube_api = YoutubeAPI(credentials)
wayback_machine_api = WaybackMachineAPI()


# for id in ids:
#     a = w.get_youtube_snapshot(id)
#     name = w.resolve_videoname_from_snapshot(a)
#     print(name)


# data = exec_api(y.list_playlists)
# playlist_id = data['items'][0]['id']
# print(playlist_id)
# videos = exec_api(y.list_playlist_item, playlist_id)
# filtered_videos = filter_deleted_video(videos)
# ids = get_id_from_video(filtered_videos)
# print(ids)


def exec_api(fn, *args):
    try:
        data = fn(*args)
        return data
    except NotAuthenticated:
        return {'error': 'not auth'}
    except APIError:
        return {'error': 'api error'}

class VideoWidget(QWidget):
    def fetch_resolved_video_name(self):
        self.btn.setEnabled(False)
        self.process_event_fn()
        snapshots = wayback_machine_api.get_youtube_snapshot(self.video_id)
        name = wayback_machine_api.resolve_videoname_from_snapshot(snapshots)
        self.resolved_label.setText(name)
        self.btn.setEnabled(True)
        pass


    def __init__(self, video, process_event_fn, parent=None):
        self.process_event_fn = process_event_fn
        super(VideoWidget, self).__init__(parent)
        self.video_id = str(get_id_from_videos([video])[0])
        main_layout = QHBoxLayout()
        label = QLabel()
        self.resolved_label = QLabel()
        label.setText(self.video_id)
        self.btn = QPushButton("Resolve")
        self.btn.clicked.connect(lambda: self.fetch_resolved_video_name())
        main_layout.addWidget(label, stretch=10)
        main_layout.addWidget(self.btn, stretch=10)
        main_layout.addStretch()
        main_layout.addWidget(self.resolved_label, stretch=20, alignment=Qt.AlignRight)
        self.setLayout(main_layout)
        pass


class Window():
    def fetch_playlist_id_videos(self):
        playlist_id = self.playlist_id_input.text()
        self.playlist_id_btn.setEnabled(False)
        self.playlist_id_input.setEnabled(False)
        self.app.processEvents()
        data = exec_api(youtube_api.list_playlist_item, playlist_id)
        if 'error' in data:
            # Error prompt somehow
            print("error")
            self.playlist_id_btn.setEnabled(True)
            self.playlist_id_input.setEnabled(True)
            return
        data = filter_deleted_videos(data)
        for video in data:
            lambda_widget_item = QListWidgetItem(self.missing_video_list)
            self.missing_video_list.addItem(lambda_widget_item)
            video_widget_item = VideoWidget(video, self.app.processEvents)
            lambda_widget_item.setSizeHint(video_widget_item.minimumSizeHint())
            self.missing_video_list.setItemWidget(lambda_widget_item, video_widget_item)
        self.playlist_id_btn.setEnabled(True)
        self.playlist_id_input.setEnabled(True)

    def window(self):
        self.app = QApplication(sys.argv)
        win = QWidget()

        main_layout = QVBoxLayout()  # Vertical layout
        hbox_control_button = QHBoxLayout()  # Layout for playlist id input + oauth
        hbox_content = QHBoxLayout()  # Horizontal layout
        main_layout.addLayout(hbox_control_button)
        main_layout.addLayout(hbox_content)

        # Create all layouts
        vbox_control_button_left = QVBoxLayout()
        vbox_control_button_right = QVBoxLayout()
        hbox_control_button.addLayout(vbox_control_button_left, stretch=70)
        hbox_control_button.addLayout(vbox_control_button_right, stretch=30)
        vbox_content_left = QVBoxLayout()
        vbox_content_right = QVBoxLayout()
        hbox_content.addLayout(vbox_content_left, stretch=70)
        hbox_content.addLayout(vbox_content_right, stretch=30)

        # Playlist id input (hbox)
        hbox_playlist_id = QHBoxLayout()
        vbox_control_button_left.addLayout(hbox_playlist_id)
        self.playlist_id_input = QLineEdit()
        self.playlist_id_input.setPlaceholderText("Playlist ID")
        self.playlist_id_input.returnPressed.connect(lambda: self.fetch_playlist_id_videos())
        self.playlist_id_btn = QPushButton("Validate")
        self.playlist_id_btn.clicked.connect(lambda: self.fetch_playlist_id_videos())
        hbox_playlist_id.addWidget(self.playlist_id_input)
        hbox_playlist_id.addWidget(self.playlist_id_btn)

        # Oauth button (hbox)
        hbox_oauth_btn = QHBoxLayout()
        vbox_control_button_right.addLayout(hbox_oauth_btn)
        oauth_btn = QPushButton("Google oauth")
        hbox_oauth_btn.addStretch()
        hbox_oauth_btn.addWidget(oauth_btn)

        self.missing_video_list = QListWidget()
        vbox_content_left.addWidget(self.missing_video_list)

        personal_playlist_video = QListWidget()
        vbox_content_right.addWidget(personal_playlist_video)

        win.setLayout(main_layout)

        win.setWindowTitle("PyQt")
        win.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    w = Window()
    w.window()
