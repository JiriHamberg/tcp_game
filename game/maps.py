import random

class Map(object):
    def __init__(self, player_list):
        self.players = player_list
        self.grid = GridFactory.generate_map(player_count=player_count)
        assert(len(player_list) == 2)
    def update(self):


class GridFactory(object):
    @staticmethod
    def generate_map(self, w=10, h=10, player_count=2):
        grid = []
        for h in range(0, n):
            grid[h] = ['r'] * w
        grid[0][random.randint(0, w - 1)] = 'p'
        grid[n - 1][random.randint(0, w - 1)] = 'p'
        return grid