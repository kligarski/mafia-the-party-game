from django.db import models

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
    players_discovered = models.ManyToManyField("self")
    state = models.JSONField()