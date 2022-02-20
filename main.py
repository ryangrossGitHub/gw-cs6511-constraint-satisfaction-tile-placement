from backtrack import backtrack
from input_variable_processor import get_landscape, validate_landscape, create_tiles, get_tile_counts, get_targets

file = 'landscape1.txt'
landscape = get_landscape(file)
validate_landscape(landscape)

# Tile counts represents the input or the number of tiles we have available
tile_counts = get_tile_counts(file)
# Tile_Locations represents the 4x4 locations that a tile can occupy
# A Tile_Location holds the bush counts that would be visible if overlaid by each tile type
tile_locations = create_tiles(landscape)

targets = get_targets(file)

backtrack(tile_counts, tile_locations, targets)




