import requests
import datetime

WAYBACK_API_URL = 'http://archive.org/wayback/available'


def do_request(url):
    try:
        r = requests.get(url)
        return r
    except:
        return None


class WaybackMachineAPI():
    def __init__(self):
        pass

    def resolve_videoname_from_snapshot(self, snapshots):
        for i, snapshot in enumerate(snapshots):
            r = do_request(snapshot)
            if r is None:
                continue
            name = r.text.split('<title>')
            if len(name) <= 1:
                continue
            name = name[1]
            name = name.split('</title>')[0]
            if name == 'YouTube' or name == 'GOOGLE - YouTube':
                continue
            # delete the ' - Youtube' string
            return name[:-10]

    def get_snapshots(self, url):
        year = 2000
        month = 0
        snapshots = []
        now = datetime.datetime.now()
        actual_year = now.year
        actual_month = now.month
        while True:
            if year == actual_year and month == actual_month:
                break
            params = {
                'url': url,
                'timestamp': str(year).zfill(4) + str(month).zfill(2)
            }
            r = requests.get(WAYBACK_API_URL, params=params)
            if r.status_code != 200:
                break
            r = r.json()
            if r['archived_snapshots'].get('closest') is None:
                month = month + 1 if month != 12 else 0
                year = year + 1 if month == 0 else year
                continue
            snapshots.append(r['archived_snapshots']['closest']['url'])
            timestamp = r['archived_snapshots']['closest']['timestamp']
            timestamp_year = int(timestamp[:4])
            timestamp_month = int(timestamp[4:6])
            if year < timestamp_year and month < timestamp_month:
                year = timestamp_year
                month = timestamp_month
            if year == actual_year and month == actual_month:
                break
            month = month + 1 if month != 12 else 0
            year = year + 1 if month == 0 else year
        res = []
        for snapshot in snapshots:
            if snapshot not in res:
                res.append(snapshot)
        return res

    def get_youtube_snapshot(self, youtube_id):
        url = 'https://www.youtube.com/watch?v=' + youtube_id
        return self.get_snapshots(url)
