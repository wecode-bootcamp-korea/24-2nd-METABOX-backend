from django.db import models
from core.models import TimeStampModel

class User(TimeStampModel):
    password     = models.CharField(max_length = 256)
    email        = models.CharField(max_length = 64, unique = True)
    birth_day    = models.DateField()
    name         = models.CharField(max_length = 32)
    phone_number = models.CharField(max_length = 16)
    kakao_id     = models.CharField(max_length = 45)

    class Meta:
        db_table = "users"
