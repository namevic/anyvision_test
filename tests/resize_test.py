import argparse
import os
import sys

from worker.app import celery_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--instances', help='instances', required=True)
    parser.add_argument('-m', '--countdown', help='seconds', required=True)
    current_path = os.path.dirname(os.path.realpath(__file__))
    arguments = vars(parser.parse_args(sys.argv[1:]))
    for dirpath, dirnames, filenames in os.walk(os.path.join(current_path, 'videos_to_split')):
        for i, filename in enumerate(filenames):
            if i == arguments['instances']:
                break
            countdown = 0 if not i else arguments['countdown']
            celery_app.send_task('split_video_to_frames', [os.path.join(dirpath, filename), i],
                                 countdown=countdown)


if __name__ == "__main__":
    main()
