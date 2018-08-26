import time

import cv2

from redis_helper import get_redis
from worker.app import celery_app

OUTPUT_PATH = '/tmp/vid-instance{}/Frame{}.jpg'


@celery_app.task(name='split_video_to_frames', ignore_result=True)
def split_video_to_frames(path, instance_num):
    video_capture = cv2.VideoCapture(path)
    success, image = video_capture.read()
    count = 0
    success = True
    redis = get_redis()
    redis_key = 'instance_{}'.format(instance_num)
    start = time.time()
    current = {}
    while success:
        out_put_file = OUTPUT_PATH.format(instance_num, str(count).zfill(5))
        cv2.imwrite(out_put_file, image)
        success, image = video_capture.read()
        celery_app.send_task('resize', [out_put_file])
        count += 1
        if int(time.time() - start) / 60:
            start = time.time()
            redis.set(redis_key, count - current)
            current = count

        redis.set(redis_key, 'completed')
