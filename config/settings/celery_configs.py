from datetime import timedelta

from decouple import config

broker_connection_retry_on_startup = True

broker_url = config('CELERY_BROKER_URL')
result_backend = config('CELERY_BROKER_URL')

worker_prefetch_multiplier = 3

timezone = config('CELERY_TIMEZONE')

task_serializer = 'pickle'
result_serializer = 'json'
accept_content = ['json', 'json', 'pickle']
result_expire = timedelta(minutes=5)
