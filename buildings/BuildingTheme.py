from random import choices


class BuildingTheme:

    def __init__(self, theme):
        self.theme = theme

    def __str__(self):
        return '\n'.join(
            "Building: " + ', '.join("%s=%s" % item for item in vars(building_type).items())
            for building_type in self.theme.keys()
        )

    def get_random_building_type(self, weighted=True):
        return choices(list(self.theme), weights=self.theme.values() if weighted else None)[0]
