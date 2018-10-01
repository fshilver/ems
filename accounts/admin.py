from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'name', 'group_names', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
            }
        ),
        ('Personal Info', {
            'fields': ('name',)
            }
        ),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'groups')
            }
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }
        ),
        ('Personal Info', {
            'fields': ('name',)
            }
        ),
        ('Permissions',
            {
                'fields': ('is_active', 'is_staff', 'groups')
            }
        ),
    )

    ordering = ('email',)