import numpy as np

from Tile import Tile


def read_landscape_file(file):
    with open(file) as f:
        landscape = [list(i[::2]) for i in f.readlines()]
        validate_landscape(landscape)
        return landscape


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
    tiles = []

    tile_size = 4
    landscape_tile_width = int(len(landscape[0])/tile_size)
    landscape_tile_length = int(len(landscape)/tile_size)
    outer_visible_coordinates = [[1, 1], [1, 2], [2, 1], [2, 2]]
    el_visible_coordinates = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]

    tile_index = 0
    for y in range(landscape_tile_length):
        for x in range(landscape_tile_width):
            tile = Tile(tile_index)
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

            tile.set_el_response(el['ones'], el['twos'], el['threes'], el['fours'])
            tile.set_outer_response(outer['ones'], outer['twos'], outer['threes'], outer['fours'])
            tiles.append(tile)
            tile_index += 1

    return tiles
