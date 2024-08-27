from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import time

from .models import User, Game, Player, Lobby

@login_required
def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        unique_username = username + "@" + str(User.objects.count()) + "." + str(time.time_ns())

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

@login_required
def game(request, game_code):
    try:
        game = Game.objects.get(code=game_code, has_finished=False)
    except Game.DoesNotExist:
        messages.error(request, "Game does not exist or it has already finished.")
        return HttpResponseRedirect(reverse("index"))
    
    if len(game.players.filter(user=request.user)) == 0:
        if len(game.players.filter(user__visible_username=request.user.visible_username)) > 0:
            messages.error(request, "Someone in this game has already chosen this username. Please change your username to join this game.")
            return HttpResponseRedirect(reverse("index"))
        elif game.has_started:
            messages.error(request, "This game has already started.")
            return HttpResponseRedirect(reverse("index"))
        else:
            Player.objects.create(user=request.user, game=game, 
                                role=Player.Role.VILLAGER)
    
    return render(request, "game.html", {
        "game_code": game_code
    })

@login_required    
def create(request):
    if request.method == "POST":
        if Game.objects.filter(players__user=request.user, has_finished=False):
            messages.error(request, "You are still in an ongoing game. Make sure you leave them or use 'Change username'.")
            return HttpResponseRedirect(reverse("index"))
        
        new_game = Game.objects.create()
        new_player = Player.objects.create(user=request.user, game=new_game, role=Player.Role.MODERATOR)
        new_game.moderator = new_player
        new_lobby = Lobby.objects.create(game=new_game)
        
        new_game.current_state = new_lobby
        new_game.save()
        
        return HttpResponseRedirect(reverse("game", args=(new_game.code,)))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def join(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("game", args=(request.POST["game_code"],)))
    else:
        HttpResponseRedirect(reverse("index"))