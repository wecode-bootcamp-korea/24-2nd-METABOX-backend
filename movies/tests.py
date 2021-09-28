from datetime import datetime
import json

from django.test import TestCase, Client
from django.test.client import CONTENT_TYPE_RE


from movies.models import Actor, Director, Genre, Movie, Theater, MovieTheater

class MovieTests(TestCase):
    def setUp(self):
        
        genres = Genre.objects.bulk_create(
            [
                Genre(
                    id = 1,
                    name = '스릴러'
                ),
                Genre(
                    id = 2,
                    name = '드라마'
                )
            ]
        )

        directors = Director.objects.bulk_create(
            [
                Director(
                    id = 1,
                    name = "묵묵"
                ),
                Director(
                    id =2,
                    name = '묵묵묵'
                )
            ]
        )

        actors = Actor.objects.bulk_create(
            [
                Actor(
                    id = 1,
                    name = '무크'
                ),
                Actor(
                    id = 2,
                    name = '무크무크'
                )
            ]
        )
        
        theaters = Theater.objects.bulk_create(
            [
                Theater(
                    id = 1,
                    location = "강남"
                ),
                Theater(
                    id = 2,
                    location = "수원"
                )
            ]
        )

        movie = Movie.objects.create(
            id             = 1,
            ko_name        = "어려운 테스트",
            en_name        = "crazy test",
            release_date   = "1990-08-02",
            close_date     = "1990-08-31",
            screening_type = "2D",
            running_time   = 120,
            age_grade      = 19,
            rating         = 9.9,
            description    = "너무너무힘들군",
            total_audience = 100000,
        )

        for genre in genres:
            movie.genre.add(genre)

        for director in directors:
            movie.director.add(director)
        
        for actor in actors:
            movie.actor.add(actor)

        for theater in theaters:
            MovieTheater.objects.create(movie_id = movie.id, theater_id = theater.id, start_time = datetime.utcnow())
            

    def tearDown(self):
        Movie.objects.all().delete()
        Genre.objects.all().delete()
        Director.objects.all().delete()
        Actor.objects.all().delete()
        Theater.objects.all().delete()

    def test_movie_get_success(self):
        client = Client()
        response = client.get('/movies/1')
        self.assertEqual(response.json(),
            {
                "Result" : 
                    {
                        "ko_name"        : "어려운 테스트",
                        "en_name"        : "crazy test",
                        "release_date"   : "1990-08-02",
                        "close_date"     : "1990-08-31",
                        "screening_type" : "2D",
                        "running_time"   : 120,
                        "age_grade"      : 19,
                        "rating"         : 9.9,
                        "description"    : "너무너무힘들군",
                        "genre"          : ["스릴러", "드라마"],
                        "director"       : ["묵묵", "묵묵묵"],
                        "actor"          : ["무크", "무크무크"],
                        "theater"        : ["강남", "수원"],
                        "total_audience" : 100000,
                    }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_moive_not_exist(self):
        client = Client()
        response = client.get('/movies/3')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {
                "Result" : "MOVIE_DOES_NOT_EXIST"
            }
        )