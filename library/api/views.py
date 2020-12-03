from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from library.api.serializers import CategorySerializer, WriterProfileSerializer
from library.models import Category, WriterProfile


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_enable=True).all()

    def list(self, request, *args, **kwargs):
        query = self.queryset.filter(parent__isnull=True)
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)

class WriterProfileViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = WriterProfileSerializer
    queryset = WriterProfile.objects.all()