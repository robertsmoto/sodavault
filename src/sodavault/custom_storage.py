from storages.backends.s3boto3 import S3Boto3Storage
import os


class StaticStorage(S3Boto3Storage):
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
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
