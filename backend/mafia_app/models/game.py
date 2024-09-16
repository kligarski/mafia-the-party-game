from django.db import models

import random, string

from . import Player

GAME_CODE_LENGTH = 6

def get_random_code():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=GAME_CODE_LENGTH))

def is_code_unique(code):
    return len(Game.objects.filter(code=code, has_finished=False)) == 0

def generate_game_code():
    code = get_random_code()
    while not is_code_unique(code):
        code = get_random_code()
    return code  

class GameManager(models.Manager):    
    def create_and_init(self, user):
        from mafia_app.models import Lobby
        
        new_game = self.create()
        new_player = Player.objects.create(user=user, game=new_game, role=Player.Role.MODERATOR)
        new_game.moderator = new_player
        new_lobby = Lobby.objects.create(game=new_game)
        
        new_game.current_state = new_lobby
        new_game.save()
        
        return new_game

class Game(models.Model):
    code = models.CharField(default=generate_game_code, max_length=GAME_CODE_LENGTH)
    has_started = models.BooleanField(default=False)
    has_finished = models.BooleanField(default=False)
    cycle = models.IntegerField(default=0)
    current_state = models.OneToOneField("GameState", on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    moderator = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name="+", null=True, blank=True) 
    
    objects = GameManager()
    
    class GameStatus(models.IntegerChoices):
        CONTINUE = 1
        MAFIA_WINS = 2
        VILLAGE_WINS = 3
    
    def regular_players(self):
        return self.players.exclude(role=Player.Role.MODERATOR)
    
    def handle_action(self, player, action_type, action_data):
        self.current_state.handle_action(player, action_type, action_data)