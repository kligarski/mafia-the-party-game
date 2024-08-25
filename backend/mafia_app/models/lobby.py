from django.db import models
from .game_state import GameState

from ..models import Player

class Lobby(GameState):
    def handle_action(self, action_type, action_data):
        # TODO
        print(action_type, action_data)
        pass
    
    def handle_players_change(self):
        connected_players = self.game.players.filter(is_connected=True)
        
        state = {
            "view": "lobby",
            "players": [
                {
                    "id": player.id,
                    "username": player.user.visible_username,
                    "isModerator": player.role == Player.Role.MODERATOR
                } for player in connected_players
            ]
        }
        
        for player in connected_players:
            player.state = state
            player.update_view()