from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class User(AbstractUser):
    """Пользователь"""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    ROLE_CHOICES = (
        (USER, "Аутентифицированный пользователь"),
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
    )

    username = models.CharField(
        verbose_name="Имя пользователя",
        unique=True,
        max_length=150,
    )
    first_name = models.CharField(verbose_name="Имя", max_length=150, blank=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=150, blank=True)
    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True,
        max_length=254,
    )
    role = models.CharField(
        verbose_name="Пользовательская роль",
        choices=ROLE_CHOICES,
        max_length=50,
        default=USER,
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Category(models.Model):
    """Категория (тип) произведения"""

    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Идентификатор категории",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр для произведения"""

    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Идентификатор жанра",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение"""

    name = models.CharField(verbose_name="Название произведение", max_length=500)
    year = models.IntegerField(verbose_name="Дата выхода", validators=(validate_year,))
    description = models.TextField(verbose_name="Описание", null=True, blank=True, max_length=256)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        related_name="titles",
        null=True,
    )
    genre = models.ManyToManyField(
        Genre, verbose_name="Жанр", related_name="titles", blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв на произведение"""

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(verbose_name="Отзыв")
    score = models.PositiveSmallIntegerField(
        verbose_name="review score",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(fields=["title", "author"], name="unique_review"),
        ]


class Comment(models.Model):
    """Комментарий к отзыву произведения"""

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField(verbose_name="Текст комментария", blank=False)
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = [
            "-pub_date",
        ]
