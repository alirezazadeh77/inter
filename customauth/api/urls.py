from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from customauth.api.views import TokenLifetimeView, RefreshLifetimeView

urlpatterns = [
    path('obtain/', TokenLifetimeView.as_view(), name='obtain-token'),
    path('refresh/', RefreshLifetimeView.as_view(), name='obtain-refresh'),

]