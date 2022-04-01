from decouple import config
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
# from pathlib import Path
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
            print(f"The s3 object does not exist: {e}")
        else:
            # Something else has gone wrong.
            print(f"Something went wrong with s3: {e}")
    else:
        # The object does exist.
        print("s3 object exists, deleted it before uploading.")
        s3resource.Object(
                config('ENV_AWS_STORAGE_BUCKET_NAME'),
                file_path).delete()

    return


def check_and_remove_file(file_path: str) -> None:
    """Checks if file exists and removes it."""
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        print(f"The file does not exist: {file_path}")
    return


class OverwriteStorage(FileSystemStorage):

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

    # build the filename

    base_fn = os.path.basename(filename)
    fn = os.path.splitext(base_fn)[0]
    fn = "".join(x for x in fn if x.isalnum())

    size = kwargs.get('size', '')
    if size:
        fn = f"{fn}-{size[0]}x{size[1]}.webp"
    else:
        fn = f"{fn}.webp"

    print(f"endof new_filename {user_date}, {fn}")
    return os.path.join(user_date, fn)


def write_image_to_path(image_read: object, file_path: dict) -> None:
    """Writes file to given file_path."""
    # write only creates the file, not the dir
    dest = open(file_path, 'wb')
    dest.write(image_read)
    return


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


def create_dirs(self, processor=None, source=None, size=None) -> dict:
    dirs = {}
    dirs['fn_base'] = os.path.basename(source.url)
    dirs['fn'] = os.path.splitext(dirs['fn_base'])[0]
    dirs['fn'] = ''.join(x for x in dirs['fn'] if x.isalnum())

    # modifies dirs['fn'] and creates dirs['user_date_fn']
    dirs['user_date_fn'] = new_filename(
            instance=self, filename=dirs['fn'], size=size)

    dirs['user_date'], dirs['fn'] = os.path.split(dirs['user_date_fn'])
    dirs['mroot'] = config('ENV_MEDIA_ROOT')
    dirs['mroot_user_date'] = os.path.join(dirs['mroot'], dirs['user_date'])
    dirs['mroot_user_date_fn'] = os.path.join(dirs['mroot'], dirs['user_date_fn'])
    dirs['temp_dir'] = config('ENV_TEMP_DIR')
    dirs['temp_filepath'] = os.path.join(dirs['temp_dir'], dirs['fn'])

    return dirs


def process_images(self, k: str, v) -> None:

    processor = v[0]
    source = v[1]
    size = v[2]
    # subdir=v[3] not currently used

    dirs = create_dirs(
            self=self,
            processor=processor,
            source=source,
            size=size
            )

    # Generate new image
    new_image = processor(source=source).generate()
    # use django api to read processed image
    image_read = new_image.read()

    # upload image
    assigned_path = ""
    if config('ENV_USE_SPACES', cast=bool):

        # need to save image to temp dir before uploading to s3
        # create the dir if it doesn't exist
        temp_dir = dirs.get('temp_dir', '')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_filepath = dirs.get('temp_filepath', '')
        check_and_remove_file(file_path=temp_filepath)

        write_image_to_path(image_read=image_read, file_path=temp_filepath)

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
        mroot_user_date_fn = dirs.get('mroot_user_date_fn', '')
        check_and_remove_s3(file_path=mroot_user_date_fn)

        try:
            with open(dirs['local_filepath'], 'rb') as file_contents:
                s3client.put_object(
                    Bucket=config('ENV_AWS_STORAGE_BUCKET_NAME'),
                    Key=mroot_user_date_fn,
                    Body=file_contents,
                    ContentEncoding='webp',
                    ContentType='image/webp',
                    CacheControl='max-age=86400',
                    ACL='public-read')
        except Exception as e:
            print(f"S3 open exception: {e}")

        # then delete the local file (local_filepath)
        check_and_remove_file(file_path=temp_filepath)
        assigned_path = mroot_user_date_fn

    else:
        # for the development server, write file directly to final location

        mroot = dirs.get('mroot', '')
        user_date = dirs.get('user_date', '')
        user_date_fn = dirs.get('user_date_fn', '')

        # create the dir if it doesn't exist
        local_dir = os.path.join(mroot, user_date)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        local_file_path = os.path.join(mroot, user_date_fn)
        check_and_remove_file(file_path=local_file_path)

        write_image_to_path(image_read=image_read, file_path=local_file_path)
        assigned_path = user_date_fn

    return assigned_path
