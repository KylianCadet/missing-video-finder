from missing_video_finder.exception import *

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