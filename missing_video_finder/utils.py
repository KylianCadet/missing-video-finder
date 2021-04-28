from missing_video_finder.exception import *
import os

def filter_deleted_videos(videos):
    return [video for video in videos if video['status']['privacyStatus'] != 'public']

def get_id_from_videos(videos):
    return [video['contentDetails']['videoId'] for video in videos]

def exec_api(fn, *args):
    try:
        data = fn(*args)
        return data
    except NotAuthenticated:
        return {'error': 'not auth'}
    except APIError:
        return {'error': 'api error'}


def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)