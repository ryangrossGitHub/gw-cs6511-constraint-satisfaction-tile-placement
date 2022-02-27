import itertools

csp_complete = False


def filter_domains(tile_counts, tile_locations, targets):
    global csp_complete
    targets = [targets['1'], targets['2'], targets['3'], targets['4']]
    location_count = len(tile_locations)
    combos = {}

    # Print stats
    el_combos = itertools.combinations(range(location_count), tile_counts['EL_SHAPE'])
    el_combo_counts = sum(1 for ignore in el_combos)
    print(f"Total Combos EL_SHAPE: {el_combo_counts:,}")
    outer_combos = itertools.combinations(range(location_count), tile_counts['OUTER_BOUNDARY'])
    outer_combo_counts = sum(1 for ignore in outer_combos)
    print(f"Total Combos OUTER_BOUNDARY: {outer_combo_counts:,}")

    # itertools requires that we re-run this after the summations above, otherwise values are empty iterables
    combos['EL_SHAPE'] = itertools.combinations(range(location_count), tile_counts['EL_SHAPE'])
    combos['OUTER_BOUNDARY'] = itertools.combinations(range(location_count), tile_counts['OUTER_BOUNDARY'])

    mrv = None
    if el_combo_counts > outer_combo_counts:
        mrv = ['OUTER_BOUNDARY', 'EL_SHAPE']
    else:
        mrv = ['EL_SHAPE', 'OUTER_BOUNDARY']

    print("Minimum Remaining Values (MRV): " + mrv[0])

    print("Applying Forward Checking on MRV combos...")
    valid_mrv = apply_forward_check(combos[mrv[0]], tile_locations, [], targets, mrv[0], False)
    print(f"Total Combos MRV after Forward Check: {len(valid_mrv):,}")

    print("Applying Arc Consistency to remaining combos...")
    mrv_2_combos = list(combos[mrv[1]])
    for valid_lcv_combos in valid_mrv:
        updated_targets = [targets[0] - valid_lcv_combos[1][0], targets[1] - valid_lcv_combos[1][1],
                           targets[2] - valid_lcv_combos[1][2], targets[3] - valid_lcv_combos[1][3]]
        valid_full_combos = apply_forward_check(mrv_2_combos, tile_locations, valid_lcv_combos[0], updated_targets,
                                                mrv[1], True)
        if csp_complete:
            print("Solution found!")

            # Order Matters for Print function
            if mrv[0] == 'EL_SHAPE':
                return [valid_full_combos, valid_lcv_combos[0]]
            else:
                return [valid_lcv_combos[0], valid_full_combos]


def apply_forward_check(combos, tile_locations, reserved_tile_locations, targets, type, last_var):
    global csp_complete
    valid_combos = []
    for combo in combos:
        overlap = False
        for element in combo:
            if element in reserved_tile_locations:
                overlap = True
                break

        if not overlap:
            actuals = forward_check(combo, tile_locations, targets, type, last_var)
            if csp_complete:
                return combo
            elif actuals != -1:
                valid_combos.append([combo, actuals])

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
        return actuals
    elif constraint_not_violated(actuals, targets):
        return actuals
    else:
        return -1


def constraint_satisfied(actuals, targets):
    global csp_complete
    if actuals[0] == targets[0] and actuals[1] == targets[1] \
            and actuals[2] == targets[2] and actuals[3] == targets[3]:
        csp_complete = True
        return True
    else:
        return False


def constraint_not_violated(actuals, targets):
    if actuals[0] <= targets[0] and actuals[1] <= targets[1] \
            and actuals[2] <= targets[2] and actuals[3] <= targets[3]:
        return True
    else:
        return False


def format_output(result, grid_width, tile_count):
    output_variable_value_maps = []

    for i in range(tile_count):
        if i in result[0]:
            output_variable_value_maps.append({
                'variable': i,
                'value': '1'
            })
        elif i in result[1]:
            output_variable_value_maps.append({
                'variable': i,
                'value': '2'
            })
        else:
            output_variable_value_maps.append({
                'variable': i,
                'value': '3'
            })

    output_variable_value_maps.sort(key=lambda k: k['variable'])

    tile_width = 4
    grid_output = chunks(output_variable_value_maps, int(grid_width / tile_width))

    i = 0
    for column_index in range(int(grid_width / tile_width)):
        for row in grid_output:
            if row[column_index]['value'] == '1':
                print(str(i) + ' 4 OUTER_BOUNDARY')
            elif row[column_index]['value'] == '2':
                print(str(i) + ' 4 EL_SHAPE')
            elif row[column_index]['value'] == '3':
                print(str(i) + ' 4 FULL_BLOCK')
            i += 1


def chunks(original_list, size):
    chunked_list = []
    for i in range(0, len(original_list), size):
        chunked_list.append(original_list[i:i + size])

    return chunked_list