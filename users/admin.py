from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile
from .models.user_rank_model import UserRank


@admin.register(UserRank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ['email', 'username', 'full_name', 'rank', 'is_staff', 'is_active']
    search_fields = ['email', 'username', 'full_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'rank')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

