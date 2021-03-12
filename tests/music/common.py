def side_effect_get_file_tags():
    index = 0
    while True:
        index += 1
        yield ['artist', 'album', f'title {index}']
