from django.db import models

from core.models import TimeStampModel

class MoviePost(TimeStampModel):
    user       = models.ForeignKey('users.User', on_delete = models.CASCADE)
    movie      = models.ForeignKey('movies.Movie', on_delete = models.CASCADE)
    content    = models.TextField()
    like_count = models.IntegerField()

    class Meta:
        db_table = "movieposts"