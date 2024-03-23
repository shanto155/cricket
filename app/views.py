from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Match
from .serializer import MatchSerializer, UserSerializer


# from .models import


# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return HttpResponse("Login Failed")

    return render(request, "login.html")


def reg(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(username, email, password)
        data = User.objects.create_user(username, email, password)
        data.save()
        return HttpResponse("Data Saved")

    return render(request, "register.html")


def logout(request):
    if not request.user.is_authenticated:
        return redirect("login")

    auth_logout(request)
    return redirect("login")


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "index.html")


def create(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        team1 = request.POST.get("team1")
        team2 = request.POST.get("team2")
        overs = int(request.POST.get("overs")) * 6
        tossWinner = request.POST.get("tossWinner")
        tossChoice = request.POST.get("tossChoice")
        if tossWinner == 'team1':
            tossWinner = team1
        else:
            tossWinner = team2

        Match.objects.create(user=request.user, team1=team1, team2=team2, total_over=overs, toss_winner=tossWinner,
                             toss_choice=tossChoice, team1_score=0, team2_score=0, team1_wicket=0, team2_wicket=0,
                             team1_over=0, team2_over=0, match_winner="")
        return HttpResponse("Match Created")
    return render(request, "create.html")


def team1_batting(cricket_match, run, wicket):
    if cricket_match.team1_wicket == 10 or cricket_match.team1_over == cricket_match.total_over:
        cricket_match.current_inning = 2
    else:
        cricket_match.current_inning = 1

    if cricket_match.current_inning == 1:
        cricket_match.team1_score += run
        cricket_match.team1_wicket += wicket
        cricket_match.team1_over += 1
    else:
        if cricket_match.match_winner == "":
            cricket_match.team2_score += run
            cricket_match.team2_wicket += wicket
            cricket_match.team2_over += 1
            if cricket_match.team2_score > cricket_match.team1_score:
                cricket_match.match_winner = cricket_match.team2
            elif cricket_match.team2_score == cricket_match.team1_score and (
                    cricket_match.team2_over == cricket_match.total_over or cricket_match.team2_wicket == 10):
                cricket_match.match_winner = "Match Draw"
            elif cricket_match.team2_wicket == 10 or cricket_match.team2_over == cricket_match.total_over:
                cricket_match.match_winner = cricket_match.team1

    cricket_match.save()

    data = {
        "match": cricket_match,
        "current_inning": cricket_match.current_inning,
        "team1": cricket_match.team1,
        "team2": cricket_match.team2,
        "total_over": cricket_match.total_over,
        "toss_winner": cricket_match.toss_winner,
        "toss_choice": cricket_match.toss_choice,
        "team1_score": cricket_match.team1_score,
        "team2_score": cricket_match.team2_score,
        "team1_wicket": cricket_match.team1_wicket,
        "team2_wicket": cricket_match.team2_wicket,
        "team1_over": cricket_match.team1_over,
        "team2_over": cricket_match.team2_over,
        "match_winner": cricket_match.match_winner,
    }
    return data


def team2_batting(cricket_match, run, wicket):
    if cricket_match.team2_wicket == 10 or cricket_match.team2_over == cricket_match.total_over:
        cricket_match.current_inning = 2
    else:
        cricket_match.current_inning = 1

    if cricket_match.current_inning == 1:
        cricket_match.team2_score += run
        cricket_match.team2_wicket += wicket
        cricket_match.team2_over += 1
    else:
        if cricket_match.match_winner == "":
            cricket_match.team1_score += run
            cricket_match.team1_wicket += wicket
            cricket_match.team1_over += 1
            if cricket_match.team1_score > cricket_match.team2_score:
                cricket_match.match_winner = cricket_match.team1
            elif cricket_match.team1_score == cricket_match.team2_score and (
                    cricket_match.team1_over == cricket_match.total_over or cricket_match.team1_wicket == 10):
                cricket_match.match_winner = "Match Draw"
            elif cricket_match.team1_wicket == 10 or cricket_match.team1_over == cricket_match.total_over:
                cricket_match.match_winner = cricket_match.team2

    cricket_match.save()

    data = {
        "match": cricket_match,
        "current_inning": cricket_match.current_inning,
        "team1": cricket_match.team2,
        "team2": cricket_match.team1,
        "total_over": cricket_match.total_over,
        "toss_winner": cricket_match.toss_winner,
        "toss_choice": cricket_match.toss_choice,
        "team1_score": cricket_match.team2_score,
        "team2_score": cricket_match.team1_score,
        "team1_wicket": cricket_match.team2_wicket,
        "team2_wicket": cricket_match.team1_wicket,
        "team1_over": cricket_match.team2_over,
        "team2_over": cricket_match.team1_over,
        "match_winner": cricket_match.match_winner,
    }
    return data


def match(request, match_id):
    if not request.user.is_authenticated:
        return redirect("login")

    cricket_match = Match.objects.get(id=match_id)
    if request.method == "POST":
        run = int(request.POST.get("run"))
        wicket = int(request.POST.get("wicket"))
        if (cricket_match.toss_winner == cricket_match.team1 and cricket_match.toss_choice == "bat") or (
                cricket_match.toss_winner == cricket_match.team2 and cricket_match.toss_choice == "bowl"):
            data = team1_batting(cricket_match, run, wicket)
        else:
            data = team2_batting(cricket_match, run, wicket)
    else:
        if (cricket_match.toss_winner == cricket_match.team1 and cricket_match.toss_choice == "bat") or (
                cricket_match.toss_winner == cricket_match.team2 and cricket_match.toss_choice == "bowl"):
            data = {
                "match": cricket_match,
                "current_inning": cricket_match.current_inning,
                "team1": cricket_match.team1,
                "team2": cricket_match.team2,
                "total_over": cricket_match.total_over,
                "toss_winner": cricket_match.toss_winner,
                "toss_choice": cricket_match.toss_choice,
                "team1_score": cricket_match.team1_score,
                "team2_score": cricket_match.team2_score,
                "team1_wicket": cricket_match.team1_wicket,
                "team2_wicket": cricket_match.team2_wicket,
                "team1_over": cricket_match.team1_over,
                "team2_over": cricket_match.team2_over,
                "match_winner": cricket_match.match_winner,
            }
        else:
            data = {
                "match": cricket_match,
                "current_inning": cricket_match.current_inning,
                "team1": cricket_match.team2,
                "team2": cricket_match.team1,
                "total_over": cricket_match.total_over,
                "toss_winner": cricket_match.toss_winner,
                "toss_choice": cricket_match.toss_choice,
                "team1_score": cricket_match.team2_score,
                "team2_score": cricket_match.team1_score,
                "team1_wicket": cricket_match.team2_wicket,
                "team2_wicket": cricket_match.team1_wicket,
                "team1_over": cricket_match.team2_over,
                "team2_over": cricket_match.team1_over,
                "match_winner": cricket_match.match_winner,
            }

    return render(request, "match.html", data)


def matches(request):
    # if not request.user.is_authenticated:
    #     return redirect("login")

    matches = Match.objects.all()
    print(len(matches))
    return render(request, "match_list.html", {"match_list": matches})




# API

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer