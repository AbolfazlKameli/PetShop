from celery import shared_task

from petshop.utils.bucket import Bucket


@shared_task
def delete_picture_from_bucket_task(file):
    bucket = Bucket()
    bucket.delete_file_object_from_bucket(key=file)
