from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.gis.measure import D
from . import serializers
from . import services
from . import permissions
from .models import Message, Point as PointModel

class PointCreateView(generics.CreateAPIView):
    """
    Создание точки на карте.
    POST /api/points/
    """
    serializer_class = serializers.PointSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description')
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Широта и долгота должны быть числами.'})

        services.create_point_service(
            name=name,
            description=description,
            latitude=latitude,
            longitude=longitude,
            owner=user
        )


class MessageCreateView(generics.CreateAPIView):
    """
    Создание сообщения к заданной точке.
    POST /api/points/messages/
    """
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        point_id = self.request.data.get('point')
        text = serializer.validated_data.get('text')

        try:
            point_id = int(point_id)
        except (TypeError, ValueError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'ID точки должен быть числом.'})

        services.create_message_service(
            point_id=point_id,
            text=text,
            author=user
        )


class PointSearchView(generics.ListAPIView):
    """
    Поиск точек в заданном радиусе.
    GET /api/points/search/
    Параметры: latitude, longitude, radius (км).
    """
    serializer_class = serializers.PointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')

        if latitude is None or longitude is None or radius is None:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Параметры latitude, longitude и radius обязательны.'})

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
        except (TypeError, ValueError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Параметры latitude, longitude и radius должны быть числами.'})

        return services.find_points_in_radius_service(latitude, longitude, radius)


class MessageSearchView(generics.ListAPIView):
    """
    Поиск сообщений в заданном радиусе.
    GET /api/messages/search/
    Параметры: latitude, longitude, radius (км).
    """
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')

        if latitude is None or longitude is None or radius is None:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Параметры latitude, longitude и radius обязательны.'})

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
        except (TypeError, ValueError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Параметры latitude, longitude и radius должны быть числами.'})

        return services.find_messages_in_radius_service(latitude, longitude, radius)