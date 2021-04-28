import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from missing_video_finder.youtube_credentials import YoutubeCredentials
from missing_video_finder.youtube_api import YoutubeAPI
from missing_video_finder.utils import filter_deleted_videos, exec_api, resource_path
from missing_video_finder.thread import Thread
from missing_video_finder.widgets.video import VideoWidget
from missing_video_finder.widgets.playlist import PlaylistWidget

youtube_credentials = YoutubeCredentials()
youtube_api = YoutubeAPI(youtube_credentials)

class Window(QMainWindow):
    def __init__(self, app, parent=None):
        super(Window, self).__init__(parent=parent)
        self.app = app

    def fetch_videos_in_playlist_callback(self, data):
        self.playlist_id_btn.setEnabled(True)
        self.playlist_id_input.setEnabled(True)
        data = data['data']
        if 'error' in data:
            print("error")
            return
        data = filter_deleted_videos(data)
        for video in data:
            lambda_widget_item = QListWidgetItem(self.missing_video_list)
            self.missing_video_list.addItem(lambda_widget_item)
            video_widget_item = VideoWidget(video)
            video_widget_item.copy_clipboard.connect(self.copy_clipboard)
            lambda_widget_item.setSizeHint(video_widget_item.minimumSizeHint())
            self.missing_video_list.setItemWidget(lambda_widget_item, video_widget_item)

    def fetch_videos_in_playlist(self):
        self.missing_video_list.clear()
        playlist_id = self.playlist_id_input.text()
        self.playlist_id_input.setEnabled(False)
        self.playlist_id_btn.setEnabled(False)
        self.app.processEvents()
        self.playlist_thread = Thread(lambda: exec_api(youtube_api.list_playlist_item, playlist_id), self.fetch_videos_in_playlist_callback)
        self.playlist_thread.start()

    def copy_clipboard(self, text):
        self.app.clipboard().setText(text)

    def fetch_personal_playlists_callback(self, data):
        self.oauth_btn.setEnabled(True)
        data = data['data']
        if 'error' in data:
            print("error")
            return
        data = data['items']
        for playlist in data:
            lambda_widget_item = QListWidgetItem(self.personal_playlists)
            self.personal_playlists.addItem(lambda_widget_item)
            playlist_widget_item = PlaylistWidget(playlist, self.playlist_id_input)
            lambda_widget_item.setSizeHint(playlist_widget_item.minimumSizeHint())
            lambda_widget_item.get_playlist_id = playlist_widget_item.get_playlist_id
            self.personal_playlists.setItemWidget(lambda_widget_item, playlist_widget_item)

    def fetch_personal_playlists(self):
        self.oauth_btn.setEnabled(False)
        self.perso_playlist_thread = Thread(lambda: exec_api(youtube_api.list_playlists), self.fetch_personal_playlists_callback)
        self.perso_playlist_thread.start()

    def oauth_connect_callback(self):
        self.oauth_btn.setText("Revoke Google")
        self.oauth_btn.disconnect()
        self.oauth_btn.clicked.connect(self.revoke_access)
        self.fetch_personal_playlists()
        self.oauth_btn.setEnabled(True)

    def oauth_connect(self):
        self.oauth_btn.setEnabled(False)
        self.oauth_thread = Thread(youtube_credentials.oauth2_flow, self.oauth_connect_callback)
        self.oauth_thread.start()

    def revoke_access_callback(self):
        self.oauth_btn.setText("Google oauth")
        self.oauth_btn.disconnect()
        self.oauth_btn.clicked.connect(self.oauth_connect)
        self.oauth_btn.setEnabled(True)

    def revoke_access(self):
        self.oauth_btn.setEnabled(False)
        self.personal_playlists.clear()
        self.revoke_thread = Thread(youtube_credentials.revoke, self.revoke_access_callback)
        self.revoke_thread.start()

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
        self.playlist_id_input.returnPressed.connect(self.fetch_videos_in_playlist)
        self.playlist_id_btn = QPushButton("Validate")
        self.playlist_id_btn.clicked.connect(self.fetch_videos_in_playlist)
        hbox_playlist_id.addWidget(self.playlist_id_input)
        hbox_playlist_id.addWidget(self.playlist_id_btn)

        # Oauth button (hbox)
        hbox_oauth_btn = QHBoxLayout()
        vbox_control_button_right.addLayout(hbox_oauth_btn)
        if youtube_credentials.get_access_token() is None:
            self.oauth_btn = QPushButton("Google oauth")
            self.oauth_btn.clicked.connect(self.oauth_connect)
        else:
            self.oauth_btn = QPushButton("Revoke Google")
            self.oauth_btn.clicked.connect(self.revoke_access)
            self.fetch_personal_playlists()
        hbox_oauth_btn.addStretch()
        hbox_oauth_btn.addWidget(self.oauth_btn)

        self.missing_video_list = QListWidget()
        self.missing_video_list.setStyleSheet("QListView::item:selected"
                                  "{"
                                  "border : 1px solid white;"
                                  "}"
                                  )
        vbox_content_left.addWidget(self.missing_video_list)

        self.personal_playlists = QListWidget()
        self.personal_playlists.setStyleSheet("QListView::item:selected"
                                  "{"
                                  "border : 1px solid white;"
                                  "}"
                                  )
        self.personal_playlists.itemClicked.connect(lambda x: self.playlist_id_input.setText(x.get_playlist_id()))
        vbox_content_right.addWidget(self.personal_playlists)

        self.setGeometry(10, 10, 800, 480)
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2)) 
        self.setWindowTitle("Missing Video Finder")
        self.setWindowIcon(QIcon(resource_path('./data/img/icon.png')))
        self.show()

def main():
    app = QApplication(sys.argv)
    w = Window(app)
    w._show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
