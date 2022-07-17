from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('random-movie/', views.get_random_movie, name='get-random-movie'),
    path('movie/<int:id>/<str:slug>/', views.movie_detail, name='movie-detail'),
    path('reviews/<int:id>/<slug:slug>/', views.reviews, name='reviews'),
    path('reviews/<int:id>/<str:author>/<slug:slug>/', views.review_detail, name='review-detail'),
]
