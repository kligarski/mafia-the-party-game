from django.db import models
from polymorphic.models import PolymorphicModel

class GameState(PolymorphicModel):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="states")
    
    def handle_action(self, action_type, action_data):
        raise NotImplementedError