class Building:

    def __init__(self, building_type, x, y):
        self.type = building_type
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y
