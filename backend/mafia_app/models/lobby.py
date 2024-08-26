from .game_state import GameState

from ..models import Player, RoleReveal

class Lobby(GameState):
    def handle_action(self, action_type, action_data):
        if action_type == "startGame":
            self.start_game()
        else:
            self.unknown_action(action_type, action_data)
    
    def handle_players_change(self):
        connected_players = self.game.players.filter(is_connected=True)
        
        view = {
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
            player.view = view
            player.update_view()
            
    def start_game(self):
        moderator_present = len(self.game.players.filter(role=Player.Role.MODERATOR, is_connected=True)) == 1
        connected_players = self.game.players.filter(is_connected=True).exclude(role=Player.Role.MODERATOR)
        
        if moderator_present and len(connected_players) >= 4:
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