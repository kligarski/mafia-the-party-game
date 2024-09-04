from django.db import models
from . import GameState, Game

class End(GameState):   
    game_result = models.IntegerField(choices=Game.GameStatus)
    
    def start(self):
        self.game.has_finished = True
        self.game.save(update_fields=["has_finished"])
        
        for player in self.game.regular_players():
            player.players_discovered.add(*self.game.regular_players())
            player.update_state()
        
        match self.game_result:
            case Game.GameStatus.MAFIA_WINS:
                mode = "mafiaWins"
            
            case Game.GameStatus.VILLAGE_WINS:
                mode = "villageWins"
        
        view = {
            "view": "end",
            "data": {
                "mode": mode,
                "data": {
                    "players": [
                        {
                            "id": player.id,
                            "username": player.user.visible_username,
                            "role": player.role,
                            "alive": player.is_alive
                        }
                        for player in self.game.regular_players()
                    ]
                }
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()
            
    def handle_action(self, player, action_type, action_data):
        match action_type:            
            case _:
                self.unknown_action(player, action_type, action_data)