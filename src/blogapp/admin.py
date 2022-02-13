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
    fields = [
            ('websites', 'parent'),
            ('name', 'slug'),
            ('description', 'kwd_list'),
            ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
            ('image_thumb', 'image_21', 'image_191'),
            ('image_lg_square', 'image_md_square', 'image_sm_square')
            ]
    search_fields = ["categories"]
    readonly_fields = ['image_lg_square', 'image_md_square', 'image_sm_square']
    autocomplete_fields = ["websites"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(blogapp.models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = [
            ('websites', 'parent'),
            ('name', 'slug'),
            ('description', 'kwd_list'),
            ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
            ('image_thumb', 'image_21', 'image_191'),
            ('image_lg_square', 'image_md_square', 'image_sm_square')
            ]
    search_fields = ["tags"]
    readonly_fields = ['image_lg_square', 'image_md_square', 'image_sm_square']
    autocomplete_fields = ["websites"]
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
        ("websites", "parent"),
        ("title", "slug"),
        (
            "menu_order", "is_primary_menu", "is_secondary_menu",
            "is_footer_menu"),
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


@admin.register(blogapp.models.Doc)
class DocAdmin(admin.ModelAdmin):
    fields = [
        ("websites", "parent"),
        ("title", "slug"),
        (
            "menu_order", "is_primary_menu", "is_secondary_menu",
            "is_footer_menu"),
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


@admin.register(blogapp.models.Page)
class PageAdmin(admin.ModelAdmin):
    fields = [
        ("websites", "parent"),
        ("title", "slug"),
        (
            "menu_order", "is_primary_menu", "is_secondary_menu",
            "is_footer_menu"),
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
