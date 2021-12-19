from ckeditor.fields import RichTextField
from django.core.files import File
from django.db import models
from django.utils import timezone
from io import BytesIO
from itemsapp.models import Product
from pathlib import Path
import PIL
import imghdr
from decouple import config
import os


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
    image_xl = models.ImageField(
            upload_to='advertisingapp/banners/%Y/%m/%d/',
            blank=True,
            null=True,
            help_text="recommended size: 1140px x 380px")
    image_skyscraper = models.ImageField(
            upload_to='advertisingapp/banners/%Y/%m/%d/',
            blank=True,
            null=True,
            help_text="recommended size: 160px x 600px")

    """The following images are automatically generated using
    the model's save method and Pillow."""

    image_lg = models.ImageField(
            upload_to='advertisingapp/banners/%Y/%m/%d/',
            blank=True,
            null=True,
            help_text="automatic size: 960px x 320px")
    image_md = models.ImageField(
            upload_to='advertisingapp/banners/%Y/%m/%d/',
            blank=True,
            null=True,
            help_text="automatic size: 720px x 240px")
    image_sm = models.ImageField(
            upload_to='advertisingapp/banners/%Y/%m/%d/',
            blank=True,
            null=True,
            help_text="automatic size: 540px x 180px")

    def save(self, *args, **kwargs):
        super(Banner, self).save(*args, **kwargs)

        # Original photos

        ORIG_IMGS = ['image_xl', 'image_skyscraper']

        IMAGE_SIZES = {
                'image_lg': (960, 320),
                'image_md': (720, 240),
                'image_sm': (540, 180)}

        def create_webp_image(
                field: str,
                new_image: object,
                sizes: tuple,
                basefn: str) -> None:
            """Creates a webp image of specified size."""

            new_image.thumbnail(sizes, PIL.Image.ANTIALIAS)

            blob = BytesIO()
            new_image.save(blob, "webp", quality=80)
            new_file_name = f"{basefn}-{sizes[0]}x{sizes[1]}.webp"
            field.save(
                    name=new_file_name,
                    content=File(blob),
                    save=False)

        for img in ORIG_IMGS:

            field = getattr(self, img)

            basefn = ""
            if field:
                basefn = Path(field.url).stem

            orig_img = None
            image_type = ""

            # check and convert orig imgs to webp format
            if field:

                img_path = field.url
                if config('ENV_DEBUG', cast=bool):
                    img_path = config('ENV_DEV_ROOT') + field.url

                orig_img = PIL.Image.open(img_path)

                image_type = orig_img.mode

                if image_type != "WEBP":
                    orig_img = orig_img.convert('RGB')

            # create and save variations if img == 'image_xl'
            if orig_img and img == 'image_xl':
                for k, v in IMAGE_SIZES.items():
                    varfield = getattr(self, k)
                    var_image = orig_img.copy()
                    create_webp_image(
                            field=varfield,
                            new_image=var_image,
                            sizes=v,
                            basefn=basefn)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banners"
