from django.contrib import admin
from .models import Doc, Breadcrumb


class BreadcrumbInline(admin.TabularInline):
    model = Breadcrumb
    extra = 0


@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    inlines = [
        BreadcrumbInline,
    ]

    list_display = (
        "title",
        "slug",
    )

    list_display_links = (
        'title',
        'slug',
    )

    ordering = ['slug']
    pass


@admin.register(Breadcrumb)
class BreadcrumbAdmin(admin.ModelAdmin):
    list_display = [
        "doc",
        "name",
        "order",
        "url_namespace",
        "url_variables",
    ]
    ordering = [
        "doc",
        "order",
    ]
    pass
