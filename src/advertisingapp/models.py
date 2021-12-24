from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from imagekit import ImageSpec
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from itemsapp.models import Product
import os
from decouple import config
import boto3
from sodavault.utils_logging import svlog_info


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


class Assett(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        related_name='assetts',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        related_name='assetts',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField('Asset Name', max_length=200, blank=True)
    excerpt = RichTextField(
            'Excerpt', max_length=400, blank=True, null=True,
            help_text="400 characters max")
    img_1x1 = models.ImageField(
        upload_to='advertisingapp/assetts/%Y/%m/%d',
        blank=True,
        null=True,
        help_text="recommended size: 250px x 250px")
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ad Assetts"


class BannerLg(ImageSpec):
    processors = [ResizeToFill(960, 320)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerMd(ImageSpec):
    processors = [ResizeToFill(720, 240)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerSm(ImageSpec):
    processors = [ResizeToFill(540, 180)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerSkyScraper(ImageSpec):
    processors = [ResizeToFill(160, 600)]
    format = 'WEBP'
    options = {'quality': 80}


def new_filename(instance, filename):

    # build the date dir
    now = timezone.now()
    date_dir = now.strftime('%Y/%m/%d/')
    # build the filename
    base_fn = os.path.basename(filename)
    fn = os.path.splitext(base_fn)[0]
    fn = "".join(x for x in fn if x.isalnum())
    fn = f"{fn}.webp"

    return os.path.join('advertisingapp/banners/', date_dir, fn)


def write_image_to_local(django_read: object, fn: str, loc_dir: str) -> str:
    # create the dir if it doesn't exist
    # write only creates the file, not the dir
    if not os.path.exists(loc_dir):
        os.makedirs(loc_dir)
    file_path = os.path.join(loc_dir, fn)
    dest = open(file_path, 'wb')
    dest.write(django_read)
    return file_path


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
    image_xl = ProcessedImageField(
            upload_to=new_filename,
            processors=[ResizeToFill(1140, 380)],
            format='WEBP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="recommended size: 1140px x 380px")
    image_skyscraper = ProcessedImageField(
            upload_to=new_filename,
            processors=[ResizeToFill(160, 600)],
            format='WEBP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="recommended size: 160px x 600px")

    """The following images are automatically generated using
    the model's save method."""

    image_lg = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 960px x 320px")
    image_md = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 720px x 240px")
    image_sm = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 540px x 180px")

    def __init__(self, *args, **kwargs):
        super(Banner, self).__init__(*args, **kwargs)
        self._orig_image_xl = self.image_xl
        self._orig_image_skyscraper = self.image_skyscraper

    def save(self, *args, **kwargs):
        """Creates new banner sizes. Save new images directly to media server
        and save the url in a char field."""

        if self._orig_image_xl != self.image_xl and self.image_xl:
            svlog_info("Creating image variations.")

            img_index = {
                    'image_lg': [
                        BannerLg, self.image_xl, (960, 320)],
                    'image_md': [
                        BannerMd, self.image_xl, (720, 240)],
                    'image_sm': [
                        BannerSm, self.image_xl, (540, 180)]}

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

                # Create dirs
                now = timezone.now()
                banner_dir = "advertisingapp/banners/"
                date_dir = now.strftime("%Y/%m/%d/")
                fn = f'{fn}-{size[0]}x{size[1]}.webp'

                # upload image
                if config('ENV_USE_SPACES', cast=bool):
                    file_path = os.path.join(
                            "media", banner_dir, date_dir, fn)

                    svlog_info("", field=banner_dir)
                    svlog_info("", field=date_dir)
                    svlog_info("", field=fn)
                    svlog_info("", field=file_path)

                    # need to save image to temp dir before uploading to s3
                    temp_dir = config('ENV_TEMP_DIR')
                    local_filepath = write_image_to_local(
                            django_read=banner_read, fn=fn, loc_dir=temp_dir)

                    # now upload the local file to CDN
                    session = boto3.session.Session()

                    client = session.client(
                            's3',
                            region_name=config('ENV_AWS_S3_REGION_NAME'),
                            endpoint_url=config('ENV_AWS_S3_ENDPOINT_URL'),
                            aws_access_key_id=config('ENV_AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=config(
                                'ENV_AWS_SECRET_ACCESS_KEY'))

                    try:
                        with open(local_filepath, 'rb') as file_contents:
                            client.put_object(
                                Bucket=config('ENV_AWS_STORAGE_BUCKET_NAME'),
                                Key=file_path,
                                Body=file_contents,
                                ContentEncoding='webp',
                                ContentType='image/webp',
                                CacheControl='max-age=86400',
                                ACL='public-read')
                    except Exception as e:
                        svlog_info("S3 open exception", field=e)

                        # then delete the local file (local_fileppath)
                        if os.path.exists(local_filepath):
                            os.remove(local_filepath)
                        else:
                            svlog_info(
                                    "The file does not exist.",
                                    field=local_filepath)

                else:
                    media_root = config('ENV_MEDIA_ROOT')
                    base_dir = os.path.join(
                        media_root, banner_dir, date_dir)

                    # for the development server, write file directly
                    # to final location
                    _ = write_image_to_local(
                            django_read=banner_read, fn=fn, loc_dir=base_dir)

                # assign the file path to the correct field
                self.k = file_path

        super(Banner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banners"
