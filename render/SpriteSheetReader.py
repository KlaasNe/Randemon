from PIL import ImageOps


class SpriteSheetReader:
    TILE_SIZE = 16

    def __init__(self, image, margin=0):
        self.sprite_sheet = image
        self.margin = margin

    def get_tile(self, tile_x, tile_y, mirror, size_x=TILE_SIZE, size_y=TILE_SIZE):
        pos_x = (size_x * tile_x) + (self.margin * (tile_x + 1))
        pos_y = (size_y * tile_y) + (self.margin * (tile_y + 1))
        box = (pos_x, pos_y, pos_x + size_x, pos_y + size_y)
        return ImageOps.mirror(self.sprite_sheet.crop(box)) if mirror else self.sprite_sheet.crop(box)
