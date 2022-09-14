from django.utils import timezone
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
import boto3
import botocore
import os
import shutil


def check_and_remove_s3(file_path: str) -> None:

    if not file_path:
        return

    """
    ENV_MEDIA_URL=https://cdn-stage.sodavault.com/media/
    """
    media_url = os.getenv('ENV_MEDIA_URL', '')
    if file_path.startswith(media_url):
        print("###starts_with: True")
        file_path = file_path.replace(media_url, '')

    file_path = os.path.join('media', file_path)
    print(f"###check and remove_s3_file:{file_path}")

    s3resource = boto3.resource(
            's3',
            region_name=os.getenv('ENV_AWS_S3_REGION_NAME', ''),
            endpoint_url=os.getenv('ENV_AWS_S3_ENDPOINT_URL', ''),
            aws_access_key_id=os.getenv('ENV_AWS_ACCESS_KEY_ID', ''),
            aws_secret_access_key=os.getenv(
                'ENV_AWS_SECRET_ACCESS_KEY', ''))

    try:
        s3resource.Object(os.getenv(
            'ENV_AWS_STORAGE_BUCKET_NAME', ''), file_path).load()
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
                os.getenv('ENV_AWS_STORAGE_BUCKET_NAME', ''),
                file_path).delete()

    return


def check_and_remove_dir(dir_path: str):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


def check_and_remove_file(file_path: str) -> None:
    """Checks if file exists and removes it."""

    print(f"###check and remove_file:{file_path}")

    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        print(f"The file does not exist: {file_path}")
    return


def write_image_to_path(image_read: bytearray, file_path: str) -> None:
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


def user_file_path(instance: object, filename: str, **kwargs) -> str:
    """Creates the user_dir and filename variations for media uploads."""

    user = instance.user.profile.cdn_dir
    date = timezone.now().strftime('%Y/%m/%d/')

    # get the basename
    basename = filename
    if not isinstance(filename, str):
        basename = os.path.basename(filename.url)

    # splits the filename
    fn, ext = os.path.splitext(basename)
    # allows only alpha-numeric characters in the filename
    fn = "".join(x for x in fn if x.isalnum())

    size = kwargs.get('size', '')
    if size:
        fn = f"{fn}-{size[0]}x{size[1]}.webp"
    else:
        fn = f"{fn}.webp"

    return os.path.join(user, date, fn)


def process_images(self, k: str, v) -> None:

    processor = v[0]
    source = v[1]  # source is the fn
    size = v[2]
    # subdir=v[3] not currently used

    print(f"###source.url: {source.url} type: {type(source.url)}")

    img_path = user_file_path(instance=self, filename=source, size=size)
    img_dir, img_fn = os.path.split(img_path)

    print("###image_path", img_path, img_dir, img_fn)
    """
    img_path = media/18fe4fa7-287d/2022/04/01/tree11-250x250.webp
    img_dir = media/18fe4fa7-287d/2022/04/01
    img_fn = tree11-250x250.webp
    """

    # Generate new image
    new_image = processor(source=source).generate()
    # use django api to read processed image
    image_read = new_image.read()

    # upload image
    if config('ENV_USE_SPACES', cast=bool):

        # need to save image to temp dir before uploading to s3
        # create the dir if it doesn't exist
        temp_dir = os.path.join(config('ENV_TEMP_DIR'), img_dir)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_filepath = os.path.join(temp_dir, img_fn)
        # check_and_remove_file(file_path=temp_filepath)

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

        # # should check if s3 file exists and if so delete it
        # # before uploading image with same name
        s3_filepath = os.path.join('media', img_path)
        # check_and_remove_s3(file_path=s3_filepath)

        try:
            with open(temp_filepath, 'rb') as file_contents:
                s3client.put_object(
                    Bucket=config('ENV_AWS_STORAGE_BUCKET_NAME'),
                    Key=s3_filepath,
                    Body=file_contents,
                    ContentEncoding='webp',
                    ContentType='image/webp',
                    CacheControl='max-age=86400',
                    ACL='public-read')

        except Exception as e:
            print(f"S3 open exception: {e}")

        # then delete the local dir (and file)
        check_and_remove_dir(dir_path=temp_dir)

    else:
        # for the development server, write file directly to final location
        # add the media root the the temp file and then save it

        # create the dir if it doesn't exist
        local_filepath = os.path.join(config('ENV_MEDIA_ROOT'), img_path)
        local_dir, _ = os.path.split(local_filepath)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        check_and_remove_file(file_path=local_filepath)

        write_image_to_path(image_read=image_read, file_path=local_filepath)

    return img_path
