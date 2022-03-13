from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    firs_name = models.CharField(max_length=154)
    last_name = models.CharField(max_length=154)
    username = models.CharField(unique=True, max_length=154)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name="follower",
        verbose_name="подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="автор",
    )

    class Meta:
        verbose_name = verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="subscription"
            ),
        ]

    def __str__(self):
        return f"{self.user} -> {self.author}"
