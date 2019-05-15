'''
@description:
This part is applied to Satellite/Aerial Image Retrieval system based on title system from bing map.
'''
from tile_system import *
import os
import sys
from PIL import Image
import urllib.request
from tile_system import TileSystem as ts

class RetrievalSystem(object):

    base_url = 'http://h0.ortho.tiles.virtualearth.net/tiles/h'

    # license key was created from https://www.bingmapsportal.com/Application#
    license_key = 'AkddKdzZuMezszzoxbyA-sDsMyAoy-yEDsHHswdJLB8y3Ni8C3V74imCk2zfEkYw'

    max_canvas_size = 8192 * 8192 * 8

    def __init__(self, lat1, lon1, lat2, lon2):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2

    def get_quadkey(self, tileX, tileY, level):
        return ts.tilexy_to_quadkey(tileX, tileY, level)

    def download_image(self, quadkey):
        #print('download with quadkey: ' + str(quadkey))
        url = self.base_url + quadkey + ".jpeg?g=131&key=" + self.license_key
        with urllib.request.urlopen(url) as file:
            return Image.open(file)

    def null_verify(self, image):
        if not os.path.exists('null.png'):
            null_image = self.download_image('1111111111111111111111')
            null_image.save('./null.png')
        return not image == Image.open('./null.png')

    def get_max_resolution(self):
        for level in range(ts.MaxLevel, 0, -1):
            pixelX1, pixelY1 = ts.latlong_to_pixelxy(self.lat1, self.lon1, level)
            pixelX2, pixelY2 = ts.latlong_to_pixelxy(self.lat2, self.lon2, level)

            # Set coordinates as upper-left (X1,Y1) and lower-right (X2, Y2)
            pixelX1, pixelX2 = min(pixelX1, pixelX2), max(pixelX1, pixelX2)
            pixelY1, pixelY2 = min(pixelY1, pixelY2), max(pixelY1, pixelY2)

            #print(level,'  ', pixelX1, '  ', pixelX2, '  ', pixelY1, '  ', pixelY2)

            if abs(pixelX1 - pixelX2) <= 1 or abs(pixelY1 - pixelY2) <= 1:
                return

            if abs(pixelX2-pixelX1) * abs(pixelY2 - pixelY1) > self.max_canvas_size:
                print('size not match at level ', level)
                continue


            # convert to tile coordinate
            tileX1, tileY1 = ts.pixelxy_to_tilexy(pixelX1, pixelY1)
            tileX2, tileY2 = ts.pixelxy_to_tilexy(pixelX2, pixelY2)

            #print(pixelX1, pixelX2, pixelY1, pixelY2)
            #print(tileX1, tileX2, tileY1, tileY2)

            result = self.retrieve_by_tile(tileX1,tileX2,tileY1,tileY2,level)

            if not result:
                print('retrieval failed at level ', level)
                continue
            else:
                result.save('semi-result.png')
                # recheck the right range of output
                leftup_cornerX, leftup_cornerY = ts.tilexy_to_pixelxy(tileX1, tileY1)
                rresult = result.crop((pixelX1 - leftup_cornerX, pixelY1 - leftup_cornerY, pixelX2 - leftup_cornerX, pixelY2 - leftup_cornerY))
                rresult.save('result.png')
                print('retrieve successfully')
                return

    def retrieve_by_tile(self,tileX1, tileX2, tileY1, tileY2, level):
        flag = True
        target = []

        result = Image.new('RGB', ((tileX2 - tileX1 + 1) * ts.TileSIZE, (tileY2 - tileY1 + 1) * ts.TileSIZE))
        # retrieve tile one by one
        for y in range(tileY1, tileY2 + 1):
            horizontal_tile_image = []
            horizontal_target = Image.new('RGB', ((tileX2 + 1 - tileX1) * ts.TileSIZE, ts.TileSIZE))
            for x in range(tileX1, tileX2 + 1):
                #print(x, y, level)
                quadkey = self.get_quadkey(x, y, level)
                #print(quadkey)
                image = self.download_image(quadkey)
                if self.null_verify(image):
                    horizontal_tile_image.append(image)
                    #print('horizontal_tile_image size is ', len(horizontal_tile_image))
                else:
                    return None
            if not flag:
                print('falsefalsefalsefalse')
                return
            else:
                for index, tile in enumerate(horizontal_tile_image):
                    horizontal_target.paste(tile, (index * ts.TileSIZE, 0))

            target.append(horizontal_target)

        if target:
            for index, horizontal_result in enumerate(target):
                result.paste(horizontal_result, (0, (index * ts.TileSIZE)))
        else:
            print('lost target')
        return result

    @staticmethod
    def fault(self, message):
        if message == 'same pixel':
            print("input coordinates invalid")
        if message == 'memory error':
            print("too large pixel size")


def main():
    try:
        args = sys.argv[1:]
    except KeyboardInterrupt:
        return
    except Exception:
        sys.exit('EEEEEEEEError!!!!!!!!!!!!!!!')

    try:
        lat1, lon1, lat2, lon2 = float(args[0]), float(args[1]), float(args[2]), float(args[3])
    except ValueError:
        sys.exit('invalid input')
    print('valid input')
    # 41.893812 -87.615195 41.885108 -87.597778
    retrieve_system = RetrievalSystem(lat1, lon1, lat2, lon2)
    print('initialization completed')
    retrieve_system.get_max_resolution()
    print('made it!!!!!!!!!!!!!')


if __name__ == '__main__':
    main()




