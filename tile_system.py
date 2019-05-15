'''
@description:
This part is python3 implementation of Bing maps tile system.
Reference:
https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system
'''

from math import *

class TileSystem(object):
    EarthRadius = 6378137
    MinLatitude = -85.05112878
    MaxLatitude = 85.05112878
    MinLongitude = -180.
    MaxLongitude = 180.
    MaxLevel = 23
    TileSIZE = 256

    @staticmethod
    def clip(n, min_value, max_value):
        return min(max(n, min_value), max_value)

    @staticmethod
    def map_size(level_detail):
        return 256 << level_detail

    @staticmethod
    def ground_resolution(latitude, level_detail):
        latitude = TileSystem.clip(latitude, TileSystem.MinLongitude, TileSystem.MaxLongitude)
        return cos(latitude * pi / 180) * 2 * pi * TileSystem.EarthRadius / TileSystem.map_size(level_detail)

    @staticmethod
    def map_scale(latitude, level_detail, screen_dpi):
        return TileSystem.ground_resolution(latitude, level_detail) * screen_dpi / 0.0254

    @staticmethod
    def latlong_to_pixelxy(latitude, longitude, level_detail):
        latitude = TileSystem.clip(latitude, TileSystem.MinLatitude, TileSystem.MaxLatitude)
        longitude = TileSystem.clip(longitude, TileSystem.MinLongitude, TileSystem.MaxLongitude)

        x = (longitude + 180) / 360
        sin_latitude = sin(latitude * pi / 180)
        y = 0.5 - log((1 + sin_latitude) / (1 - sin_latitude)) / (4 * pi)

        mapsize = TileSystem.map_size(level_detail)

        return floor(TileSystem.clip(x * mapsize + 0.5, 0, mapsize - 1)), floor(TileSystem.clip(y * mapsize + 0.5, 0, mapsize - 1))

    @staticmethod
    def pixelxy_to_latlong(pixelX, pixelY, level_detail):
        mapsize = TileSystem.map_size(level_detail)
        x = (TileSystem.clip(pixelX, 0, mapsize - 1) / mapsize) -0.5
        y = 0.5 - (TileSystem.clip(pixelY, 0, mapsize - 1) / mapsize)

        return 90 - 360 * atan(exp(-y * 2 * pi)) / pi, 360 * x

    @staticmethod
    def pixelxy_to_tilexy(pixelX, pixelY):
        return floor(pixelX / 256), floor(pixelY / 256)

    @staticmethod
    def tilexy_to_pixelxy(tileX, tileY):
        return tileX * 256, tileY * 256

    @staticmethod
    def tilexy_to_quadkey(tileX, tileY, level_detail):
        quadkey = ""
        for i in range(level_detail, 0, -1):
            digit = '0'
            mask = 1 << (i-1)
            if (tileX & mask) != 0:
                digit = chr(ord(digit) + 1)
            if (tileY & mask) != 0:
                digit = chr(ord(digit) + 2)
            quadkey += digit

        return quadkey

    @staticmethod
    def quadkey_to_tilexy(quadkey):
        pass




