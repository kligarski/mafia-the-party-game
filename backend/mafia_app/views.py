from django.shortcuts import render

def game(request):
    return render(request, "game.html")

def login(request):
    return render(request, "login.html")