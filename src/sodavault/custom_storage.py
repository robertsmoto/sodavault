from storages.backends.s3boto3 import S3Boto3Storage
from decouple import config

class StaticStorage(S3Boto3Storage):
    bucket_name = config('ENV_AWS_STORAGE_BUCKET_NAME')
    location = 'static'
    default_acl = 'public-read'

class MediaStorage(S3Boto3Storage):
    bucket_name = config('ENV_AWS_STORAGE_BUCKET_NAME')
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


