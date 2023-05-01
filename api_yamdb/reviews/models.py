from django.conf import settings
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    validate_slug)
from users.models import User
from django.db import models

from .validators import validate_year


class GenreCategoryModel(models.Model):
    slug = models.SlugField(
        'Slug',
        max_length=settings.LENG_SLUG,
        unique=True,
        validators=[validate_slug],
    )
    name = models.CharField(
        'Название',
        max_length=settings.LENG_MAX,
    )

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self):
        return self.name[:settings.LENG_CUT]


class Category(GenreCategoryModel):
    class Meta(GenreCategoryModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Genre(GenreCategoryModel):
    class Meta(GenreCategoryModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.LENG_MAX
    )
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=(validate_year, )
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    def __str__(self):
        return f'{self.title} {self.genre}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            )
        ]
        ordering = ['title']
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField('Оценка', validators=[MinValueValidator(1),
                                MaxValueValidator(10)])
    pub_date = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return f'{self.author}-{self.title}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        ordering = ['author']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
