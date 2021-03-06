from missing_video_finder.youtube_credentials import YoutubeCredentials
from missing_video_finder.credentials import API_KEY
from missing_video_finder.exception import *
from missing_video_finder.utils import filter_deleted_videos, get_id_from_videos
import requests

YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3'

# https://developers.google.com/youtube/v3/docs youtube api doc


class YoutubeAPI():
    def __init__(self, youtube_credentials: YoutubeCredentials):
        self._youtube_credentials = youtube_credentials

    def check_credentials(func):
        def inner(self, *args, **kwargs):
            if self._youtube_credentials.get_access_token() is None:
                raise NotAuthenticated
            return func(self)
        return inner

    @check_credentials
    def list_playlists(self):
        params = {
            'part': 'id, snippet',
            'mine': True
        }
        headers = {
            'Authorization': 'Bearer ' + self._youtube_credentials.get_access_token()
        }
        r = requests.get(YOUTUBE_API_URL + '/playlists', params=params, headers=headers)
        if r.status_code != 200:
            raise APIError
        return r.json()

    def list_playlist_item(self, playlist_id):
        if playlist_id.__contains__('https://www.youtube.com/playlist?list='):
            playlist_id = playlist_id.split('=')[1]
        headers = {
            'Authorization': 'Bearer ' + self._youtube_credentials.get_access_token()
        } if self._youtube_credentials.get_access_token() else {}
        page_token = None
        res = []
        while True:
            params = {
                'key': API_KEY,
                'part': 'id, snippet, status, contentDetails',
                'playlistId': playlist_id,
                'maxResults': 50,
                'page_token': page_token
            }
            r = requests.get(YOUTUBE_API_URL + '/playlistItems', params=params, headers=headers)
            if r.status_code != 200:
                raise APIError
            r = r.json()
            res += r['items']
            page_token = r['nextPageToken'] if r.get('nextPageToken') else None
            if page_token is None:
                return res