from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from imagekit import ImageSpec
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from itemsapp.models import Product
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


class BannerXl(ImageSpec):
    processors = [ResizeToFill(1140, 380)]
    format = 'WEBP'
    options = {'quality': 80}


class BannerImgSpec(ImageSpec):
    def __init__(self, format, options, processors):
        self.format = 'WEBP'
        self.options = {'quality': 80}
        self.processors = self.resize

    def resize(self, processors, sizes: tuple):
        processors = [ResizeToFill(sizes[0], sizes[1])]
        return processors


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
            upload_to='advertisingapp/banners/%Y/%m/%d/',
            processors=[ResizeToFill(1140, 380)],
            format='WEBP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="recommended size: 1140px x 380px")
    image_skyscraper = ProcessedImageField(
            upload_to='advertisingapp/banners/%Y/%m/%d/',
            processors=[ResizeToFill(160, 600)],
            format='WEBP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="recommended size: 160px x 600px")

    """The following images are automatically generated using
    the model's save method."""

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

    def __init__(self, *args, **kwargs):
        super(Banner, self).__init__(*args, **kwargs)
        self._orig_image_xl = self.image_xl
        self._orig_image_skyscraper = self.image_skyscraper

    def save(self, *args, **kwargs):
        """Creates new banner sizes."""

        if self._orig_image_xl != self.image_xl and self.image_xl:

            base_fn = os.path.basename(self.image_xl.url)
            fn = os.path.splitext(base_fn)[0]
            fn = ''.join(x for x in fn if x.isalnum())

            banlg = BannerLg(
                    source=self.image_xl).generate()
            pathlg = f'/home/robertsmoto/dev/temp/{fn}-960x320.webp'
            destlg = open(pathlg, 'wb')
            destlg.write(banlg.read())

            banmd = BannerMd(
                    source=self.image_xl).generate()
            destmd = f'/home/robertsmoto/dev/temp/{fn}-720x240.webp'
            dest = open(destmd, 'wb')
            dest.write(banmd.read())

            bansm = BannerSm(
                    source=self.image_xl).generate()
            destsm = f'/home/robertsmoto/dev/temp/{fn}-540x180.webp'
            dest = open(destsm, 'wb')
            dest.write(bansm.read())

        super(Banner, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banners"
