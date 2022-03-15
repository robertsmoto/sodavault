from configapp.utils import utils_images
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from sodavault.utils_logging import svlog_info
import uuid


class Timestamps(models.Model):
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GroupABC(models.Model):

    parent = models.ForeignKey(
            'self',
            related_name="subgroups",
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    slug = models.SlugField(
            max_length=50,
            unique=True,
            help_text="Is required and must be unique.")
    name = models.CharField(max_length=200, blank=True)
    description = models.CharField(
            max_length=100,
            blank=True)
    kwd_list = models.CharField(
            max_length=100,
            blank=True,
            help_text="Comma-separated values.")

    is_primary = models.BooleanField(default=False)
    is_secondary = models.BooleanField(default=False)
    is_tertiary = models.BooleanField(default=False)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['slug']

    @property
    def parent_name(self):
        return self.parent.name

    def save(self, *args, **kwargs):
        if self.parent and not self.slug.startswith(self.parent.name):
            parent_slug = self.parent.name.lower().replace(' ', '-')
            self.slug = f"{parent_slug}-{self.slug}"
        super(GroupABC, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class NoteABC(models.Model):
    date = models.DateField(
            blank=True,
            null=True)
    note = models.TextField(
            max_length=3000,
            blank=True)

    class Meta:
        abstract = True
        ordering = ['-date']

    def __str__(self):
        return self.date.isoformat()


class ImageABC(models.Model):

    lg_21 = models.ImageField(
            upload_to=utils_images.new_filename,
            storage=utils_images.OverwriteStorage(),
            null=True,
            blank=True,
            help_text="Recommended size: 2100px x 600px. "
            "Recommended name: name-21.jpg")
    lg_11 = models.ImageField(
            upload_to=utils_images.new_filename,
            storage=utils_images.OverwriteStorage(),
            null=True,
            blank=True,
            help_text="Recommended size: 500px x 500px "
            "Recommended name: name-11.jpg")
    custom = models.ImageField(
            upload_to=utils_images.new_filename,
            storage=utils_images.OverwriteStorage(),
            null=True,
            blank=True,
            help_text="Image with custom size.")
    lg_191 = models.ImageField(
            upload_to=utils_images.new_filename,
            storage=utils_images.OverwriteStorage(),
            null=True,
            blank=True,
            help_text="1.9:1 ratio recommended size 2100px x 630px "
            "Recommended name: name-191.jpg")
    title = models.CharField(
            max_length=200,
            blank=True,
            help_text="Alt text for image.")
    caption = models.CharField(
            max_length=200,
            blank=True,
            help_text="Caption for image.")
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    """The following are automatically generated using the
    model's save method."""
    md_21 = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 800px x 400px")
    sm_21 = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 400px x 200px")
    md_11 = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 250px x 250px")
    sm_11 = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 200px x 200px")

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ImageABC, self).__init__(*args, **kwargs)
        self._orig_lg_21 = self.lg_21
        self._orig_lg_11 = self.lg_11

    def save(self, *args, **kwargs):
        """Creates new image sizes. Save new images directly to media server
        and save the url in a char field."""

        index = {}

        if (
                self._orig_lg_21 != self.lg_21
                and self.lg_21):

            svlog_info("Creating blog featured image variations.")

            index['Md21'] = [
                    utils_images.Md21WebP,
                    self.lg_21,
                    (800, 400),
                    "subdir/not-currently-used"]
            index['Sm21'] = [
                    utils_images.Sm21WebP,
                    self.lg_21,
                    (400, 200),
                    "subdir/not-currently-used"]

        if (
                self._orig_lg_11 != self.lg_11
                and self.lg_11):

            svlog_info("Creating blog thumbnail image variations.")

            index['Md11'] = [
                    utils_images.Md11WebP,
                    self.lg_11,
                    (250, 250),
                    "subdir/not-currently-used"]
            index['Sm11'] = [
                    utils_images.Sm11WebP,
                    self.lg_11,
                    (200, 200),
                    "subdir/not-currently-used"]

        for k, v in index.items():

            file_path = utils_images.process_images(self=self, k=k, v=v)

            if k == "Md21":
                self.md_21 = file_path
            if k == "Sm21":
                self.sm_21 = file_path
            if k == "Md11":
                self.md_11 = file_path
            if k == "Sm11":
                self.sm_11 = file_path

        super(ImageABC, self).save(*args, **kwargs)

    def __str__(self):
        strname = "image"
        if self.lg_11:
            strname = f"{self.lg_11}"
        if self.lg_21:
            strname = f"{self.lg_21}"
        if self.title:
            strname = f"{self.title}"
        return strname


class Image(ImageABC):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='config_user_images',
            on_delete=models.CASCADE,
            blank=True,
            null=True)


class Currency(Timestamps, models.Model):
    """Config for currency and currency display."""
    # currency (smallest denomination plus symbol)
    territory = models.CharField(
            max_length=100,
            blank=True)
    currency = models.CharField(
            max_length=100,
            blank=True)
    symbol = models.CharField(
            max_length=50,
            blank=True)
    iso_code = models.CharField(
            max_length=50,
            blank=True)
    fractional_unit = models.CharField(
            max_length=50,
            blank=True)
    number_basic = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.territory} {self.symbol} {self.currency}"


class CurrencyConfig(Timestamps, models.Model):
    """Config for currency and currency display."""
    # currency (smallest denomination plus symbol)
    SEPARATOR_CHOICES = [
            ('DEC', '.'),
            ('COM', ',')
            ]
    currency = models.ForeignKey(
            Currency,
            blank=True,
            null=True,
            on_delete=models.CASCADE
            )
    symbol_location = models.CharField(
            max_length=200,
            blank=True)
    is_space_separation = models.BooleanField(
            default=True,
            help_text="Provides a space between the currency symbol and price."
            )
    fractional_separator = models.CharField(
            max_length=3,
            blank=True,
            choices=SEPARATOR_CHOICES)
    thousands_separator = models.CharField(
            max_length=3,
            blank=True,
            choices=SEPARATOR_CHOICES)

    def __str__(self):
        return f"{self.currency}"


class Profile(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE)
    pen_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(
            upload_to="configapp/avatars/%Y/%m/%d",
            blank=True,
            null=True,
            help_text="Recommended size 250 x 250px"
            )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    cdn_dir = models.CharField(
            max_length=20,
            blank=True,
            help_text="User root cdn dir.eg. "
            "https://cdn.sodavault.com/image_dir/Y/m/d/image.webp"
            )

    class Meta:
        permissions = [
            ("create_users", "Can create new users."),
            ("view_token", "Can view token."),
            ("change_token", "Can change token."),
        ]

    def save(self, *args, **kwargs):
        if not self.cdn_dir:
            self.cdn_dir = str(uuid.uuid4())[:13]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
    # if created:
#         Token.objects.create(user=instance)
