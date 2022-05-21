# Arkive

Automate the management of your audio library.

## Usage

```shell
$ arkive --help
```

```
usage: arkive [-h] [-v] <command> ...

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit

commands:
  <command>
    flat         Creates a flat folder structure.
    nest         Creates a nested folder structure.
    fmt          Creates a custom filename structure.
```

### flat

The application will traverse all the subfolders and move your audio files up to the given folder while changing their
name. The new name given to each file will be a concatenation of its artist, album and title.

*e.g.* .../folder/subfolder/myfile.mp3 -> .../folder/artist - album - title.mp3

**Note:** the new name will be sanitized to make sure the result is a valid filename.

```
$ arkive flat ~/Music
```

### nest

The application will traverse all the subfolders and move your audio files up to the given folder while renaming name
organizing them in new subfolders. The names given to each file and folder structures will result from taking the artist
and album names for the folders, and track title for its name.

*e.g.* .../folder/subfolder/myfile.mp3 -> .../folder/artist/album/title.mp3

**Note:** the new names for each file and folder will be sanitized to make sure the result is a valid file/directory.

```
$ arkive nest ~/Music
```

### fmt

This command is similar to the previous 2 commands, but instead of deciding the final names and folders of your files,
the user can decide what format to use instead. You only need to write the tag name within braces to write the
formatting string to use as a template.

*e.g.* To get a similar behaviour to the nest and flat commands, you can use respectively: "{artist}/{album}/{title}"
and "{artist} - {album} - {title}".

**Note:** Both folder and file names will be sanitized to ensure compatibility with your O.S. filesystem.
