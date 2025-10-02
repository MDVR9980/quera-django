from django.urls import path
from .views import *

urlpatterns = [
    path('', list_movies, name='list_movies'),
    path('<int:movie_id>/seats', list_seats, name='list_seats'),
    path('seat/reserve/<int:movie_id>/<int:seat_id>', reserve_seat, name='reserve_seat'),
]
