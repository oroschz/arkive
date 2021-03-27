from pathlib import Path
from unittest.mock import patch, call

from arkive.music.nest import nest_music_file, nest_music_collection
from tests.music.common import side_effect_get_file_tags


@patch('arkive.music.nest.file_move')
@patch('arkive.music.nest.get_file_tags')
def test_nest_music_file(mock_get_file_tags, mock_file_move):
    mock_get_file_tags.return_value = ['artist', 'album', 'title']

    file = Path('c:/Users/Profile/Music/file.mp3')
    destination = Path('C:/Users/Profile/Music/')
    output = (destination / 'artist' / 'album' / 'title.mp3')

    nest_music_file(file, destination)
    mock_file_move.assert_called_once_with(file, output)


@patch('arkive.music.nest.folder_files')
@patch('arkive.music.nest.file_move')
@patch('arkive.music.nest.get_file_tags')
def test_nest_music_collection(mock_get_file_tags, mock_file_move, mock_folder_files):
    mock_get_file_tags.side_effect = side_effect_get_file_tags()

    folder = Path('C:/Users/Profile/Music/')
    files = [(folder / f'file{index}.mp3') for index in range(1, 4)]
    outputs = [(folder / 'artist' / 'album' / f'title {index}.mp3') for index in range(1, 4)]

    mock_folder_files.return_value = files
    nest_music_collection(folder, folder)

    file_move_calls = [call(file, output) for file, output in zip(files, outputs)]
    mock_file_move.assert_has_calls(file_move_calls)