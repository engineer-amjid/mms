from django.urls import path
from users.views.user_view import RegisterUserView, UserView, AllUsersView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'users'

urlpatterns = [
    path('', AllUsersView.as_view(), name='all_users'),
    path('<int:pk>/', UserView.as_view(), name='user_detail'),  # Dynamic user detail endpoint
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]