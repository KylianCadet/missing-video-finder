import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class VideoComponent(QWidget):
    def __init__(self, video):

        pass



def window():
    app = QApplication(sys.argv)
    win = QWidget()

    main_layout = QVBoxLayout() # Vertical layout
    hbox_control_button = QHBoxLayout() # Layout for playlist id input + oauth
    hbox_content = QHBoxLayout() # Horizontal layout
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
    playlist_id_input = QLineEdit()
    playlist_id_input.setPlaceholderText("Playlist ID")
    playlist_id_btn = QPushButton("Validate")
    hbox_playlist_id.addWidget(playlist_id_input)
    hbox_playlist_id.addWidget(playlist_id_btn)

    # Oauth button (hbox)
    hbox_oauth_btn = QHBoxLayout()
    vbox_control_button_right.addLayout(hbox_oauth_btn)
    oauth_btn = QPushButton("Google oauth")
    hbox_oauth_btn.addStretch()
    hbox_oauth_btn.addWidget(oauth_btn)


    missing_video_list = QListWidget()
    vbox_content_left.addWidget(missing_video_list)

    personal_playlist_video = QListWidget()
    vbox_content_right.addWidget(personal_playlist_video)

    win.setLayout(main_layout)

    win.setWindowTitle("PyQt")
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
