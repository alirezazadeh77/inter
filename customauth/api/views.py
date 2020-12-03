from rest_framework_simplejwt.views import TokenViewBase

from customauth.api.serializers import TokenLifetimeSerializer, RefreshLifetimeSerializer


class TokenLifetimeView(TokenViewBase):
    serializer_class = TokenLifetimeSerializer


class RefreshLifetimeView(TokenViewBase):
    serializer_class = RefreshLifetimeSerializer