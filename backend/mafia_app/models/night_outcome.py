from django.db import models
from . import GameState, Player

class NightOutcome(GameState):
    night_event = models.ForeignKey("Night", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    day_event = models.ForeignKey("Day", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    
    def start(self):
        mafia_pick_dies = True
        
        if (self.night_event.protector_pick is not None 
            and self.night_event.mafia_pick.id == self.night_event.protector_pick.id):
            mafia_pick_dies = False
            
        view = {
            "view": "nightOutcome",
            "data": {
                "mode": "someoneDied" if mafia_pick_dies else "nooneDied",
                "data": {
                    "id": self.night_event.mafia_pick.id,
                    "username": self.night_event.mafia_pick.user.visible_username
                } if mafia_pick_dies else {}
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()
        
        if mafia_pick_dies:
            self.night_event.mafia_pick.is_alive = False
            self.night_event.mafia_pick.save(update_fields=["is_alive"])
            self.night_event.mafia_pick.update_state()
    
    def handle_action(self, player, action_type, action_data):
        match action_type:
            case "nightOutcomeConfirm" if player.role == Player.Role.MODERATOR:
                self.end()
            
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def end(self):
        self.day_event.night_outcome_end()