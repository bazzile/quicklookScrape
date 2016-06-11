# -*- coding: utf-8 -*-
import os
import time
from PIL import Image
from hurry.filesize import size
import requests
from tempfile import TemporaryFile
import ogr
from attribute2wld import attr2wld
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, AdaptiveETA, AbsoluteETA, AdaptiveTransferSpeed


input_file = r"E:\Geoportal\ShapesDB\unZipped\WV03_ImageLibraryStrips_2015.shp"

out_dir = os.path.join(r"E:\Geoportal\ShapesDB\QuickLooks_from_unZipped", os.path.basename(input_file).split('.')[0])
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

shapefile = ogr.Open(input_file)
layer = shapefile.GetLayer()
counter = 0
start_time = time.time()
files_to_download = layer.GetFeatureCount()
for i in range(layer.GetFeatureCount()):
    x, y = [], []
    feature = layer.GetFeature(i)
    CATALOGID = feature.GetField("CATALOGID")
    img_name = CATALOGID + '.jpg'

    for index in ['x1', 'x2', 'x3', 'x4']:
        x.append(feature.GetField(index))

    for index in ['y1', 'y2', 'y3', 'y4']:
        y.append(feature.GetField(index))

    img_url = 'https://browse.digitalglobe.com/imagefinder/showBrowseImage?catalogId=' + \
              CATALOGID + '&imageHeight=natres&imageWidth=natres'
    # &imageHeight=1024&imageWidth=1024 - для 1024 * 1024 разрешения (работает только тогда, когда высота < ширины)
    # 512 * 512 работает без пересчёта разрешения?
    counter += 1
    # пропускаем скачанные снимки
    if os.path.isfile(os.path.join(out_dir, img_name)):
        print('{} уже скачан, пропускаем'.format(img_name))
        continue
    print('Запрашиваю квиклук {} из {}...'.format(counter, files_to_download))
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        file_size = int(r.headers['Content-Length'])
        widgets = ['Ход загрузки: ', Percentage(), ' ',
                   Bar(marker='=', left='[', right=']'),
                   ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, max_value=file_size)
        with TemporaryFile() as tempf:
            pbar.start()
            downloaded = 0
            # скачиваем файл по кускам в 1024 байта (chunks)
            for chunk in r.iter_content(1024):
                downloaded += len(chunk)
                pbar.update(downloaded)
                tempf.write(chunk)
            pbar.finish()
            # на лету конвертируем изначально полученный png в jpg
            i = Image.open(tempf)
            i.save(os.path.join(out_dir, img_name), quality=85)
            attr2wld(out_dir, CATALOGID, x, y)
            print('{} готов. Размер = {}'.format(
                img_name, size(os.path.getsize(os.path.join(out_dir, img_name)))))
end_time = (time.time() - start_time)/60
print("Готово. %s квиклуков сгенерировано за %s минут" % (counter, end_time))
