# -*- coding: utf-8 -*-
import os


def attr2wld(dirname, CATALOGID, x, y, resolution):
    a = str((max(x)-min(x))/resolution)
    b = '0'
    c = '0'
    d = str(-(max(y)-min(y))/resolution)
    e = str(min(x))
    f = str(max(y))

    with open(os.path.join(dirname, CATALOGID + '.wld'), 'w') as f_out:
        f_out.write('\n'.join((a, b, c, d, e, f)))

