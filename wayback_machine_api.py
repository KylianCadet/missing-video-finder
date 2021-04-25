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
            if name == 'YouTube':
                continue
            return name

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


w = WaybackMachineAPI()

ids = [
    'TNHsw8TLf6Y',
    'TVl9qR89bYk',
    'S5FpomvfaBo',
    'VNWxDa_RS6c',
    'SX5RJ4OgvPM',
    'Ejxtu8Fkdso',
    'NO_eODrvBlg',
    'lOUCvNNYktM',
    'NMfoV9zdiiQ',
    'HbSE6jGVd5U',
    'HbSE6jGVd5U',
    'Mbrjzggz26w',
    'lLlSrkVsjqs',
    'S3x2Ic3lCEA',
    '8UfMvtTT7Oc',
    'w-b1y8IC4zQ',
    'qFroEnGNoeg',
    'PXI1SgHSteo',
    '4tU5O7wFFM8',
    '1oQWvoXMWME',
    'SlbBxWeBlDg',
    'HNFV6UhBYN0',
    'Xgt6ONSd7OQ',
    '8EmxAhduLCU',
    'P2eagqSw8V0',
    '3hyPkFGPa48',
    '251UF6gFCIk',
    'BuoaGPlWr-4',
    'Sfnh4XJ64fE',
    'JcQ_rv_kTxA',
    'gNZjTAA97Zs',
    'YlF63vbrfeM',
    'Xrvciw8D5I0',
    'TNHsw8TLf6Y',
    'BAs8weim90M',
    'obkm4J-mmOc',
    '4tUxTkXYazk',
    'dJ-3_XM2rVI',
    'btCKtQmN49w',
    'Epgvx4Zq_xY',
    '9eBfa9nNzvk',
    'J5wnlnhIL2s',
    'LzVjuQj8Bsg',
    '-n4lvh_NZDw',
    '758Y3qGecX4',
    'jTrzAUWIChs',
    'p0vMu5ZwSCU',
    'dHDWtJpvURU',
    'wIyETQyuwAc',
    'l7ZlSHGFfdc',
    'iXYmFqEkCGQ',
    'MgbDWmtn_9o',
    'BdF90Czu9UU',
    'Sp4Sp2X-Rko',
    '7Lo0EeWoXis',
    'dP9Wp6QVbsk',
    'gNJ-3blp56w',
    'VsVhdth8QLw',
    '8iLI0z7VY6M',
    'h7NbxyKXLC8',
    'd3MjwnhKLsc']

for id in ids:
    a = w.get_youtube_snapshot(id)
    name = w.resolve_videoname_from_snapshot(a)
    print(name)
