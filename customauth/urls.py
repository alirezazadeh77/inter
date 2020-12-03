from django.urls import path, include

urlpatterns = [
    path('token/', include('customauth.api.urls')),

]
