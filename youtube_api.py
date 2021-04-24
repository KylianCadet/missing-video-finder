from credentials import Credentials
from exception import *
from utils import filter_deleted_video, get_id_from_video
import requests

YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3'


class YoutubeAPI():
    def __init__(self, credentials: Credentials):
        self._credentials = credentials

    def check_credentials(func):
        def inner(self, *args, **kwargs):
            if self._credentials.get_access_token() is None:
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
            'Authorization': 'Bearer ' + self._credentials.get_access_token()
        }
        r = requests.get(YOUTUBE_API_URL + '/playlists', params=params, headers=headers)
        if r.status_code != 200:
            raise APIError
        return r.json()

    def list_playlist_item(self, playlist_id):
        headers = {
            'Authorization': 'Bearer ' + self._credentials.get_access_token()
        }
        page_token = None
        res = []
        while True:
            params = {
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
            print(page_token)
            if page_token is None:
                return res

c = Credentials()
y = YoutubeAPI(c)

def exec_api(fn, *args):
    try:
        data = fn(*args)
        return data
    except NotAuthenticated:
        return {'error': 'not auth'}
    except APIError:
        return {'error': 'api error'}


data = exec_api(y.list_playlists)
playlist_id = data['items'][0]['id']
print(playlist_id)
videos = exec_api(y.list_playlist_item, playlist_id)
filtered_videos = filter_deleted_video(videos)
ids = get_id_from_video(filtered_videos)
print(ids)