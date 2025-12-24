from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.db import models
from django.utils import timezone


class Point(models.Model):
    """
    Модель для хранения географических точек.
    """
    name = models.CharField(max_length=255, help_text="Название точки")
    description = models.TextField(blank=True, null=True, help_text="Описание точки")
    location = gis_models.PointField(geography=True, help_text="Географическая координата (широта, долгота)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points', help_text="Пользователь, создавший точку")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

    class Meta:
        verbose_name = "Гео-точка"
        verbose_name_plural = "Гео-точки"
        ordering = ['-created_at']


class Message(models.Model):
    """
    Модель для хранения сообщений, привязанных к гео-точке.
    """
    point = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='messages', help_text="Точка, к которой привязано сообщение")
    text = models.TextField(help_text="Текст сообщения")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', help_text="Пользователь, написавший сообщение")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Сообщение от {self.author.username} к точке '{self.point.name}'"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['created_at']