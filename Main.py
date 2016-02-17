# -*- coding: utf-8 -*-
import os
from urllib import urlretrieve
import ogr
from attribute2wld import attr2wld

input_file = r"E:\GitHub\geoportal\quicklookScrape\GE01_ImageLibraryStrips_2016\GE01_ImageLibraryStrips_2016.shp"
out_dir = r"E:\Geoportal\Imagery\database"

shapefile = ogr.Open(input_file)
layer = shapefile.GetLayer()
counter = 0
for i in range(layer.GetFeatureCount()):
    if i == 7:
        x = []
        y = []
        feature = layer.GetFeature(i)
        CATALOGID = feature.GetField("CATALOGID")
        BROWSEURL = feature.GetField("BROWSEURL")

        for index in ['x1', 'x2', 'x3', 'x4']:
            x.append(feature.GetField(index))

        for index in ['y1', 'y2', 'y3', 'y4']:
            y.append(feature.GetField(index))

        img_url = 'https://browse.digitalglobe.com/imagefinder/showBrowseImage?catalogId=' + CATALOGID + '&imageHeight=natres&imageWidth=natres'
        # &imageHeight=1024&imageWidth=1024 - для 1024 * 1024 разрешения (работает только тогда, когда высота < ширины)
        # 512 * 512 работает без пересчёта разрешения?
        counter += 1
        print(CATALOGID, img_url, max(x), max(y))

        # resolution = 1024
        print((max(x)-min(x))/1280)
        print('0')
        print('0')
        print(-(max(y)-min(y))/7397)
        print(min(x))
        print(max(y))

        print(x[0], y[0])
        print(x[1], y[1])
        print(x[2], y[2])
        print(x[3], y[3])

        print(BROWSEURL)

# print(counter)
urlretrieve(img_url, os.path.join(out_dir, CATALOGID + '.png'))
attr2wld(out_dir, CATALOGID, x, y, 1024)
