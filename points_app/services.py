from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from .models import GeoPoint as PointModel, GeoComment as CommentModel
from django.db import connection
from django.db.models import Q

def create_geopoint_service(title: str, description: str, latitude: float, longitude: float, owner: User) -> PointModel:
    """
    Создает новую гео-точку.
    """
    location = Point(x=longitude, y=latitude, srid=4326)
    point = PointModel.objects.create(
        title=title,
        description=description,
        coordinates=location,
        owner=owner
    )
    return point


def create_geocomment_service(point_id: int, content: str, author: User) -> CommentModel:
    """
    Создает новый комментарий, привязанный к точке.
    """
    point = PointModel.objects.get(id=point_id)
    if point.owner != author:
        raise PermissionError("Только владелец точки может добавлять к ней комментарии.")

    comment = CommentModel.objects.create(
        point=point,
        content=content,
        author=author
    )
    return comment


def find_geopoints_in_radius_service(latitude: float, longitude: float, radius_km: float) -> list[PointModel]:
    """
    Находит точки в заданном радиусе от координат.
    """
    search_point = Point(x=longitude, y=latitude, srid=4326)
    points = PointModel.objects.filter(
        coordinates__distance_lte=(search_point, D(km=radius_km))
    )
    return list(points)


def find_geocomments_in_radius_service(latitude: float, longitude: float, radius_km: float) -> list[CommentModel]:
    """
    Находит комментарии, привязанные к точкам в заданном радиусе.
    """
    search_point = Point(x=longitude, y=latitude, srid=4326)
    points_in_radius = PointModel.objects.filter(
        coordinates__distance_lte=(search_point, D(km=radius_km))
    )
    comments = CommentModel.objects.filter(point__in=points_in_radius)
    return list(comments)