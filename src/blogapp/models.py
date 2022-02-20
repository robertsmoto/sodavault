from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from sodavault.utils_logging import svlog_info
from utilities import utils_images
import configapp.models
import contactapp.models
import datetime


NOREC = (0, 'Not Recommended')
RECOM = (1, 'Recommended')
ENDORSEMENT_CHOICES = [
    ('NOREC', 'Not Recommended'),
    ('RECOM', 'Recommended'),
]
COUNTRY_CHOICES = [
    ('AT', 'Austria'),
    ('CZ', 'Czech Republic'),
    ('DE', 'Germany'),
    ('FR', 'France'),
    ('IT', 'Italy'),
    ('SK', 'Slovakia'),
    ('US', 'United States of America'),
]
LANGUAGE_CHOICES = [
    ('en-GB', 'English United Kingdom'),
    ('en-IE', 'English Ireland'),
    ('en-US', 'English United States'),
    ('cs-CZ', 'Czech Czech Republic'),
    ('de-DE', 'German Germany'),
    ('fr-FR', 'French France'),
    ('it-IT', 'Italian Italy'),
    ('sk-SK', 'Slovak Slovakia')
]
RATING_CHOICES = [
    ('1_0', '1.0 worst'),
    ('1_5', '1.5'),
    ('2_0', '2.0'),
    ('2_5', '2.5'),
    ('3_0', '3.0 average'),
    ('3_5', '3.5'),
    ('4_0', '4.0'),
    ('4_5', '4.5'),
    ('5_0', '5.0 best')
]
COST_CHOICES = [
    ('FREE', 'Free'),
    ('CHEA', 'Cheap'),
    ('MODE', 'Moderate'),
    ('EXPE', 'Expensive'),
]
RES_TYPE_CHOICES = [
    ('CASU', 'Casual Dining'),
    ('FINE', 'Fine Dining'),
    ('FAST', 'Fast Service'),
]
DOW_CHOICES = [
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
]


class PostCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='POSTCAT')


class PostCategory(configapp.models.Group):

    objects = PostCategoryManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.group_type = 'POSTCAT'
        super(PostCategory, self).save(*args, **kwargs)


class PostTagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='POSTTAG')


class PostTag(configapp.models.Group):

    objects = PostTagManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.group_type = 'POSTTAG'
        super(PostTag, self).save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(
            'Book title',
            max_length=200,
            blank=True,
            null=True)
    isbn = models.CharField(
            'ISBN',
            max_length=13,
            blank=True,)
    author = models.CharField(
            'Book Author',
            max_length=100,
            blank=True,
            null=True,
            help_text='Author of book.')
    author_url = models.URLField(
            'Link to Book Author',
            max_length=100,
            blank=True,
            help_text='Website or wiki of Book Author.')
    url_book = models.URLField(
            'Link to book.',
            max_length=100,
            blank=True,
            help_text='Website of item being reviewed.')
    language = models.CharField(
            'Language',
            max_length=5,
            choices=LANGUAGE_CHOICES,
            default='en-US')
    cost = models.CharField(
            'Cost',
            max_length=4,
            choices=COST_CHOICES,
            blank=True,
            help_text='How expensive?')

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.title)


class Movie(models.Model):
    title = models.CharField(
            'Movie title',
            max_length=200,
            blank=True,
            null=True)
    url_item = models.URLField(
            'Movie website.',
            max_length=100,
            blank=True,)
    language = models.CharField(
            'Language',
            max_length=5,
            choices=LANGUAGE_CHOICES,
            default='en-US')

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.title)


class LocalBusiness(models.Model):
    bus_type = models.CharField(
            'Business Type',
            max_length=200,
            blank=True,
            help_text="Be specific eg. Restaurant, see schema.org 'types'")
    name = models.CharField(
            'Business name',
            max_length=200,
            blank=True)
    address_street = models.CharField(
            'Street Address',
            max_length=100,
            blank=True)
    address_city = models.CharField(
            'City',
            max_length=100,
            blank=True,)
    address_state = models.CharField(
            'State',
            max_length=100,
            blank=True,
            help_text='state or province')
    address_zipcode = models.CharField(
            'Zip Code',
            max_length=20,
            blank=True,)
    address_country = models.CharField(
            'Country',
            choices=COUNTRY_CHOICES,
            max_length=2,
            default='CZ',)
    phone = models.CharField(
            'Phone Number',
            max_length=20,
            blank=True,
            help_text='Including country code, only for businesses.')
    website = models.URLField(
            'Business website.',
            max_length=100,
            blank=True,
            help_text='Use google maps link.')
    map_link = models.URLField(
            'Map link.',
            max_length=100,
            blank=True,
            help_text='Use google maps link.')
    latitude = models.DecimalField(
            'Latitude',
            max_digits=8,
            decimal_places=6,
            blank=True,
            null=True)
    longitude = models.DecimalField(
            'Longitude',
            max_digits=8,
            decimal_places=6,
            blank=True,
            null=True)
    restaurant_menu = models.URLField(
            'Menu',
            max_length=100,
            blank=True,
            help_text='Link to menu for restaurants.')
    restaurant_type = models.CharField(
            'Restaurant Type',
            max_length=4,
            choices=RES_TYPE_CHOICES,
            blank=True,)
    restaurant_cuisine = models.CharField(
            'Cuisine Offered.',
            max_length=100,
            blank=True,
            help_text='Cuisine')
    restaurant_reservations = models.BooleanField(
            'Accepts Reservations',
            default=False,
            help_text='Does the restaurant accept reservations?')
    price_range = models.CharField(
            'Price Range',
            max_length=4,
            choices=COST_CHOICES,
            blank=True,
            help_text='How expensive?')

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)


