from django.contrib.auth.models import User
from rest_framework import serializers

from library.models import WriterProfile, Category, Book


class WriterProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = WriterProfile
        fields = ['stage_name', 'birthday', 'number_of_books', 'user', ]
        read_only_fields = ['user', 'number_of_books']

    def get_user(self,obj):
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
    categurise = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = ['name', 'writer', 'publisher', 'description', 'release_date', 'book', 'categurise']
