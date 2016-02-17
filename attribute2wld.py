# -*- coding: utf-8 -*-
import os
from PIL import Image


def attr2wld(dirname, CATALOGID, x, y):
    im = Image.open(os.path.join(dirname, CATALOGID + '.png'))
    width = im.size[0]
    height = im.size[1]
    a = str((max(x)-min(x))/width)
    b = '0'
    c = '0'
    d = str(-(max(y)-min(y))/height)
    e = str(min(x))
    f = str(max(y))

    with open(os.path.join(dirname, CATALOGID + '.wld'), 'w') as f_out:
        f_out.write('\n'.join((a, b, c, d, e, f)))

