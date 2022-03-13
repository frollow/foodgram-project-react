from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Переопределённый класс юзера.
    """

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLES = (
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    )
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Пользователь",
        help_text="Пользователь",
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Имя",
        help_text="Имя пользователя",
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Фамилия",
        help_text="Фамилия пользователя",
    )
    is_subscribed = models.BooleanField(
        default=False,
        blank=True,
        null=True
    )
    password = models.CharField(max_length=100, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default="user",
        verbose_name="Роль",
        help_text="Роль пользователя",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_staff

    @property
    def is_moderator(self):
        return self.role == "moderator"

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
