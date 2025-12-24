from django.urls import path
from . import views

app_name = 'points_app'

urlpatterns = [
    path('points/', views.PointCreateView.as_view(), name='point-create'),
    path('points/messages/', views.MessageCreateView.as_view(), name='message-create'),
    path('points/search/', views.PointSearchView.as_view(), name='point-search'),
    path('messages/search/', views.MessageSearchView.as_view(), name='message-search'),
]