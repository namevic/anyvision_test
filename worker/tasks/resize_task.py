from __future__ import absolute_import, unicode_literals

import os

from PIL import Image

from worker.app import celery_app


@celery_app.task(name='resize', ignore_result=True)
def resize(path):
    size = 128, 128

    outfile = os.path.splitext(path)[0] + 'resize.jpg'
    if path != outfile:
        try:
            im = Image.open(path)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, 'JPEG')
        except IOError:
            print 'cannot create thumbnail for {}'.format(path)
