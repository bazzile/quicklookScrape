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


def example4():
    widgets = ['Test: ', Percentage(), ' ',
               Bar(marker='=', left='[', right=']'),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, max_value=500)
    pbar.start()
    for i in range(100, 500 + 1, 50):
        time.sleep(0.001)
        pbar.update(i)
    pbar.finish()


r = requests.get(img_url, stream=True)
if r.status_code == 200:
    length = int(r.headers['Content-Length'])
    with TemporaryFile() as tempf:
        for chunk in r.iter_content(1024):
            length -= len(chunk)
            print(length)
            tempf.write(chunk)
        i = Image.open(tempf)
        i.save(os.path.join(out_dir, 'image.jpg'), quality=85)
