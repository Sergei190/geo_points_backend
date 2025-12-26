# points_app/tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import GeoPoint as PointModel, GeoComment as CommentModel


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_geopoint_create_view(self):
        url = reverse('points_app:geopoint-create')
        data = {
            'title': 'API Point',
            'description': 'Created via API',
            'latitude': 55.7558,
            'longitude': 37.6173
        }
        import json
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PointModel.objects.count(), 1)
        point = PointModel.objects.get()
        self.assertEqual(point.title, 'API Point')

    def test_geocomment_create_view(self):
        point = PointModel.objects.create(
            title='Test Point',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )
        url = reverse('points_app:comment-create')
        data = {
            'point_id': point.id,
            'content': 'API comment'
        }
        import json
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CommentModel.objects.count(), 1)
        comment = CommentModel.objects.get()
        self.assertEqual(comment.content, 'API comment')

    def test_geopoint_search_view(self):
        PointModel.objects.create(
            title='Point 1',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )
        url = reverse('points_app:geopoint-search')
        response = self.client.get(url, {'latitude': 55.7558, 'longitude': 37.6173, 'radius_km': 5.0})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Point 1')

    def test_geocomment_search_view(self):
        point = PointModel.objects.create(
            title='Point Near',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )
        CommentModel.objects.create(point=point, content='Near comment', author=self.user)
        url = reverse('points_app:comment-search')
        response = self.client.get(url, {'latitude': 55.7558, 'longitude': 37.6173, 'radius_km': 1.0})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Near comment')