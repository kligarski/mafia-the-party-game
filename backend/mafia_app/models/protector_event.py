from polymorphic.models import PolymorphicManager
from django.db import models
from . import GameState, Player

class ProtectorEventManager(PolymorphicManager):
    def create_and_init(self, game, night_event):
        protector = game.players.get(role=Player.Role.PROTECTOR)
        return self.create(game=game, night_event=night_event, protector=protector)

class ProtectorEvent(GameState):
    class State(models.IntegerChoices):
        MODERATOR_INFO = 1
        PICK = 2
        MODERATOR_RESULT = 3
        EVENT_FINISHED = 4
    
    protector = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    night_event = models.ForeignKey("Night", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    current_state = models.IntegerField(choices=State, default=State.MODERATOR_INFO)
    
    objects = ProtectorEventManager()
    
    def start(self):
        self.protector.refresh_from_db()
        
        moderator_view = {
            "view": "protectorPick",
            "data": {
                "mode": "moderatorInfo",
                "data": {
                    "protector": {
                        "id": self.protector.id,
                        "username": self.protector.user.visible_username,
                        "alive": self.protector.is_alive
                    }
                }
            }
        }
        
        player_view = {
            "view": "noPeeking",
            "data": {}
        }
        
        for player in self.game.regular_players():
            player.view = player_view
            player.save(update_fields=["view"])
            player.update_view()
        
        self.game.moderator.view = moderator_view
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
    
    def handle_action(self, player, action_type, action_data):
        match action_type:
            case "startProtectorPick" if (player.role == Player.Role.MODERATOR
                                          and self.current_state == self.State.MODERATOR_INFO):
                self.start_protector_pick()
                
            case "skipProtectorPick" if (player.role == Player.Role.MODERATOR
                                         and self.current_state == self.State.MODERATOR_INFO
                                         and not self.protector.is_alive):
                self.end()
                
            case "protectorPick" if (player.role == Player.Role.PROTECTOR
                                     and self.current_state == self.State.PICK
                                     and self.protector.is_alive):
                self.protector_pick(action_data)
            
            case "endProtectorPick" if (player.role == Player.Role.MODERATOR
                                        and self.current_state == self.State.MODERATOR_RESULT
                                        and self.protector.is_alive):
                self.end()
                
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def start_protector_pick(self):
        if not self.protector.is_alive:
            self.end()
            return
        
        self.current_state = self.State.PICK
        self.save(update_fields=["current_state"])
        
        moderator_view = {
            "view": "protectorPick",
            "data": {
                "mode": "moderatorWait",
                "data": {
                    "protector": {
                        "id": self.protector.id,
                        "username": self.protector.user.visible_username,
                        "alive": self.protector.is_alive
                    }
                }
            }
        }
        
        self.game.refresh_from_db()
        
        protector_view = {
            "view": "protectorPick",
            "data": {
                "mode": "pick",
                "data": {
                    "players": [
                        {
                            "id": player.id,
                            "username": player.user.visible_username,
                            "alive": player.is_alive
                        }
                        for player in self.game.regular_players()
                    ]
                }
            }
        }
        
        self.game.moderator.view = moderator_view
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        self.protector.view = protector_view
        self.protector.save(update_fields=["view"])
        self.protector.update_view()
    
    def protector_pick(self, data):
        try:
            picked_player = self.game.players.get(id=data["id"])
            if not picked_player.is_alive or picked_player == self.game.moderator:
                raise Player.DoesNotExist
        except Player.DoesNotExist:
            return
        
        self.current_state = self.State.MODERATOR_RESULT
        self.save(update_fields=["current_state"])

        self.night_event.protector_pick = picked_player
        self.night_event.save(update_fields=["protector_pick"])
        
        moderator_view = {
            "view": "protectorPick",
            "data": {
                "mode": "moderatorResult",
                "data": {
                    "pick": {
                        "id": self.night_event.protector_pick.id,
                        "username": self.night_event.protector_pick.user.visible_username
                    }
                }
            }
        }
        
        protector_view = {
            "view": "backToSleep",
            "data": {}
        }
        
        self.game.moderator.view = moderator_view
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        self.protector.view = protector_view
        self.protector.save(update_fields=["view"])
        self.protector.update_view()
        
    def end(self):
        self.current_state = self.State.EVENT_FINISHED
        self.save(update_fields=["current_state"])
        
        self.night_event.protector_event_end()
    