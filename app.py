import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from credentials import Credentials
from wayback_machine_api import WaybackMachineAPI
from youtube_api import YoutubeAPI
from utils import filter_deleted_videos, get_id_from_videos
from exception import *
from thread import Thread
import requests

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
        pass


class PlaylistWidget(QWidget):
    def __init__(self, playlist, playlist_id_input, parent=None):
        super(PlaylistWidget, self).__init__(parent)
        self.playlist_id_input = playlist_id_input
        self.playlist = playlist

        image_data = requests.get(self.playlist['snippet']['thumbnails']['high']['url'])
        self.pixmap = QPixmap()

        self.pixmap.loadFromData(image_data.content)
        self.pixmap = self.pixmap.scaledToWidth(200)
        self.pic = QLabel()
        self.pic.setPixmap(self.pixmap)

        label_name = QLabel()
        label_name.setText(self.playlist['snippet']['title'])

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.pic)
        main_layout.addWidget(label_name)

        self.setLayout(main_layout)

class Window(QMainWindow):

    def __init__(self, app, parent=None):
        super(Window, self).__init__(parent=parent)
        self.app = app

    def fetch_callback(self, data):
        self.playlist_id_btn.setEnabled(True)
        self.playlist_id_input.setEnabled(True)

        data = data['data']
        if 'error' in data:
            # Error prompt somehow
            print("error")
            return
        data = filter_deleted_videos(data)
        for video in data:
            lambda_widget_item = QListWidgetItem(self.missing_video_list)
            self.missing_video_list.addItem(lambda_widget_item)
            video_widget_item = VideoWidget(video)
            lambda_widget_item.setSizeHint(video_widget_item.minimumSizeHint())
            self.missing_video_list.setItemWidget(lambda_widget_item, video_widget_item)

    def fetch_playlist_id_videos(self):
        playlist_id = self.playlist_id_input.text()
        self.playlist_id_input.setEnabled(False)
        self.playlist_id_btn.setEnabled(False)
        self.app.processEvents()
        self.playlist_thread = Thread(lambda: exec_api(youtube_api.list_playlist_item, playlist_id), self.fetch_callback)
        self.playlist_thread.start()

    def fetch_perso_callback(self, data):
        self.oauth_btn.setEnabled(True)
        data = data['data']
        if 'error' in data:
            # Error prompt somehow
            print("error")
            return
        data = data['items']
        for playlist in data:
            lambda_widget_item = QListWidgetItem(self.personal_playlist_video)
            self.personal_playlist_video.addItem(lambda_widget_item)
            video_widget_item = PlaylistWidget(playlist, self.playlist_id_input)
            lambda_widget_item.setSizeHint(video_widget_item.minimumSizeHint())
            self.personal_playlist_video.setItemWidget(lambda_widget_item, video_widget_item)

    def fetch_perso_playlist(self):
        self.oauth_btn.setEnabled(False)
        self.perso_playlist_thread = Thread(lambda: exec_api(youtube_api.list_playlists), self.fetch_perso_callback)
        self.perso_playlist_thread.start()

    def oauth_callback(self):
        self.oauth_btn.setEnabled(True)
        self.oauth_btn.setText("Revoke Google")
        self.oauth_btn.clicked.connect(self.revoke_access)
        self.fetch_perso_playlist()

    def oauth_connect(self):
        self.oauth_btn.setEnabled(False)
        self.oauth_thread = Thread(credentials.oauth2_flow, self.oauth_callback)
        self.oauth_thread.start()

    def revoke_callback(self):
        self.oauth_btn.setEnabled(True)
        self.oauth_btn.setText("Google oauth")
        self.oauth_btn.clicked.connect(self.oauth_connect)

    def revoke_access(self):
        self.oauth_btn.setEnabled(False)
        self.revoke_thread = Thread(credentials.revoke, self.revoke_callback)
        self.revoke_thread.start()

    def on_resize(self, win):
        print(win.width())
        pass

    def _show(self):
        win = QWidget()
        self.setCentralWidget(win)

        main_layout = QVBoxLayout(win)  # Vertical layout
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
        self.playlist_id_input.returnPressed.connect(self.fetch_playlist_id_videos)
        self.playlist_id_btn = QPushButton("Validate")
        self.playlist_id_btn.clicked.connect(self.fetch_playlist_id_videos)
        hbox_playlist_id.addWidget(self.playlist_id_input)
        hbox_playlist_id.addWidget(self.playlist_id_btn)

        # Oauth button (hbox)
        hbox_oauth_btn = QHBoxLayout()
        vbox_control_button_right.addLayout(hbox_oauth_btn)
        if credentials.get_access_token() is None:
            self.oauth_btn = QPushButton("Google oauth")
            self.oauth_btn.clicked.connect(self.oauth_connect)
        else:
            self.oauth_btn = QPushButton("Revoke Google")
            self.oauth_btn.clicked.connect(self.revoke_access)
            self.fetch_perso_playlist()
        hbox_oauth_btn.addStretch()
        hbox_oauth_btn.addWidget(self.oauth_btn)

        self.missing_video_list = QListWidget()
        vbox_content_left.addWidget(self.missing_video_list)

        self.personal_playlist_video = QListWidget()
        vbox_content_right.addWidget(self.personal_playlist_video)

        self.setGeometry(10, 10, 800, 480)
        self.setWindowTitle("PyQt")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window(app)
    w._show()
    sys.exit(app.exec_())
