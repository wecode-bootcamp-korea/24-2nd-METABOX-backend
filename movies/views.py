from django.http import JsonResponse
from django.views import View

from movies.models import Movie

# Create your views here.

class  MovieView(View):
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.filter(id=movie_id).get()

            result = {
                "ko_name"        : movie.ko_name,
                "en_name"        : movie.en_name,
                "release_date"   : movie.release_date,
                "close_date"     : movie.close_date,
                "screening_type" : movie.screening_type,
                "running_time"   : movie.running_time,
                "age_grade"      : movie.age_grade,
                "rating"         : movie.rating,
                "description"    : movie.description,
                "genre"          : [genre.name for genre in movie.genre.all()],
                "director"       : [director.name for director in movie.director.all()],
                "actor"          : [actor.name for actor in movie.actor.all()],
                "theater"        : [theater.location for theater in movie.theater.all()],
                "total_audience" : movie.total_audience,
            }

            return JsonResponse({"Result" : result}, status=200)

        except Movie.DoesNotExist:
            return JsonResponse({"Result" : "MOVIE_DOES_NOT_EXIST"}, status=404)