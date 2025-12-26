from django.test import TestCase
from django.contrib.auth.models import User
from ..models import GeoPoint, GeoComment
from ..serializers import GeoPointSerializer, GeoCommentSerializer


class GeoPointSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_geo_point_serializer_create(self):
        data = {
            'title': 'New Point',
            'description': 'A new point',
            'latitude': 55.7558,
            'longitude': 37.6173
        }
        serializer = GeoPointSerializer(data=data, context={'request': type('obj', (object,), {'user': self.user})()})
        self.assertTrue(serializer.is_valid())
        point = serializer.save()
        self.assertEqual(point.title, 'New Point')
        self.assertEqual(point.owner, self.user)


class GeoCommentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.point = GeoPoint.objects.create(
            title='Test Point',
            description='A test point',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )

    def test_geo_comment_serializer_create(self):
        data = {
            'point_id': self.point.id,
            'content': 'New comment text'
        }
        serializer = GeoCommentSerializer(data=data, context={'request': type('obj', (object,), {'user': self.user})()})
        self.assertTrue(serializer.is_valid())
        comment = serializer.save()
        self.assertEqual(comment.content, 'New comment text')
        self.assertEqual(comment.point, self.point)
        self.assertEqual(comment.author, self.user)

    def test_geo_comment_serializer_validate_point_id(self):
        data = {
            'point_id': 99999,
            'content': 'Invalid point id'
        }
        serializer = GeoCommentSerializer(data=data, context={'request': type('obj', (object,), {'user': self.user})()})
        self.assertFalse(serializer.is_valid())
        self.assertIn('point_id', serializer.errors)