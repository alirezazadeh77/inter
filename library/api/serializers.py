from django.contrib.auth.models import User
from rest_framework import serializers

from library.models import WriterProfile, Category, Book


class WriterProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = WriterProfile
        fields = ['stage_name', 'birthday', 'number_of_books', 'user', ]
        read_only_fields = ['user', 'number_of_books']

    def get_user(self, obj):
        user = User.objects.get(id=obj.id)
        return user.username

    def create(self, validated_data):
        default = {'stage_name': validated_data.pop('stage_name', ""),
                   'birthday': validated_data.pop('birthday', "0001-01-01")}
        instance, _created = WriterProfile.objects.update_or_create(
            **validated_data,
            defaults=default
        )
        return instance


class CategorySerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'child']

    def get_child(self, obj):
        query = Category.objects.filter(parent=obj.id)
        serializer = CategorySerializer(query, many=True)
        return serializer.data


class BookSerializer(serializers.ModelSerializer):
    categorise = CategorySerializer(many=True)
    writer = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'writer', 'publisher', 'description', 'release_date', 'book', 'categorise']
        read_only_fields = ['writer', 'id']

    def get_writer(self, obj):
        return f'{obj.writer}'

    def create(self, validated_data):
        _temp = []
        categorise = validated_data.pop('categorise')
        for category in categorise:
            _temp.append(Category.objects.get(name=category['name']))

        instance, _created = Book.objects.update_or_create(
            **validated_data,
        )

        for category in _temp:
            instance.categorise.add(category)

        return instance
