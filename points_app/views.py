from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.gis.measure import D
from . import serializers
from . import services
from . import permissions
from .models import GeoComment as CommentModel, GeoPoint as PointModel

class GeoPointCreateView(generics.CreateAPIView):
    """
    Создание гео-точки.
    POST /api/geopoints/
    """
    serializer_class = serializers.GeoPointSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Широта и долгота должны быть числами.'})

        services.create_geopoint_service(
            title=title,
            description=description,
            latitude=latitude,
            longitude=longitude,
            owner=user
        )


class GeoCommentCreateView(generics.CreateAPIView):
    """
    Создание комментария к заданной точке.
    POST /api/comments/
    """
    serializer_class = serializers.GeoCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        point_id = serializer.validated_data.get('point_id')
        content = serializer.validated_data.get('content')

        try:
            point_id = int(point_id)
        except (TypeError, ValueError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'ID точки должен быть числом.'})

        services.create_geocomment_service(
            point_id=point_id,
            content=content,
            author=user
        )


class GeoPointSearchView(generics.ListAPIView):
    """
    Поиск точек в заданном радиусе.
    GET /api/geopoints/search/
    Параметры: latitude, longitude, radius_km (км).
    """
    serializer_class = serializers.GeoPointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius_km = self.request.query_params.get('radius_km')

        if latitude is None or longitude is None or radius_km is None:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Параметры latitude, longitude и radius_km обязательны.'})

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius_km = float(radius_km)
        except (TypeError, ValueError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Параметры latitude, longitude и radius_km должны быть числами.'})

        return services.find_geopoints_in_radius_service(latitude, longitude, radius_km)


class GeoCommentSearchView(generics.ListAPIView):
    """
    Поиск комментариев в заданном радиусе.
    GET /api/comments/search/
    Параметры: latitude, longitude, radius_km (км).
    """
    serializer_class = serializers.GeoCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius_km = self.request.query_params.get('radius_km')

        if latitude is None or longitude is None or radius_km is None:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Параметры latitude, longitude и radius_km обязательны.'})

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius_km = float(radius_km)
        except (TypeError, ValueError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'error': 'Параметры latitude, longitude и radius_km должны быть числами.'})

        return services.find_geocomments_in_radius_service(latitude, longitude, radius_km)