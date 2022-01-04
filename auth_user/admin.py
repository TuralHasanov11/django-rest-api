from django.contrib import admin
from .models import AuthUser

# Modifiying Admin page for Users
from django.contrib.auth.admin import UserAdmin


class AuthUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'created_at', 'updated_at', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(AuthUser, AuthUserAdmin)
