class BuildingType:

    def __init__(self, building_type, t_pos, size, door_pos):
        self.building_type = building_type
        self.t_pos = t_pos
        self.size = size
        self.door_pos = door_pos

    def __str__(self):
        return "Building: " + ', '.join("%s=%s" % item for item in vars(self).items())
