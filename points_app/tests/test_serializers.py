from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Point, Message
from ..serializers import PointSerializer, MessageSerializer


class PointSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_point_serializer_create(self):
        data = {
            'name': 'New Point',
            'description': 'A new point',
            'latitude': 55.7558,
            'longitude': 37.6173
        }
        # Создаем сериализатор с контекстом запроса (имитируем)
        serializer = PointSerializer(data=data, context={'request': type('obj', (object,), {'user': self.user})()})
        self.assertTrue(serializer.is_valid())
        point = serializer.save()
        self.assertEqual(point.name, 'New Point')
        self.assertEqual(point.owner, self.user)


class MessageSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.point = Point.objects.create(
            name='Test Point',
            description='A test point',
            location='POINT(37.6173 55.7558)',
            owner=self.user
        )

    def test_message_serializer_create(self):
        data = {
            'point': self.point.id,
            'text': 'New message text'
        }
        serializer = MessageSerializer(data=data, context={'request': type('obj', (object,), {'user': self.user})()})
        self.assertTrue(serializer.is_valid())
        message = serializer.save()
        self.assertEqual(message.text, 'New message text')
        self.assertEqual(message.point, self.point)
        self.assertEqual(message.author, self.user)

    def test_message_serializer_validate_point(self):
        # Создаем точку другого пользователя
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_point = Point.objects.create(
            name='Other Point',
            description='Another point',
            location='POINT(38.0 56.0)',
            owner=other_user
        )
        data = {
            'point': other_point.id,
            'text': 'Message to other user\'s point'
        }
        serializer = MessageSerializer(data=data, context={'request': type('obj', (object,), {'user': self.user})()})
        self.assertFalse(serializer.is_valid())
        self.assertIn('point', serializer.errors)