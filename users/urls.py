# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import  CustomLoginView,UserView

urlpatterns = [
    # Use the custom serializer for obtaining the token
    path('', UserView.as_view(), name='users'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    # Token refresh endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
