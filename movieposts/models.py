from django.db import models

from core.models import TimeStampModel

class MoviePost(TimeStampModel):
    user       = models.ForeignKey('users.User', on_delete = models.CASCADE)
    movie      = models.ForeignKey('movies.Movie', on_delete = models.CASCADE)
    content    = models.TextField()
    like_count = models.IntegerField()
    user_like  = models.ManyToManyField('users.User', through = 'LikeButton', related_name = 'movieposts')

    class Meta:
        db_table = "movieposts"

class LikeButton(TimeStampModel):
    user      = models.ForeignKey('User', on_delete = models.CASCADE)
    moviepost = models.ForeignKey('MoviePost', on_delete = models.CASCADE)

    class Meta:
        db_table = 'likebuttons'

