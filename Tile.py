class Tile:
    def __init__(self, index):
        self.index = index
        self.el = None
        self.outer = None

    def set_el_response(self, ones, twos, threes, fours):
        self.el = {'ones': ones, 'twos': twos, 'threes': threes, 'fours': fours}

    def set_outer_response(self, ones, twos, threes, fours):
        self.outer = {'ones': ones, 'twos': twos, 'threes': threes, 'fours': fours}
