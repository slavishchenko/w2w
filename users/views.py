from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from movies.models import Movie, Review
from users.models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ShareYourThoughts


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request, f'Account created! You can log in now.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'W2W / Register'
    }

    return render(request, 'users/register.html', context)

@login_required
def profile(request, slug):
    try:
        user = User.objects.get(username=slug)
    except:
        raise Http404

    reviews = Review.objects.filter(author__id=user.id).order_by('date_posted').reverse()

    try:
        user = User.objects.get(id=user.id)
        watchlist = [movie for movie in user.profile.watchlist.all()]
    except:
        watchlist = []
    
    favourites = list(user.profile.favourites.all())

    editable = False
    if request.user.is_authenticated and request.user == user:
        editable = True

    context = {
        'title': f' W2W / Profile',
        'user': user,
        'editable': editable,
        'watchlist': watchlist,
        'reviews': reviews,
        'favourites': favourites
    }
    return render(request, 'users/profile.html', context)


@login_required
def settings(request, slug):
    username = request.user.username
    user_id = request.user.id
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            if 'cancel' in request.POST:
                return redirect('profile', username)
            elif 'delete' in request.POST:
                user = get_object_or_404(User, id=user_id)
                if user is not None:
                    user.delete()
                    messages.success(request, f'Account deleted. Sorry to see you go!')
                    return redirect('index')
            else:
                u_form.save()
                p_form.save() 
                messages.success(request, f'Saved!')
                return redirect('settings', slug)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': f'W2W / Settings',
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/settings.html', context)

@login_required
def add_to_watchlist(request):
    if request.method == 'POST':
        user_id = request.user.id
        movie_id = request.POST['movie_id']
        movie = Movie.objects.get(id=movie_id)
        profile = get_object_or_404(Profile, user=user_id)
        profile.watchlist.add(movie)
        messages.success(request, f'{movie} added to the watchlist!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('index')

@login_required
def rm_from_watchlist(request):
    if request.method == 'POST':
        user_id = request.user.id
        movie_id = request.POST['movie_id']
        movie = Movie.objects.get(id=movie_id)
        profile = get_object_or_404(Profile, user=user_id)
        profile.watchlist.remove(movie)
        messages.warning(request, f'{movie} removed from the watchlist!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('index')

@login_required
def favourite(request):
    if request.method == 'POST':
        user_id = request.user.id
        movie_id = request.POST['movie_id']
        user = get_object_or_404(User, id=user_id)
        movie = Movie.objects.get(id=movie_id)
        profile = get_object_or_404(Profile, user=user_id)
        profile.favourites.add(movie)
        movie.favourited.add(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('index')

@login_required
def rm_favourite(request):
    if request.method == 'POST':
        user_id = request.user.id
        movie_id = request.POST['movie_id']
        user = get_object_or_404(User, id=user_id)
        movie = Movie.objects.get(id=movie_id)
        profile = get_object_or_404(Profile, user=user_id)
        profile.favourites.remove(movie)
        movie.favourited.remove(user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('index')


@login_required
def share_your_thoughts(request, id, slug):
    movie_id = id
    try:
        slug = slug.split('-')
        slug = ' '.join(slug)
        movie_title = slug
    except:
        movie_title = slug

    form = ShareYourThoughts()

    if request.method == 'POST':
        form = ShareYourThoughts(request.POST)
        user = request.user
        if form.is_valid():                
            review = form.save(commit=False)
            review.movie_id = movie_id
            review.author = user
            review.save()

            messages.success(request, f'Your review has been posted!')
            return redirect('movie-detail', movie_id, movie_title )
    context = {
        'title': f'W2W / Share your thoughts',
        'form': form,
        'movie_title': movie_title,
        'id': id
    }
    return render(request, 'users/share-your-thoughts.html', context)



        