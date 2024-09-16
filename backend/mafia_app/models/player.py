from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

class Discovery(models.Model):
    class Type(models.IntegerChoices):
        TEAM = 1
        TEAM_AND_ROLE = 2
    
    from_player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="discoveries")
    to_player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="dsicoveries")
    type = models.IntegerField(choices=Type, default=2)

class Player(models.Model):   
    class Role(models.TextChoices):
        MODERATOR = "moderator"
        VILLAGER = "villager"
        MAFIA = "mafia"
        PROTECTOR = "protector"
        SEER = "seer"
        
    class Team(models.TextChoices):
        VILLAGE = "village"
        MAFIA = "mafia"
    
    ROLE_TO_TEAM = {
        Role.MODERATOR: Team.VILLAGE,
        Role.VILLAGER: Team.VILLAGE,        
        Role.MAFIA: Team.MAFIA,
        Role.PROTECTOR: Team.VILLAGE,
        Role.SEER: Team.VILLAGE,
    }
    
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="players")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="players")
    role = models.CharField(max_length=16, choices=Role, null=True, blank=True)
    is_alive = models.BooleanField(default=True)
    is_connected = models.BooleanField(default=False)
    channel_name = models.CharField(max_length=get_channel_layer().MAX_NAME_LENGTH, null=True, blank=True)
    players_discovered = models.ManyToManyField("self", 
                                                symmetrical=False, 
                                                through=Discovery, 
                                                through_fields=("from_player", "to_player"))
    view = models.JSONField(default=dict)
    
    def update_view(self):
        self.send("changeView", self.view)
    
    def update_state(self):
        state = {
            "id": self.id,
            "username": self.user.visible_username,
            "role": self.role,
            "playersDiscovered": 
                [self.get_player_data(discovery) 
                 for discovery in self.discoveries.all()],
            "alive": self.is_alive,
            "cycle": self.game.cycle
        }
        
        self.send("changePlayerState", state)
        
    def get_player_data(self, discovery: Discovery):
        data = {
            "id": discovery.to_player.id,
            "username": discovery.to_player.user.visible_username
        }
        
        if discovery.type == Discovery.Type.TEAM:
            data["team"] = Player.ROLE_TO_TEAM[discovery.to_player.role]
        elif discovery.type == Discovery.Type.TEAM_AND_ROLE:
            data["role"] = discovery.to_player.role
            
        return data
    
    def send(self, action, data):
        if self.is_connected:
            async_to_sync(channel_layer.send)(self.channel_name, {
                "type": "game.message",
                "message": {
                    "action": action,
                    "data": data
                }
            })