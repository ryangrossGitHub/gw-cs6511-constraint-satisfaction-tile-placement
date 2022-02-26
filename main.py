import time

from backtrack import backtrack, format_output
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

start = time.time()
result = backtrack(tile_counts, tile_locations, targets)
end = time.time()
if result == -1:
    print("There is no solution to this problem.")
else:
    print("Solution Found!")
    print("Time: " + str(end - start) + "s")
    format_output(result, len(tile_locations))

