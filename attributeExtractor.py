# -*- coding: utf-8 -*-
import os
import ogr

input_file = r"E:\GitHub\geoportal\quicklookScrape\GE01_ImageLibraryStrips_2016\GE01_ImageLibraryStrips_2016.shp"
shapefile = ogr.Open(input_file)
layer = shapefile.GetLayer()
counter = 0
for i in range(layer.GetFeatureCount()):
    if i < 1:
        x = []
        y = []
        feature = layer.GetFeature(i)
        CATALOGID = feature.GetField("CATALOGID")
        BROWSEURL = feature.GetField("BROWSEURL")

        for index in ['x1', 'x2', 'x3', 'x4']:
            x.append(feature.GetField(index))

        for index in ['y1', 'y2', 'y3', 'y4']:
            y.append(feature.GetField(index))


        counter += 1
        print(CATALOGID, BROWSEURL, max(x), max(y))
print(counter)
# TODO рассчитать wld - файл
