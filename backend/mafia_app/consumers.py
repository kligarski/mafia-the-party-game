import json

from channels.generic.websocket import JsonWebsocketConsumer

from .models import Game, Player, Lobby

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
            self.player.save()
        else:
            self.close(4004)
        
        self.player.channel_name = self.channel_name
        self.player.save()
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
        self.player.save()
        
        if not self.game.has_started:
            lobby = Lobby.objects.get(game=self.game)
            lobby.handle_players_change()
    
    def receive_json(self, content: dict):
        if "action" in content.keys() and "data" in content.keys():
            self.game.handle_action(content["action"], content["data"])
        else:
            print("Invalid message from client")
            print(content)
    
    def game_message(self, event):
        self.send_json(event["message"])