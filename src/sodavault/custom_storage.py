from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

CONF = settings.CONF

class StaticStorage(S3Boto3Storage):
    bucket_name = CONF.get('aws', {}).get('storage_bucket_name', '')
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    bucket_name = CONF.get('aws', {}).get('storage_bucket_name', '')
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = True


# class OverwriteStorage(FileSystemStorage):

    # def get_available_name(self, name, max_length=None):

        # print(f"###OverwriteStorage name:{name}")
        # if config('ENV_USE_SPACES', cast=bool):
            # check_and_remove_s3(file_path=name)
        # else:
            # check_and_remove_file(file_path=name)

        # return super().get_available_name(name, max_length)
