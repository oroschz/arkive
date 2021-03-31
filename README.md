# Arkive

Manage your music/audio collections.

## 1. Installation

A package with the same name is available in [pypi](https://pypi.org/project/arkive)

```
  $ pip install --user arkive
```

This package has been tested mainly on Windows 10, but it should work on all platforms since it only makes use of
cross-platform libraries. You may need to use "pip3", "python3 -m pip" or "python -m" when running on other platforms,
or different Python setups.

## 2. General usage

```
$ arkive -h

usage: arkive [-h] {show,flat,nest} ...

positional arguments:
  {show,flat,nest}
    show            display music collection inside a given folder.
    flat            flatten music files inside a given folder.
    nest            nesting music files inside a given folder.

optional arguments:
  -h, --help        show this help message and exit
```

As explained above, you can use one of 3 commands: show, flat and nest, and fianlly a positional argument indicating a
folder path.

### show

It will traverse the folders inside the given path and display a table of all the existing (with compatible audio
formats) files, showing artist, album and title.

### flat

The application will traverse all the subfolders and move the music files up to the given folder while changing their
name. The new name given to each file will be a concatenation of its artist, album and title.

*e.g.* .../folder/subfolder/myfile.mp3 -> .../folder/artist - album - title.mp3

**Note:** the new name will be sanitized to make sure the result is a valid filename.

### nest

The application will traverse all the subfolders and move the music files up to the given folder while renaming name
organizing them in new subfolders. The names given to each file and folder structures will result from taking the artist
and album names for the folders, and track title for its name.

*e.g.* .../folder/subfolder/myfile.mp3 -> .../folder/artist/album/title.mp3

**Note:** the new names for each file and folder will be sanitized to make sure the result is a valid file/directory.

#### Destination folder

An optional argument "-o/-output" may be used to change the destination directory for the audio files.

## 3. Side-effects

This implementation includes a "cleanup" procedure which removes empty subfolders from the origin directory. This is a
personal decision due to convenience, but it may be changed in the near future to act only under explicit indication.