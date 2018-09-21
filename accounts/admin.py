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

    list_display = ('email', 'name', 'display_groups', 'is_active', 'is_staff', 'is_superuser', 'created_at')
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

    # ManyToMany 필드인 groups는 기본적으로 list_display 에 설정할 수 없다.
    # 따라서 , 를 구분자로 하는 string 을 groups 필드로부터 생성하고, 이를 list_display 에 설정한다.
    def display_groups(self, obj):
        return ','.join([g.name for g in obj.groups.all()]) if obj.groups.count() else ''