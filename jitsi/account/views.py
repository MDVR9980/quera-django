from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, TeamForm
from .models import Account, Team


def home(request):
    team_name = "None"
    if request.user.is_authenticated and request.user.team:
        team_name = request.user.team.name
    return render(request, "home.html", {"team_name": team_name})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("joinoradd_team")
        return redirect("signup")
    else:
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})


def login_account(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
        return redirect("login_account")
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def logout_account(request):
    logout(request)
    return redirect("login_account")


@login_required
def joinoradd_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data.get("name")
            team, created = Team.objects.get_or_create(
                name=team_name,
                defaults={"jitsi_url_path": f"http://meet.jit.si/{team_name}"},
            )
            request.user.team = team
            request.user.save()
            return redirect("home")
        return redirect("home")
    else:
        if request.user.team:
            return redirect("home")
        form = TeamForm()
        return render(request, "team.html", {"form": form})


@login_required
def exit_team(request):
    request.user.team = None
    request.user.save()
    return redirect("home")
