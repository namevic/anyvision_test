from __future__ import absolute_import

from celery import Celery

from config.settings import rabbit_mq

BROKER_STRING = '{protocol}://{username}:{password}@{host}:{port}/{vhost}'.format(**rabbit_mq)

celery_app = Celery('celery_app',
                    broker=BROKER_STRING,
                    backend='amqp://',
                    include=['tasks.resize_task', 'tasks.split_video_to_frames'])

celery_app.conf.update(result_expires=3600,
                       task_serializer='pickle',
                       accept_content=['pickle', 'json'],
                       result_serializer='pickle'
                       )

if __name__ == '__main__':
    celery_app.start()
