def get_lcv_order(combos):
    print("Sorting MRV combos into Least Constrained Value (LCV) order...")
    combos.sort(key=lambda k: k[2], reverse=True)
