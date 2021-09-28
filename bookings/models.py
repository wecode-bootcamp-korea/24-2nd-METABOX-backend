from django.db import models

from core.models import TimeStampModel

class Booking(TimeStampModel):
    movie_theater  = models.ForeignKey('movies.MovieTheater', on_delete = models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete = models.CASCADE)
    booking_number = models.CharField(max_length = 64)
    price          = models.IntegerField()
    adult          = models.IntegerField(null = True)
    teenager       = models.IntegerField(null = True)
    kid            = models.IntegerField(null = True)

    class Meta:
        db_table = "bookings"

class SeatNumber(TimeStampModel):
    booking     = models.ForeignKey('Booking', on_delete = models.CASCADE)
    seat_number = models.CharField(max_length = 4, unique = True)

    class Meta:
        db_table = 'seatnumbers'