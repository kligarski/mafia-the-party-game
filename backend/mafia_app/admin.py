from django.contrib import admin
from .models import User, Game, GameState, Player, Lobby, RoleReveal

admin.site.register(User)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(GameState)
admin.site.register(Lobby)
admin.site.register(RoleReveal)
