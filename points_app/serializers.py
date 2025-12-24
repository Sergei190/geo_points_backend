from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import Point as PointModel, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователей (для отображения владельца/автора).
    """
    class Meta:
        model = User
        fields = ('id', 'username')


class PointSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и отображения гео-точек.
    """
    owner = UserSerializer(read_only=True)

    class Meta:
        model = PointModel
        fields = ('id', 'name', 'description', 'location', 'owner', 'created_at')
        read_only_fields = ('owner', 'created_at')

    def create(self, validated_data):
        """
        Переопределяем create, чтобы автоматически назначить владельца.
        """
        user = self.context['request'].user
        point = PointModel.objects.create(owner=user, **validated_data)
        return point


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и отображения сообщений.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'point', 'text', 'author', 'created_at')
        read_only_fields = ('author', 'created_at')

    def validate_point(self, value):
        """
        Проверяем, что пользователь является владельцем точки, к которой пытается добавить сообщение.
        """
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("Вы можете добавлять сообщения только к своим точкам.")
        return value

    def create(self, validated_data):
        """
        Переопределяем create, чтобы автоматически назначить автора.
        """
        user = self.context['request'].user
        message = Message.objects.create(author=user, **validated_data)
        return message


class PointSearchSerializer(serializers.Serializer):
    """
    Сериализатор для валидации параметров поиска точек в радиусе.
    """
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    radius = serializers.FloatField(min_value=0.001)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass