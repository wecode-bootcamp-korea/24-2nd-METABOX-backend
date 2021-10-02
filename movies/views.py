from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Count
from django.core.exceptions import FieldError

from movies.models import Movie

class  MovieView(View):
    def get(self, movie_id):
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
                "image_url"      : movie.images.first().image_url,
            }

            return JsonResponse({"Result" : result}, status=200)

        except Movie.DoesNotExist:
            return JsonResponse({"Result" : "MOVIE_DOES_NOT_EXIST"}, status=404)

class MovieListView(View):
    def get(self, request):
        try:
            movies_annotate = Movie.objects.annotate(likes=Count("wishmovies"))
            movies          = movies_annotate.order_by("-likes")
            order_condition = request.GET.get("orderby", "None")
            OFFSET          = int(request.GET.get("offset", 0))
            LIMIT           = int(request.GET.get("limit", 4))
            Movie_name      = request.GET.get("movie_name")
            total_count     = movies_annotate.count()

            if order_condition == "release_date":
                movies = movies_annotate.order_by("-release_date")

            if order_condition == "rating":
                movies = movies_annotate.order_by("-rating")

            if order_condition == "likes":
                movies = movies_annotate.order_by("-likes")

            if Movie_name:
                movies = movies_annotate.filter(ko_name__contains = Movie_name)

            movies = movies[0:OFFSET+LIMIT]

            result = [{
                "ko_name"        : movie.ko_name,                
                "release_date"   : movie.release_date,
                "age_grade"      : movie.age_grade,
                "rating"         : movie.rating,
                "description"    : movie.description,
                "like_count"     : movie.likes,
                "image_url"      : movie.images.first().image_url,

            } for movie in movies]

            return JsonResponse({"Result" : result, "Total_Count":total_count}, status=200)
    
        except FieldError:
            return JsonResponse({"Result": "ORDER_BY_ERROR"}, status=404)