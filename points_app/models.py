from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.db import models
from django.utils import timezone

class GeoPoint(models.Model):
    """
    Модель для хранения географических точек.
    """
    title = models.CharField(max_length=255, help_text="Название точки")
    description = models.TextField(blank=True, null=True, help_text="Описание точки")
    coordinates = gis_models.PointField(geography=True, help_text="Географическая координата (широта, долгота)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_geopoints', help_text="Пользователь, создавший точку")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

    class Meta:
        verbose_name = "Гео-точка"
        verbose_name_plural = "Гео-точки"
        ordering = ['-created_at']


class GeoComment(models.Model):
    """
    Модель для хранения сообщений, привязанных к гео-точке.
    """
    point = models.ForeignKey(GeoPoint, on_delete=models.CASCADE, related_name='comments', help_text="Точка, к которой привязано сообщение")
    content = models.TextField(help_text="Текст сообщения")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_comments', help_text="Пользователь, написавший сообщение")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Комментарий от {self.author.username} к '{self.point.title}'"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']