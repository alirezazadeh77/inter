from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from library.api.serializers import CategorySerializer, WriterProfileSerializer
from library.models import Category, WriterProfile


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_enable=True).all()

    def list(self, request, *args, **kwargs):
        query = self.queryset.filter(parent__isnull=True)
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)

class WriterProfileViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = WriterProfileSerializer

    @action(methods=['get'], detail=False)
    def profile(self, request, *args, **kwargs):
        user = request.user
        try:
            writer = WriterProfile.objects.filter(user=user)
        except WriterProfile.DoesNotExist:
            raise ParseError({"error": "first you need creat profile"})
        serializer = WriterProfileSerializer(writer,many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path="manage-profile")
    def create_of_update_profile(self, request, *args, **kwargs):
        user = request.user
        serializer = WriterProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)