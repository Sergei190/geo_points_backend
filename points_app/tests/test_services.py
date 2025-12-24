from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point as GeosPoint
from ..models import Point as PointModel, Message
from .. import services


class ServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_point_service(self):
        point = services.create_point_service(
            name='Service Point',
            description='Created via service',
            latitude=55.7558,
            longitude=37.6173,
            owner=self.user
        )
        self.assertEqual(point.name, 'Service Point')
        self.assertEqual(point.owner, self.user)
        self.assertIsInstance(point.location, GeosPoint)

    def test_create_message_service(self):
        point = PointModel.objects.create(
            name='Test Point',
            description='A test point',
            location='POINT(37.6173 55.7558)',
            owner=self.user
        )
        message = services.create_message_service(
            point_id=point.id,
            text='Service message',
            author=self.user
        )
        self.assertEqual(message.text, 'Service message')
        self.assertEqual(message.point, point)
        self.assertEqual(message.author, self.user)

    def test_create_message_service_permission_error(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_point = PointModel.objects.create(
            name='Other Point',
            description='Another point',
            location='POINT(38.0 56.0)',
            owner=other_user
        )
        with self.assertRaises(PermissionError):
            services.create_message_service(
                point_id=other_point.id,
                text='Invalid message',
                author=self.user
            )

    def test_find_points_in_radius_service(self):
        # Создаем точки
        p1 = PointModel.objects.create(
            name='Point 1',
            location='POINT(37.6173 55.7558)',  # Москва
            owner=self.user
        )
        p2 = PointModel.objects.create(
            name='Point 2',
            location='POINT(37.65 55.76)', # Рядом с Москвой
            owner=self.user
        )
        # Точка далеко
        PointModel.objects.create(
            name='Point Far',
            location='POINT(0 0)', # Где-то в Атлантике
            owner=self.user
        )

        points_in_radius = services.find_points_in_radius_service(55.7558, 37.6173, 5.0) # 5 км
        self.assertIn(p1, points_in_radius)
        self.assertIn(p2, points_in_radius)
        self.assertEqual(len(points_in_radius), 2) # или 2, в зависимости от точности

    def test_find_messages_in_radius_service(self):
        # Создаем точку в радиусе
        point_in_radius = PointModel.objects.create(
            name='Point In Radius',
            location='POINT(37.6173 55.7558)',
            owner=self.user
        )
        # Создаем точку вне радиуса
        point_far = PointModel.objects.create(
            name='Point Far',
            location='POINT(0 0)',
            owner=self.user
        )
        # Создаем сообщения
        msg_in = Message.objects.create(point=point_in_radius, text='In radius', author=self.user)
        msg_far = Message.objects.create(point=point_far, text='Far away', author=self.user)

        messages_in_radius = services.find_messages_in_radius_service(55.7558, 37.6173, 1.0) # 1 км
        self.assertIn(msg_in, messages_in_radius)
        self.assertNotIn(msg_far, messages_in_radius)
        self.assertEqual(len(messages_in_radius), 1)