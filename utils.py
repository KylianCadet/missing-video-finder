def filter_deleted_video(videos):
    return [video for video in videos if video['status']['privacyStatus'] != 'public']

def get_id_from_video(videos):
    return [video['contentDetails']['videoId'] for video in videos]