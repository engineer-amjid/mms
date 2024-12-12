from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from users.managers import UserProfileManager
from django.utils.translation import gettext_lazy as _

class UserRank(models.Model):
    name = models.CharField(_('Rank Name'), max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), max_length=255, unique=True)
    username = models.CharField(_('User Name'), max_length=255, unique=True)
    phone = models.CharField(_('Phone Number'), max_length=255, blank=True, null=True)
    full_name = models.CharField(_('Full Name'), max_length=255, blank=True, null=True)
    rank = models.ForeignKey(UserRank, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email