# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from imagekit.models import ProcessedImageField
# from imagekit.processors import ResizeToFill
import datetime
from utilities import utils_images
from sodavault.utils_logging import svlog_info


class Location(models.Model):
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
            blank=True)
    description = models.CharField(
            'Category Description',
            max_length=100,
            blank=True)
    kwd_list = models.CharField(
            'Category Keywords',
            max_length=100,
            blank=True,
            help_text="Comma-separated values.")
    image = models.ImageField(
            upload_to=utils_images.new_filename_blog_cat,
            null=True,
            blank=True,
            help_text="recommended size 500px x 500px")
    image_191 = models.ImageField(
            upload_to=utils_images.new_filename_blog_cat,
            null=True,
            blank=True,
            help_text="1.9:1 ratio recommended size 1200px x 630px")
    image_21 = models.ImageField(
            upload_to=utils_images.new_filename_blog_cat,
            null=True,
            blank=True,
            help_text="recommended size 1200px x 600px")

    """The following are automatically generated using the
    model's save method."""

    image_lg_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 500px x 500px")
    image_md_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 250px x 250px")
    image_sm_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 200px x 200px")

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self._orig_image = self.image

    def save(self, *args, **kwargs):
        """Creates new image sizes. Save new images directly to media server
        and save the url in a char field."""

        img_index = {}

        if self._orig_image != self.image and self.image:
            svlog_info("Creating blog category image variations.")

            img_index['image_lg_square'] = [
                    utils_images.BannerLgSqWebp,
                    self.image,
                    (500, 500),
                    "blogapp/category"]
            img_index['image_md_square'] = [
                    utils_images.BannerMdSqWebp,
                    self.image,
                    (250, 250),
                    "blogapp/category"]
            img_index['image_sm_square'] = [
                    utils_images.BannerSmSqWebp,
                    self.image,
                    (200, 200),
                    "blogapp/category"]

        for k, v in img_index.items():

            file_path = utils_images.process_images(k=k, v=v)

            if k == "image_lg_square":
                self.image_lg_square = file_path
            if k == "image_md_square":
                self.image_md_square = file_path
            if k == "image_sm_square":
                self.image_sm_square = file_path

        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "05. Categories"

    def __str__(self):
        return '%s' % (self.name)


