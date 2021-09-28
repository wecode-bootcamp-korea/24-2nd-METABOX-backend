from django.urls import path

from movies.views import MovieListView, MovieView

urlpatterns = [
    path("/<int:movie_id>", MovieView.as_view()),
    path("/list", MovieListView.as_view()),
]