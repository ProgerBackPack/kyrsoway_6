from django.db import models
from django.utils import timezone

from users.models import User


class Message(models.Model):
    """
    Модель сообщения для рассылки писем
    """
    title_letter = models.CharField(max_length=100, verbose_name="Тема",)
    body_letter = models.TextField(verbose_name="Сообщение", null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель сообщения",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("id",)

    def __str__(self):
        return self.title_letter


class Client(models.Model):
    """
    Модель клиента для рассылки писем (кому отправляется письмо)
    """
    name = models.CharField(max_length=250, verbose_name="Ф.И.О",)
    email = models.EmailField(verbose_name="Email", unique=True)
    comment = models.TextField(
        max_length=100, verbose_name="Комментарий", null=True, blank=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель клиента",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.email})"


class MailingList(models.Model):
    """
    Параметры рассылки
    """
    PERIODICITY_CHOICES = [
        ("Раз в день", "Раз в день"),
        ("Раз в неделю", "Раз в неделю"),
        ("Раз в месяц", "Раз в месяц"),
    ]
    STATUS_CHOICES = [
        ("Завершена", "Завершена"),
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
    ]
    date_and_time_of_sending = models.DateTimeField(
        verbose_name="Дата и время первой отправки отправки",
        default=timezone.now,
        null=True,
        blank=True,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="messages",
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name="Клиенты",
    )
    periodicity = models.CharField(
        max_length=50,
        choices=PERIODICITY_CHOICES,
        verbose_name="Периодичность рассылки",
        default="Раз в день",
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=50,
        choices=STATUS_CHOICES,
        default="Создана",
    )
    next_date = models.DateTimeField(
        verbose_name="Дата и время следующей отправки отправки",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель рассылки",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_edit_status", "can_edit_status"),
        ]
        ordering = ("id",)

    def __str__(self):
        return f'Рассылка "{self.message}"'


class Attempt(models.Model):
    """
    Попытка отправки рассылки
    """
    STATUS_CHOICES = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]
    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts",
    )
    date_time_last_attempt = models.DateTimeField(
        verbose_name="Дата и время последнего попытки отправки",
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        verbose_name="Статус попытки",
        default="Не успешно",
    )
    mail_server_response = models.TextField(
        verbose_name="Ответ почтового сервера",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ("id",)

    def __str__(self):
        return f"Попытка отправки письма N {self.pk}"
