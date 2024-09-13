from polymorphic.models import PolymorphicManager
from django.db import models
from . import GameState, Player

class SeerEventManager(PolymorphicManager):
    def create_and_init(self, game, night_event):
        seer = game.players.get(role=Player.Role.SEER)
        return self.create(game=game, night_event=night_event, seer=seer)

class SeerEvent(GameState):
    class State(models.IntegerChoices):
        MODERATOR_INFO = 1
        PICK = 2
        RESULT = 3
        MODERATOR_END = 4
        EVENT_FINISHED = 5
    
    seer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="+")
    night_event = models.ForeignKey("Night", on_delete=models.CASCADE, related_name="+")
    current_state = models.IntegerField(choices=State, default=State.MODERATOR_INFO)
    
    objects = SeerEventManager()
    
    def start(self):
        self.seer.refresh_from_db()
        
        moderator_view = {
            "view": "seerPick",
            "data": {
                "mode": "moderatorInfo",
                "data": {
                    "seer": {
                        "id": self.seer.id,
                        "username": self.seer.user.visible_username,
                        "alive": self.seer.is_alive
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
            case "startSeerPick" if (player.role == Player.Role.MODERATOR
                                     and self.current_state == self.State.MODERATOR_INFO
                                     and self.seer.is_alive):
                self.start_seer_pick()
                
            case "skipSeerPick" if (player.role == Player.Role.MODERATOR
                                    and self.current_state == self.State.MODERATOR_INFO
                                    and not self.seer.is_alive):
                self.end()
                
            case "seerPick" if (player.role == Player.Role.SEER
                                and self.current_state == self.State.PICK
                                and self.seer.is_alive):
                self.seer_pick(action_data)
                
            case "seerConfirm" if (player.role == Player.Role.SEER
                                   and self.current_state == self.State.RESULT
                                   and self.seer.is_alive):
                self.seer_confirm()
            
            case "endSeerPick" if (player.role == Player.Role.MODERATOR
                                   and self.current_state == self.State.MODERATOR_END
                                   and self.seer.is_alive):
                self.end()
                
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def start_seer_pick(self):
        self.current_state = self.State.PICK
        self.save(update_fields=["current_state"])
        
        moderator_view = {
            "view": "seerPick",
            "data": {
                "mode": "moderatorWaitForPick",
                "data": {
                    "seer": {
                        "id": self.seer.id,
                        "username": self.seer.user.visible_username,
                        "alive": self.seer.is_alive
                    }
                }
            }
        }
        
        self.game.refresh_from_db()
        
        seer_view = {
            "view": "seerPick",
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
        
        self.seer.view = seer_view
        self.seer.save(update_fields=["view"])
        self.seer.update_view()
    
    def seer_pick(self, data):
        try:
            picked_player = self.game.players.get(id=data["id"])
            if not picked_player.is_alive or picked_player == self.game.moderator:
                raise Player.DoesNotExist
        except Player.DoesNotExist:
            return
        
        self.current_state = self.State.RESULT
        self.save(update_fields=["current_state"])
        
        moderator_view = {
            "view": "seerPick",
            "data": {
                "mode": "moderatorWaitForConfirm",
                "data": {
                    "pick": {
                        "id": picked_player.id,
                        "username": picked_player.user.visible_username
                    }
                }
            }
        }
        
        
        # TODO: reveal only team (mafia vs village), instead of role (e.g. protector or seer!)
        # possibly use additional data for the relation that will make clear whether player knows the team or the role of another player.
        seer_view = {
            "view": "seerPick",
            "data": {
                "mode": "result",
                "data": {
                    "pick": {
                        "id": picked_player.id,
                        "username": picked_player.user.visible_username,
                        "role": picked_player.role
                    }
                }
            }
        }
        
        self.game.moderator.view = moderator_view
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        self.seer.view = seer_view
        self.seer.save(update_fields=["view"])
        self.seer.update_view()
        
        self.seer.players_discovered.add(picked_player)
        self.seer.update_state()
        
    def seer_confirm(self):
        self.current_state = self.State.MODERATOR_END
        self.save(update_fields=["current_state"])
        
        seer_view = {
            "view": "backToSleep",
            "data": {}
        }
        
        moderator_view = {
            "view": "seerPick",
            "data": {
                "mode": "moderatorEnd",
                "data": {
                    "seer": {
                        "id": self.seer.id,
                        "username": self.seer.user.visible_username,
                        "alive": self.seer.is_alive
                    }
                }
            }
        }
        
        self.game.moderator.view = moderator_view
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        self.seer.view = seer_view
        self.seer.save(update_fields=["view"])
        self.seer.update_view()
        
    def end(self):
        self.current_state = self.State.EVENT_FINISHED
        self.save(update_fields=["current_state"])
        
        self.night_event.seer_event_end()