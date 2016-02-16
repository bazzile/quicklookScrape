# -*- coding: utf-8 -*-
import os
import ogr

input_file = r"E:\Geoportal\Imagery\GE01_ImageLibraryStrips_2016\GE01_ImageLibraryStrips_2016.shp"
shapefile = ogr.Open(input_file)
layer = shapefile.GetLayer()
counter = 0
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    CATALOGID = feature.GetField('CATALOGID')
    counter += 1
    print(CATALOGID)
print(counter)
# TODO извлечь координаты всех углов снимка
# TODO рассчитать wld - файл