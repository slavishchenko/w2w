from django.urls import path
from . import views

urlpatterns = [
    path('popular/', views.discover_popular, name='discover-popular'),
    path('new/', views.discover_new, name='discover-new'),
    path('community-favourites/', views.community_favourites, name='community-favourites'),
]