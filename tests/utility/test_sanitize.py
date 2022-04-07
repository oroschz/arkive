import pytest
from pathlib import Path

from arkive.utility.sanitize import sanitize_name, sanitize_path


def test_sanitize_name():
    assert sanitize_name("My/File") == "MyFile"


# noinspection PyTypeChecker
def test_sanitize_name_when_input_is_none():
    assert sanitize_name(None) == "BLANK"


def test_sanitize_name_when_input_is_emtpy():
    assert sanitize_name("") == "BLANK"


def test_sanitize_name_when_input_is_completely_illegal():
    assert sanitize_name("***") == "BLANK"


def test_sanitize_path_when_input_is_folder():
    assert sanitize_path(Path("/path/to/folder")) == Path("/path/to/folder")


def test_sanitize_path_when_input_is_file():
    assert sanitize_path(Path("/path/to/folder/file.ext")) == Path("/path/to/folder/file.ext")


# noinspection PyTypeChecker
def test_sanitize_path_when_input_is_none():
    with pytest.raises(ValueError):
        sanitize_path(None)
