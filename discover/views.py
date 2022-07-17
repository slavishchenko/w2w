from datetime import datetime
import os

from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator

from movies.models import Movie

API_KEY = os.environ.get('TMDB_API_KEY')

CURRENT_YEAR = f'{datetime.now().year}-01-01'

def discover_popular(request):
    # GET POPULAR MOVIES
    popular_movies = Movie.objects.all()
    paginator = Paginator(popular_movies, 8) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        user = User.objects.get(id=request.user.id)
        watchlist = [movie.id  for movie in user.profile.watchlist.all()]
    except:
        watchlist = []

    context = {
        'title': f'W2W / Popular Movies',
        'popular_movies': popular_movies,
        'page_obj': page_obj,
        'watchlist': watchlist
    }
    return render(request, 'discover/discover-popular.html', context)

def discover_new(request):
    # GET NEW MOVIES
    new_movies = Movie.objects.filter(release_date__gte=CURRENT_YEAR).order_by('-release_date')

    paginator = Paginator(new_movies, 8) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        user = User.objects.get(id=request.user.id)
        watchlist = [movie.id for movie in user.profile.watchlist.all()]
    except:
        watchlist = []

    context = {
        'title': f'W2W / New Movies',
        'new_movies': new_movies,
        'page_obj': page_obj,
        'watchlist': watchlist
    }
    return render(request, 'discover/discover-new.html', context)

def community_favourites(request):
    # GET COMMUNITY FAVOURITE MOVIES
    favourites = Movie.objects.filter(favourited__gte=1).distinct()
    
    paginator = Paginator(favourites, 8) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        user = User.objects.get(id=request.user.id)
        watchlist = [movie.id for movie in user.profile.watchlist.all()]
    except:
        watchlist = []

    context = {
        'title': f'W2W / Community Favourites',
        'favourites': favourites,
        'page_obj': page_obj,
        'watchlist': watchlist
    }
    return render(request, 'discover/community-favourites.html', context)


