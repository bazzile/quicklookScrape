# -*- coding: utf-8 -*-
import os
import time
import shutil
from hurry.filesize import size
from urllib.request import urlretrieve
import ogr
from attribute2wld import attr2wld

# input_file = r"E:\Geoportal\ShapesDB\temp\WV03_cl15_mos.shp"
input_file = r"E:\!Go\YarTask\DG_dm2014_для скачки qlooks\dg2014_for_vasya.shp"
# out_dir = r"E:\Geoportal\Imagery\database\test"
out_dir = r"E:\!Go\YarTask\DG_dm2014_для скачки qlooks\quick_looks"

crs_file = r"E:\Geoportal\Imagery\database\source_crs.prj"

shapefile = ogr.Open(input_file)
layer = shapefile.GetLayer()
counter = 0
bad_ql_list = []
start_time = time.time()
for i in range(layer.GetFeatureCount()):
    x = []
    y = []
    feature = layer.GetFeature(i)
    CATALOGID = feature.GetField("CATALOGID")

    for index in ['x1', 'x2', 'x3', 'x4']:
        x.append(feature.GetField(index))
    # if not (29 < int(min(x)) < 45):
    #     continue

    for index in ['y1', 'y2', 'y3', 'y4']:
        y.append(feature.GetField(index))

    # if not (52 < int(max(y)) < 67):
    #     continue

    img_url = 'https://browse.digitalglobe.com/imagefinder/showBrowseImage?catalogId=' + CATALOGID + '&imageHeight=natres&imageWidth=natres'
    # &imageHeight=1024&imageWidth=1024 - для 1024 * 1024 разрешения (работает только тогда, когда высота < ширины)
    # 512 * 512 работает без пересчёта разрешения?
    counter += 1
    img_name = CATALOGID + '.png'
    # пропускаем скачанные снимки
    if os.path.isfile(os.path.join(out_dir, img_name)):
        print('{} уже скачан, пропускаем'.format(img_name))
        continue
    urlretrieve(img_url, os.path.join(out_dir, img_name))
    attr2wld(out_dir, CATALOGID, x, y)
    shutil.copy(crs_file, os.path.join(out_dir, CATALOGID + '.prj'))
    print(i + 1, CATALOGID, size(os.path.getsize(os.path.join(out_dir, img_name))))
end_time = (time.time() - start_time)/60
print("Готово. %s квиклуков сгенерировано за %s минут" % (counter, end_time))

