from django import forms
from django.contrib import admin
import blogapp.models


class ReviewInline(admin.TabularInline):
    fields = ['rating', 'endorsement']
    model = blogapp.models.Review


class HoursInline(admin.TabularInline):
    model = blogapp.models.OpeningHours


class IngredientInline(admin.TabularInline):
    model = blogapp.models.Ingredient


class RecipeInline(admin.StackedInline):
    model = blogapp.models.Recipe


@admin.register(blogapp.models.PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    fields = [
            ('name', 'slug', 'parent'),
            ('description', 'kwd_list'),
            ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
            ('image_thumb', 'image_21', 'image_191'),
            ('image_lg_square', 'image_md_square', 'image_sm_square')
            ]
    search_fields = ["categories"]
    readonly_fields = ['image_lg_square', 'image_md_square', 'image_sm_square']
    prepopulated_fields = {"slug": ("name",)}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PostCategoryAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="POSTCAT")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "POSTCAT"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(blogapp.models.PostTag)
class PostTagAdmin(admin.ModelAdmin):
    fields = [
            ('name', 'slug', 'parent'),
            ('description', 'kwd_list'),
            ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
            ('image_thumb', 'image_21', 'image_191'),
            ('image_lg_square', 'image_md_square', 'image_sm_square')
            ]
    search_fields = ["tags"]
    readonly_fields = ['image_lg_square', 'image_md_square', 'image_sm_square']
    prepopulated_fields = {"slug": ("name",)}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PostTagAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="POSTTAG")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "POSTTAG"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


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
        ("image_featured", "image_thumb", "image_191"),
        ("image_title", "image_caption"),
        ("categories", "tags", "kwd_list"),
        ("local_business", "book", "movie", "recipe")
    ]

    list_display = ["title", "author", "date_published", "status"]
    list_filter = ["status", "websites__domain"]
    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["websites", "categories", "tags"]


class DocForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DocForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = blogapp.models.Doc.objects.all()

    class Meta:
        model = blogapp.models.Post
        fields = '__all__'


@admin.register(blogapp.models.Doc)
class DocAdmin(admin.ModelAdmin):

    form = DocForm

    fields = [
        ("websites", "parent"),
        ("title", "slug"),
        ("menu_order", "is_primary", "is_secondary", "is_tertiary"),
        ("author", "status", "is_featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("image_featured", "image_thumb", "image_191"),
        ("image_title", "image_caption"),
        ("categories", "tags", "kwd_list"),
    ]

    list_display = ["title", "author", "date_published", "status"]
    list_filter = ["status", "websites__domain"]
    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["websites", "categories", "tags"]


class PageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = blogapp.models.Page.objects.all()

    class Meta:
        model = blogapp.models.Post
        fields = '__all__'


@admin.register(blogapp.models.Page)
class PageAdmin(admin.ModelAdmin):

    form = PageForm

    fields = [
        ("websites", "parent"),
        ("title", "slug"),
        ("menu_order", "is_primary", "is_secondary", "is_tertiary"),
        ("author", "status", "is_featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("image_featured", "image_thumb", "image_191"),
        ("image_title", "image_caption"),
        ("categories", "tags", "kwd_list"),
    ]

    list_display = ["title", "author", "date_published", "status"]
    list_filter = ["status", "websites__domain"]
    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["websites", "categories", "tags"]
