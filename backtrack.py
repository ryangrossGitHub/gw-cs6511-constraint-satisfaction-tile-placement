# Actual counts as apposed to target counts
import bisect
import copy

actuals = {'1': 0, '2': 0, '3': 0, '4': 0}

tile_locations_remaining = []
tile_counts_remaining = {}
visited_states = []
current_state = [[],[]]
variable_try_ordering = []
value_try_ordering = []

OUTER_BOUNDARY = '1'
EL_SHAPE = '2'
FULL_BLOCK = '3'


def constraint_satisfied(targets):
    if actuals['1'] == targets['1'] and actuals['2'] == targets['2'] \
            and actuals['3'] == targets['3'] and actuals['4'] == targets['4']:
        return True
    else:
        return False


def backtrack(tile_counts, tile_locations, targets):
    global current_state
    global tile_locations_remaining
    global tile_counts_remaining
    if len(tile_locations) > (tile_counts['OUTER_BOUNDARY'] +
                               tile_counts['EL_SHAPE'] +
                               tile_counts['FULL_BLOCK']):
        raise ValueError('There are not enough tiles to cover the landscape!')

    tile_locations_remaining = [*range(len(tile_locations))]
    tile_counts_remaining = tile_counts.copy()
    while True:
        value = get_least_constraining_value()
        if value == '3':
            if constraint_satisfied(targets):
                visited_states.append(copy.deepcopy(current_state))
                print('Visited State Count: ' + str(len(visited_states)))
                print('Actuals: ' + str(actuals))
                return current_state
            else:
                visited_states.append(copy.deepcopy(current_state))
                reset_backtracking_vars(tile_locations, tile_counts)
                continue

        variable = get_next_variable(value, tile_locations, targets)

        # Constraint check is passing
        if variable != -1:
            update_caches(value, variable)
            add_actuals(tile_locations, variable, value)
        else:  # Constraint check is failing
            if len(current_state[0]) == 0 and len(current_state[1]) == 0:  # If at top of tree, then no solution exists
                print('Visited State Count: ' + str(len(visited_states)))
                return -1
            else:
                visited_states.append(copy.deepcopy(current_state))
                reset_backtracking_vars(tile_locations, tile_counts)

        # If we make it down to a leaf node (bottom of the tree)
        # if len(current_state[0]) + len(current_state[1]) == len(tile_locations) or value == '3':
        #     if constraint_satisfied(targets):
        #         visited_states.append(current_state)
        #         print('Visited State Count: ' + str(len(visited_states)))
        #         print('Actuals: ' + str(actuals))
        #         return current_state
        #     else:
        #         visited_states.append(current_state)
        #         reset_backtracking_vars(tile_locations, tile_counts)


def get_next_variable(value, tile_locations, targets):
    global variable_try_ordering
    variables_leading_to_visited_state = []
    while True:
        if value == '3':
            mvr = -1
            for loc in tile_locations_remaining:
                if loc not in variables_leading_to_visited_state:
                    mvr = loc
        else:
            mvr = get_minimum_remaining_value(value, tile_locations, targets, variables_leading_to_visited_state)

        if mvr == -1:
            return mvr
        elif not state_visited(value, mvr):
            variable_try_ordering.append(mvr)
            value_try_ordering.append(value)
            return mvr
        else:
            if len(tile_locations_remaining) == 1:  # Nothing left to try
                return -1

            variables_leading_to_visited_state.append(mvr)


