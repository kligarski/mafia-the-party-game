from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

class Player(models.Model):
    class Role(models.TextChoices):
        MODERATOR = "moderator"
        VILLAGER = "villager"
        MAFIA = "mafia"
        PROTECTOR = "protector"
        SEER = "seer"
    
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="players")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="players")
    role = models.CharField(max_length=16, choices=Role, null=True, blank=True)
    is_alive = models.BooleanField(default=True)
    is_connected = models.BooleanField(default=True)
    channel_name = models.CharField(max_length=get_channel_layer().MAX_NAME_LENGTH, null=True, blank=True)
    players_discovered = models.ManyToManyField("self", symmetrical=False)
    view = models.JSONField(default=dict)
    
    def update_view(self):
        self.send("changeView", self.view)
    
    def update_state(self):
        state = {
            "id": self.id,
            "username": self.user.visible_username,
            "role": self.role,
            "playersDiscovered": [{
                "id": player.id,
                "username": player.user.visible_username,
                "role": player.role
            } for player in self.players_discovered.all()],
            "alive": self.is_alive,
            "cycle": self.game.cycle
        }
        
        self.send("changePlayerState", state)
    
    def send(self, action, data):
        async_to_sync(channel_layer.send)(self.channel_name, {
            "type": "game.message",
            "message": {
                "action": action,
                "data": data
            }
        })