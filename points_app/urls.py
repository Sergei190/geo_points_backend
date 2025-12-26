from django.urls import path
from . import views

app_name = 'points_app'

urlpatterns = [
    path('geopoints/', views.GeoPointCreateView.as_view(), name='geopoint-create'),
    path('comments/', views.GeoCommentCreateView.as_view(), name='comment-create'),
    path('geopoints/search/', views.GeoPointSearchView.as_view(), name='geopoint-search'),
    path('comments/search/', views.GeoCommentSearchView.as_view(), name='comment-search'),
]