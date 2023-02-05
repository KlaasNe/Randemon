class WeightTile:

    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight
        self.dist = 999999
        self.visited = False
        self.prev = None

    def __gt__(self, other):
        return self.dist > other.dist

    def __lt__(self, other):
        return self.dist < other.dist

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "WeightTile: " + "x={}, y={}, weight={}, dist={}, visited={}".format(self.x, self.y, self.weight, self.dist, self.visited)

    def __hash__(self):
        return hash((self.x, self.y))

    def get_pos(self):
        return self.x, self.y
