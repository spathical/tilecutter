import mercantile
import time
import re
import sys
import collections

input = (-122.094727, 37.390260)

ZOOM = 12

Bounds = collections.namedtuple('Bounds', ['min_x', 'min_y', 'max_x', 'max_y'])

def poly2latlng(polyfile):
    """Parse lng, lat co-ordinates from polyfile"""
    with open(polyfile) as f:
        coordinates = f.readlines()[2:][:-2]
        coordinates = [re.split(r'[\s\t]+', item) for item in coordinates]
        coordinates = [list(filter(None, item)) for item in coordinates]
        coordinates = [(float(item[0]), float(item[1])) for item in coordinates]
    return coordinates


def bounding_tiles(coordinates, zoom=ZOOM):
    """return the bounds that we care about"""
    min_x = sys.maxint
    min_y = sys.maxint
    max_x = -1
    max_y = -1
    for c in coordinates:
        tile = mercantile.tile(c[0], c[1], zoom)
        if min_x > tile.x:
            min_x = tile.x
        if min_y > tile.y:
            min_y = tile.y
        if max_x < tile.x:
            max_x = tile.x
        if max_y < tile.y:
            max_y = tile.y
    return Bounds(min_x, min_y, max_x, max_y)

def tiles(boundingbox, zoom=ZOOM):
    for x in range(boundingbox.min_x, boundingbox.max_x + 1):
        for y in range(boundingbox.min_y, boundingbox.max_y + 1):


if __name__ == '__main__':
    print "**Start**"
    start = time.time()
    coordinates = poly2latlng('./resources/california.poly')
    b = bounding_tiles(coordinates)
    print b
