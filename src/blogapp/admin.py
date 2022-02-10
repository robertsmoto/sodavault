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


@admin.register(blogapp.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["categories"]
    exclude = ["group_type"]
    autocomplete_fields = ["locations"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(blogapp.models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["tags"]
    exclude = ["group_type"]
    autocomplete_fields = ["locations"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(blogapp.models.LocalBusiness)
class LocalBusinessAdmin(admin.ModelAdmin):
    inlines = [HoursInline, ReviewInline]
    pass


@admin.register(blogapp.models.Book)
class ReviewBookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    pass


@admin.register(blogapp.models.Movie)
class ReviewMovieAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    pass


@admin.register(blogapp.models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(blogapp.models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]
    pass


@admin.register(blogapp.models.Article)
class PostAdmin(admin.ModelAdmin):

    fields = [
        ("locations", "author"),
        ("title", "slug"),
        ("status", "is_featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("image_featured", "image_191", "image_thumb"),
        ("image_title", "image_caption"),
        ("categories", "tags", "kwd_list"),
        "recipe",
        ("local_business", "movie", "book"),
    ]

    list_display = ["title", "author", "date_published", "status"]
    list_filter = ["status", "locations__domain"]
    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["locations", "categories", "tags"]


@admin.register(blogapp.models.Doc)
class DocAdmin(admin.ModelAdmin):
    fields = [
        ("locations"),
        ("title", "slug"),
        (
            "parent", "menu_order", "is_primary_menu", "is_secondary_menu",
            "is_footer_menu"),
        ("author"),
        ("status", "featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("image_featured", "image_thumb"),
        ("image_191", "image_21"),
        ("image_title", "image_caption"),
        ("categories", "tags", "kwd_list"),
    ]

    list_display = ["title", "author", "date_published", "status"]
    list_filter = ["status", "locations__domain"]
    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["locations", "categories", "tags"]


@admin.register(blogapp.models.Page)
class PageAdmin(admin.ModelAdmin):
    fields = [
        ("locations"),
        ("title", "slug"),
        (
            "parent", "menu_order", "is_primary_menu", "is_secondary_menu",
            "is_footer_menu"),
        ("author"),
        ("status", "is_featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("image_featured", "image_thumb", "image_191"),
        ("image_title", "image_caption"),
        ("categories", "tags", "kwd_list"),
    ]

    list_display = ["title", "author", "date_published", "status"]
    list_filter = ["status", "locations__domain"]
    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["locations", "categories", "tags"]
