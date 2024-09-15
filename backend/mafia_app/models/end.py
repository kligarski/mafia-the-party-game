from django.db import models
from . import GameState, Game, Player

class End(GameState):   
    game_result = models.IntegerField(choices=Game.GameStatus)
    
    def start(self):       
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
            case "backToMenu" if (player.role == Player.Role.MODERATOR 
                                  and self.game.has_finished == False):
                self.back_to_menu()
            
            case "newGame" if (player.role == Player.Role.MODERATOR
                               and self.game.has_finished == False):
                self.new_game()
            
            case _:
                self.unknown_action(player, action_type, action_data)
                
    def back_to_menu(self):
        self.game.has_finished = True
        self.game.save(update_fields=["has_finished"])
        
        view = {
            "view": "redirect",
            "data": {
                "path": "/"
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()
    
    def new_game(self):
        self.game.has_finished = True
        self.game.save(update_fields=["has_finished"])
        
        created_game = Game.objects.create_and_init(self.game.moderator.user)
        
        view = {
            "view": "redirect",
            "data": {
                "path": "/game/" + created_game.code
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()