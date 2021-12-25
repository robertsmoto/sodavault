from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from imagekit import ImageSpec
# from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import os
from decouple import config
import boto3
from sodavault.utils_logging import svlog_info
import botocore


def create_dir_size_var(fn: str, size: tuple) -> str:
    # Create dirs
    now = timezone.now()
    banner_dir = "advertisingapp/banners/"
    date_dir = now.strftime("%Y/%m/%d/")
    fn = f'{fn}-{size[0]}x{size[1]}.webp'
    return banner_dir, date_dir, fn


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


class Campaign(models.Model):
    name = models.CharField(
        max_length=200, blank=True,
        help_text='Name of the Campaign')
    site_name = models.CharField(
        'Site Name', max_length=200, blank=True,
        help_text='Text of site advertised, will show in the URL')
    site_url = models.URLField(
        'URL of advertised site', max_length=200, blank=True)
    url_analyticscode = models.CharField(
        'URL Analytics Code', max_length=100, blank=True,
        help_text=(
            "?utm_source=swimexpress&utm_medium=webads&"
            "utm_campaign=campaign_name"))
    date_added = models.DateTimeField(
        'Date Added', default=timezone.now, blank=True)
    date_expires = models.DateTimeField(
        'Expiration Date', blank=True, null=True,
        help_text='Leave blank = never expires')
    notes = RichTextField(
            'Notes',
            blank=True,
            null=True,
            help_text="Notes about how the campaign is used.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ad Campaigns"


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


class Banner(models.Model):
    campaign = models.ForeignKey(
            Campaign,
            related_name='banners',
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    name = models.CharField(
            'Name', max_length=200, blank=True,
            help_text='Name of the Banner')
    excerpt = RichTextField(
            'Excerpt', max_length=400, blank=True, null=True,
            help_text="400 characters max")
    url_name = models.CharField(
        'URL Name',
        max_length=70,
        blank=True,
        help_text="URL tool tip on mouse hover.")
    url_link = models.URLField(
        'URL',
        max_length=100,
        blank=True,
        help_text="End url with '/'")
    ban_square = models.ImageField(
            upload_to=new_filename_banner,
            blank=True,
            null=True,
            help_text="recommended size: 500px x 500px")
    ban_leaderboard = models.ImageField(
            upload_to=new_filename_banner,
            blank=True,
            null=True,
            help_text="recommended size: 728px x 90px")
    ban_lg_leaderboard = models.ImageField(
            upload_to=new_filename_banner,
            blank=True,
            null=True,
            help_text="recommended size: 970px x 90px")
    ban_inline_rectangle = models.ImageField(
            upload_to=new_filename_banner,
            blank=True,
            null=True,
            help_text="recommended size: 300px x 250px")
    ban_lg_rectangle = models.ImageField(
            upload_to=new_filename_banner,
            blank=True,
            null=True,
            help_text="recommended size: 336px x 280px")
    ban_skyscraper = models.ImageField(
            upload_to=new_filename_banner,
            blank=True,
            null=True,
            help_text="recommended size: 160px x 600px")

    """The following images are automatically generated using
    the model's save method."""

    ban_lg_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 500px x 500px")
    ban_med_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 250px x 250px")
    ban_sm_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 200px x 200px")

    def __init__(self, *args, **kwargs):
        super(Banner, self).__init__(*args, **kwargs)
        # this needs to change for each image
        self._orig_ban_square = self.ban_square
        self._orig_ban_leaderboard = self.ban_leaderboard
        self._orig_ban_lg_leaderboard = self.ban_lg_leaderboard
        self._orig_ban_inline_rectangle = self.ban_inline_rectangle
        self._orig_ban_lg_rectangle = self.ban_lg_rectangle
        self._orig_ban_skyscraper = self.ban_skyscraper

    def save(self, *args, **kwargs):
        """Creates new banner sizes. Save new images directly to media server
        and save the url in a char field."""

        img_index = {}

        if self._orig_ban_square != self.ban_square and self.ban_square:
            svlog_info("Creating ban_square image variations.")

            img_index['ban_lg_square'] = [
                    BannerLgSqWebp, self.ban_square, (500, 500)]
            img_index['ban_md_square'] = [
                    BannerMdSqWebp, self.ban_square, (250, 250)]
            img_index['ban_sm_square'] = [
                    BannerSmSqWebp, self.ban_square, (200, 200)]

        if (
                self._orig_ban_leaderboard != self.ban_leaderboard
                and self.ban_leaderboard):

            svlog_info("Creating ban_leaderboard image variations.")

            img_index['ban_leaderboard'] = [
                BannerLeaderboardWebp, self.ban_leaderboard, (728, 90)]

        if (
                self._orig_ban_lg_leaderboard != self.ban_lg_leaderboard
                and self.ban_lg_leaderboard):

            svlog_info("Creating ban_lg_leaderboard image variations.")

            img_index['ban_lg_lederboard'] = [
                BannerLgLeaderboardWebp, self.ban_lg_leaderboard, (790, 90)]

        if (
                self._orig_ban_inline_rectangle != self.ban_inline_rectangle
                and self.ban_inline_rectangle):

            svlog_info("Creating ban_inline_rectangle image variations.")

            img_index['ban_inline_rectangle'] = [
                BannerInlineRectangleWebp,
                self.ban_inline_rectangle,
                (300, 250)]

        if (
                self._orig_ban_lg_rectangle != self.ban_lg_rectangle
                and self.ban_lg_rectangle):

            svlog_info("Creating ban_lg_rectangle image variations.")

            img_index['ban_lg_rectangle'] = [
                BannerLgRectangleWebp, self.ban_lg_rectangle, (336, 280)]

        if (
                self._orig_ban_skyscraper != self.ban_skyscraper
                and self.ban_skyscraper):

            svlog_info("Creating ban_skyscraper image variations.")

            img_index['ban_skyscraper'] = [
                BannerSkyScraperWebp, self.ban_skyscraper, (160, 600)]

        for k, v in img_index.items():

            processor = v[0]
            source = v[1]
            size = v[2]

            base_fn = os.path.basename(source.url)
            fn = os.path.splitext(base_fn)[0]
            fn = ''.join(x for x in fn if x.isalnum())

            # Generate new image
            ban = processor(source=source).generate()
            # use django api to read processed image
            banner_read = ban.read()

            banner_dir, date_dir, fn = create_dir_size_var(fn=fn, size=size)

            # upload image
            if config('ENV_USE_SPACES', cast=bool):
                file_path = os.path.join(banner_dir, date_dir, fn)
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
                    media_root, banner_dir, date_dir)

                # first check if file exists and remove it
                # for the development server, write file directly
                # to final location
                file_path = write_image_to_local(
                        django_read=banner_read, fn=fn, loc_dir=base_dir)

            # assign the file path to the correct field
            svlog_info(f"Assign file_path {k}.", field=file_path)

            if k == "ban_lg_square":
                self.ban_lg_square = file_path
            if k == "ban_md_square":
                self.ban_med_square = file_path
            if k == "ban_sm_square":
                self.ban_sm_square = file_path

        super(Banner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banners"


# class Assett(models.Model):
    # campaign = models.ForeignKey(
        # Campaign,
        # related_name='assetts',
        # blank=True,
        # null=True,
        # on_delete=models.CASCADE)
    # product = models.ForeignKey(
        # Product,
        # related_name='assetts',
        # blank=True,
        # null=True,
        # on_delete=models.CASCADE)
    # name = models.CharField('Asset Name', max_length=200, blank=True)
    # excerpt = RichTextField(
            # 'Excerpt', max_length=400, blank=True, null=True,
            # help_text="400 characters max")
    # image = models.ImageField(
            # upload_to=new_filename_assett,
            # blank=True,
            # null=True,
            # help_text="recommended size: 1000px x 1000px")
    # url_name = models.CharField(
        # 'URL Name',
        # max_length=70,
        # blank=True,
        # help_text="URL tool tip on mouse hover.")
    # url_link = models.URLField(
        # 'URL',
        # max_length=100,
        # blank=True,
        # help_text="End url with '/'")

    # def __str__(self):
        # return self.name

    # class Meta:
        # verbose_name_plural = "Ad Assetts"
