import json

from channels.generic.websocket import JsonWebsocketConsumer

class GameConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        
    def disconnect(self, code):
        pass
    
    def receive_json(self, content):
        print(content)
        self.send_json({
            "message": "Hello, world!"
        })