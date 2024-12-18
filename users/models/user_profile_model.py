from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers.managers import UserProfileManager
from django.utils.translation import gettext_lazy as _

from users.models.user_rank_model import UserRank


class UserProfile(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    STAFF = 'staff'
    MEMBER = 'member'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (MEMBER, 'Member'),
    ]

    email = models.EmailField(_('Email Address'), max_length=255, unique=True)
    username = models.CharField(_('User Name'), max_length=255, unique=True)
    role = models.CharField(_('Role'), max_length=255, choices=ROLE_CHOICES, default=MEMBER)
    phone = models.CharField(_('Phone Number'), max_length=255, blank=True, null=True)
    full_name = models.CharField(_('Full Name'), max_length=255, blank=True, null=True)
    rank = models.ForeignKey(UserRank, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    is_approved = models.BooleanField(_('Is Approved'), default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email