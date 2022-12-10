from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    def save(self, *args, **kwargs):
        if not self.cdn_dir:
            self.cdn_dir = str(uuid.uuid4())[:13]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL,
)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class APICredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    aid = models.CharField(
        primary_key = False,
        default = uuid.uuid4,
        editable = False,
        max_length=36
        )
    auth = models.CharField(
        primary_key = False,
        default = uuid.uuid4,
        editable = True,
        max_length=36
        )
    prefix = models.CharField(
        primary_key = False,
        default = uuid.uuid4,
        editable = False,
        max_length=36
        )
    is_current = models.BooleanField(
        default = False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_apicredentials(sender, instance, created, **kwargs):
        if created:
            APICredentials.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_apicredentials(sender, instance, **kwargs):
        instance.apicredentials.save()
