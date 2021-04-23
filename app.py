import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from google_auth_oauthlib.flow import InstalledAppFlow
import threading
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pickle

load_dotenv('.env')

# https://github.com/googleapis/google-api-python-client Good doc
# https://developers.google.com/youtube/v3/docs youtube api doc
# https://developers.google.com/identity/protocols/oauth2/scopes#youtube google api youtube scopes

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CREDENTIALS_FILE = '.credentials'

def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'rb') as fd:
            return pickle.load(fd)
    except IOError:
        os.remove(CREDENTIALS_FILE) if os.path.exists(CREDENTIALS_FILE) else None
    return None


def save_credentials(credentials):
    with open(CREDENTIALS_FILE, 'wb') as fd:
        pickle.dump(credentials, fd)

def get_credentials(flow):
    print(CLIENT_ID)
    print(CLIENT_SECRET)
    credentials = flow.run_local_server(host='localhost',
                                        port=0,
                                        success_message='The auth flow is complete; you may close this window.',
                                        open_browser=True)
    save_credentials(credentials)
    youtube_service = build('youtube', 'v3', credentials=credentials)
    a = youtube_service.playlists().list(part="snippet, contentDetails, id, status", mine=True).execute()
    print(a)
    youtube_service.close()


def on_click():
    client_config = {
        'installed': {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'project_id': 'playlist-recover',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob', 'http://localhost']
        }
    }
    scopes = ['https://www.googleapis.com/auth/youtube.readonly']
    flow = InstalledAppFlow.from_client_config(client_config, scopes)
    x = threading.Thread(target=get_credentials, args=(flow, ))
    x.start()
    # credentials = google.oauth2.credentials.Credentials('access_token')
    print("clicked")


def window():
    credentials = None
    credentials = load_credentials()
    app = QApplication(sys.argv)
    w = QWidget()
    w.setGeometry(100, 100, 200, 50)
    w.setWindowTitle("PyQt5")
    if not credentials:
        y = QPushButton(w)
        y.setText("Google oauth")
        y.clicked.connect(on_click)
    print(credentials)
    a = QAction(w)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
