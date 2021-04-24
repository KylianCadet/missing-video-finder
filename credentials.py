from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import requests
import os
import webbrowser
import socketserver
import pickle
import json
import datetime

load_dotenv('.env')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_REVOKE_URL = 'https://oauth2.googleapis.com/revoke'
CREDENTIALS_FILE = '.credentials'


class Server():
    HOST = ""
    PORT = 0

    class RequestHandler(socketserver.BaseRequestHandler):
        def handle(self):
            self.data = self.request.recv(1024).strip()
            self.data = str(self.data, "utf-8")
            self.server.code = parse_qs(urlparse(self.data).query)['code'][0]
            self.request.sendall(b"Oauth complete, close window")

    def __init__(self):
        self._httpd = socketserver.TCPServer((self.HOST, self.PORT), self.RequestHandler)
        self._httpd.code = None
        self._httpd.timeout = 100
        self._httpd.handle_timeout = self._handle_timeout

    def handle(self):
        self._httpd.handle_request()

    def _handle_timeout(self):
        pass

    def get_auth_code(self):
        return self._httpd.code

    def get_port(self):
        ip, port = self._httpd.server_address
        return port


class Credentials():
    def __init__(self):
        self._access_token = None
        self._refresh_token = None
        self._load_credentials()

    def _refresh_access_token(self):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': self._refresh_token,
            'grant_type': 'refresh_token',
        }
        r = requests.post(GOOGLE_TOKEN_URL, params=params)
        if (r.status_code != 200):
            self._delete_credentials()
            return
        credentials = r.json()
        self._access_token = credentials['access_token']

    def _delete_credentials(self):
        os.remove(CREDENTIALS_FILE) if os.path.exists(CREDENTIALS_FILE) else None
        self._access_token = None
        self._refresh_token = None

    def _load_credentials(self):
        try:
            with open(CREDENTIALS_FILE, 'rb') as fd:
                self._refresh_token = pickle.load(fd)
                self._refresh_access_token()
        except IOError:
            os.remove(CREDENTIALS_FILE) if os.path.exists(CREDENTIALS_FILE) else None

    def _save_refresh_token(self):
        with open(CREDENTIALS_FILE, 'wb') as fd:
            pickle.dump(self._refresh_token, fd)

    def revoke(self):
        data = {
            'token': self._refresh_token
        }
        r = requests.post(GOOGLE_REVOKE_URL, params=data)
        self._delete_credentials()

    def get_access_token(self):
        return self._access_token

    def oauth2_flow(self):
        server = Server()
        # add state for security ?
        # https://developers.google.com/identity/protocols/oauth2/web-server#httprest_1
        # Get auth code with user conscentement
        params = {
            'client_id': CLIENT_ID,
            'redirect_uri': 'http://localhost:{}/'.format(server.get_port()),
            'response_type': 'code',
            'scope': 'https://www.googleapis.com/auth/youtube.readonly',
            'access_type': 'offline',
        }
        r = requests.Request('GET', GOOGLE_AUTH_URL, params=params).prepare()
        webbrowser.open(r.url, new=2)
        server.handle()
        auth_code = server.get_auth_code()

        # Get access + refresh token
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:{}/'.format(server.get_port()),
        }
        r = requests.post(GOOGLE_TOKEN_URL, params=params)
        credentials = r.json()
        self._access_token = credentials['access_token']
        self._refresh_token = credentials['refresh_token']
        self._save_refresh_token()
