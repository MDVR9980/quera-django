from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.IntegerField()
    play_time = models.DateTimeField()


class Seat(models.Model):
    number = models.IntegerField()


class Ticket(models.Model):
    class Meta:
        unique_together = ('movie', 'seat')

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    date_bought = models.DateTimeField(auto_now_add=True)
