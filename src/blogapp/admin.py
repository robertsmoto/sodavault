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


@admin.register(Doc)
class PostAdmin(admin.ModelAdmin):
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
class PostAdmin(admin.ModelAdmin):
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
