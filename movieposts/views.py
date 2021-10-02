import json
from datetime import datetime

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count

from bookings.models   import Booking
from movieposts.models import LikeButton, MoviePost
from movies.models     import Movie
from core.utils        import authentication
from decorators        import query_debugger

class MoviePostWriteView(View):
    @authentication
    def get(self, request):
        movies = Movie.objects.order_by('-rating')[:5]
        return JsonResponse({
            'RESULT' : [
                {
                    "movie_id"    : movie.id,
                    "movie_title" : movie.ko_name,
                    "movie_image" : [img.image_url for img in movie.images.all()],
                } for movie in movies]}, status = 200
        )

class MoviePostView(View):
    @authentication
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id     = request.user
            movie_id    = data['movie_id']
            contents = data['contents']
            img_url = data['image_url']
            movie_query_set = Movie.objects.filter(id = movie_id).prefetch_related('images')

            if not movie_query_set.exists():
                return JsonResponse({'MESSAGE' : 'MOVIE DOES NOT EXISTS'}, status = 400)

            MoviePost.objects.create(
                user_id    = user_id,
                movie_id   = movie_id,
                content   = contents + '###' + img_url,
                like_count = 0
            )

            return JsonResponse({'MESSAGE' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)
        
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status = 400)

    def get(self, request):
        try:
            ordering = request.GET.get("ordering", '-created_at')
            # page = int(request.GET.get("page", 1))
            Movie_name      = request.GET.get("movie_name")

            OFFSET          = int(request.GET.get("offset", 0))
            LIMIT           = int(request.GET.get("limit", 8))
            print(OFFSET, LIMIT)
            movies = MoviePost.objects.order_by(ordering)[OFFSET:OFFSET+LIMIT]
            print(len(movies))
            # limit = 8
            # offset = (page-1) * limit

            # if Movie_name:
            #     movies = MoviePost.objects.filter(movie_id__ko_name__icontains = Movie_name)#movies_annotate.filter(ko_name__contains = Movie_name)


            moviepostings = MoviePost.objects.select_related('user', 'movie')
            total_count   = moviepostings.count()
            posting_count = moviepostings.values('movie_id').annotate(count=Count('movie_id')).order_by('-count')[:5]
           
            movie_post_result = []

            for moviepost in movies:
                user_email = moviepost.user.email 
                at         = user_email.find('@')
                user_email = user_email.replace(user_email[at-2:at],'**')
                user_email = user_email.split('@')[0]
                like_count = moviepost.like_count
                contents = moviepost.content
                con = contents.split('###')[0]
                url = contents.split('###')[1]


                movie_post_result.append(
                    {
                        'moviepost_id' : moviepost.id,
                        'user_id'      : moviepost.user.id,
                        'user_email'   : user_email,
                        'movie_id'     : moviepost.movie.id,
                        'movie_title'  : moviepost.movie.ko_name,
                        'contents'     : con,
                        'image_url'    : url,
                        'created_time' : (datetime.today() - moviepost.created_at).seconds//60,
                        'like_count'   : like_count
                    }
                )

            return JsonResponse(
                {
                    'total_count': total_count,
                    'result': movie_post_result,
                    'movie_posting_count' : [
                        {
                            'image_url' : Movie.objects.get(id = moviepost['movie_id']).images.first().image_url,     
                            'movie_id' : moviepost['movie_id'],
                            'movie_title' : Movie.objects.get(id = moviepost['movie_id']).ko_name,
                            'count' : moviepost['count']
                        }
                    for moviepost in posting_count]
                }, status = 400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)
        
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status = 400)

class LikeButtonView(View):
    @authentication
    def post(self, request):
        try:
            user_id  = request.user
            data     = json.loads(request.body)
            moviepost_id = data['moviepost_id']

            like_is_true = LikeButton.objects.filter(user_id = user_id, moviepost_id = moviepost_id)
            like_cnt = MoviePost.objects.get(id = moviepost_id).like_count

            if not like_is_true.exists():
                LikeButton.objects.create(user_id = user_id, moviepost_id = moviepost_id)
                MoviePost.objects.filter(id = moviepost_id).update(like_count = like_cnt + 1)
                return JsonResponse({'MESSAGE' : 'LIKE', 'True' : True}, status = 201)

            like_is_true.delete()
            if like_cnt > 0:
                MoviePost.objects.filter(id = moviepost_id).update(like_count = like_cnt - 1)

            return JsonResponse({'MESSAGE' : 'DISLIKE', 'False' : False}, status = 201)
            

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status = 400)
        