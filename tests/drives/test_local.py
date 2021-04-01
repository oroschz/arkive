import pytest
from unittest.mock import patch

from arkive.drives.local import LocalDrive


class CustomTinyTag:
    def __init__(self, path):
        with open(path) as f:
            self.artist = f.readline().strip()
            self.album = f.readline().strip()
            self.title = f.readline().strip()


def make_track(file, artist, album, title):
    file.parent.mkdir(parents=True, exist_ok=True)
    file.open('w')
    file.write_text(f'{artist}\n{album}\n{title}')


@pytest.fixture(scope='module')
def local_drive():
    with patch('arkive.drives.local.TinyTag.get') as mock:
        mock.side_effect = CustomTinyTag
        yield LocalDrive()


def test_index(tmp_path, local_drive):
    make_track(tmp_path / 'file-0.mp3', 'artist-0', 'album-0', 'title-0')
    make_track(tmp_path / 'file-1.mp3', 'artist-1', 'album-1', 'title-1')
    make_track(tmp_path / 'file-2.mp3', 'artist-2', 'album-2', 'title-2')
    make_track(tmp_path / 'file-3.mp3', 'artist-3', 'album-3', 'title-3')

    expected = [
        {'artist': 'artist-0', 'album': 'album-0', 'title': 'title-0', 'path': tmp_path / 'file-0.mp3'},
        {'artist': 'artist-1', 'album': 'album-1', 'title': 'title-1', 'path': tmp_path / 'file-1.mp3'},
        {'artist': 'artist-2', 'album': 'album-2', 'title': 'title-2', 'path': tmp_path / 'file-2.mp3'},
        {'artist': 'artist-3', 'album': 'album-3', 'title': 'title-3', 'path': tmp_path / 'file-3.mp3'}
    ]

    actual = local_drive.index(tmp_path)

    assert list(actual) == expected


def test_rename(tmp_path, local_drive):
    input_path_1 = tmp_path / 'file1.mp3'
    input_path_2 = tmp_path / 'file2.mp3'
    input_path_3 = tmp_path / 'file3.mp3'

    make_track(input_path_1, 'artist', 'album', 'first')
    make_track(input_path_2, 'artist', 'album', 'second')
    make_track(input_path_3, 'artist', 'album', 'third')

    output_path_1 = tmp_path / 'file4.mp3'
    output_path_2 = tmp_path / 'folderA' / 'file2.mp3'
    output_path_3 = tmp_path / 'folderB' / 'folderC' / 'file3.mp3'

    local_drive.rename(input_path_1, output_path_1)
    local_drive.rename(input_path_2, output_path_2)
    local_drive.rename(input_path_3, output_path_3)

    assert not input_path_1.exists() and output_path_1.exists()
    assert not input_path_2.exists() and output_path_2.exists()
    assert not input_path_3.exists() and output_path_3.exists()

    assert output_path_1.open('r').readlines() == ['artist\n', 'album\n', 'first']
    assert output_path_2.open('r').readlines() == ['artist\n', 'album\n', 'second']
    assert output_path_3.open('r').readlines() == ['artist\n', 'album\n', 'third']


def test_cleanup(tmp_path, local_drive):
    folder = tmp_path / 'origin'
    folder.mkdir()

    assert folder.exists()
    local_drive.cleanup(tmp_path)

    assert not folder.exists()
