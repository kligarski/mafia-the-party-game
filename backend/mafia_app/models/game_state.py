from django.db import models
from polymorphic.models import PolymorphicModel

class GameState(PolymorphicModel):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="states")
    
    def handle_action(self, player, action_type, action_data):
        raise NotImplementedError

    def unknown_action(self, action_type, action_data):
        print("Unknown action for this state:")
        print(action_type, action_data)
        
    def unauthorized_action(self, player, action_type, action_data):
        print("Unauthorized action:")
        print(player.user.username, action_type, action_data)