import time

from arc_consistency import filter_domains
from output_formatter import format_output
from input_variable_processor import get_landscape, validate_landscape, create_tiles, get_tile_counts, get_targets

file = 'test7.txt'
path = 'test_files/'
print("Processing: " + file)
landscape = get_landscape(path + file)
validate_landscape(landscape)

# Tile counts represents the input or the number of tiles we have available
tile_counts = get_tile_counts(path + file)
# Tile_Locations represents the 4x4 locations that a tile can occupy
# A Tile_Location holds the bush counts that would be visible if overlaid by each tile type
tile_locations = create_tiles(landscape)

targets = get_targets(path + file)

start = time.time()
result = filter_domains(tile_counts, tile_locations, targets)
end = time.time()

print("Time: " + str(end - start) + "s")
format_output(result, len(landscape[0]), len(tile_locations))

