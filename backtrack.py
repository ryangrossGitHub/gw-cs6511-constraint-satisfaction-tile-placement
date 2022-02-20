# Actual counts as apposed to target counts
actuals = {'1': 0, '2': 0, '3': 0, '4': 0}


def constraint_satisfied(targets):
    if actuals['1'] >= targets['1'] and actuals['2'] >= targets['2'] \
            and actuals['3'] >= targets['3'] and actuals['4'] >= targets['4']:
        return True
    else:
        return False


def backtrack(tile_counts, tile_locations, targets):
    return ''
