from pathlib import Path
from unittest.mock import patch

from arkive.music.show import show_music_file, show_music_collection
from tests.music.common import side_effect_get_file_tags


@patch('arkive.music.show.get_file_tags')
def test_nest_music_file(mock_get_file_tags):
    mock_get_file_tags.return_value = ['artist', 'album', 'title']

    expected = ['artist', 'album', 'title']
    actual = show_music_file(Path('c:/Users/Profile/Music/file.mp3'))

    assert actual == expected


@patch('arkive.music.show.folder_files')
@patch('arkive.music.show.get_file_tags')
def test_show_music_collection(mock_get_file_tags, mock_folder_files):
    mock_get_file_tags.side_effect = side_effect_get_file_tags()

    folder = Path('C:/Users/Profile/Music/')
    files = [(folder / f'file{index}.mp3') for index in range(1, 4)]
    expected = [['artist', 'album', f'title {index}'] for index in range(1, 4)]

    mock_folder_files.return_value = files
    header, content = show_music_collection(folder)

    assert header == ['ARTIST', 'ALBUM', 'TITLE']
    assert content == expected
