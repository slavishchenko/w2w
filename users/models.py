from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    about = models.CharField(max_length=240, blank=True, null=True)
    watchlist = models.ManyToManyField(Movie, blank=True)
    favourites = models.ManyToManyField(Movie, blank=True, related_name='user_favourites')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 340 and img.width > 340:
            output_size = (340, 340) 
            img.thumbnail(output_size)
            img.save(self.image.path)
