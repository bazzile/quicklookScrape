# -*- coding: utf-8 -*-
import os
import time
from urllib import urlretrieve
import ogr
from attribute2wld import attr2wld

input_file = r"D:\GitHub\quicklookScrape\GE01_ImageLibraryStrips_2016\GE01_ImageLibraryStrips_2016.shp"
out_dir = r"D:\GitHub\quicklookScrape\database"

shapefile = ogr.Open(input_file)
layer = shapefile.GetLayer()
counter = 0
start_time = time.time()
for i in range(layer.GetFeatureCount()):
    if 9 < i < 16:
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
        img_name = CATALOGID + '.png'
        urlretrieve(img_url, os.path.join(out_dir, img_name))
        attr2wld(out_dir, CATALOGID, x, y)
        print(CATALOGID, img_url, max(x), max(y))
end_time = (time.time() - start_time)/60
print("Готово. %s квиклуков сгенерировано за %s минут" % (counter, end_time))

