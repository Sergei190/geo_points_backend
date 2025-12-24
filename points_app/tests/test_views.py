from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Point as PointModel, Message


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_point_create_view(self):
        url = reverse('points_app:point-create')
        data = {
            'name': 'API Point',
            'description': 'Created via API',
            'latitude': 55.7558,
            'longitude': 37.6173
        }
        response = self.client.post(url, data, content_type='application/json')
        # Предполагаем, что валидация JSON и аутентификация прошли, но нужно обернуть в json.dumps если передаем как json
        import json
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201) # 201 Created
        self.assertEqual(PointModel.objects.count(), 1)
        point = PointModel.objects.get()
        self.assertEqual(point.name, 'API Point')

    def test_message_create_view(self):
        point = PointModel.objects.create(
            name='Test Point',
            location='POINT(37.6173 55.7558)',
            owner=self.user
        )
        url = reverse('points_app:message-create')
        data = {
            'point': point.id,
            'text': 'API message'
        }
        import json
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201) # 201 Created
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.get()
        self.assertEqual(message.text, 'API message')

    def test_point_search_view(self):
        PointModel.objects.create(
            name='Point 1',
            location='POINT(37.6173 55.7558)', # Москва
            owner=self.user
        )
        url = reverse('points_app:point-search')
        response = self.client.get(url, {'latitude': 55.7558, 'longitude': 37.6173, 'radius': 5.0})
        self.assertEqual(response.status_code, 200)
        # Проверить, что в ответе есть Point 1
        self.assertContains(response, 'Point 1')

    def test_message_search_view(self):
        point = PointModel.objects.create(
            name='Point Near',
            location='POINT(37.6173 55.7558)',
            owner=self.user
        )
        Message.objects.create(point=point, text='Near message', author=self.user)
        url = reverse('points_app:message-search')
        response = self.client.get(url, {'latitude': 55.7558, 'longitude': 37.6173, 'radius': 1.0})
        self.assertEqual(response.status_code, 200)
        # Проверить, что в ответе есть 'Near message'
        self.assertContains(response, 'Near message')