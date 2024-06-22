from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    """
    Модель для хранения информации о клиенте
    """

    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(
        max_length=100, verbose_name="Электронная почта", unique=True
    )
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("name",)


class Mailing(models.Model):
    """
    Модель для хранения информации о рассылке
    """

    FIVE_MINUTES = "Каждые пять минут"
    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (FIVE_MINUTES, "Каждые пять минут"),
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = "Создана"
    STARTED = "Запущена"
    COMPLETED = "Завершена"

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]

    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(
        **NULLABLE, verbose_name="Описание", help_text="не обязательное поле"
    )
    status = models.CharField(
        max_length=150, choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус"
    )
    periodicity = models.CharField(
        max_length=150,
        choices=PERIODICITY_CHOICES,
        default=DAILY,
        verbose_name="Периодичность",
    )
    start_date = models.DateTimeField(
        verbose_name="Дата начала",
        **NULLABLE,
        help_text="(формат 11.05.2024) не обязательное поле",
    )
    end_date = models.DateTimeField(
        verbose_name="Дата окончания", **NULLABLE, help_text="не обязательное поле"
    )

    clients = models.ManyToManyField(Client, related_name='mailing', verbose_name="Клиенты для рассылки")
    owner = models.ForeignKey(User, verbose_name='Владелец',  on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.name} {self.status}, время работы: {self.start_date} - {self.end_date}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("name",)
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]


class Log(models.Model):
    """
    Модель для хранения информации о логах рассылок
    """

    time = models.DateTimeField(
        verbose_name="Дата и время попытки отправки", auto_now_add=True
    )
    status = models.BooleanField(verbose_name="Статус попытки отправки")
    server_response = models.CharField(
        max_length=150, verbose_name="Ответ сервера почтового сервиса", **NULLABLE
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")

    def __str__(self):
        return f"{self.client} {self.mailing} {self.time} {self.status} {self.server_response}"

    class Meta:
        verbose_name = "Лог рассылки"
        verbose_name_plural = "Логи рассылок"


class Message(models.Model):
    """
    Модель для хранения информации о сообщении для рассылки
    """

    title = models.CharField(max_length=255, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
