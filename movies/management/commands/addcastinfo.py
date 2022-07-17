import csv

from django.core.management.base import BaseCommand

from movies.models import Movie

class Command(BaseCommand):
    help = 'Add cast info'

    def handle(self, *args, **option):
        movies = Movie.objects.all()
        for i, movie in enumerate(movies):
            with open('data/cast.csv', 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)
                for line in csv_reader:
                    if int(line[0]) == movie.tmdb_movie_id:
                        movie.actors = line[1]
                        movie.save()
                self.stdout.write(self.style.SUCCESS('Cast info saved!'))
            if i == 1000:
                break

        self.stdout.write(self.style.SUCCESS(f'All done! Saved cast info for {i} movies.'))