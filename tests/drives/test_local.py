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
    with patch('arkive.drives.local.utils.TinyTag.get') as mock:
        mock.side_effect = CustomTinyTag
        yield LocalDrive()


def test_index(tmp_path, local_drive):
    path_0 = tmp_path / 'file-0.mp3'
    path_1 = tmp_path / 'file-1.mp3'
    path_2 = tmp_path / 'folder' / 'file-2.mp3'
    path_3 = tmp_path / 'nested' / 'folder' / 'file-3.mp3'

    make_track(path_0, 'artist-0', 'album-0', 'title-0')
    make_track(path_1, 'artist-1', 'album-1', 'title-1')
    make_track(path_2, 'artist-2', 'album-2', 'title-2')
    make_track(path_3, 'artist-3', 'album-3', 'title-3')

    expected = [
        {'artist': 'artist-0', 'album': 'album-0', 'title': 'title-0', 'path': path_0},
        {'artist': 'artist-1', 'album': 'album-1', 'title': 'title-1', 'path': path_1},
        {'artist': 'artist-2', 'album': 'album-2', 'title': 'title-2', 'path': path_2},
        {'artist': 'artist-3', 'album': 'album-3', 'title': 'title-3', 'path': path_3}
    ]

    for actual in local_drive.index(tmp_path):
        assert actual in expected


def test_rename_changes_file_name(tmp_path, local_drive):
    input_path = tmp_path / 'file1.mp3'
    make_track(input_path, 'artist', 'album', 'first')

    output_path = tmp_path / 'file4.mp3'
    local_drive.rename(input_path, output_path)

    assert not input_path.exists() and output_path.exists()
    assert output_path.open('r').readlines() == ['artist\n', 'album\n', 'first']


def test_rename_moves_file_to_new_folder(tmp_path, local_drive):
    input_path = tmp_path / 'file2.mp3'
    make_track(input_path, 'artist', 'album', 'second')

    output_path = tmp_path / 'folderA' / 'file2.mp3'
    local_drive.rename(input_path, output_path)

    assert not input_path.exists() and output_path.exists()
    assert output_path.open('r').readlines() == ['artist\n', 'album\n', 'second']


def test_rename_moves_file_to_new_nested_folders(tmp_path, local_drive):
    input_path = tmp_path / 'file3.mp3'
    make_track(input_path, 'artist', 'album', 'third')

    output_path = tmp_path / 'folderB' / 'folderC' / 'file3.mp3'
    local_drive.rename(input_path, output_path)

    assert not input_path.exists() and output_path.exists()
    assert output_path.open('r').readlines() == ['artist\n', 'album\n', 'third']


def test_cleanup_deletes_empty_folder(tmp_path, local_drive):
    folder = tmp_path / 'origin'
    folder.mkdir()

    assert folder.exists()
    local_drive.cleanup(tmp_path)

    assert not folder.exists()


def test_cleanup_ignores_occupied_folder(tmp_path, local_drive):
    folder = tmp_path / 'origin'
    folder.mkdir()

    file = folder / 'file.txt'
    file.open('w')

    local_drive.cleanup(tmp_path)

    assert folder.exists() and file.exists()
