from django.urls import path

from movieposts.views import *

urlpatterns = [
    path("", MoviePostView.as_view()),
    path("/write", MoviePostWriteView.as_view()),
    path("/like", LikeButtonView.as_view()),
]