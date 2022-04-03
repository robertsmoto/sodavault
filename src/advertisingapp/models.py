from ckeditor.fields import RichTextField
from configapp.utils import images
from django.conf import settings
from django.db import models
from django.utils import timezone
from sodavault.custom_storage import MediaStorage


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


class Banner(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='advertisingapp_user_banner',
            on_delete=models.CASCADE,
            blank=True,
            null=True)
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

    lg_11 = models.ImageField(
            upload_to=images.user_file_path,
            storage=MediaStorage(),
            blank=True,
            null=True,
            help_text="Recommended size: 500px x 500px "
            "Recommended name: name-11.jpg")
    lg_leaderboard = models.ImageField(
            upload_to=images.user_file_path,
            storage=MediaStorage(),
            blank=True,
            null=True,
            help_text="recommended size: 970px x 90px")
    md_leaderboard = models.ImageField(
            upload_to=images.user_file_path,
            storage=MediaStorage(),
            blank=True,
            null=True,
            help_text="recommended size: 790px x 90px")
    sm_leaderboard = models.ImageField(
            upload_to=images.user_file_path,
            storage=MediaStorage(),
            blank=True,
            null=True,
            help_text="recommended size: 728px x 90px")
    md_rectangle = models.ImageField(
            upload_to=images.user_file_path,
            storage=MediaStorage(),
            blank=True,
            null=True,
            help_text="recommended size: 336px x 280px")
    sm_rectangle = models.ImageField(
            upload_to=images.user_file_path,
            storage=MediaStorage(),
            blank=True,
            null=True,
            help_text="recommended size: 300px x 250px")

    skyscraper = models.ImageField(
            upload_to=images.user_file_path,
            storage=MediaStorage(),
            blank=True,
            null=True,
            help_text="recommended size: 160px x 600px")

    """The following images are automatically generated using
    the model's save method."""

    md_11 = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 250px x 250px")
    sm_11 = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 200px x 200px")

    def __init__(self, *args, **kwargs):
        super(Banner, self).__init__(*args, **kwargs)
        # this needs to change for each image
        self._orig_lg_11 = self.lg_11
        self._orig_lg_leaderboard = self.lg_leaderboard
        self._orig_md_leaderboard = self.md_leaderboard
        self._orig_sm_leaderboard = self.sm_leaderboard
        self._orig_md_rectangle = self.md_rectangle
        self._orig_sm_rectangle = self.sm_rectangle
        self._orig_skyscraper = self.skyscraper

    def save(self, *args, **kwargs):
        """Creates new banner sizes. Save new images directly to media server
        and save the url in a char field."""

        index = {}

        if self._orig_lg_11 != self.lg_11 and self.lg_11:

            print("Creating blog thumbnail image variations.")

            index['md_11'] = [
                    images.Md11WebP,
                    self.lg_11,
                    (250, 250),
                    "subdir/not-currently-used"]

            index['sm_11'] = [
                    images.Sm11WebP,
                    self.lg_11,
                    (200, 200),
                    "subdir/not-currently-used"]

        for k, v in index.items():

            file_path = images.process_images(self=self, k=k, v=v)

            if k == "md_11":
                self.md_11 = file_path
            if k == "sm_11":
                self.sm_11 = file_path

        # deletes images
        image_set = set()

        if self._orig_lg_11 != self.lg_11 and self._orig_lg_11:
            image_set = image_set | {self._orig_lg_11.url, self.md_11, self.sm_11}

        # resets the field values in model
        if self._orig_lg_11 != self.lg_11 and self._orig_lg_11:
            self.md_11 = ''
            self.sm_11 = ''

        if self._orig_lg_leaderboard != self.lg_leaderboard \
                and self._orig_lg_leaderboard:
            image_set = image_set | {self._orig_lg_leaderboard.url}

        if self._orig_md_leaderboard != self.md_leaderboard \
                and self._orig_md_leaderboard:
            image_set = image_set | {self._orig_md_leaderboard.url}

        if self._orig_sm_leaderboard != self.sm_leaderboard \
                and self._orig_sm_leaderboard:
            image_set = image_set | {self._orig_sm_leaderboard.url}

        if self._orig_md_rectangle != self.md_rectangle \
                and self._orig_md_rectangle:
            image_set = image_set | {self._orig_md_rectangle.url}

        if self._orig_sm_rectangle != self.sm_rectangle \
                and self._orig_sm_rectangle:
            image_set = image_set | {self._orig_sm_rectangle.url}

        if self._orig_skyscraper != self.skyscraper \
                and self._orig_skyscraper:
            image_set = image_set | {self._orig_skyscraper.url}

        for image in image_set:
            print("image", image)
            images.check_and_remove_s3(file_path=image)

        super(Banner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banners"
