import json
from urllib import request, parse
from pathlib import Path

from arkive.core.drive import Drive


def _pcloud_metadata(track: dict):
    return {'artist': track['artist'], 'album': track['album'], 'title': track['title'], 'path': track['path']}


def _pcloud_recurse(root: dict, path: Path):
    for item in root.get('contents', []):
        item["path"] = path / item['name']
        if not item["isfolder"]:
            yield _pcloud_metadata(item)
        yield from _pcloud_recurse(item, item["path"])


def _pcloud_index(path: Path, auth: dict):
    params = parse.urlencode({'path': path.as_posix(), 'recursive': True, **auth})
    response = request.urlopen('https://api.pcloud.com/listfolder?' + params)
    data = json.load(response)
    yield from _pcloud_recurse(data['metadata'], path)


class PCloudDrive(Drive):
    def __init__(self, auth: dict):
        self.auth = auth

    def index(self, folder: Path):
        yield from _pcloud_index(folder, self.auth)

    def rename(self, source: Path, dest: Path):
        pass

    def cleanup(self, folder: Path):
        pass
