from django.db import models
from .game_state import GameState

class Lobby(GameState):
    def handle_action(self, action_type, action_data):
        # TODO
        pass