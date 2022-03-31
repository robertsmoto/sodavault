from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from configapp.utils import images, logging


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
            upload_to=images.new_filename,
            blank=True,
            null=True,
            help_text="recommended size: 500px x 500px")
    ban_leaderboard = models.ImageField(
            upload_to=images.new_filename,
            blank=True,
            null=True,
            help_text="recommended size: 728px x 90px")
    ban_lg_leaderboard = models.ImageField(
            upload_to=images.new_filename,
            blank=True,
            null=True,
            help_text="recommended size: 970px x 90px")
    ban_inline_rectangle = models.ImageField(
            upload_to=images.new_filename,
            blank=True,
            null=True,
            help_text="recommended size: 300px x 250px")
    ban_lg_rectangle = models.ImageField(
            upload_to=images.new_filename,
            blank=True,
            null=True,
            help_text="recommended size: 336px x 280px")
    ban_skyscraper = models.ImageField(
            upload_to=images.new_filename,
            blank=True,
            null=True,
            help_text="recommended size: 160px x 600px")

    """The following images are automatically generated using
    the model's save method."""

    ban_lg_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 500px x 500px")
    ban_md_square = models.CharField(
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
            logging.SVlog().info("Creating ban_square image variations.")

            img_index['ban_lg_square'] = [
                    images.BannerLgSqWebp,
                    self.ban_square,
                    (500, 500),
                    "advertisingapp/banner"]
            img_index['ban_md_square'] = [
                    images.BannerMdSqWebp,
                    self.ban_square,
                    (250, 250),
                    "advertisingapp/banner"]
            img_index['ban_sm_square'] = [
                    images.BannerSmSqWebp,
                    self.ban_square,
                    (200, 200),
                    "advertisingapp/banner"]

        if (
                self._orig_ban_leaderboard != self.ban_leaderboard
                and self.ban_leaderboard):

            logging.SVlog().info("Creating ban_leaderboard image variations.")

            img_index['ban_leaderboard'] = [
                    images.BannerLeaderboardWebp,
                    self.ban_leaderboard,
                    (728, 90),
                    "advertisingapp/banner"]

        if (
                self._orig_ban_lg_leaderboard != self.ban_lg_leaderboard
                and self.ban_lg_leaderboard):

            logging.SVlog().info(
                    "Creating ban_lg_leaderboard image variations.")

            img_index['ban_lg_lederboard'] = [
                    images.BannerLgLeaderboardWebp,
                    self.ban_lg_leaderboard,
                    (790, 90),
                    "advertisingapp/banner"]

        if (
                self._orig_ban_inline_rectangle != self.ban_inline_rectangle
                and self.ban_inline_rectangle):

            logging.SVlog().info(
                    "Creating ban_inline_rectangle image variations.")

            img_index['ban_inline_rectangle'] = [
                    images.BannerInlineRectangleWebp,
                    self.ban_inline_rectangle,
                    (300, 250),
                    "advertisingapp/banner"]

        if (
                self._orig_ban_lg_rectangle != self.ban_lg_rectangle
                and self.ban_lg_rectangle):

            logging.SVlog().info("Creating ban_lg_rectangle image variations.")

            img_index['ban_lg_rectangle'] = [
                    images.BannerLgRectangleWebp,
                    self.ban_lg_rectangle,
                    (336, 280),
                    "advertisingapp/banner"]

        if (
                self._orig_ban_skyscraper != self.ban_skyscraper
                and self.ban_skyscraper):

            logging.SVlog().info("Creating ban_skyscraper image variations.")

            img_index['ban_skyscraper'] = [
                    images.BannerSkyScraperWebp,
                    self.ban_skyscraper,
                    (160, 600),
                    "advertisingapp/banner"]

        for k, v in img_index.items():

            file_path = images.process_images(k=k, v=v)

            if k == "ban_lg_square":
                self.ban_lg_square = file_path
            if k == "ban_md_square":
                self.ban_md_square = file_path
            if k == "ban_sm_square":
                self.ban_sm_square = file_path

        super(Banner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banners"
