from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title

admin.site.register(Genre)
admin.site.register(Category)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "category")
    search_fields = ("name",)
    list_filter = ("category",)
    empty_value_display = "-пусто-"


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "genre")
    list_filter = ("genre",)
    search_fields = ("title__name",)
    empty_value_display = "-пусто-"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", "author", "score", "pub_date")
    list_filter = ("author",)
    search_fields = ("title__name",)
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "text", "author", "pub_date")
    list_filter = (
        "review",
        "author",
    )
    search_fields = ("text",)
    empty_value_display = "-пусто-"
