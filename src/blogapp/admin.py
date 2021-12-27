from django.contrib import admin
from .models import *


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ["interests"]
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["topics"]
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["interests"]
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
        ("featured_image", "thumbnail_image"),
        ("image_title", "image_caption"),
        ("categories", "tags", "keyword_list"),
    ]

    list_display = ["title", "locations", "author", "date_published", "status"]
    list_filter = ["status"]

    list_editable = ["author", "status"]

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["locations", "categories", "tags"]


@admin.register(Doc)
class PostAdmin(admin.ModelAdmin):
    fields = [
        ("locations", "post_type"),
        ("title", "slug"),
        ("parent", "menu_order", "primary_menu"),
        ("keyword_list", "author"),
        ("status", "featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("featured_image", "thumbnail_image"),
        ("image_title", "image_caption"),
        ("categories", "tags"),
    ]

    pass


@admin.register(Page)
class PostAdmin(admin.ModelAdmin):
    fields = [
        ("locations", "post_type"),
        ("title", "slug"),
        ("parent", "menu_order", "primary_menu"),
        ("keyword_list", "author"),
        ("status", "featured"),
        ("date_published", "date_modified"),
        "excerpt",
        "body",
        "footer",
        ("featured_image", "thumbnail_image"),
        ("image_title", "image_caption"),
        ("categories", "tags"),
    ]

    pass
