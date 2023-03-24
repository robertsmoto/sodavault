from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

CONF = settings.CONF


class S3MediaStorage(S3Boto3Storage):
    print("## in custom storage")
    bucket_name = CONF.get(
        'aws', {}).get(
        'storage_bucket_name', '')
    custom_domain = CONF.get('aws', {}).get('custom_domain', '')
    location = 'media'
    print("## data", S3Boto3Storage.__dir__)
