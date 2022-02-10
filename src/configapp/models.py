from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from utilities import utils_images
from sodavault.utils_logging import svlog_info


class Timestamps(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(Timestamps, models.Model):
    domain = models.CharField(
            'Domain eg. example.com',
            max_length=200,
            blank=True)
    name = models.CharField(
            'Location Name',
            max_length=200,
            blank=True)
    description = models.CharField(
            'Location Description',
            max_length=200,
            blank=True)

    class Meta:
        verbose_name_plural = "01. Locations"

    def __str__(self):
        return '%s' % (self.name)


class Group(Timestamps, models.Model):

    GROUP_TYPE_CHOICES = [
        ('BLOGCAT', 'Blog Category'),
        ('BLOGTAG', 'Blog Tag'),
        ('ITEMCAT', 'Item Category'),
        ('ITEMTAG', 'Item Tag'),
        ('ITEMDEP', 'Item Department'),
        ('ITEMATT', 'Item Attribute'),
    ]
    group_type = models.CharField(
        max_length=7,
        blank=True,
        choices=GROUP_TYPE_CHOICES,
    )
    locations = models.ManyToManyField(
            Location,
            blank=True)
    subgroup = models.ForeignKey(
            'self', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    description = models.CharField(
            'Category Description',
            max_length=100,
            blank=True)
    kwd_list = models.CharField(
            'Category Keywords',
            max_length=100,
            blank=True,
            help_text="Comma-separated values.")

    is_primary = models.BooleanField(default=False)
    is_secondary = models.BooleanField(default=False)
    is_tertiary = models.BooleanField(default=False)
    order = models.CharField(max_length=20, blank=True)
    image_thumb = models.ImageField(
            upload_to=utils_images.new_filename_config_group,
            null=True,
            blank=True,
            help_text="Recommended size 500px x 500px")
    image_191 = models.ImageField(
            upload_to=utils_images.new_filename_config_group,
            null=True,
            blank=True,
            help_text="1.9:1 ratio recommended size 1200px x 630px")
    image_21 = models.ImageField(
            upload_to=utils_images.new_filename_config_group,
            null=True,
            blank=True,
            help_text="Recommended size 1200px x 600px")

    # The following are automatically generated using the
    # model's save method.

    image_lg_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 500px x 500px")
    image_md_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 250px x 250px")
    image_sm_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 200px x 200px")

    class Meta:
        verbose_name_plural = "05. Groups"
        # ordering = ['menu_order', 'name']

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        self._orig_image = self.image

    def save(self, *args, **kwargs):
        # Creates new image sizes. Save new images directly to media server
        # and save the url in a char field.

        img_index = {}

        if self._orig_image_thumb != self.image_thumb and self.image_thumb:
            svlog_info("Creating blog category image variations.")

            img_index['image_lg_square'] = [
                    utils_images.BannerLgSqWebp,
                    self.image_thumb,
                    (500, 500),
                    "configapp/group"]
            img_index['image_md_square'] = [
                    utils_images.BannerMdSqWebp,
                    self.image_thumb,
                    (250, 250),
                    "configapp/group"]
            img_index['image_sm_square'] = [
                    utils_images.BannerSmSqWebp,
                    self.image_thumb,
                    (200, 200),
                    "configapp/group"]

        for k, v in img_index.items():

            file_path = utils_images.process_images(k=k, v=v)

            if k == "image_lg_square":
                self.image_lg_square = file_path
            if k == "image_md_square":
                self.image_md_square = file_path
            if k == "image_sm_square":
                self.image_sm_square = file_path

        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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

    class Meta:
        permissions = [
            ("create_users", "Can create new users."),
            ("view_token", "Can view token."),
            ("change_token", "Can change token."),
        ]

    def __str__(self):
        return self.user.username
