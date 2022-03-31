from django import forms
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


@admin.register(blogapp.models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


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


class ArticleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = blogapp.models.Article.objects.all()

    class Meta:
        model = blogapp.models.Post
        fields = '__all__'


@admin.register(blogapp.models.Article)
class ArticleAdmin(admin.ModelAdmin):

    form = ArticleForm
    fields = [
        ("websites", "parent"),
        ("title", "slug"),
        ("menu_order", "is_primary", "is_secondary", "is_tertiary"),
        ("author", "status", "is_featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("categories", "tags", "kwd_list"),
        ("local_business", "book", "movie", "recipe")
    ]
    autocomplete_fields = ["websites", "categories", "tags"]
    inlines = [ImageInline, ]
    list_display = ["title", "author", "status", "date_published", ]
    list_filter = ["author", "status", "websites__domain"]
    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}

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
class DocAdmin(ArticleAdmin):
    pass


@admin.register(blogapp.models.Page)
class PageAdmin(ArticleAdmin):
    pass
