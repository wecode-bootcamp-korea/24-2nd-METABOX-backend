import json

from datetime import datetime

from django.db import reset_queries
from django.http import response
from django.test import TestCase, Client
from django.test.client import CONTENT_TYPE_RE

from movies.models import Actor, Director, Genre, Image, Movie, Theater, MovieTheater, WishMovie
from users.models import User

class MovieTest(TestCase):
    def setUp(self):
        
        genres = Genre.objects.bulk_create(
            [
                Genre(
                    id   = 1,
                    name = '스릴러'
                ),
                Genre(
                    id   = 2,
                    name = '드라마'
                )
            ]
        )

        directors = Director.objects.bulk_create(
            [
                Director(
                    id   = 1,
                    name = "묵묵"
                ),
                Director(
                    id   = 2,
                    name = '묵묵묵'
                )
            ]
        )

        actors = Actor.objects.bulk_create(
            [
                Actor(
                    id   = 1,
                    name = '무크'
                ),
                Actor(
                    id   = 2,
                    name = '무크무크'
                )
            ]
        )
        
        theaters = Theater.objects.bulk_create(
            [
                Theater(
                    id       = 1,
                    location = "강남"
                ),
                Theater(
                    id       = 2,
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

        Image.objects.create(
            movie_id = movie.id,
            image_url = "aaaa"
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
        Image.objects.all().delete()

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
                        "image_url"      : "aaaa"
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

class MovieListTest(TestCase):
    def setUp(self):
        movie = Movie.objects.create(
            id             = 1,
            ko_name        = "용의 눈물",
            en_name        = "tears of dragon",
            release_date   = "2002-01-02",
            close_date     = "2002-03-01",
            screening_type = "2D",
            running_time   = 120,
            age_grade      = 12,
            rating         = 8.9,
            description    = "용이 눈물을 흘리면 생기는 일",
            total_audience = 1002020,
        )

        Image.objects.create(
            movie_id = movie.id,
            image_url = 'aaa'
        )
        movie = Movie.objects.create(
            id             = 2,
            ko_name        = "나의 눈물",
            en_name        = "tears of muk",
            release_date   = "2012-03-22",
            close_date     = "2012-06-21",
            screening_type = "2D",
            running_time   = 150,
            age_grade      = 15,
            rating         = 9.9,
            description    = "내가 눈물을 흘리면 생기는 일",
            total_audience = 455520,
        )
        Image.objects.create(
            movie_id = movie.id,
            image_url = 'aaa'
        )
        movie = Movie.objects.create(
            id             = 3,
            ko_name        = "바보 돼지 삼형제",
            en_name        = "stupid pigs",
            release_date   = "2020-08-12",
            close_date     = "2020-11-11",
            screening_type = "2D",
            running_time   = 90,
            age_grade      = 0,
            rating         = 2.2,
            description    = "바보 돼지 삼형제의 이야기",
            total_audience = 520,
        )
        Image.objects.create(
            movie_id = movie.id,
            image_url = 'aaa'
        )
        movie = Movie.objects.create(
            id             = 4,
            ko_name        = "생선 게임",
            en_name        = "fish game",
            release_date   = "2010-08-19",
            close_date     = "2010-11-18",
            screening_type = "2D",
            running_time   = 123,
            age_grade      = 0,
            rating         = 5.5,
            description    = "생선들의 목숨을 건 생존게임",
            total_audience = 51120,
        )
        Image.objects.create(
            movie_id = movie.id,
            image_url = 'aaa'
        )
        movie = Movie.objects.create(
            id             = 5,
            ko_name        = "코코코딩",
            en_name        = "cococoding",
            release_date   = "2017-11-12",
            close_date     = "2018-02-11",
            screening_type = "2D",
            running_time   = 133,
            age_grade      = 12,
            rating         = 3.5,
            description    = "코코코딩딩딩",
            total_audience = 130,
        )
        Image.objects.create(
            movie_id = movie.id,
            image_url = 'aaa'
        )
        movie = Movie.objects.create(
            id             = 6,
            ko_name        = "데스노트북",
            en_name        = "death labtop",
            release_date   = "2014-05-05",
            close_date     = "2014-08-04",
            screening_type = "2D",
            running_time   = 153,
            age_grade      = 0,
            rating         = 7.5,
            description    = "노트북에 이름을 쓰면 죽음이...",
            total_audience = 112130,
        )
        Image.objects.create(
            movie_id = movie.id,
            image_url = 'aaa'
        )

        User.objects.bulk_create(
            [
                User(
                    id = i,
                    password     = "1111aaa",
                    email        = f"aaaa{e}@gmail.com",
                    birth_day    = "2001-01-01",
                    name         = "i호기",
                    phone_number = "010-1111-1111",
                    kakao_id     = "kakakao"
                ) for i,e in zip(range(1,7), range(1,7))
            ]
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=1), 
           user  = User.objects.get(id=1)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=1), 
           user  = User.objects.get(id=2)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=1), 
           user  = User.objects.get(id=3)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=2), 
           user  = User.objects.get(id=1)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=2), 
           user  = User.objects.get(id=2)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=2), 
           user  = User.objects.get(id=3)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=2), 
           user  = User.objects.get(id=4)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=3), 
           user  = User.objects.get(id=4)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=4), 
           user  = User.objects.get(id=6)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=4), 
           user  = User.objects.get(id=5)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=5), 
           user  = User.objects.get(id=1)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=5), 
           user  = User.objects.get(id=2)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=5), 
           user  = User.objects.get(id=3)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=5), 
           user  = User.objects.get(id=4)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=5), 
           user  = User.objects.get(id=5)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=5), 
           user  = User.objects.get(id=6)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=1), 
           user  = User.objects.get(id=6)
        )

        WishMovie.objects.create(
           movie = Movie.objects.get(id=6), 
           user  = User.objects.get(id=6)
        )

    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        WishMovie.objects.all().delete()
    
    def test_movielist_get_success(self):
        client   = Client()
        response = client.get('/movies/list')
        self.assertEqual(response.json(),
            {
                "Result": [
                    {
                        "ko_name"      : "코코코딩",
                        "release_date" : "2017-11-12",
                        "age_grade"    : 12,
                        "rating"       : 3.5,
                        "description"  : "코코코딩딩딩",
                        "like_count"   : 6,
                        "image_url"    : "aaa"
                    },
                    {
                        "ko_name"      : "용의 눈물",
                        "release_date" : "2002-01-02",
                        "age_grade"    : 12,
                        "rating"       : 8.9,
                        "description"  : "용이 눈물을 흘리면 생기는 일",
                        "like_count"   : 4,
                        "image_url"    : "aaa"
                    },
                    {
                        "ko_name"      : "나의 눈물",
                        "release_date" : "2012-03-22",
                        "age_grade"    : 15,
                        "rating"       : 9.9,
                        "description"  : "내가 눈물을 흘리면 생기는 일",
                        "like_count"   : 4,
                        "image_url"    : "aaa"
                    },
                    {
                        "ko_name"      : "생선 게임",
                        "release_date" : "2010-08-19",
                        "age_grade"    : 0,
                        "rating"       : 5.5,
                        "description"  : "생선들의 목숨을 건 생존게임",
                        "like_count"   : 2,
                        "image_url"    : "aaa"
                    },
                ],
                "Total_Count": 6
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_movielist_get_success_order_by_release_date(self):
        client   = Client()
        response = client.get('/movies/list?order-by=release_date')
        self.assertEqual(response.json(),
            {
                "Result": [
                    {
                        "ko_name"      : "바보 돼지 삼형제",
                        "release_date" : "2020-08-12",
                        "age_grade"    : 0,
                        "rating"       : 2.2,
                        "description"  : "바보 돼지 삼형제의 이야기",
                        "like_count"   : 1,
                        "image_url"    : "aaa"
                    },
                    {
                        "ko_name"      : "코코코딩",
                        "release_date" : "2017-11-12",
                        "age_grade"    : 12,
                        "rating"       : 3.5,
                        "description"  : "코코코딩딩딩",
                        "like_count"   : 6,
                        "image_url"    : "aaa"
                    },
                    {
                        "ko_name"      : "데스노트북",
                        "release_date" : "2014-05-05",
                        "age_grade"    : 0,
                        "rating"       : 7.5,
                        "description"  : "노트북에 이름을 쓰면 죽음이...",
                        "like_count"   : 1,
                        "image_url"    : "aaa"
                    },
                    {
                        "ko_name"      : "나의 눈물",
                        "release_date" : "2012-03-22",
                        "age_grade"    : 15,
                        "rating"       : 9.9,
                        "description"  : "내가 눈물을 흘리면 생기는 일",
                        "like_count"   : 4,
                        "image_url"    : "aaa"
                    }
                ],
                "Total_Count": 6
            }
        )
        self.assertEqual(response.status_code, 200)