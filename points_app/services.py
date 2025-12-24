from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from .models import Point as PointModel, Message


def create_point_service(name: str, description: str, latitude: float, longitude: float, owner: User) -> PointModel:
    """
    Создает новую гео-точку.

    :param name: Название точки.
    :param description: Описание точки.
    :param latitude: Широта.
    :param longitude: Долгота.
    :param owner: Владелец точки (пользователь).
    :return: Созданный объект PointModel.
    """
    location = Point(x=longitude, y=latitude, srid=4326)
    point = PointModel.objects.create(
        name=name,
        description=description,
        location=location,
        owner=owner
    )
    return point


def create_message_service(point_id: int, text: str, author: User) -> Message:
    """
    Создает новое сообщение, привязанное к точке.

    :param point_id: ID точки, к которой привязывается сообщение.
    :param text: Текст сообщения.
    :param author: Автор сообщения (пользователь).
    :return: Созданный объект Message.
    :raises: PointModel.DoesNotExist если точка не найдена.
    :raises: PermissionError если автор не является владельцем точки.
    """
    point = PointModel.objects.get(id=point_id)
    if point.owner != author:
        raise PermissionError("Только владелец точки может добавлять к ней сообщения.")

    message = Message.objects.create(
        point=point,
        text=text,
        author=author
    )
    return message


def find_points_in_radius_service(latitude: float, longitude: float, radius_km: float) -> list[PointModel]:
    """
    Находит точки в заданном радиусе от координат.

    :param latitude: Широта центра поиска.
    :param longitude: Долгота центра поиска.
    :param radius_km: Радиус поиска в километрах.
    :return: Список точек в радиусе.
    """
    search_point = Point(x=longitude, y=latitude, srid=4326)
    points = PointModel.objects.filter(
        location__distance_lte=(search_point, D(km=radius_km))
    )
    return list(points)


def find_messages_in_radius_service(latitude: float, longitude: float, radius_km: float) -> list[Message]:
    """
    Находит сообщения, привязанные к точкам в заданном радиусе.

    :param latitude: Широта центра поиска.
    :param longitude: Долгота центра поиска.
    :param radius_km: Радиус поиска в километрах.
    :return: Список сообщений в радиусе.
    """
    search_point = Point(x=longitude, y=latitude, srid=4326)
    points_in_radius = PointModel.objects.filter(
        location__distance_lte=(search_point, D(km=radius_km))
    )
    messages = Message.objects.filter(point__in=points_in_radius)
    return list(messages)