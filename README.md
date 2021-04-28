# Missing Video Finder

A Minimal GUI to find **deleted** or **private** videos in youtube playlists

![app screenshot](https://raw.githubusercontent.com/KylianCadet/missing-video-finder/master/docs/img/missing-video-finder.png)

## Key Features
- Find lists of deleted or private videos in a playlist and resolve their names
- Google Oauth to access private playlists of a user
- Cross-platform


## How it works

Missing Video Finder uses the [Wayback Machine](https://archive.org/web/) to resolve the names of missing videos.

> This means it can fail to resolve some names if no snapshots were created for a video

## Download

You can [download](https://github.com/KylianCadet/missing-video-finder/releases) the latest release for Windows and Linux.

## Credits

This software uses the following open source packages:

- [PyQt5](https://pypi.org/project/PyQt5/5.6/)
- [Requests](https://pypi.org/project/requests/)

## License

MIT
