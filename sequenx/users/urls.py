from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,  # Add this import
)

app_name = 'api'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('profile/', views.UserProfileRetrieveUpdateAPIView.as_view(), name="profile"),
    # path('password-update/', views.UpdatePasswordView.as_view(), name='password-update'),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Add this path
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]