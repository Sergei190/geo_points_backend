from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import GeoPoint, GeoComment


class GeoPointModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.point = GeoPoint.objects.create(
            title='Test Point',
            description='A test point',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )

    def test_point_creation(self):
        self.assertEqual(self.point.title, 'Test Point')
        self.assertEqual(self.point.description, 'A test point')
        self.assertEqual(self.point.owner, self.user)
        self.assertIsNotNone(self.point.created_at)

    def test_point_str(self):
        expected_str = f"{self.point.title} ({self.point.owner.username})"
        self.assertEqual(str(self.point), expected_str)


class GeoCommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.point = GeoPoint.objects.create(
            title='Test Point',
            description='A test point',
            coordinates='POINT(37.6173 55.7558)',
            owner=self.user
        )
        self.comment = GeoComment.objects.create(
            point=self.point,
            content='Test comment',
            author=self.user
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Test comment')
        self.assertEqual(self.comment.point, self.point)
        self.assertEqual(self.comment.author, self.user)
        self.assertIsNotNone(self.comment.created_at)

    def test_comment_str(self):
        expected_str = f"Комментарий от {self.comment.author.username} к '{self.comment.point.title}'"
        self.assertEqual(str(self.comment), expected_str)