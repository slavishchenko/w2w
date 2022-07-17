from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Genre(models.Model):
    tmdb_genre_id = models.PositiveBigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Movie(models.Model):
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre)
    tmdb_movie_id = models.PositiveBigIntegerField()
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255)
    release_date = models.DateField()
    title = models.CharField(max_length=255)
    video = models.BooleanField()
    vote_average = models.FloatField()
    vote_count = models.PositiveBigIntegerField()
    actors = models.CharField(max_length=500, blank=True, null=True)
    trailer = models.CharField(max_length=100, blank=True, null=True)
    favourited = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ('-popularity',)

    def actors_format(self):
        self.actors = self.actors.replace('[', '')
        self.actors = self.actors.replace(']', '')
        self.actors = self.actors.replace("'", '')
        self.actors = self.actors.split(',')
        self.actors = ', '.join(self.actors)
        return self.actors

    def __str__(self):
        return self.original_title

class Review(models.Model):
    RATINGS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]

    title = models.CharField(max_length=255)
    body = models.TextField()
    tldr = models.CharField(max_length=120, blank=True)
    rating = models.CharField(max_length=2, choices=RATINGS)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} by {self.author.username}'
