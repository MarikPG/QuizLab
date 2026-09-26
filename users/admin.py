
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Особиста інформація', {'fields': ('email', 'bio', 'avatar')}),
        ('Права доступу та ролі', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Важливі дати', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'role', 'is_staff')

    list_editable = ('role',)

    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    search_fields = ('username', 'email', 'bio')