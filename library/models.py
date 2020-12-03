from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


def save_dir(instance, filename):
    return f'./book/{instance.id}-{filename}'


# Create your models here.
# set a profile for writers
# other ways:
# over write user model
class WriterProfile(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(verbose_name=_("name"), max_length=50)
    stage_name = models.CharField(verbose_name=_("stage name"), blank=True, max_length=50)
    number_of_books = models.PositiveIntegerField(verbose_name=_("number of books"), default=0,)
    birthday = models.DateField(verbose_name=_("birthday"), blank=True)
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name=_("user"), related_name="WriterProfile",
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="category")
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.parent and self == self.parent.parent:
            raise ValidationError("you cant set this to category")


class Book(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(verbose_name=_("name"), max_length=50)
    writer = models.ForeignKey("WriterProfile", blank=True, null=True, verbose_name=_("writer"),
                               on_delete=models.CASCADE, related_name="Book")
    publisher = models.CharField(verbose_name=_("name"), max_length=50)
    description = models.TextField(verbose_name=_("description"), blank=True)
    release_date = models.DateField(verbose_name=_("release date"))
    book = models.FileField(blank=True, upload_to=save_dir, verbose_name=_("book"))
    categurise = models.ManyToManyField('Category', verbose_name=_("categurise"), related_name="book")
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.writer.name} -- {self.name}'

    def save(self, *args, **kwargs):
        old_file = ''
        if self.book:
            old_file = self.book
            self.book = ''
            super().save(*args, **kwargs)
        self.book = old_file
        super().save(*args, **kwargs)
