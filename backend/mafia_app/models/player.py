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
    players_discovered = models.ManyToManyField("self")
    state = models.JSONField()
    
    def update_view(self):
        async_to_sync(channel_layer.send)(self.channel_name, {
            "type": "game.message",
            "message": {
                "action": "changeView",
                "data": self.state
            }
        })