import random

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Movie, Review
from .forms import FilterMoviesForm


def index(request):
    title = f'W2W / Welcome'
    form = FilterMoviesForm()

    if request.method == 'POST':
        form = FilterMoviesForm(request.POST)
        if form.is_valid():
            genre_id = form.cleaned_data['genre']
            genre = [int(genre_id)]
            rating = form.cleaned_data['rating']
            release = form.cleaned_data['release']

            if release == 'None':
                release_date = '1990-01-01'
                movies = Movie.objects.filter(Q(release_date__gte=release_date) & Q(genre__id__in=genre) & Q(vote_average__gte=int(rating)))
            elif int(release) == 2020:
                release_date = '2020-01-01'
                movies = Movie.objects.filter(Q(release_date__gte=release_date) & Q(genre__id__in=genre) & Q(vote_average__gte=int(rating)))
            elif int(release) == 2010:
                start_date = '2020-01-01'
                end_date = '2020-12-31'
                movies = Movie.objects.filter(Q(release_date__range=(start_date, end_date)) & Q(genre__id__in=genre) & Q(vote_average__gte=int(rating)))
            elif int(release) == 2000:
                start_date = '2000-01-01'
                end_date = '2010-12-31'
                movies = Movie.objects.filter(Q(release_date__range=(start_date, end_date)) & Q(genre__id__in=genre) & Q(vote_average__gte=int(rating)))
            elif int(release) == 1990:
                start_date = '1990-01-01'
                end_date = '2000-12-31'
                movies = Movie.objects.filter(Q(release_date__range=(start_date, end_date)) & Q(genre__id__in=genre) & Q(vote_average__gte=int(rating)))
            
            if movies:
                ids = [movie.id for movie in movies]

                movie_id = random.choice(ids)
                for movie in movies:
                    if movie.id == movie_id:
                        movie_title = movie.original_title
                        return HttpResponseRedirect(reverse('movie-detail', args=(movie_id, slugify(movie_title))))
            else:
                messages.info(request, f'Couldn\'t find a movie for specified filters, so here\'s a random movie for you.')
                return HttpResponseRedirect(reverse('get-random-movie'))
    else:
        form = FilterMoviesForm()

    # GET POPULAR MOVIES
    popular_movies = Movie.objects.all()

    try:
        user = User.objects.get(id=request.user.id)
        watchlist = [movie.id for movie in user.profile.watchlist.all()]
    except:
        watchlist = []
    
    context = {
        'title': title,
        'form': form,
        'popular_movies': popular_movies,
        'watchlist': watchlist
    }
    return render(request, 'movies/index.html', context)

def get_random_movie(request):
    id_list = Movie.objects.all().values_list('id', flat=True)
    x = random.choice(id_list)

    movie = get_object_or_404(Movie, id=x)

    context = {
        'title': f'W2W / Random Movie',
        'movie': movie
    }
 
    return render(request, 'movies/random-movie.html/', context)

def movie_detail(request, id, slug):
    slug = slug.split('-')
    slug = ' '.join(slug)
    movie_title = slug

    movie_obj = Movie.objects.get(id=id)

    try:
        user = User.objects.get(id=request.user.id)
        watchlist = [movie.id for movie in user.profile.watchlist.all()]
    except:
        watchlist = []
    
    # GET RELEASE DATE RANGE
    release_date = movie_obj.release_date
    if release_date == 'None':
        start_date, end_date = '1990-01-01', '2030-12-31'       
    elif str(release_date).startswith('1'):
        start_date, end_date = '1990-01-01', '2000-12-31'
    elif str(release_date).startswith('200'):
        start_date, end_date = '2000-01-01', '2010-12-31'
    elif str(release_date).startswith('201'):
        start_date, end_date = '2010-01-01', '2020-12-31'
    elif str(release_date).startswith('202'):
        start_date, end_date = '2020-01-01', '2030-12-31'
    # GET GENRE
    genre = [genre.id for genre in movie_obj.genre.all()]
    related_movies = []
    for movie in Movie.objects.filter(Q(release_date__range=(start_date, end_date)) & Q(genre__id__in=genre)).exclude(id=id):
        if not movie in related_movies:
            related_movies.append(movie)

    try:
        similar_movies = random.sample(related_movies, 16)
    except:
        similar_movies = random.sample(related_movies, len(related_movies))
    

    reviews = Review.objects.filter(movie__id=id)

    context = {
        'title': f'W2W / {movie_title.title()} ',
        'movie_title': movie_title,
        'movie_obj': movie_obj,
        'similar_movies': similar_movies,
        'watchlist': watchlist,
        'reviews': reviews
    }

    return render(request, 'movies/movie-detail.html', context)

def reviews(request, id, slug):

    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie__id=id)
    try:
        user = User.objects.get(id=request.user.id)
        watchlist = [movie.id for movie in user.profile.watchlist.all()]
    except:
        watchlist = []

    context = {
        'title': f'W2W / Reviews',
        'reviews': reviews,
        'movie': movie,
        'watchlist': watchlist
    }

    return render(request, 'movies/reviews.html', context)

def review_detail(request, id, slug, author):

    review = Review.objects.get(id=id)
    movie = review.movie

    try:
        user = User.objects.get(id=request.user.id)
        watchlist = [movie.id for movie in user.profile.watchlist.all()]
    except:
        watchlist = []

    context = {
        'title': f'W2W / Reviews',
        'review': review,
        'movie': movie,
        'watchlist': watchlist
    }

    return render(request, 'movies/review-detail.html', context)
