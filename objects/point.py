class Point:
    def __init__(self, pixel, coord_baricentrica, coord_original):
        self.pixel = pixel
        self.coord_baricentrica = coord_baricentrica
        self.p_original = coord_original
        self.normal = None
