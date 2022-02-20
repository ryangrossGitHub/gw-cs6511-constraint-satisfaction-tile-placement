# Actual counts as apposed to target counts
actuals = {'1': 0, '2': 0, '3': 0, '4': 0}

tile_locations_remaining = []
tile_counts_remaining = {}

# Determine if a combo has already been tried
# Values in the list are numbers that represent a sequence of states
# Values take on this format: <location_index><location_value>
# '01' represents placing an outer_boundary tile at location 0
# '02' represents placing an el_shape tile at location 0
# '011223' represents outer_boundary tile on 4x4 area 0, el_shape on 4x4 area 1, full_block on area 2
# '031323' represents full_block tile on 4x4 area 0, full_block on 4x4 area 1, full_block on area 2
# Each DFS traversal will be a single value in the list
visited_states = []

current_state = ''

# For visited check performance translate tile type to number
OUTER_BOUNDARY = '1'
EL_SHAPE = '2'
FULL_BLOCK = '3'


def constraint_satisfied(targets):
    if actuals['1'] >= targets['1'] and actuals['2'] >= targets['2'] \
            and actuals['3'] >= targets['3'] and actuals['4'] >= targets['4']:
        return True
    else:
        return False


def backtrack(tile_counts, tile_locations, targets):
    global current_state
    if len(tile_locations) > (tile_counts['OUTER_BOUNDARY'] +
                               tile_counts['EL_SHAPE'] +
                               tile_counts['FULL_BLOCK']):
        raise ValueError('There are not enough tiles to cover the landscape!')

    reset_backtracking_vars(tile_locations, tile_counts)
    while True:
        variable = get_next_variable()
        value = get_next_value(variable)

        if value != '-1':
            current_state += str(variable) + value
            add_actuals(tile_locations, variable, value)

            if constraint_satisfied(targets):
                print('Visited States: ' + str(visited_states))
                return current_state
        else:  # There are no tiles left to choose that don't conflict with already visited states
            if current_state == '':
                print('Visited States: ' + str(visited_states))
                return -1  # If we are at the top of the tree then there is no solution
            else:
                visited_states.append(current_state)  # Append this parent node so we don't go back down this path
                reset_backtracking_vars(tile_locations, tile_counts)

        # If we make it down to a leaf node (bottom of the tree)
        if len(current_state)/2 == len(tile_locations):
            visited_states.append(current_state)
            reset_backtracking_vars(tile_locations, tile_counts)


def get_next_variable():
    return get_minimum_remaining_value()


def get_minimum_remaining_value():
    # Nothing to do here as all 4x4 locations have equal remaining values
    # Default to left to right, top to bottom
    return tile_locations_remaining.pop(0)


def get_next_value(variable):
    next_value = get_least_constraining_value([])

    # If LCV takes us to already visited state
    # Keep looking for state we haven't been in yet until there are no options left
    if current_state + str(variable) + next_value in visited_states:
        already_visited_next_values = []
        while current_state + str(variable) + next_value in visited_states:
            already_visited_next_values.append(next_value)
            next_value = get_least_constraining_value(already_visited_next_values)

    if next_value != '-1':
        if next_value == '1':
            tile_counts_remaining['OUTER_BOUNDARY'] -= 1
        elif next_value == '2':
            tile_counts_remaining['EL_SHAPE'] -= 1
        elif next_value == '3':
            tile_counts_remaining['FULL_BLOCK'] -= 1


    return next_value


def get_least_constraining_value(values_to_avoid):
    # Least constraining is the tile that leaves the most bushes visible (el, then outer, then full)
    # El leaves 9 bushes visible
    # Outer leaves 4 bushes visible
    # Full leaves 0 bushes visible
    # Condition statements ensures there is enough tiles in inventory
    # value_to_avoid is passed in to filter out options that would put us in an already visited state
    if tile_counts_remaining['EL_SHAPE'] > 0 and EL_SHAPE not in values_to_avoid:
        return EL_SHAPE
    elif tile_counts_remaining['OUTER_BOUNDARY'] > 0 and OUTER_BOUNDARY not in values_to_avoid:
        return OUTER_BOUNDARY
    elif tile_counts_remaining['FULL_BLOCK'] > 0 and FULL_BLOCK not in values_to_avoid:
        return FULL_BLOCK
    else:
        return '-1'  # No tiles left to choose from


def add_actuals(tile_locations, variable, value):
    index = int(variable)
    if value == '1':  # Outer
        actuals['1'] += tile_locations[index].outer['ones']
        actuals['2'] += tile_locations[index].outer['twos']
        actuals['3'] += tile_locations[index].outer['threes']
        actuals['4'] += tile_locations[index].outer['fours']
    elif value == '2':  # El
        actuals['1'] += tile_locations[index].el['ones']
        actuals['2'] += tile_locations[index].el['twos']
        actuals['3'] += tile_locations[index].el['threes']
        actuals['4'] += tile_locations[index].el['fours']
        # Full block won't have any bushes visible so no need to add anything to actuals


def reset_backtracking_vars(tile_locations, tile_counts):
    global tile_locations_remaining
    global tile_counts_remaining
    global actuals
    global current_state
    current_state = ''
    tile_locations_remaining = [*range(len(tile_locations))]
    tile_counts_remaining = tile_counts.copy()
    actuals = {'1': 0, '2': 0, '3': 0, '4': 0}


def format_output(result):
    output = [char for char in result]

    # Even numbers represent locations, odd numbers represent the tile type at that location
    even = True
    for char in output:
        if even:
            even = False
            print(char + ' 4 ', end='')
        else:
            even = True
            if char == '1':
                print('OUTER_BOUNDARY')
            elif char == '2':
                print('EL_SHAPE')
            elif char == '3':
                print('FULL_BLOCK')