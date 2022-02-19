from landscape_processor import read_landscape_file, validate_landscape, create_tiles

landscape = read_landscape_file('landscape1.txt')
validate_landscape(landscape)
tiles = create_tiles(landscape)
print(tiles)

