from typing import Any
from uuid import uuid4 as u4
import json

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from bookings.models import Booking, SeatNumber
from movies.models   import MovieTheater
from core.utils      import authentication
from decorators      import query_debugger

class BookingView(View):
    @authentication
    @query_debugger
    def post(self, request):
        try:
            data = json.loads(request.body)
            seat_list = list(set(request.GET.getlist('seat-number')))

            if SeatNumber.objects.filter(seat_number__in = seat_list):
                return JsonResponse( {'MESSAGE' : 'ALREADY EXISTS'}, status = 400)
            
            user_id        = request.user
            movie_id       = data['movie_id']
            theater_id     = data['theater_id']
            price          = data['price']
            adult          = data['adult']
            teenager       = data['teenager']
            kid            = data['kid']
            booking_number = u4().hex            

            if not MovieTheater.objects.filter(movie_id = movie_id, theater_id = theater_id):
                return JsonResponse( {'MESSAGE' : 'MOVIE OR THEATER DOES NOT EXISTS'}, status = 400)

            if int(adult) + int(teenager) + int(kid) != len(seat_list):
                return JsonResponse( {'MESSAGE' : 'THE NUMBER OF SEATS DOES NOT MATCHED'}, status = 400)

            movie_theater = MovieTheater.objects.get(movie_id = movie_id, theater_id = theater_id)

            booking = Booking.objects.create(
                movie_theater_id = movie_theater.id,
                user_id          = user_id,
                booking_number   = booking_number,
                price            = price,
                adult            = adult,
                teenager         = teenager,
                kid              = kid
            )

            SeatNumber.objects.bulk_create(
                [
                    SeatNumber(
                        booking_id = booking.id,
                        seat_number = seat
                    )
                for seat in seat_list]
            )

            return JsonResponse( {'MESSAGE' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse( {'MESSAGE' : 'KEY ERROR'}, status = 400)

        except ValueError:
            return JsonResponse( {'MESSAGE' : 'VALUE ERROR'}, status = 400)

    @authentication
    @query_debugger
    def get(self, request):
        user_id = request.user

        bookings = Booking.objects.filter(user_id = user_id)

        if not bookings:
            return JsonResponse( {'MESSAGE' : 'HISTORY DOES NOT EXISTS'}, status = 400)

        return JsonResponse(
            {
                'history' : [
                    {
                        "korean_name"    : booking.movie_theater.movie.ko_name,
                        "english_name"   : booking.movie_theater.movie.en_name,
                        "booking_number" : booking.booking_number,
                        "start_time"     : booking.movie_theater.start_time,
                        "seat_number"    : [seat_number.seat_number for seat_number in booking.seatnumber_set.all()],
                        "adult"          : booking.adult,
                        "teenager"       : booking.teenager,
                        "kid"            : booking.kid,
                        "price"          : booking.price
                    }
                for booking in bookings]
            }, status = 200
        )
