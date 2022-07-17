from django import forms
from .models import Genre


genres = Genre.objects.all()

GENRE_CHOICES = []
for genre in genres:
    GENRE_CHOICES.append((genre.id, genre.name))

# RELEASED
RELEASED_CHOICES = [
    ('None', 'All time'),
    (2020, '2020s'),
    (2010, '2010s'),
    (2000, '2000s'),
    (1990, '1990s'),
]

# RATING
RATING_CHOICES = [
    (6, '6 and above'),
    (7, '7 and above'),
    (8, '8 and above'),
    (9, '9 and above'),
]


class FilterMoviesForm(forms.Form):
    genre = forms.ChoiceField(
        label='Pick a genre: ',
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=GENRE_CHOICES,
    )
    release = forms.ChoiceField(
        label='Released in: ',
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=RELEASED_CHOICES
    )
    rating = forms.ChoiceField(
        label = 'Rating: ',
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices = RATING_CHOICES
    )