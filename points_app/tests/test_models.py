from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Point, Message


class PointModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.point = Point.objects.create(
            name='Test Point',
            description='A test point',
            location='POINT(37.6173 55.7558)',
            owner=self.user
        )

    def test_point_creation(self):
        self.assertEqual(self.point.name, 'Test Point')
        self.assertEqual(self.point.description, 'A test point')
        self.assertEqual(self.point.owner, self.user)
        self.assertIsNotNone(self.point.created_at)

    def test_point_str(self):
        expected_str = f"{self.point.name} ({self.point.owner.username})"
        self.assertEqual(str(self.point), expected_str)


class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.point = Point.objects.create(
            name='Test Point',
            description='A test point',
            location='POINT(37.6173 55.7558)',
            owner=self.user
        )
        self.message = Message.objects.create(
            point=self.point,
            text='Test message',
            author=self.user
        )

    def test_message_creation(self):
        self.assertEqual(self.message.text, 'Test message')
        self.assertEqual(self.message.point, self.point)
        self.assertEqual(self.message.author, self.user)
        self.assertIsNotNone(self.message.created_at)

    def test_message_str(self):
        expected_str = f"Сообщение от {self.message.author.username} к точке '{self.message.point.name}'"
        self.assertEqual(str(self.message), expected_str)