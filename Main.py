# -*- coding: utf-8 -*-
import os
import time
from PIL import Image
from hurry.filesize import size
from urllib.request import urlretrieve
import ogr
from attribute2wld import attr2wld

input_file = r"E:\Geoportal\ShapesDB\unZipped\WV03_ImageLibraryStrips_2015.shp"

out_dir = os.path.join("E:\Geoportal\ShapesDB\QuickLooks_from_unZipped", os.path.basename(input_file).split('.')[0])
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

shapefile = ogr.Open(input_file)
layer = shapefile.GetLayer()
counter = 0
bad_ql_list = []
start_time = time.time()
for i in range(layer.GetFeatureCount()):
    x, y = [], []
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
    # пропускаем скачанные снимки
    if os.path.isfile(os.path.join(out_dir, CATALOGID + '.jpg')):
        print('{} уже скачан, пропускаем'.format(CATALOGID + '.jpg'))
        continue
    img_name = CATALOGID + '.png'
    urlretrieve(img_url, os.path.join(out_dir, img_name))
    png_image = Image.open(os.path.join(out_dir, img_name))
    # конвертируем png в jpeg и удаляем оригинал
    png_image.save(os.path.join(out_dir, img_name).replace('.png', '.jpg'), 'JPEG', quality=85)
    os.remove(os.path.join(out_dir, img_name))
    attr2wld(out_dir, CATALOGID, x, y)
    print(i + 1, CATALOGID, size(os.path.getsize(os.path.join(out_dir, img_name).replace('.png', '.jpg'))))
end_time = (time.time() - start_time)/60
print("Готово. %s квиклуков сгенерировано за %s минут" % (counter, end_time))

