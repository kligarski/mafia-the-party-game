from .game_state import GameState

from ..models import Player, RoleReveal

class Lobby(GameState):
    def handle_action(self, player, action_type, action_data):
        match action_type:
            case "startGame" if player.role == Player.Role.MODERATOR:
                self.start_game()
                    
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def handle_players_change(self):
        connected_players = self.game.players.filter(is_connected=True)
        
        view = {
            "view": "lobby",
            "data": {
                "players": [
                    self.get_player_data(player) for player in connected_players
                ]   
            }
        }
        
        for player in connected_players:
            player.view = view
            player.update_view()
            
    def start_game(self):
        connected_players = self.game.players.filter(is_connected=True).exclude(role=Player.Role.MODERATOR)
        
        if self.game.moderator.is_connected and len(connected_players) >= 4:
            self.game.has_started = True
            self.game.save()
            
            self.game.players.filter(is_connected=False).delete()
            self.game.save()
            
            role_reveal = RoleReveal.objects.create_and_init(self.game)
            self.game.current_state = role_reveal
            self.game.save()
            
            role_reveal.start()
        else:
            self.game.report_error_to_moderator(("There are not enough players to start the game "
                                                "(at least 4 regular players are required)."))
            
    def get_player_data(self, player: Player):
        data = {
            "id": player.id,
            "username": player.user.visible_username
        }
        
        if player.role:
            data["role"] = player.role
            
        return data