#!/usr/bin/python
# -*- coding: utf-8 -*-
import progressbar
import time
import os
import requests
from PIL import Image
import io
from tempfile import TemporaryFile
import shutil


from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, AdaptiveETA, AbsoluteETA, AdaptiveTransferSpeed

img_url = 'https://browse.digitalglobe.com/imagefinder/showBrowseImage?catalogId=104001000C880D00&imageHeight=natres&imageWidth=natres'
out_dir = r"E:\!"

# TODO убрать или видоизменить функцию, добавить filename после 'Загружаем: ' Объём файла тоже можно отображать


def downloader():
    widgets = ['Загружаем: ', Percentage(), ' ',
               Bar(marker='=', left='[', right=']'),
               ' ', ETA(), ' ', FileTransferSpeed()]
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        length = int(r.headers['Content-Length'])
        pbar = ProgressBar(widgets=widgets, max_value=length)
        pbar.start()
        with TemporaryFile() as tempf:
            downloaded = 0
            for chunk in r.iter_content(1024):
                downloaded += len(chunk)
                pbar.update(downloaded)
                tempf.write(chunk)
            pbar.finish()
            i = Image.open(tempf)
            i.save(os.path.join(out_dir, 'image.jpg'), quality=85)

downloader()
