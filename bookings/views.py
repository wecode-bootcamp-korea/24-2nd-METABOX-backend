from datetime import date
from uuid     import uuid4 as u4
import json

from django.db.models.query import Prefetch
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, Count
from django.core.exceptions import ValidationError
from django.db.utils        import IntegrityError

from bookings.models import Booking, SeatNumber
from movies.models   import Movie, MovieTheater, Theater
from core.utils      import authentication

class ReserveView(View):
    def get(self, request):
        select_date = request.GET.get('date', date.today())
        movie_id    = request.GET.get('movie-id')
        theater_id  = request.GET.get('theater-id')

        Q_LTE     = Q(release_date__lte = select_date)
        Q_GTE     = Q(close_date__gte = select_date)
        Q_MOVIE   = Q()
        Q_THEATER = Q()

        if movie_id:
            Q_MOVIE &= Q(movie_id = movie_id)
        
        if theater_id:
            Q_THEATER &= Q(theater_id = theater_id)
        
        movie_query_set = Movie.objects.filter(Q_LTE & Q_GTE).prefetch_related(
            Prefetch('images'),
            Prefetch('movie_theaters')
        )

        movie_filter_query_set   = MovieTheater.objects.filter(Q_MOVIE, Q_THEATER).prefetch_related('movie')
        
        if not movie_filter_query_set:
            return JsonResponse({'MESSAGE' : 'MOVIE OR THEATER DOES NOT EXISTS'}, status = 400)    
        
        movie_count_list  = movie_filter_query_set.values_list('theater_id').annotate(count=Count('movie_id'))
        theater_id_list   = [theater_id[0] for theater_id in movie_count_list]
        theater_list      = Theater.objects.filter(id__in = theater_id_list)

        end_table = []
        for theater in movie_filter_query_set:
            H, M              = map(int, theater.start_time.strftime('%H:%M').split(':'))
            start_time_min    = H * 60 + M
            end_time          = theater.movie.running_time + start_time_min
            end_hour, end_min = end_time//60, end_time%60
            end_table.append(str(end_hour) + ':' + str(end_min))

        return JsonResponse({
            'MOVIES' : [
                {
                    'movie_id'        : movie.id,
                    'movie_title'     : movie.ko_name,
                    'movie_age_grade' : movie.age_grade,
                    'release_date'    : movie.release_date,
                    'close_date'      : movie.close_date,
                    'running_time'    : movie.running_time,
                    'screening_type'  : movie.screening_type,
                    'movie_poster'    : movie.images.first().image_url
                } for movie in movie_query_set],
            'THEATERS' : [
                {
                    'theater_id'   : theater_obj.id,
                    'location'     : theater_obj.location,
                    'total_movies' : count[1]
                } for theater_obj, count in zip(theater_list, movie_count_list)],
            'TIMETABLE' : [
                {
                    'start_time' : [theater.start_time.strftime('%H:%M')  for theater in movie_filter_query_set],
                    'end_time'   : end_table
                }
            ]
            }, status = 201)

    @authentication
    def post(self, request):
        try:
            data      = json.loads(request.body)
            seat_list = request.GET.getlist('seat-number')

            if SeatNumber.objects.filter(seat_number__in = seat_list):
                return JsonResponse( {'MESSAGE' : 'ALREADY EXISTS'}, status = 400)
            
            user_id        = request.user
            movie_id       = data['movie_id']
            theater_id     = data['theater_id']
            start_time     = data['start_time']
            price          = data['price']
            adult          = data['adult']
            teenager       = data['teenager']
            kid            = data['kid']
            booking_number = u4().hex

            if not MovieTheater.objects.filter(movie_id = movie_id, theater_id = theater_id, start_time = start_time):
                return JsonResponse( {'MESSAGE' : 'MOVIE OR THEATER DOES NOT EXISTS'}, status = 400)

            if int(adult) + int(teenager) + int(kid) != len(seat_list):
                return JsonResponse( {'MESSAGE' : 'THE NUMBER OF SEATS DOES NOT MATCHED'}, status = 400)

            movie_theater = MovieTheater.objects.get(movie_id = movie_id, theater_id = theater_id, start_time = start_time)

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
                        booking_id  = booking.id,
                        seat_number = seat
                    )
                for seat in seat_list]
            )

            return JsonResponse( {'MESSAGE' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse( {'MESSAGE' : 'KEY ERROR'}, status = 400)

        except ValueError:
            return JsonResponse( {'MESSAGE' : 'VALUE ERROR'}, status = 400)

        except ValidationError:
            return JsonResponse( {'MESSAGE' : 'VALIDATION ERROR'}, status = 400)
        
        except IntegrityError:
            return JsonResponse( {'MESSAGE' : 'ALREADY EXISTS'}, status = 400)


class BookingHistoryView(View):
    @authentication
    def get(self, request):
        user_id = request.user

        bookings = Booking.objects.filter(user_id = user_id).select_related('movie_theater').prefetch_related('seatnumber_set')

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
