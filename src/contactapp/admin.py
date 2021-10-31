from django.contrib import admin
from .models import Company, Person


class PersonInline(admin.StackedInline):
    model = Person
#     fields = [
        # ('gtin', 'isbn'),
        # ('pid_i', 'pid_c')
    # ]
    extra = 0
    verbose_name = "people"


@admin.register(Person)                                                        
class PersonAdmin(admin.ModelAdmin):  

    verbose_name = "people"


@admin.register(Company)
class CategoryAdmin(admin.ModelAdmin):
#     list_display = [
        # 'name',
        # 'parent',
        # 'slug',
    # ]
#     ordering = [
        # '-slug',
        # 'name'
    # ]
#     list_display_links = [
        # 'name',
    # ]
    # list_filter = [ 
        # 'parent',
    # ]
    search_fields = ['name']
#     fields = [
        # 'parent',
        # 'name',
        # 'slug'
    # ]
   
#     prepopulated_fields = {'slug': ('name',)}
    # autocomplete_fields = ['parent']
    inlines = [PersonInline,]

    verbose_name = "companies"
