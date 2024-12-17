from django.urls import path
from users.views.user_view import RegisterUserView, AdminCreateUserView, AllMembersView, ProfileDetailView, \
    ProfileUpdateView, UserLoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'users'

urlpatterns = [
    # Dynamic user detail endpoint
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', UserLoginView.as_view(), name='login_user'),
    path('create-user/', AdminCreateUserView.as_view(), name='create_user'),
    path('members/', AllMembersView.as_view(), name='all_members'),
    path('profile-detail/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]