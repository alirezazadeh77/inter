from django.urls import include, path
from rest_framework.routers import SimpleRouter

from library.api.views import CategoryViewSet, WriterProfileViewSet

router = SimpleRouter()

router.register('category', CategoryViewSet, basename="ca")
router.register('writerprofile', WriterProfileViewSet, basename="ca")

urlpatterns = [
    path('', include(router.urls), name="product-router"),
]