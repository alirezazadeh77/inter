from django.contrib import admin

# Register your models here.
from library.models import Book, Category, WriterProfile


@admin.register(Category)
class CtegoriesAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "is_enable"]
    list_filter = ["is_enable", ]
    raw_id_fields = ["parent", ]
    search_fields = ["name", ]
    actions = ['set_enable', 'set_disable']

    def set_enable(self, request, queryset):
        queryset.filter(is_enable=False).update(is_enable=True)

    def set_disable(self, request, queryset):
        queryset.filter(is_enable=True).update(is_enable=False)


@admin.register(WriterProfile)
class WriterProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "stage_name", "birthday"]
    list_filter = ["birthday"]
    search_fields = ["user", ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "writer", "publisher", "book"]
    list_filter = ["release_date", "is_enable"]
    search_fields = ["name", "writer", "publisher", "book", "categorise"]
    actions = ['set_enable', 'set_disable']

    def set_enable(self, request, queryset):
        queryset.filter(is_enable=False).update(is_enable=True)

    def set_disable(self, request, queryset):
        queryset.filter(is_enable=True).update(is_enable=False)
