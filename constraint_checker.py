def constraint_satisfied(actuals, targets):
    if actuals[0] == targets[0] and actuals[1] == targets[1] \
            and actuals[2] == targets[2] and actuals[3] == targets[3]:
        return True
    else:
        return False


def constraint_not_violated(actuals, targets):
    if actuals[0] <= targets[0] and actuals[1] <= targets[1] \
            and actuals[2] <= targets[2] and actuals[3] <= targets[3]:
        return True
    else:
        return False
