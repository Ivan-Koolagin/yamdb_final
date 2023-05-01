from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    ROLE_CHOICES = (
        (USER, "Аутентифицированный пользователь"),
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
    )

    username = models.CharField(
        "Имя пользователя",
        max_length=settings.LENG_DATA_USER,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username],
    )
    email = models.EmailField(
        'Эл. почта',
        max_length=settings.LENG_EMAIL,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.LENG_DATA_USER,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LENG_DATA_USER,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        choices=ROLE_CHOICES,
        max_length=settings.LENG_SLUG,
        default=USER,
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