class OpeningHours(models.Model):
    business = models.ForeignKey(LocalBusiness, on_delete=models.CASCADE)
    day_of_week = models.CharField(
            'Day of Week',
            max_length=3,
            choices=DOW_CHOICES,
            blank=True)
    opens = models.TimeField(
            'Opening Time',
            blank=True,
            null=True)
    closes = models.TimeField(
            'Closing Time',
            blank=True,
            null=True)
    valid_from = models.DateField(
            'Valid from',
            blank=True,
            null=True,
            help_text="Use for special hours eg. holiday hours")
    valid_to = models.DateField(
            'Valid to',
            blank=True,
            null=True,
            help_text="Use for special hours eg. holiday hours")

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.day_of_week)


class Review(models.Model):
    """The review summary, full-lenth review, link to review can all be
    geneated from the linked item"""

    business = models.OneToOneField(
            LocalBusiness,
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    movie = models.OneToOneField(
            Movie,
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    book = models.OneToOneField(
            Book,
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    rating = models.CharField(
            'Rating',
            max_length=3,
            choices=RATING_CHOICES,
            blank=True,
            help_text='5 stars is best.')
    endorsement = models.CharField(
            'Endorsement',
            max_length=5,
            choices=ENDORSEMENT_CHOICES,
            blank=True,
            help_text='Select Recommendation')

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)


class Recipe(models.Model):
    name = models.CharField(
            'Name',
            max_length=100,
            blank=True,
            help_text='Name of dish.')
    prep_time = models.IntegerField(
            'Prep Time',
            blank=True,
            null=True,
            help_text='Time in minutes. eg. 30')
    cook_time = models.IntegerField(
            'Cook Time',
            blank=True,
            null=True,
            help_text='Time in minutes. eg. 45')
    instructions = models.TextField(
            'Instructions',
            blank=True,
            help_text='In a large bowl ...')
    recipe_yield_qnty = models.IntegerField(
            'Yield Qnty',
            blank=True,
            null=True,
            help_text='eg. 25')
    recipe_yield_description = models.CharField(
            'Yield Description',
            max_length=50,
            blank=True,
            help_text='eg. cookies, loaf, servings')
    recipe_yield_notes = models.CharField(
            'Yield Notes',
            max_length=50,
            blank=True,
            help_text='eg. Cookies approx. size 25 grams.')
    cooking_method = models.CharField(
            'Cooking method',
            max_length=50,
            blank=True,
            help_text='eg. Frying, Steaming, Baking.')
    category = models.CharField(
            'Category',
            max_length=50,
            blank=True,
            help_text='eg. Entree, Appetizer, Side.')
    cuisine = models.CharField(
            'Cuisine',
            max_length=50,
            blank=True,
            help_text='eg. Italian, French, American.')
    suitable = models.CharField(
            'Suitable for',
            max_length=50,
            blank=True,
            help_text='Restricted Diet eg. Vegan.')
    nutr_serving = models.CharField(
            'Serving Size',
            max_length=50,
            blank=True,
            help_text='10 gram slice')
    nutr_calories = models.CharField(
            'Number of calories per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_carbs = models.CharField(
            'Grams of carbohydrates per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_choles = models.CharField(
            'Milligrams of cholesterol per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_fat = models.CharField(
            'Grams of fat per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_fiber = models.CharField(
            'Grams of fiber per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_protein = models.CharField(
            'Grams of protein per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_sat_fat = models.CharField(
            'Grams of staurated fat per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_sodium = models.CharField(
            'Milligrams of sodium per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_sugar = models.CharField(
            'Grams of sugar per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_trans_fat = models.CharField(
            'Grams of trans fat per serving.',
            max_length=10,
            blank=True,
            help_text='100')
    nutr_unsat_fat = models.CharField(
            'Grams of unstaurated fat per serving.',
            max_length=10,
            blank=True,
            help_text='100')

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)

    @property
    def total_time(self):
        return self.prep_time + self.cook_time


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    weight = models.IntegerField(
        'Weight (grams)',
        blank=True,
        null=True,
        help_text="Weight in grams. eg. 50"
    )
    name = models.CharField(
        'Ingredient',
        max_length=100,
        blank=True,
        help_text='ex. white onion, celery, pasta'
    )
    notes = models.CharField(
        'Note',
        max_length=200,
        blank=True,
        help_text='ex. finely chopped'
    )

    def __str__(self):
        return '%s' % (self.name)


class Post(models.Model):

    POST_TYPE_CHOICES = [
        ('ARTICLE', 'Article'),
        ('PAGE', 'Page'),
        ('DOC', 'Docs')
    ]
    STATUS_CHOICES = [
        ('PUBLI', 'Published'),
        ('DRAFT', 'Draft'),
        ('TRASH', 'Trash'),
    ]
    websites = models.ManyToManyField(contactapp.models.Website, blank=True)
    categories = models.ManyToManyField(
            PostCategory,
            related_name="category_posts",
            blank=True)
    tags = models.ManyToManyField(
            PostTag,
            related_name="tag_posts",
            blank=True)
    author = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            blank=True,
            null=True)
    parent = models.ForeignKey(
            'self',
            on_delete=models.CASCADE,
            blank=True,
            null=True,
            help_text="Self-referencing field to nest menus.")
    local_business = models.OneToOneField(
            LocalBusiness,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,)
    book = models.OneToOneField(
            Book,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,)
    movie = models.OneToOneField(
            Movie,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,)
    recipe = models.OneToOneField(
            Recipe,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,)
    slug = models.SlugField(
            unique=True,
            help_text="Is required, must be unique.")
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
    status = models.CharField(
            'Status',
            choices=STATUS_CHOICES,
            max_length=5,
            blank=True,)
    is_featured = models.BooleanField(
            'Featured Post',
            default=False,
            help_text='Moves post to front page.')
    menu_order = models.IntegerField(
            'Menu Order',
            default=0,
            help_text="Use to order menu")
    is_primary = models.BooleanField(
            default=False,
            help_text="Use if in primary menu.")
    is_secondary = models.BooleanField(
            default=False,
            help_text="Use if in secondary menu.")
    is_tertiary = models.BooleanField(
            default=False,
            help_text="Use if in footer menu.")
    post_type = models.CharField(
            'Post Type',
            max_length=20,
            choices=POST_TYPE_CHOICES,
            default='article',)
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
            help_text='Comma-separated list')
    image_featured = models.ImageField(
            upload_to=utils_images.new_filename_blog_feat,
            null=True,
            blank=True,
            help_text="Recommended size: 1200 x 600px")
    image_thumb = models.ImageField(
            upload_to=utils_images.new_filename_blog_thumb,
            null=True,
            blank=True,
            help_text="Recommended size: 500 x 500px")
    image_191 = models.ImageField(
            upload_to=utils_images.new_filename_blog_feat,
            null=True,
            blank=True,
            help_text="1.9:1 ratio recommended size 1200px x 630px")
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
            help_text="Automatic size: 1200px x 600px")
    featured_md = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 800px x 400px")
    featured_sm = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 400px x 200px")

    thumb_lg = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 500px x 500px")
    thumb_md = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 250px x 250px")
    thumb_sm = models.CharField(
            max_length=200,
            blank=True,
            help_text="Automatic size: 200px x 200px")

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
                    (1200, 600),
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
        ordering = ('-is_featured', '-date_published')
        indexes = [
            models.Index(fields=[
                'status',
                'date_published',
                'post_type',
                'is_featured'
            ]),
        ]


"""Using proxy models for: 1. Articles 2. Docs 3. Pages"""


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post_type='ARTICLE')


class Article(Post):
    objects = ArticleManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Articles"

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.post_type != 'ARTICLE':
            self.post_type = 'ARTICLE'
        super(Article, self).save(*args, **kwargs)


class DocManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post_type='DOC')


class Doc(Post):
    objects = DocManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Docs"

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.post_type != 'DOC':
            self.post_type = 'DOC'
        super(Doc, self).save(*args, **kwargs)


class PageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post_type='PAGE')


class Page(Post):
    objects = PageManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Pages"

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.post_type != 'PAGE':
            self.post_type = 'PAGE'
        super(Page, self).save(*args, **kwargs)
