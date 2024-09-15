from channels.generic.websocket import JsonWebsocketConsumer
from random import choice

from .models import Game, Lobby, Player

class GameConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.game_code = self.scope["url_route"]["kwargs"]["game_code"]
        
        if not self.user.is_authenticated:
            self.close(4003)
        
        try:
            self.game = Game.objects.get(code=self.game_code)    
        except Game.DoesNotExist:
            self.close(4004)
        
        game_player = self.game.players.filter(user=self.user)
        if len(game_player) == 1:
            self.player = game_player[0]
            self.player.is_connected = True
            self.player.channel_name = self.channel_name
            self.player.save(update_fields=["is_connected", "channel_name"])
        elif len(game_player) == 0:
            self.player = Player.objects.create(user=self.user, game=self.game, 
                                                role=Player.Role.VILLAGER,
                                                is_connected=True, channel_name=self.channel_name)
        else:
            self.close(4004)
            return
        
        self.accept()
        
        print(f"{self.user.visible_username} joined {self.game_code}")
        
        self.player.update_state()
        
        if not self.game.has_started: 
            lobby = Lobby.objects.get(game=self.game)
            lobby.handle_players_change()
        else:
            self.player.update_view()
        
    def disconnect(self, code):        
        self.player.is_connected = False
        self.player.channel_name = None
        self.player.save(update_fields=["is_connected", "channel_name"])
        
        self.game.refresh_from_db()
        
        if not self.game.has_started:            
            if len(self.game.players.all()) == 1:
                self.game.delete()
            else:
                self.player.refresh_from_db()
                
                old_moderator = self.player
                new_moderator = None
                
                if old_moderator.role == Player.Role.MODERATOR:
                    new_moderator = choice(list(self.game.regular_players()))
                    new_moderator.role = Player.Role.MODERATOR
                    self.game.moderator = new_moderator

                    new_moderator.save(update_fields=["role"])
                    self.game.save(update_fields=["moderator"])
                    
                old_moderator.delete()
                
                if new_moderator is not None:
                    new_moderator.update_state()
                
                lobby = Lobby.objects.get(game=self.game)
                lobby.handle_players_change()
    
    def receive_json(self, content: dict):
        if "action" in content.keys() and "data" in content.keys():
            self.game.refresh_from_db()
            self.player.refresh_from_db()
            self.game.handle_action(self.player, content["action"], content["data"])
        else:
            print("Invalid message from client")
            print(content)
    
    def game_message(self, event):
        self.send_json(event["message"])