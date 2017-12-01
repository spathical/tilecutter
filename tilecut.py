import mercantile
import time
import re
import sys
import collections
import os
import shutil

from subprocess import call

input = (-122.434966, 37.762864)

ZOOM = 12

Bounds = collections.namedtuple('Bounds', ['min_x', 'min_y', 'max_x', 'max_y'])

VERSION = 1

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

def tiles(pbf_filename, boundingbox, zoom=ZOOM):
    with open(pbf_filename) as f:
        i = 1
        for x in range(boundingbox.min_x, boundingbox.max_x + 1):
            for y in range(boundingbox.min_y, boundingbox.max_y + 1):
                out_dir = "./tiles/" + str(VERSION) + "/" + str(zoom) + "/" + str(y) + "/" + str(x)
                os.makedirs(out_dir)
                filename = out_dir + "/" + str(x) + "_" + str(y) + "_" + str(zoom) + ".pbf"
                bbox = mercantile.bounds(x, y, zoom)
                bbox_latlng = ",".join(map(str, [bbox.west, bbox.south, bbox.east, bbox.north]))
                call(["osmconvert", "./resources/sf.osm.pbf", "-b=" + bbox_latlng, "-o=" + filename])


def lookup_tile(lng, lat, zoom=ZOOM):
    tile = mercantile.tile(lng, lat, zoom)
    out_dir =  "./tiles/" + str(VERSION) + "/" + str(zoom) + "/" + str(tile.y) + "/" + str(tile.x)
    filename = out_dir + "/" + str(tile.x) + "_" + str(tile.y) + "_" + str(zoom) + ".pbf"
    return filename

if __name__ == '__main__':
    print "**Start**"
    if os.path.exists('./tiles'):
        shutil.rmtree('./tiles')
    start = time.time()
    coordinates = poly2latlng('./resources/sf.poly')
    bounds = bounding_tiles(coordinates)
    tiles('resources/sf.osm.pbf', bounds)
    end = time.time()
    print "Tile generation took ", int(end - start), "seconds"
    print  "Tile is", lookup_tile(input[0], input[1])
