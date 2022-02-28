import itertools

from forward_check import apply_forward_check
from global_vars import get_csp_complete
from least_constrained_value import get_lcv_order
from minimum_remaining_values import get_mvr


def filter_domains(tile_counts, tile_locations, targets):
    targets = [targets['1'], targets['2'], targets['3'], targets['4']]
    location_count = len(tile_locations)

    el_combo_counts = get_combo_count(location_count, tile_counts, 'EL_SHAPE')
    outer_combo_counts = get_combo_count(location_count, tile_counts, 'OUTER_BOUNDARY')

    combos = {'EL_SHAPE': itertools.combinations(range(location_count), tile_counts['EL_SHAPE']),
              'OUTER_BOUNDARY': itertools.combinations(range(location_count), tile_counts['OUTER_BOUNDARY'])}

    mrv = get_mvr(el_combo_counts, outer_combo_counts)
    print("Minimum Remaining Values (MRV): " + mrv[0])

    print("Applying Forward Checking on MRV combos...")
    valid_mrv = apply_forward_check(combos[mrv[0]], tile_locations, [], targets, mrv[0], False)
    print(f"Total Combos MRV after Forward Check: {len(valid_mrv):,}")

    get_lcv_order(valid_mrv)

    return enforce_consistency(combos, targets, valid_mrv, mrv, tile_locations)


def enforce_consistency(combos, targets, valid_mrv, mrv, tile_locations):
    print("Applying Arc Consistency to remaining combos...")
    mrv_2_combos = list(combos[mrv[1]])
    for valid_lcv_combos in valid_mrv:
        updated_targets = [targets[0] - valid_lcv_combos[1][0], targets[1] - valid_lcv_combos[1][1],
                           targets[2] - valid_lcv_combos[1][2], targets[3] - valid_lcv_combos[1][3]]
        valid_full_combos = apply_forward_check(mrv_2_combos, tile_locations, valid_lcv_combos[0], updated_targets,
                                                mrv[1], True)
        if get_csp_complete():
            print("Solution found!")

            # Order Matters for Print function
            if mrv[0] == 'EL_SHAPE':
                return [valid_full_combos, valid_lcv_combos[0]]
            else:
                return [valid_lcv_combos[0], valid_full_combos]


def get_combo_count(location_count, tile_counts, type):
    combos = itertools.combinations(range(location_count), tile_counts[type])
    combo_counts = sum(1 for ignore in combos)
    print(f"Total Combos {type}: {combo_counts:,}")
    return combo_counts


