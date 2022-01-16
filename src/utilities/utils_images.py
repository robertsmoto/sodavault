from decouple import config
from django.utils import timezone
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from sodavault.utils_logging import svlog_info
import boto3
import botocore
import os


def create_dir_size_var(fn: str, size: tuple) -> str:
    # Create dirs
    now = timezone.now()
    date_dir = now.strftime("%Y/%m/%d/")
    fn = f'{fn}-{size[0]}x{size[1]}.webp'
    return date_dir, fn


def modify_fn_and_path(filename: str) -> str:
    now = timezone.now()
    date_dir = now.strftime('%Y/%m/%d/')
    # build the filename
    base_fn = os.path.basename(filename)
    fn = os.path.splitext(base_fn)[0]
    fn = "".join(x for x in fn if x.isalnum())
    fn = f"{fn}.webp"
    return date_dir, fn


def new_filename(instance, filename):
    date_dir, fn = modify_fn_and_path(filename=filename)
    return os.path.join('advertisingapp/banners/', date_dir, fn)


def new_filename_blog_feat(instance, filename):
    date_dir, fn = modify_fn_and_path(filename=filename)
    return os.path.join('blogapp/featured/', date_dir, fn)


def new_filename_blog_thumb(instance, filename):
    date_dir, fn = modify_fn_and_path(filename=filename)
    return os.path.join('blogapp/thumbnail/', date_dir, fn)


def new_filename_blog_cat(instance, filename):
    date_dir, fn = modify_fn_and_path(filename=filename)
    return os.path.join('blogapp/category/', date_dir, fn)


def new_filename_blog_tag(instance, filename):
    date_dir, fn = modify_fn_and_path(filename=filename)
    return os.path.join('blogapp/tag/', date_dir, fn)


def new_filename_banner(instance, filename):
    date_dir, fn = modify_fn_and_path(filename=filename)
    return os.path.join('advertisingapp/banners/', date_dir, fn)


def new_filename_assett(instance, filename):
    date_dir, fn = modify_fn_and_path(filename=filename)
    return os.path.join('advertisingapp/assetts/', date_dir, fn)


def check_and_remove_file(file_path: str) -> None:
    """Checks if file exists and removes it."""
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        svlog_info(
                "The file does not exist.",
                field=file_path)
    return


def write_image_to_local(django_read: object, fn: str, loc_dir: str) -> str:
    # create the dir if it doesn't exist
    # write only creates the file, not the dir
    if not os.path.exists(loc_dir):
        os.makedirs(loc_dir)
    file_path = os.path.join(loc_dir, fn)

    check_and_remove_file(file_path=file_path)

    dest = open(file_path, 'wb')
    dest.write(django_read)
    return file_path


class FeaturedLgWebp(ImageSpec):
    processors = [ResizeToFill(1600, 800)]
    format = 'WEBP'
    options = {'quality': 80}


class FeaturedMdWebp(ImageSpec):
    processors = [ResizeToFill(800, 400)]
    format = 'WEBP'
    options = {'quality': 80}


class FeaturedSmWebp(ImageSpec):
    processors = [ResizeToFill(400, 200)]
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


def process_images(k: str, v) -> None:
    processor = v[0]
    source = v[1]
    size = v[2]
    subdir = v[3]

    base_fn = os.path.basename(source.url)
    fn = os.path.splitext(base_fn)[0]
    fn = ''.join(x for x in fn if x.isalnum())

    # Generate new image
    ban = processor(source=source).generate()
    # use django api to read processed image
    banner_read = ban.read()

    date_dir, fn = create_dir_size_var(
            fn=fn,
            size=size)

    # upload image
    if config('ENV_USE_SPACES', cast=bool):
        file_path = os.path.join(subdir, date_dir, fn)
        s3_upload_path = os.path.join('media', file_path)

        # need to save image to temp dir before uploading to s3
        temp_dir = config('ENV_TEMP_DIR')
        local_filepath = write_image_to_local(
                django_read=banner_read, fn=fn, loc_dir=temp_dir)

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
                    s3_upload_path).load()
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
        try:
            with open(local_filepath, 'rb') as file_contents:
                s3client.put_object(
                    Bucket=config('ENV_AWS_STORAGE_BUCKET_NAME'),
                    Key=s3_upload_path,
                    Body=file_contents,
                    ContentEncoding='webp',
                    ContentType='image/webp',
                    CacheControl='max-age=86400',
                    ACL='public-read')
        except Exception as e:
            svlog_info("S3 open exception", field=e)

        # then delete the local file (local_filepath)
        check_and_remove_file(file_path=local_filepath)

    else:
        media_root = config('ENV_MEDIA_ROOT')
        base_dir = os.path.join(
            media_root, subdir, date_dir)

        # first check if file exists and remove it
        # for the development server, write file directly
        # to final location
        file_path = write_image_to_local(
                django_read=banner_read, fn=fn, loc_dir=base_dir)

    # assign the file path to the correct field
    svlog_info(f"Assign file_path {k}.", field=file_path)

    return file_path
