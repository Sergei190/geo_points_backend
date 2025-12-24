from django.contrib.gis.geos import Point


def create_gis_point(latitude: float, longitude: float) -> Point:
    """
    Вспомогательная функция для создания объекта Point из GeoDjango.

    :param latitude: Широта.
    :param longitude: Долгота.
    :return: Готовый объект Point с SRID 4326.
    """
    return Point(x=longitude, y=latitude, srid=4326)