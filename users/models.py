from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель Пользователя
    """

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    avatar = models.ImageField(
        upload_to="users/", verbose_name="Аватар", blank=True, null=True
    )
    token = models.CharField(max_length=50, verbose_name="Токен", blank=True, null=True)
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_edit_is_active", "can_edit_is_active"),
        ]
        ordering = ("id",)

    def __srt__(self):
        return self.email

    def delete(self, *args, **kwargs):
        """
        Удаляет изображение аватара при удалении пользователя
        """
        self.avatar.delete()
        super(User, self).delete(*args, **kwargs)