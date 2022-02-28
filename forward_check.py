from constraint_checker import constraint_satisfied, constraint_not_violated
from global_vars import set_csp_complete, get_csp_complete


def apply_forward_check(combos, tile_locations, reserved_tile_locations, targets, type, last_var):
    valid_combos = []
    for combo in combos:
        overlap = False
        for element in combo:
            if element in reserved_tile_locations:
                overlap = True
                break

        if not overlap:
            actuals = forward_check(combo, tile_locations, targets, type, last_var)
            if get_csp_complete():
                return combo
            elif actuals != -1:
                min_delta = min([targets[0] - actuals[0], targets[1] - actuals[1], targets[2] - actuals[2],
                                 targets[3] - actuals[3]])
                valid_combos.append([combo, actuals, min_delta])

    return valid_combos


def forward_check(combo, tile_locations, targets, type, last_var):
    actuals = [0, 0, 0, 0]
    for location in combo:
        if type == 'EL_SHAPE':
            actuals[0] += tile_locations[location].el['ones']
            actuals[1] += tile_locations[location].el['twos']
            actuals[2] += tile_locations[location].el['threes']
            actuals[3] += tile_locations[location].el['fours']
        else:
            actuals[0] += tile_locations[location].outer['ones']
            actuals[1] += tile_locations[location].outer['twos']
            actuals[2] += tile_locations[location].outer['threes']
            actuals[3] += tile_locations[location].outer['fours']

    if last_var and constraint_satisfied(actuals, targets):
        set_csp_complete(True)
        return actuals
    elif constraint_not_violated(actuals, targets):
        return actuals
    else:
        return -1