class Tag(models.Model):
    name = models.CharField(
            'Tag Name',
            max_length=100,
            blank=True)
    description = models.CharField(
            'Tag Description',
            max_length=100,
            blank=True)
    kwd_list = models.CharField(
            'Tag Keywords',
            max_length=100,
            blank=True,
            help_text="Comma-separated values.")
    image = models.ImageField(
            upload_to=utils_images.new_filename_blog_tag,
            null=True,
            blank=True,
            help_text="recommended size 500px x 500px")
    image_191 = models.ImageField(
            upload_to=utils_images.new_filename_blog_tag,
            null=True,
            blank=True,
            help_text="1.9:1 ratio recommended size 1200px x 630px")
    image_21 = models.ImageField(
            upload_to=utils_images.new_filename_blog_tag,
            null=True,
            blank=True,
            help_text="recommended size 1200px x 600px")

    """The following are automatically generated using the
    model's save method."""

    image_lg_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 500px x 500px")
    image_md_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 250px x 250px")
    image_sm_square = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 200px x 200px")

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self._orig_image = self.image

    def save(self, *args, **kwargs):
        """Creates new image sizes. Save new images directly to media server
        and save the url in a char field."""

        img_index = {}

        if self._orig_image != self.image and self.image:
            svlog_info("Creating blog tag image variations.")

            img_index['image_lg_square'] = [
                    utils_images.BannerLgSqWebp,
                    self.image,
                    (500, 500),
                    "blogapp/tag"]
            img_index['image_md_square'] = [
                    utils_images.BannerMdSqWebp,
                    self.image,
                    (250, 250),
                    "blogapp/tag"]
            img_index['image_sm_square'] = [
                    utils_images.BannerSmSqWebp,
                    self.image,
                    (200, 200),
                    "blogapp/tag"]

        for k, v in img_index.items():

            file_path = utils_images.process_images(k=k, v=v)

            if k == "image_lg_square":
                self.image_lg_square = file_path
            if k == "image_md_square":
                self.image_md_square = file_path
            if k == "image_sm_square":
                self.image_sm_square = file_path

        super(Tag, self).save(*args, **kwargs)

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
            related_name='posts')
    categories = models.ManyToManyField(
            Category,
            blank=True,
            related_name='posts')
    tags = models.ManyToManyField(
            Tag,
            blank=True,
            related_name='posts')
    author = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            related_name='posts')
    menu_order = models.IntegerField(
            'Menu Order',
            default=0,
            help_text="Use to order menu")
    parent = models.ForeignKey(
            'self',
            on_delete=models.CASCADE,
            blank=True,
            null=True,
            related_name='children',
            help_text="Self-referencing field to nest menus.")
    is_primary_menu = models.BooleanField(
            default=False,
            help_text="Use if in primary menu.")
    is_secondary_menu = models.BooleanField(
            default=False,
            help_text="Use if in secondary menu.")
    is_footer_menu = models.BooleanField(
            default=False,
            help_text="Use if in footer menu.")
    post_type = models.CharField(
            'Post Type',
            max_length=20,
            choices=POST_TYPE_CHOICES,
            default='ARTI',)
    title = models.CharField(
            'Title',
            max_length=200,
            blank=True,)
    excerpt = RichTextUploadingField(
            max_length=200,
            null=True,
            blank=True,
            help_text='Max 200 characters.',
            config_name='blog',)
    body = RichTextUploadingField(
            null=True,
            blank=True,
            config_name='blog',)
    slug = models.SlugField('Slug',)  # <-- add autofill in admin
    status = models.CharField(
            'Status',
            choices=STATUS_CHOICES,
            max_length=5,
            blank=True,)
    featured = models.BooleanField(
            'Featured Post',
            default=False,
            help_text='Moves post to front page.')
    date_published = models.DateField(
            'Date Published',
            default=datetime.date.today,)
    date_modified = models.DateField(
            'Date Modified',
            default=datetime.date.today,
            blank=True,
            null=True,)
    kwd_list = models.CharField(
            'Keyword List',
            max_length=200,
            blank=True,
            help_text='comma-separated list')
    image_featured = models.ImageField(
            upload_to=utils_images.new_filename_blog_feat,
            null=True,
            blank=True,
            help_text="Recommended size: 1600 x 800px")
    image_thumb = models.ImageField(
            upload_to=utils_images.new_filename_blog_thumb,
            null=True,
            blank=True,
            help_text="Recommended size: 500 x 500px")
    image_191 = models.ImageField(
            upload_to=utils_images.new_filename_blog_tag,
            null=True,
            blank=True,
            help_text="1.9:1 ratio recommended size 1200px x 630px")
    image_21 = models.ImageField(
            upload_to=utils_images.new_filename_blog_tag,
            null=True,
            blank=True,
            help_text="recommended size 1200px x 600px")
    image_title = models.CharField(
            'Image Title',
            max_length=200,
            blank=True,
            help_text="Alt text for image.")
    image_caption = models.CharField(
            'Image Caption',
            max_length=200,
            blank=True,
            help_text="Caption for image.")
    footer = RichTextUploadingField(
            null=True,
            blank=True,
            help_text=(
                "Use for footnotes, redactions and notes of "
                "changes or updates."),
            config_name='blog',)

    """The following are automatically generated using the
    model's save method."""

    featured_lg = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 1600px x 800px")
    featured_md = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 800px x 400px")
    featured_sm = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 400px x 200px")

    thumb_lg = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 500px x 500px")
    thumb_md = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 250px x 250px")
    thumb_sm = models.CharField(
            max_length=200,
            blank=True,
            help_text="automatic size: 200px x 200px")

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self._orig_image_featured = self.image_featured
        self._orig_image_thumb = self.image_thumb

    def metadata_data(self):
        data = {
                'title': self.title,
                'description': self.excerpt,
                'image': 'hello'
                }
        return data

    def save(self, *args, **kwargs):
        """Creates new image sizes. Save new images directly to media server
        and save the url in a char field."""

        img_index = {}

        if (
                self._orig_image_featured != self.image_featured
                and self.image_featured):

            svlog_info("Creating blog featured image variations.")

            img_index['featured_lg'] = [
                    utils_images.FeaturedLgWebp,
                    self.image_featured,
                    (1600, 800),
                    "blogapp/featured"]
            img_index['featured_md'] = [
                    utils_images.FeaturedMdWebp,
                    self.image_featured,
                    (800, 400),
                    "blogapp/featured"]
            img_index['featured_sm'] = [
                    utils_images.FeaturedSmWebp,
                    self.image_featured,
                    (400, 200),
                    "blogapp/featured"]

        if (
                self._orig_image_thumb != self.image_thumb
                and self.image_thumb):

            svlog_info("Creating blog thumbnail image variations.")

            img_index['thumb_lg'] = [
                    utils_images.BannerLgSqWebp,
                    self.image_thumb,
                    (500, 500),
                    "blogapp/thumbnail"]
            img_index['thumb_md'] = [
                    utils_images.BannerMdSqWebp,
                    self.image_thumb,
                    (250, 250),
                    "blogapp/thumbnail"]
            img_index['thumb_sm'] = [
                    utils_images.BannerSmSqWebp,
                    self.image_thumb,
                    (200, 200),
                    "blogapp/thumbnail"]

        for k, v in img_index.items():

            file_path = utils_images.process_images(k=k, v=v)

            if k == "featured_lg":
                self.featured_lg = file_path
            if k == "featured_md":
                self.featured_md = file_path
            if k == "featured_sm":
                self.featured_sm = file_path
            if k == "thumb_lg":
                self.thumb_lg = file_path
            if k == "thumb_md":
                self.thumb_md = file_path
            if k == "thumb_sm":
                self.thumb_sm = file_path

        super(Post, self).save(*args, **kwargs)

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
            self.post_type = 'ARTI'
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
            self.post_type = 'DOCS'
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
            self.post_type = 'PAGE'
        super(Page, self).save(*args, **kwargs)
