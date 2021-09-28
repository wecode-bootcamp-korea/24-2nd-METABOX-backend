from django.urls import path

from movies.views import MovieView

urlpatterns = [
    path("/<int:movie_id>", MovieView.as_view())
]