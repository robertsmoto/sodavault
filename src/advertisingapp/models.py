from django.db import models
from imagekit.models import  ProcessedImageField # ImageSpecField <-- don't use
from imagekit.processors import ResizeToFill
from django.utils import timezone
from itemsapp.models import Product
from ckeditor.fields import RichTextField


class Campaign(models.Model):
#     products = models.ManyToManyField(
        # Product,
        # related_name='campaigns',
        # blank=True,
        # verbose_name='products')
    name = models.CharField(
        max_length=200, blank=True,
        help_text='Name of the Campaign')
    # is_banner_campaign = models.BooleanField(default=False)
    # is_assett_campaign = models.BooleanField(default=False)
    site_name = models.CharField(
        'Site Name', max_length=200, blank=True,
        help_text='Text of site advertised, will show in the URL')
    site_url = models.URLField(
        'URL of advertised site', max_length=200, blank=True)
    url_analyticscode = models.CharField(
        'URL Analytics Code', max_length=100, blank=True,
        help_text="?utm_source=swimexpress&utm_medium=webads&utm_campaign=campaign_name")
    date_added = models.DateTimeField(
        'Date Added', default=timezone.now, blank=True)
    date_expires = models.DateTimeField(
        'Expiration Date', blank=True, null=True,
        help_text='Leave blank = never expires')
    notes = RichTextField('Notes', blank=True, null=True,
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
    img_1x1 = ProcessedImageField(
        upload_to='advertisingapp/assetts/%Y/%m/%d',
        processors=[ResizeToFill(250, 250)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True,
        help_text="250px x 250px")
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
    image_xl = ProcessedImageField(
        upload_to='ad_banners/%Y/%m/%d',
        processors=[ResizeToFill(1140, 380)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True,
        help_text="auto rsizes to 1140px x 380px")
    image_lg = ProcessedImageField(
        upload_to='ad_banners/%Y/%m/%d',
        processors=[ResizeToFill(960, 320)],
        format='JPEG',
        options={'quality': 60}, 
        blank=True,
        null=True,
        help_text="auto resizes to 960px x 320px")
    image_md = ProcessedImageField(
        upload_to='ad_banners/%Y/%m/%d',
        processors=[ResizeToFill(720, 240)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True,
        help_text="auto resizes to 720px x 240px")
    image_sm = ProcessedImageField(
        upload_to='ad_banners/%Y/%m/%d',
        processors=[ResizeToFill(540, 180)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True,
        help_text="auto resizes to 540px x 180px")
    image_skyscraper = ProcessedImageField(
        upload_to='ad_banners/%Y/%m/%d',
        processors=[ResizeToFill(160, 600)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True,
        help_text="160px x 600px")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banners"
