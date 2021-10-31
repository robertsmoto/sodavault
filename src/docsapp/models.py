from django.db import models
import datetime


class Doc(models.Model):

    NORMAL = 'light'
    DANGER = 'danger'
    WARNING = 'warning'
    INFORMATION = 'info'

    COLOR_CHOICES = [
        (NORMAL, 'Normal'),
        (DANGER, 'Danger'),
        (WARNING, 'Warning'),
        (INFORMATION, 'Information'),
    ]
    title = models.CharField(
        "Title",
        max_length=100,
        blank=True,
        help_text="Add Component"
    )
    slug = models.SlugField(
        "Slug",
        help_text="object-action or object-view eg. component-add"
    )
    url = models.URLField(
        "URL",
        blank=True,
        help_text='Link to doc.'
    )
    timestamp_created = models.DateTimeField(
        editable=False,
        blank=True,
        null=True
    )
    timestamp_modified = models.DateTimeField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.timestamp_created = datetime.datetime.utcnow()
        self.timestamp_modified = datetime.datetime.utcnow()
        return super(Doc, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.title)


class Breadcrumb(models.Model):

    doc = models.ForeignKey(
        Doc,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="breadcrumbs"
    )
    name = models.CharField(
        "Name",
        max_length=100,
        blank=True,
        help_text="In last field, use 'title' to use metadata.title, or use_custom_varialbe and coordinate logic with view to use custom name."
    )
    order = models.IntegerField(
        blank=True,
        null=True
    )
    url_namespace = models.CharField(
        "URL Namespace",
        max_length=200,
        blank=True,
        help_text="Must match the URL namespace"
    )
    url_variables = models.CharField(
        "URL Variables",
        max_length=200,
        blank=True,
        help_text="Variables same as view context eg: comp_pk | part_pk"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '%s' % (self.name)
