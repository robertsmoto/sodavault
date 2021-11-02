from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import datetime


class Location(models.Model):
    domain = models.CharField(
            'Domain eg. example.com',
        max_length=200,
        blank=True
    )
    name = models.CharField(
        'Location Name',
        max_length=200,
        blank=True
    )
    description = models.CharField(
        'Location Description',
        max_length=200,
        blank=True
    )

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "04. Locations"

    def __str__(self):
        return '%s' % (self.name)


class Category(models.Model):
    name = models.CharField(
        'Category Name',
        max_length=100,
        blank=True
    )
    description = models.CharField(
        'Category Description',
        max_length=100,
        blank=True
    )
    image = ProcessedImageField(
        upload_to='blog_images/category/%Y/%m/%d/',
        processors=[ResizeToFill(250, 250)],
        format='WebP',
        options={'quality': 60},
        null=True,
        blank=True,
        help_text="resizes to 250 x 250px"
    )

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "05. Categories"

    def __str__(self):
        return '%s' % (self.name)


class Tag(models.Model):
    name = models.CharField(
        'Tag Name',
        max_length=100,
        blank=True
    )

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "06. Tags"

    def __str__(self):
        return '%s' % (self.name)

class Post(models.Model):

    POST_TYPE_CHOICES = [
        ('ARTI', 'Article'),
        ('PAGE', 'Page'),
        ('DOCS', 'Docs')
    ]
    STATUS_CHOICES = [
        ('PUBLI', 'Published'),
        ('DRAFT', 'Draft'),
        ('TRASH', 'Trash'),
    ]
    locations = models.ManyToManyField(
        Location,
        blank=True,
        related_name='posts'
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts'
    )
    menu_order = models.IntegerField(
        'Menu Order',
        blank=True,
        null=True,
        help_text="Use to order menu"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        help_text="Self-referencing field to nest menus."
    )
    primary_menu = models.BooleanField(
        default=False,
        help_text="Use if in primary menu."
    )
    post_type = models.CharField(
        'Post Type',
        max_length=20,
        choices=POST_TYPE_CHOICES,
        default='ARTI',
    )
    title = models.CharField(
        'Title',
        max_length=200,
        blank=True,
    )
    excerpt = RichTextUploadingField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Max 200 characters.',
        config_name='blog',
    )
    body = RichTextUploadingField(
        null=True,
        blank=True,
        config_name='blog',
    )
    slug = models.SlugField(
        'Slug',
    )  # <-- add autofill in admin
    status = models.CharField(
        'Status',
        choices=STATUS_CHOICES,
        max_length=5,
        blank=True,
    )
    featured = models.BooleanField(
        'Featured Post',
        default=False,
        help_text='Moves post to front page.'
    )
    date_published = models.DateField(
        'Date Published',
        default=datetime.date.today,
    )
    date_modified = models.DateField(
        'Date Modified',
        default=datetime.date.today,
        blank=True,
        null=True,
    )
    keyword_list = models.CharField(
        'Keyword List',
        max_length=200,
        blank=True,
        help_text='comma, separated, list'
    )
    featured_image = ProcessedImageField(
        upload_to='blog_images/featured/%Y/%m/%d/',
        processors=[ResizeToFill(800, 400)],
        format='WebP',
        options={'quality': 60},
        null=True,
        blank=True,
        help_text="resizes to 800 x 400px"
    )
    thumbnail_image = ProcessedImageField(
        upload_to='blog_images/thumbnail/%Y/%m/%d/',
        processors=[ResizeToFill(250, 250)],
        format='WebP',
        options={'quality': 60},
        null=True,
        blank=True,
        help_text="resizes to 250 x 250px"
    )
    image_title = models.CharField(
        'Image Title',
        max_length=200,
        blank=True,
        help_text="Alt text for image."
    )
    image_caption = models.CharField(
        'Image Caption',
        max_length=200,
        blank=True,
        help_text="Caption for image."
    )
    footer = RichTextUploadingField(
        null=True,
        blank=True,
        help_text="Use for footnotes, redactions and notes of changes or updates.",
        config_name='blog',
    )

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.title)

    def get_absolute_url(self):
        return reverse(
            'blogapp-post-detail',
            args=[
                str.lower(self.post_type),
                str(self.date_published.year),
                str(self.date_published.month),
                str(self.date_published.day),
                str(self.slug)
            ],
        )

    @property
    def reading_time(self):
        text = ""
        if len(self.body) > 0 or len(self.excerpt) > 0:
            text = self.body + self.excerpt
        time = round((len(text.split()) / 250))
        if time < 1:
            time = 1
        return time

    class Meta:
        ordering = ('-featured', '-date_published')

        indexes = [
            models.Index(fields=[
                'status',
                'date_published',
                'post_type',
                'featured'
            ]),
        ]


"""
Using proxy models for:
    1. Articles
    2. Docs
    3. Pages
"""

class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post_type='ARTI')

class Article(Post):
    objects = ArticleManager()

    class Meta:
        proxy = True
        verbose_name_plural = "01. Articles"


    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.post_type == '':
            self.post_type='ARTI'
        super(Article, self).save(*args, **kwargs)

class DocManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post_type='DOCS')

class Doc(Post):
    objects = DocManager()

    class Meta:
        proxy = True
        verbose_name_plural = "02. Docs"

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.post_type == '':
            self.post_type='DOCS'
        super(Article, self).save(*args, **kwargs)

class PageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post_type='PAGE')

class Page(Post):
    objects = PageManager()

    class Meta:
        proxy = True
        verbose_name_plural = "03. Pages"

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.post_type == '':
            self.post_type='PAGE'
        super(Page, self).save(*args, **kwargs)

