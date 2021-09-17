from django.db import models

from core.models import TimeStampModel

class Movie(TimeStampModel):
    ko_name        = models.CharField(max_length = 45)
    en_name        = models.CharField(max_length = 100)
    release_date   = models.DateField()
    close_date     = models.DateField()
    screening_type = models.CharField(max_length = 45)
    running_time   = models.IntegerField()
    age_grade      = models.IntegerField()
    rating         = models.FloatField()
    description    = models.TextField()
    user           = models.ManyToManyField('users.User', through = 'WishMovie')
    genre          = models.ManyToManyField('Genre')
    director       = models.ManyToManyField('Director')
    actor          = models.ManyToManyField('Actor')
    theater        = models.ManyToManyField('Theater', through = 'MovieTheater')
    total_audience = models.IntegerField()

    class Meta:
        db_table = "movies"

class Image(TimeStampModel):
    movie     = models.ForeignKey('Movie', on_delete = models.CASCADE, related_name = 'images')
    image_url = models.CharField(max_length = 200)

    class Meta:
        db_table = 'images'

class WishMovie(TimeStampModel):
    user  = models.ForeignKey('users.User', on_delete = models.CASCADE, related_name = 'wishmovies')
    movie = models.ForeignKey('Movie', on_delete = models.CASCADE, related_name = 'wishmovies')

    class Meta:
        db_table = 'wishmovies'

class Genre(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'genres'

class Director(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'directors'

class Actor(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'actors'

class Theater(models.Model):
    location = models.CharField(max_length = 32)

    class Meta:
        db_table = 'theaters'

class MovieTheater(TimeStampModel):
    movie         = models.ForeignKey('Movie', on_delete = models.CASCADE, related_name = 'movie_theaters')
    theater       = models.ForeignKey('Theater', on_delete = models.CASCADE, related_name = 'movie_theaters')
    start_time    = models.DateTimeField()

    class Meta:
        db_table = 'movietheaters'
