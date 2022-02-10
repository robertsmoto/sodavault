from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


class Timestamps(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Group(Timestamps, models.Model):

    CAT_TYPE_CHOICES = [
        ('CAT', 'Category'),
        ('TAG', 'Tag'),
        ('DEP', 'Department'),
        ('ATT', 'Attribute'),
    ]
    cat_type = models.CharField(
        max_length=3,
        blank=True,
        choices=CAT_TYPE_CHOICES,
    )
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    subgroup = models.ForeignKey(
            'self', on_delete=models.CASCADE, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    is_secondary = models.BooleanField(default=False)
    is_tertiary = models.BooleanField(default=False)
    order = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['name', ]

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
