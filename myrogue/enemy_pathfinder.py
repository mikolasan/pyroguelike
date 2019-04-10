import math
from astar import AStar


class EnemyPathfinder(AStar):
    """sample use of the astar algorithm. In this exemple we work on a maze
    made of ascii characters, and a 'node' is just a (x,y) tuple that
    represents a reachable position
    """

    def __init__(self, tiled_map, position):
        self.tiled_map = tiled_map
        self.position = position
        self.radius = 5
        self.test_tile_wall = lambda x, y: self.tiled_map.layers[0].data[y][x] in [1,2]
        self.width = tiled_map.width
        self.height = tiled_map.height

    def heuristic_cost_estimate(self, n1, n2):
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = n1
        (x2, y2) = n2
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adjacent
        """
        return 1

    def test_tile_normal(self, x, y):
        r = self.radius
        cx = self.position[0] // 48
        cy = self.position[1] // 48
        return (cx - r <= x < cx + r
                and cy - r <= y < cy + r
                and 0 <= x < self.width
                and 0 <= y < self.height
                and not self.test_tile_wall(x, y))

    def neighbors(self, node):
        """ for a given coordinate in the maze, returns up to 4 adjacent
        (north,east,south,west) nodes that can be reached (=any adjacent
        coordinate that is not a wall)
        """
        x, y = node
        return [(ax, ay) for ax, ay in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if self.test_tile_normal(ax, ay)]
