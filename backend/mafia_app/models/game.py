from django.db import models
import random, string

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

class Game(models.Model):
    code = models.CharField(default=generate_game_code, max_length=GAME_CODE_LENGTH)
    has_started = models.BooleanField(default=False)
    has_finished = models.BooleanField(default=False)
    current_state = models.OneToOneField("GameState", on_delete=models.SET_NULL, related_name="+", null=True, blank=True)

    @property
    def has_connected_players(self):
        return len(self.players.filter(is_connected=True)) > 0

    def update_user(self, user):
        # TODO
        raise NotImplementedError
    
    def handle_action(self, action_type, action_data):
        self.current_state.handle_action(action_type, action_data)