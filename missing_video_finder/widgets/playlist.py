from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import requests

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
    
    def get_playlist_id(self):
        return self.playlist['id']
