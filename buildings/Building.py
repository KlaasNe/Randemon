class Building:

    def __init__(self, building_type, x, y):
        self.type = building_type
        self.x = x
        self.y = y

    def __str__(self):
        return ', '.join("%s=%s" % item for item in vars(self).items())

    def get_pos(self):
        return self.x, self.y

    def get_abs_door_pos(self):
        # +1 in door pos y because this is the square below the door
        return self.x + self.type.door_pos[0], self.y + self.type.door_pos[1] + 2
