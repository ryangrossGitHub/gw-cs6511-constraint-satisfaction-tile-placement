def get_mvr(el_combo_counts, outer_combo_counts):
    mrv = None
    if el_combo_counts > outer_combo_counts:
        mrv = ['OUTER_BOUNDARY', 'EL_SHAPE']
    else:
        mrv = ['EL_SHAPE', 'OUTER_BOUNDARY']

    return mrv
