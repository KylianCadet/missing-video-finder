def filter_deleted_videos(videos):
    return [video for video in videos if video['status']['privacyStatus'] != 'public']

def get_id_from_videos(videos):
    return [video['contentDetails']['videoId'] for video in videos]