from django.contrib import admin

# Register your models here.
from library.models import Book, Category, WriterProfile

admin.site.register(WriterProfile)
admin.site.register(Category)
admin.site.register(Book)