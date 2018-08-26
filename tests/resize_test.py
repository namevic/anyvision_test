import argparse
import os
import sys
import time

from redis_helper import get_redis
from worker.app import celery_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--instances', help='instances', required=True)
    parser.add_argument('-m', '--countdown', help='seconds', required=True)
    current_path = os.path.dirname(os.path.realpath(__file__))
    arguments = vars(parser.parse_args(sys.argv[1:]))
    start_times = {}
    for dirpath, dirnames, filenames in os.walk(os.path.join(current_path, 'videos_to_split')):
        for instance, filename in enumerate(filenames[:arguments['instances']]):
            countdown = 0 if not instance else arguments['countdown']
            start_times[instance] = time.time()
            celery_app.send_task('split_video_to_frames', [os.path.join(dirpath, filename), instance],
                                 countdown=countdown)
    redis = get_redis()
    while True:
        for instance in range(arguments['instances']):
            start = time.time()
            redis_key = 'instance_'.format(instance)
            instance_data = redis.get(redis_key)
            template = None
            if instance_data == 'completed':
                total_time = time.time() - start_times[instance]
                template = 'Instance {{}} finished spliting total time {} seconds'.format(total_time)
            elif int(time.time() - start) / 60:
                template = 'Instance {} split rpm {}'
            if template:
                template.format(instance, instance_data)


if __name__ == "__main__":
    main()
