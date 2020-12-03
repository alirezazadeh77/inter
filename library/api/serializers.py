from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from library.models import WriterProfile, Category, Book


class WriterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterProfile
        fields = ['stage_name', 'birthday', 'number_of_books', 'user', ]
        read_only_fields = ['birthday', 'stage_name', ]

    def create(self, validated_data):
        default = {'stage_name': validated_data.pop('stage_name', ""),
                   'birthday': validated_data.pop('birthday', "0000-00-00")}
        instance, _created = WriterProfile.objects.update_or_create(
            **validated_data,
            defaults=default
        )
        return instance


class CategorySerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'child']

    def get_child(self, obj):
        query = Category.objects.filter(parent=obj.id)
        serializer = CategorySerializer(query, many=True)
        # return CategorySetializer(obj.(related_name).all).data()
        return serializer.data


class BookSerializer(serializers.ModelSerializer):
    categurise = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = ['name', 'writer', 'publisher', 'description', 'release_date', 'book', 'categurise']
