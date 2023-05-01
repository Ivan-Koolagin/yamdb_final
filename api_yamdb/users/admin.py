from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'role', 'first_name', 'last_name')
    search_fields = ('name',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'
