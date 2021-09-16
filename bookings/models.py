from django.db import models

from core.models import TimeStampModel

class Booking(TimeStampModel):
    movie_theater  = models.ForeignKey('movies.MovieTheater', on_delete = models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete = models.CASCADE)
    quantity       = models.IntegerField()
    booking_number = models.CharField(max_length = 64)
    seat_number    = models.CharField(max_length = 8)
    price          = models.IntegerField()
    adult          = models.IntegerField()
    teenager       = models.IntegerField()
    kid            = models.IntegerField()

    class Meta:
        db_table = "bookings"