from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import GeoPoint as PointModel, GeoComment as CommentModel
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователей (для отображения владельца/автора).
    """
    class Meta:
        model = User
        fields = ('id', 'username')


class GeoPointSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и отображения гео-точек.
    """
    owner = UserSerializer(read_only=True)
    latitude = serializers.FloatField(write_only=True, min_value=-90, max_value=90)
    longitude = serializers.FloatField(write_only=True, min_value=-180, max_value=180)

    class Meta:
        model = PointModel
        fields = ('id', 'title', 'description', 'coordinates', 'owner', 'created_at', 'latitude', 'longitude')
        read_only_fields = ('owner', 'created_at', 'coordinates')

    def create(self, validated_data):
        """
        Переопределяем create, чтобы автоматически назначить владельца и координаты.
        """
        user = self.context['request'].user
        lat = validated_data.pop('latitude')
        lng = validated_data.pop('longitude')
        validated_data['coordinates'] = Point(x=lng, y=lat, srid=4326)
        point = PointModel.objects.create(owner=user, **validated_data)
        return point

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(instance, 'coordinates') and instance.coordinates:
            data['latitude'] = instance.coordinates.y
            data['longitude'] = instance.coordinates.x
        return data


class GeoCommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и отображения комментариев.
    """
    author = UserSerializer(read_only=True)
    point_id = serializers.IntegerField(write_only=True, help_text="ID точки")

    class Meta:
        model = CommentModel
        fields = ('id', 'point_id', 'point', 'content', 'author', 'created_at')
        read_only_fields = ('author', 'created_at', 'point')

    def validate_point_id(self, value):
        """
        Проверяем, что точка существует.
        """
        try:
            point = PointModel.objects.get(id=value)
        except PointModel.DoesNotExist:
            raise serializers.ValidationError("Точка с таким ID не найдена.")
        return value

    def validate(self, attrs):
        """
        Проверяем, что автор является владельцем точки.
        """
        point = PointModel.objects.get(id=attrs['point_id'])
        if point.owner != self.context['request'].user:
            raise serializers.ValidationError("Вы можете добавлять комментарии только к своим точкам.")
        return attrs

    def create(self, validated_data):
        """
        Переопределяем create, чтобы автоматически назначить автора и точку.
        """
        user = self.context['request'].user
        point_id = validated_data.pop('point_id')
        point = PointModel.objects.get(id=point_id)
        comment = CommentModel.objects.create(author=user, point=point, **validated_data)
        return comment

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(instance, 'point') and instance.point:
            point_serializer = GeoPointSerializer(instance.point)
            data['point'] = point_serializer.data
        return data


class GeoPointSearchSerializer(serializers.Serializer):
    """
    Сериализатор для валидации параметров поиска точек в радиусе.
    """
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    radius_km = serializers.FloatField(min_value=0.001)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass