from django.contrib import admin
import blogapp.models


class ImageInline(admin.StackedInline):
    model = blogapp.models.Image
    fields = [
        ('title', 'caption'),
        ('featured', 'order'),
        ('lg_11', 'md_11', 'sm_11'),
        ('lg_21', 'md_21', 'sm_21'),
        'lg_191',
        'custom',
    ]
    readonly_fields = ['md_11', 'sm_11', 'md_21', 'sm_21']
    verbose_name = "image"
    verbose_name_plural = "images"
    extra = 0


class ReviewInline(admin.TabularInline):
    fields = ['rating', 'endorsement']
    model = blogapp.models.Review


class HoursInline(admin.TabularInline):
    model = blogapp.models.OpeningHours


class IngredientInline(admin.TabularInline):
    model = blogapp.models.Ingredient


class RecipeInline(admin.StackedInline):
    model = blogapp.models.Recipe


@admin.register(blogapp.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = [
            'parent',
            ('name', 'slug'),
            'description',
            'kwd_list',
            ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
            ]
    prepopulated_fields = {'slug': ('name',), }
    autocomplete_fields = ['parent']


@admin.register(blogapp.models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = [
            'parent',
            ('name', 'slug'),
            'description',
            'kwd_list',
            ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
            ]
    prepopulated_fields = {'slug': ('name',), }
    autocomplete_fields = ['parent']


@admin.register(blogapp.models.LocalBusiness)
class LocalBusinessAdmin(admin.ModelAdmin):
    inlines = [HoursInline, ReviewInline]

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(blogapp.models.Book)
class ReviewBookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(blogapp.models.Movie)
class ReviewMovieAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(blogapp.models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(blogapp.models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


# class ArticleForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
        # super(ArticleForm, self).__init__(*args, **kwargs)
        # self.fields['parent'].queryset = blogapp.models.Article.objects.all()

    # class Meta:
        # model = blogapp.models.Post
        # fields = '__all__'


# @admin.register(blogapp.models.Post)
# class PostAdmin(admin.ModelAdmin):
    # search_fields = ['id']


POST_FIELDS = [
    ("websites", "parent"),
    ("title", "slug"),
    ("menu_order", "is_primary", "is_secondary", "is_tertiary"),
    ("status", "is_featured"),
    ("date_published", "date_modified"),
    "excerpt",
    "body",
    "footer",
    ("categories", "tags", "kwd_list"),
    ]
POST_SEARCH_FIELDS = ['title']
POST_AUTOCOMPLETE = ["websites", "categories", "tags", "parent"]
POST_INLINES = [ImageInline, ]
POST_LIST_DISPLAY = ["title", "status", "date_published"]
POST_LIST_EDITABLE = ["status"]
POST_LIST_FILTER = ["status", "websites__domain"]
POST_PREPOPULATED_FIELDS = {"slug": ("title",)}


@admin.register(blogapp.models.Article)
class ArticleAdmin(admin.ModelAdmin):

    # form = ArticleForm
    fields = POST_FIELDS.copy()
    fields.append(("local_business", "book", "movie", "recipe"))
    search_fields = POST_SEARCH_FIELDS
    autocomplete_fields = POST_AUTOCOMPLETE
    inlines = POST_INLINES
    list_display = POST_LIST_DISPLAY
    list_filter = POST_LIST_FILTER
    list_editable = POST_LIST_EDITABLE
    prepopulated_fields = POST_PREPOPULATED_FIELDS

    def save_formset(self, request, form, formset, change):
        """This method ensures that there is a user saved in the Image
        model before the image file paths are updated."""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, blogapp.models.Image):
                instance.user = request.user
                instance.save()
        formset.save()


@admin.register(blogapp.models.Doc)
class DocAdmin(admin.ModelAdmin):

    # form = ArticleForm
    fields = POST_FIELDS  # .append(("local_business", "book", "movie", "recipe"))
    search_fields = POST_SEARCH_FIELDS
    autocomplete_fields = POST_AUTOCOMPLETE
    inlines = POST_INLINES
    list_display = POST_LIST_DISPLAY
    list_filter = POST_LIST_FILTER
    list_editable = POST_LIST_EDITABLE
    prepopulated_fields = POST_PREPOPULATED_FIELDS

    def save_formset(self, request, form, formset, change):
        """This method ensures that there is a user saved in the Image
        model before the image file paths are updated."""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, blogapp.models.Image):
                instance.user = request.user
                instance.save()
        formset.save()


@admin.register(blogapp.models.Page)
class PageAdmin(admin.ModelAdmin):

    # form = ArticleForm
    fields = POST_FIELDS  # .append(("local_business", "book", "movie", "recipe"))
    search_fields = POST_SEARCH_FIELDS
    autocomplete_fields = POST_AUTOCOMPLETE
    inlines = POST_INLINES
    list_display = POST_LIST_DISPLAY
    list_filter = POST_LIST_FILTER
    list_editable = POST_LIST_EDITABLE
    prepopulated_fields = POST_PREPOPULATED_FIELDS

    def save_formset(self, request, form, formset, change):
        """This method ensures that there is a user saved in the Image
        model before the image file paths are updated."""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, blogapp.models.Image):
                instance.user = request.user
                instance.save()
        formset.save()
