from django.db import models

class Reply(models.Model):
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3

    user_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    response = models.IntegerField(default=NEUTRAL)