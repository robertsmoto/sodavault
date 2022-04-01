from decouple import config
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
# from pathlib import Path
from . import logging
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
        s3resource.Object(config(
            'ENV_AWS_STORAGE_BUCKET_NAME'), file_path).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            logging.SVlog().warn(f"The s3 object does not exist: {e}")
        else:
            # Something else has gone wrong.
            logging.SVlog().error(f"Something went wrong with s3: {e}")
    else:
        # The object does exist.
        logging.SVlog().info(
                "s3 object exists, deleted it before "
                "uploading.")
        s3resource.Object(
                config('ENV_AWS_STORAGE_BUCKET_NAME'),
                file_path).delete()

    return


def check_and_remove_file(file_path: str) -> None:
    """Checks if file exists and removes it."""
    if file_path.is_file():
        os.remove(file_path)
    else:
        logging.SVlog().error(f"The file does not exist: {file_path}")
    return


class OverwriteStorage(FileSystemStorage):

    print("in overwite storage")

    def get_available_name(self, name, max_length=None):

        if config('ENV_USE_SPACES', cast=bool):
            check_and_remove_s3(file_path=name)
        else:
            check_and_remove_file(file_path=name)

        return super().get_available_name(name, max_length)


def new_filename(instance: object, filename: str, **kwargs) -> (str, str):
    """Creates the base dir and filename variations for user uploads."""
    # create the directory
    now = timezone.now()
    user_dir = instance.user.profile.cdn_dir
    date_dir = now.strftime('%Y/%m/%d/')
    user_date = os.path.join(user_dir, date_dir)

    print("### instance", instance)
    # build the filename

    print("01")
    base_fn = os.path.basename(filename)
    fn = os.path.splitext(base_fn)[0]
    fn = "".join(x for x in fn if x.isalnum())

    print("02")
    size = kwargs.get('size', '')
    if size:
        fn = f"{fn}-{size[0]}x{size[1]}.webp"
    else:
        fn = f"{fn}.webp"

    print(f"endof new_filename {user_date}, {fn}")
    return os.path.join(user_date, fn)


def write_image_to_temp(image_read: object, dirs: dict) -> None:
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

    logging.SVlog().debug("Writing image to temp", field=temp_filepath)
    logging.SVlog().debug("Dirs", field=dirs)

    return


def write_image_to_local(image_read: object, dirs: dict) -> None:
    """This writes to local filesystem for development server."""

    # create the dir if it doesn't exist
    # write only creates the file, not the dir
    mroot = dirs.get('mroot', '')
    user_date = dirs.get('user_date', '')
    user_date_fn = dirs.get('user_date_fn', '')

    local_dir = os.path.join(mroot, user_date)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    local_file_path = os.path.join(mroot, user_date_fn)
    check_and_remove_file(file_path=local_file_path)

    dest = open(local_file_path, 'wb')
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
    new_image = processor(source=source).generate()
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

    # upload image
    if config('ENV_USE_SPACES', cast=bool):
        print("###in spaces")

        # need to save image to temp dir before uploading to s3
        write_image_to_temp(image_read=image_read, dirs=dirs)

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

        check_and_remove_s3(file_path=dirs['mroot_user_date_fn'])

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
            logging.SVlog().error(f"S3 open exception: {e}")

        # then delete the local file (local_filepath)
        temp_filepath = dirs.get('temp_filepath', '')
        check_and_remove_file(file_path=temp_filepath)

    else:
        print("### before write to local")
        # first check if file exists and remove it
        # for the development server, write file directly
        # to final location
        # print("image_read", image_read)
        write_image_to_local(image_read=image_read, dirs=dirs)

    # assign the file path to the correct field
    logging.SVlog().info(
            f"Assign file_path {k} {dirs.get('user_date_fn', '')}")

    return dirs.get('user_date_fn', '')
