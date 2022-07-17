import csv
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre

genre_list = Genre.objects.all()

def add_genre(s):
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace(',', '')
    s = s.strip()
    tmdb_ids = s.split(' ')

    genres = []
    for genre in genre_list:
        for genre_id in tmdb_ids:
            if int(genre_id) == genre.tmdb_genre_id:
                genres.append(genre)
    
    return genres

class Command(BaseCommand):
    help = 'Populate db'

    def handle(self, *args, **option):
        movies = 'data/movies.csv'

        with open(movies, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)

            for i, line in enumerate(csv_reader):
                if not line or line[0] == 'adult':
                    pass
                else:
                    m = Movie(
                            adult = line[0],
                            backdrop_path = line[1],
                            tmdb_movie_id = line[3],
                            original_language = line[4],
                            original_title = line[5],
                            overview = line[6],
                            popularity = line[7],
                            poster_path = line[8],
                            release_date = line[9],
                            title = line[10],
                            video = line[11],
                            vote_average = line[12],
                            vote_count = line[13]
                    )
                    m.save()
                    m.genre.add(*add_genre(line[2]))
                    self.stdout.write(self.style.SUCCESS(f'{i} movie(s) added'))
                    
                if i == 1000:
                    break

        self.stdout.write(self.style.SUCCESS('All done!'))
