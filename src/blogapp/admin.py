from django.contrib import admin
from .models import Location, Category, Tag
from .models import Article, Doc, Page
from .models import Recipe, Ingredient
from .models import ReviewBusiness, ReviewRestaurant, ReviewBook, ReviewMovie


class IngredientInline(admin.TabularInline):
    model = Ingredient


class RecipeInline(admin.StackedInline):
    model = Recipe


@admin.register(ReviewBusiness)
class ReviewBusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewRestaurant)
class ReviewRestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewBook)
class ReviewBookAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewMovie)
class ReviewMovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ["interests"]
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["topics"]
    autocomplete_fields = ["locations"]
    prepopulated_fields = {"slug": ("name",)}
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["interests"]
    autocomplete_fields = ["locations"]
    prepopulated_fields = {"slug": ("name",)}
    pass


@admin.register(Article)
class PostAdmin(admin.ModelAdmin):

    fields = [
        ("locations", "author"),
        ("title", "slug"),
        ("status", "featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("image_featured", "image_thumb"),
        ("image_191", "image_21"),
        ("image_title", "image_caption"),
        ("categories", "tags", "kwd_list"),
        "recipe",
        ("review_business", "review_restaurant", "review_movie", "review_book")
    ]

    list_display = ["title", "author", "date_published", "status"]
    list_filter = ["status", "locations__domain"]
    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["locations", "categories", "tags"]


@admin.register(Doc)
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


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
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



