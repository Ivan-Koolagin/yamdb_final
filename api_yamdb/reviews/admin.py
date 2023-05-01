from django.contrib import admin

from .models import Category, Genre, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "bio",
    )
    list_editable = ("role",)
    search_fields = ("bio",)
    empty_value_display = "-пусто-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_editable = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_editable = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "description")
    search_fields = ("name", "year")
