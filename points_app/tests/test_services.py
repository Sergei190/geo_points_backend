# points_app/tests/test_services.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point as GeosPoint
from ..models import GeoPoint as PointModel, GeoComment as CommentModel
from .. import services


class ServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_geopoint_service(self):
        point = services.create_geopoint_service(
            title='Service Point',
            description='Created via service',
            latitude=55.7558,
            longitude=37.6173,
            owner=self.user
        )
        self.assertEqual(point.title, 'Service Point')
        self.assertEqual(point.owner, self.user)
        self.assertIsInstance(point.coordinates, GeosPoint)

    def test_create_geocomment_service(self):
        point = PointModel.objects.create(
            title='Test Point',
            description='A test point',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )
        comment = services.create_geocomment_service(
            point_id=point.id,
            content='Service comment',
            author=self.user
        )
        self.assertEqual(comment.content, 'Service comment')
        self.assertEqual(comment.point, point)
        self.assertEqual(comment.author, self.user)

    def test_create_geocomment_service_permission_error(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_point = PointModel.objects.create(
            title='Other Point',
            description='Another point',
            coordinates='POINT(38.0 56.0)',
            owner=other_user
        )
        with self.assertRaises(PermissionError):
            services.create_geocomment_service(
                point_id=other_point.id,
                content='Invalid comment',
                author=self.user
            )

    def test_find_geopoints_in_radius_service(self):
        p1 = PointModel.objects.create(
            title='Point 1',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )
        p2 = PointModel.objects.create(
            title='Point 2',
            coordinates='POINT(37.65 55.76)',
            owner=self.user
        )
        PointModel.objects.create(
            title='Point Far',
            coordinates='POINT(0 0)',
            owner=self.user
        )

        points_in_radius = services.find_geopoints_in_radius_service(55.7558, 37.6173, 5.0)
        self.assertIn(p1, points_in_radius)
        self.assertIn(p2, points_in_radius)
        self.assertEqual(len(points_in_radius), 2)

    def test_find_geocomments_in_radius_service(self):
        point_in_radius = PointModel.objects.create(
            title='Point In Radius',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )
        point_far = PointModel.objects.create(
            title='Point Far',
            coordinates='POINT(0 0)',
            owner=self.user
        )
        msg_in = CommentModel.objects.create(point=point_in_radius, content='In radius', author=self.user)
        msg_far = CommentModel.objects.create(point=point_far, content='Far away', author=self.user)

        comments_in_radius = services.find_geocomments_in_radius_service(55.7558, 37.6173, 1.0)
        self.assertIn(msg_in, comments_in_radius)
        self.assertNotIn(msg_far, comments_in_radius)
        self.assertEqual(len(comments_in_radius), 1)