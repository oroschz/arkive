import json
from urllib import request, parse
from pathlib import Path

from arkive.core.drive import Drive


def _pcloud_metadata(track: dict):
    return {key: track[key] for key in ['artist', 'album', 'title', 'path']}


def _pcloud_recurse(root: dict, path: Path):
    for item in root.get('contents', []):
        item['path'] = path / item['name']
        if not item['isfolder'] and item['icon'] == 'audio':
            yield _pcloud_metadata(item)
        yield from _pcloud_recurse(item, item["path"])


def _pcloud_request(action: str, params: dict, auth: dict):
    queries = parse.urlencode({**params, **auth})
    response = request.urlopen(f'https://api.pcloud.com/{action}?{queries}')
    return json.load(response)


def _pcloud_index(path: Path, auth: dict):
    params = {'path': path.as_posix(), 'recursive': True}
    data = _pcloud_request('listfolder', params, auth)
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
