from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = 'sodavault'
    location = 'media'
    # ACL = 'public-read'
#     AWS_S3_OBJECT_PARAMETERS = {
        # 'ACL': 'public-read',
        # 'CacheControl': 'max-age=86400',
#     }

class StaticStorage(S3Boto3Storage):
    bucket_name = 'sodavault'
    location = 'static'

