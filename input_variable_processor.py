import json

import numpy as np

from Tile_Location import Tile_Location


def get_landscape(file):
    landscape = []
    reading_landscape = False
    with open(file) as f:
        for i in f.readlines():
            if i.startswith('# Landscape'):  # Next line starts landscape
                reading_landscape = True
                continue

            if reading_landscape:
                if i in ['\n', '\r\n']:  # Blank line represents end of landscape
                    return landscape
                else:
                    landscape.append(list(i[::2]))


def get_tile_counts(file):
    reading_tiles = False
    with open(file) as f:
        for i in f.readlines():
            if i.startswith('# Tiles:'):  # Next line starts tile counts
                reading_tiles = True
                continue

            # Transform input to valid json
            if reading_tiles:
                i = i.replace('=', ':')
                i = i.replace('OUTER_BOUNDARY', '"OUTER_BOUNDARY"')
                i = i.replace('EL_SHAPE', '"EL_SHAPE"')
                i = i.replace('FULL_BLOCK', '"FULL_BLOCK"')
                i = i.replace('\n', '')
                return json.loads(i)


def get_targets(file):
    targets = {}
    reading_targets = False
    with open(file) as f:
        for i in f.readlines():
            if i.startswith('# Targets:'):  # Next line starts tile counts
                reading_targets = True
                continue

            # Transform input to valid json
            if reading_targets:
                if i in ['\n', '\r\n']:  # Blank line represents end of targets
                    return targets
                else:
                    targets[i[0]] = i[2:-1]

        return targets  # Handle case where the line after targets is EOF


def validate_landscape(landscape):
    # Check list length is a multiple of 4
    if len(landscape) % 4 != 0:
        raise ValueError('The landscape is not a multiple of 4!')

    # Check lines length is a multiple of 4
    for i in landscape:
        if len(i) % 4 != 0:
            raise ValueError('The landscape is not a multiple of 4!')


# Start at coordinate 0, 0 (top left) and work left to right, line by line, top to bottom
def create_tiles(landscape):
    tile_locations = []

    tile_size = 4
    landscape_tile_width = int(len(landscape[0])/tile_size)
    landscape_tile_length = int(len(landscape)/tile_size)
    outer_visible_coordinates = [[1, 1], [1, 2], [2, 1], [2, 2]]
    el_visible_coordinates = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]

    tile_index = 0
    for y in range(landscape_tile_length):
        for x in range(landscape_tile_width):
            tile_location = Tile_Location(tile_index)
            el = {'ones': 0, 'twos': 0, 'threes': 0, 'fours': 0}
            outer = {'ones': 0, 'twos': 0, 'threes': 0, 'fours': 0}

            x_offset = x * tile_size
            y_offset = y * tile_size

            for coordinate in outer_visible_coordinates:
                value_at_coordinate = landscape[y_offset + coordinate[0]][x_offset + coordinate[1]]
                if value_at_coordinate == '1':
                    outer['ones'] += 1
                elif value_at_coordinate == '2':
                    outer['twos'] += 1
                elif value_at_coordinate == '3':
                    outer['threes'] += 1
                elif value_at_coordinate == '4':
                    outer['fours'] += 1

            for coordinate in el_visible_coordinates:
                value_at_coordinate = landscape[y_offset + coordinate[0]][x_offset + coordinate[1]]
                if value_at_coordinate == '1':
                    el['ones'] += 1
                elif value_at_coordinate == '2':
                    el['twos'] += 1
                elif value_at_coordinate == '3':
                    el['threes'] += 1
                elif value_at_coordinate == '4':
                    el['fours'] += 1

            tile_location.set_el_response(el['ones'], el['twos'], el['threes'], el['fours'])
            tile_location.set_outer_response(outer['ones'], outer['twos'], outer['threes'], outer['fours'])
            tile_locations.append(tile_location)
            tile_index += 1

    return tile_locations
