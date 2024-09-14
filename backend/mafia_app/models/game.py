from django.db import models

import random, string

from . import Player

GAME_CODE_LENGTH = 6

def get_random_code():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=GAME_CODE_LENGTH))

def is_code_unique(code):
    return len(Game.objects.filter(code=code)) == 0

def generate_game_code():
    code = get_random_code()
    while not is_code_unique(code):
        code = get_random_code()
    return code  

class Game(models.Model):
    code = models.CharField(default=generate_game_code, max_length=GAME_CODE_LENGTH)
    has_started = models.BooleanField(default=False)
    has_finished = models.BooleanField(default=False)
    cycle = models.IntegerField(default=0)
    current_state = models.OneToOneField("GameState", on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    moderator = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name="+", null=True, blank=True) 
    
    class GameStatus(models.IntegerChoices):
        CONTINUE = 1
        MAFIA_WINS = 2
        VILLAGE_WINS = 3
    
    def regular_players(self):
        return self.players.exclude(role=Player.Role.MODERATOR)
    
    def handle_action(self, player, action_type, action_data):
        self.current_state.handle_action(player, action_type, action_data)
        
    def report_error_to_moderator(self, error_msg):
        if self.moderator is None:
            return
        
        self.moderator.send("error", error_msg)