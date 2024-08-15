from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User

def game(request, game_code):
    return render(request, "game.html", {
        "game_code": game_code
    })

@login_required
def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        unique_username = username + str(User.objects.count())

        try:
            user = User.objects.create_user(unique_username, visible_username=username)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, "login.html")
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))