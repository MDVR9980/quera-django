from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.urls import reverse
from django.db.models import Count
from .models import Movie, Seat, Ticket


def list_movies(request):
    movies = Movie.objects.all()
    return render(request, "app/movies.html", {"movies": movies})


def list_seats(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reserved = Ticket.objects.filter(movie=movie).values_list("seat_id", flat=True)
    seats = Seat.objects.exclude(id__in=reserved)
    return render(request, "app/seats.html", {"movie": movie, "seats": seats})


def reserve_seat(request, movie_id, seat_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seat = get_object_or_404(Seat, id=seat_id)

    if not request.user.is_authenticated:
        login_url = reverse("login")
        next_url = reverse("list_seats", args=[movie.id])
        return redirect(f"{login_url}?next={next_url}")

    if Ticket.objects.filter(movie=movie, seat=seat).exists():
        return redirect("list_seats", movie_id=movie.id)

    Ticket.objects.create(
        movie=movie, user=request.user, seat=seat, date_bought=timezone.now()
    )
    return redirect("list_seats", movie_id=movie.id)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # handle redirect after signup
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("list_movies")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def stats(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    data = (
        Ticket.objects.values("seat__number")
        .order_by("seat__number")
        .annotate(total_count=Count("id"))
    )

    stats_data = [
        {"seat__number": row["seat__number"], "total": row["total_count"]}
        for row in data
    ]
    return JsonResponse({"stats": stats_data})