def get_minimum_remaining_value(value, tile_locations, targets, var_avoid_list):
    # Find location with bushes that get us closest to target
    # Another way to say this: choose the variable that is most constrained
    # The location that gets us closest to our constraint is the most constrained because we have to
    # make this location visible to capitalize on the bushes in the location or else our solution won't
    # meet the bush count constraint
    mrv = -1
    closest_to_target_delta = 999  # Large number avoid None check with each cycle of the loop
    for i in tile_locations_remaining:
        if i in var_avoid_list:
            continue

        deltas = []
        # min used as an alternative to subtraction to ensure we don't get into negative utility
        if value == '1':
            deltas.append(targets['1'] - actuals['1'] - tile_locations[i].outer['ones'])
            deltas.append(targets['2'] - actuals['2'] - tile_locations[i].outer['twos'])
            deltas.append(targets['3'] - actuals['3'] - tile_locations[i].outer['threes'])
            deltas.append(targets['4'] - actuals['4'] - tile_locations[i].outer['fours'])
        else:
            deltas.append(targets['1'] - actuals['1'] - tile_locations[i].el['ones'])
            deltas.append(targets['2'] - actuals['2'] - tile_locations[i].el['twos'])
            deltas.append(targets['3'] - actuals['3'] - tile_locations[i].el['threes'])
            deltas.append(targets['4'] - actuals['4'] - tile_locations[i].el['fours'])

        total = 0
        for delta in deltas:
            if delta < 0:
                total = -1
                break

            total += delta

        if total != -1 and total < closest_to_target_delta:
            closest_to_target_delta = total
            mrv = i

    # Dead end. No places to put this panel that won't take us over bush targets
    if mrv == -1:
        return -1

    else:
        return mrv


def state_visited(value, variable):
    if value == '1':
        bisect.insort(current_state[0], variable)
    elif value == '2':
        bisect.insort(current_state[1], variable)

    if current_state not in visited_states:
        return False
    else:
        if value == '1':
            current_state[0].remove(variable)
        elif value == '2':
            current_state[1].remove(variable)
        return True


def update_caches(value, variable):
    # Update tile locations
    tile_locations_remaining.pop(tile_locations_remaining.index(variable))
    # Update remaining tile counts
    if value != '-1':
        if value == '1':
            tile_counts_remaining['OUTER_BOUNDARY'] -= 1
        elif value == '2':
            tile_counts_remaining['EL_SHAPE'] -= 1
        elif value == '3':
            tile_counts_remaining['FULL_BLOCK'] -= 1


def get_least_constraining_value():
    # Least constraining is the tile that leaves the most bushes visible (el, then outer, then full)
    # El leaves 9 bushes visible
    # Outer leaves 4 bushes visible
    # Full leaves 0 bushes visible
    if tile_counts_remaining['EL_SHAPE'] > 0:
        return EL_SHAPE
    elif tile_counts_remaining['OUTER_BOUNDARY'] > 0:
        return OUTER_BOUNDARY
    elif tile_counts_remaining['FULL_BLOCK'] > 0:
        return FULL_BLOCK


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
    last_variable = variable_try_ordering[-1]
    if value_try_ordering[-1] == '1':
        current_state[0].remove(last_variable)
        tile_counts_remaining['OUTER_BOUNDARY'] += 1
        actuals['1'] -= tile_locations[last_variable].outer['ones']
        actuals['2'] -= tile_locations[last_variable].outer['twos']
        actuals['3'] -= tile_locations[last_variable].outer['threes']
        actuals['4'] -= tile_locations[last_variable].outer['fours']
    elif value_try_ordering[-1] == '2':
        current_state[1].remove(last_variable)
        tile_counts_remaining['EL_SHAPE'] += 1
        actuals['1'] -= tile_locations[last_variable].el['ones']
        actuals['2'] -= tile_locations[last_variable].el['twos']
        actuals['3'] -= tile_locations[last_variable].el['threes']
        actuals['4'] -= tile_locations[last_variable].el['fours']

    del value_try_ordering[-1]
    del variable_try_ordering[-1]
    tile_locations_remaining.append(last_variable)

    if len(visited_states) > 0:
        print(visited_states[-1])


def format_output(result, tile_count):
    for i in range(tile_count):
        if i in result[0]:
            print(str(i) + ' 4 OUTER_BOUNDARY')
        elif i in result[1]:
            print(str(i) + ' 4 EL_SHAPE')
        else:
            print(str(i) + ' 4 FULL_BLOCK')
