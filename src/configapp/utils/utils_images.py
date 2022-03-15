from decouple import config
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from pathlib import Path
from sodavault.utils_logging import svlog_info
import boto3
import botocore
import os


def check_and_remove_s3(file_path: str) -> None:

    s3resource = boto3.resource(
            's3',
            region_name=config('ENV_AWS_S3_REGION_NAME'),
            endpoint_url=config('ENV_AWS_S3_ENDPOINT_URL'),
            aws_access_key_id=config('ENV_AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config(
                'ENV_AWS_SECRET_ACCESS_KEY'))

    try:
        s3resource.Object(
                config('ENV_AWS_STORAGE_BUCKET_NAME'),
                file_path).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            svlog_info("The s3 object does not exist.")
        else:
            # Something else has gone wrong.
            svlog_info(f"Something went wrong with s3: {e}")
    else:
        # The object does exist.
        svlog_info(
                "s3 object exists, deleted it before "
                "uploading.")
        s3resource.Object(
                config('ENV_AWS_STORAGE_BUCKET_NAME'),
                file_path).delete()

    return


def check_and_remove_file(file_path: str) -> None:
    """Checks if file exists and removes it."""

    if not file_path.startswith(config('ENV_MEDIA_ROOT')):
        file_path = os.path.join(config('ENV_MEDIA_ROOT'), file_path)
    path = Path(file_path)
    if path.is_file():
        os.remove(file_path)
    else:
        svlog_info(
                "The file does not exist.",
                field=file_path)
    return


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """

        print("***name", name)
        # If the filename already exists, remove it as if it was a true file system
        if config('ENV_USE_SPACES', cast=bool):
            check_and_remove_s3(file_path=name)
        else:
            check_and_remove_file(file_path=name)

        return super(OverwriteStorage, self).get_available_name(name, max_length)


def new_filename(instance: object, filename: str, **kwargs) -> (str, str):
    """Creates the base dir and filename variations for user uploads."""
    # create the directory
    now = timezone.now()
    print("instance", instance)
    print("instance", instance.user)
    user_dir = instance.user.profile.cdn_dir
    date_dir = now.strftime('%Y/%m/%d/')
    user_date = os.path.join(user_dir, date_dir)

    # build the filename
    base_fn = os.path.basename(filename)
    fn = os.path.splitext(base_fn)[0]
    fn = "".join(x for x in fn if x.isalnum())

    size = kwargs.get('size', '')
    if size:
        fn = f"{fn}-{size[0]}x{size[1]}.webp"
    else:
        fn = f"{fn}.webp"

    return os.path.join(user_date, fn)


def write_image_to_local(image_read: object, dirs: dict) -> None:
    """Need dirs['mroot_user_date'] and dirs['mroot_user_date_filename'] """

    # create the dir if it doesn't exist
    # write only creates the file, not the dir
    temp_dir = dirs.get('temp_dir', '')
    temp_filepath = dirs.get('temp_filepath', '')

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    check_and_remove_file(file_path=temp_filepath)

    dest = open(temp_filepath, 'wb')
    dest.write(image_read)

    return


# class Lg21WebP(ImageSpec):
    # processors = [ResizeToFill(1600, 800)]
    # format = 'WEBP'
    # options = {'quality': 80}


class Md21WebP(ImageSpec):
    processors = [ResizeToFill(800, 400)]
    format = 'WEBP'
    options = {'quality': 80}


class Sm21WebP(ImageSpec):
    processors = [ResizeToFill(400, 200)]
    format = 'WEBP'
    options = {'quality': 80}


class Md11WebP(ImageSpec):
    processors = [ResizeToFill(250, 250)]
    format = 'WEBP'
    options = {'quality': 80}


class Sm11WebP(ImageSpec):
    processors = [ResizeToFill(200, 200)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerLgSqWebp(ImageSpec):
    processors = [ResizeToFill(500, 500)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerMdSqWebp(ImageSpec):
    processors = [ResizeToFill(250, 250)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerSmSqWebp(ImageSpec):
    processors = [ResizeToFill(200, 200)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerLeaderboardWebp(ImageSpec):
    processors = [ResizeToFill(728, 90)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerLgLeaderboardWebp(ImageSpec):
    processors = [ResizeToFill(970, 90)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerInlineRectangleWebp(ImageSpec):
    processors = [ResizeToFill(300, 250)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerLgRectangleWebp(ImageSpec):
    processors = [ResizeToFill(336, 280)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerSkyScraperWebp(ImageSpec):
    processors = [ResizeToFill(160, 600)]
    format = 'WEBP'
    options = {'quality': 80}


def process_images(self, k: str, v) -> None:
    processor = v[0]
    source = v[1]
    size = v[2]
    # subdir = v[3]

    dirs = {}
    dirs['fn_base'] = os.path.basename(source.url)
    dirs['fn'] = os.path.splitext(dirs['fn_base'])[0]
    dirs['fn'] = ''.join(x for x in dirs['fn'] if x.isalnum())

    # Generate new image
    print('before')
    new_image = processor(source=source).generate()
    print('after new image', new_image)
    # use django api to read processed image
    image_read = new_image.read()

    # modifies dirs['fn'] and creates dirs['user_date_fn']
    dirs['user_date_fn'] = new_filename(
            instance=self, filename=dirs['fn'], size=size)

    dirs['user_date'], dirs['fn'] = os.path.split(dirs['user_date_fn'])
    dirs['mroot'] = config('ENV_MEDIA_ROOT')
    dirs['mroot_user_date'] = os.path.join(dirs['mroot'], dirs['user_date'])
    dirs['mroot_user_date_fn'] = os.path.join(dirs['mroot'], dirs['user_date_fn'])
    dirs['temp_dir'] = config('ENV_TEMP_DIR')
    dirs['temp_filepath'] = os.path.join(dirs['temp_dir'], dirs['fn'])

    print("dirs", dirs)

    # upload image
    if config('ENV_USE_SPACES', cast=bool):
        # s3_upload_path = os.path.join('media', dirs['full_path'])

        # need to save image to temp dir before uploading to s3
        write_image_to_local(
                image_read=image_read,
                dirs=dirs)

        # now upload the local file to CDN
        session = boto3.session.Session()

        s3client = session.client(
                's3',
                region_name=config('ENV_AWS_S3_REGION_NAME'),
                endpoint_url=config('ENV_AWS_S3_ENDPOINT_URL'),
                aws_access_key_id=config('ENV_AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=config(
                    'ENV_AWS_SECRET_ACCESS_KEY'))

        # should check if s3 file exists and if so delete it
        # before uploading image with same name

#################

        check_and_remove_s3(file_path=dirs['mroot_user_date_fn'])
################

        try:
            with open(dirs['local_filepath'], 'rb') as file_contents:
                s3client.put_object(
                    Bucket=config('ENV_AWS_STORAGE_BUCKET_NAME'),
                    Key=dirs['mroot_user_date_fn'],
                    Body=file_contents,
                    ContentEncoding='webp',
                    ContentType='image/webp',
                    CacheControl='max-age=86400',
                    ACL='public-read')
        except Exception as e:
            svlog_info("S3 open exception", field=e)

        # then delete the local file (local_filepath)
        check_and_remove_file(dirs=dirs)

    else:
        print("im here")
        # first check if file exists and remove it
        # for the development server, write file directly
        # to final location
        # print("image_read", image_read)
        write_image_to_local(
                image_read=image_read,
                dirs=dirs)

    # assign the file path to the correct field
    svlog_info(f"Assign file_path {k}.", field=dirs['temp_filepath'])

    return dirs['temp_filepath']
