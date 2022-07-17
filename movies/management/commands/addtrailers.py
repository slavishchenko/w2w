import csv

from django.core.management.base import BaseCommand

from movies.models import Movie

class Command(BaseCommand):
    help = 'Add trailers'

    def handle(self, *args, **option):
        movies = Movie.objects.all()
        for i, movie in enumerate(movies):
            with open('data/trailers.csv', 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)
                for line in csv_reader:
                    if int(line[0]) == movie.tmdb_movie_id:
                        movie.trailer = line[1]
                        movie.save()
                self.stdout.write(self.style.SUCCESS('Trailer saved!'))
            if i == 1000:
                break

        self.stdout.write(self.style.SUCCESS('All done!'))