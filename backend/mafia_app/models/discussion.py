from django.db import models
from datetime import timedelta, datetime, timezone
from . import GameState, Player

class Discussion(GameState):
    class State(models.IntegerChoices):
        EVENT_INFO = 1
        DISCUSSION_ONGOING = 2
        DISCUSSION_FINISHED = 3
        EVENT_FINISHED = 4
    
    INITIAL_DURATION = timedelta(minutes=5)
    EXTENSION = timedelta(minutes=2)
    
    day_event = models.ForeignKey("Day", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    current_state = models.IntegerField(choices=State, default=State.EVENT_INFO)
    discussion_end_time = models.DateTimeField(null=True, blank=True)
    
    def start(self):
        view = {
            "view": "eventInfo",
            "data": {
                "mode": "discussionInfo",
                "data": {}
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()
    
    def handle_action(self, player, action_type, action_data):
        match action_type:
            case "startDiscussion" if (player.role == Player.Role.MODERATOR
                                       and self.current_state == self.State.EVENT_INFO):
                self.discussion_start()
            
            case "extendDiscussion" if (player.role == Player.Role.MODERATOR
                                        and self.current_state == self.State.DISCUSSION_ONGOING):
                self.discussion_extend()
            
            case "finishDiscussion" if (player.role == Player.Role.MODERATOR
                                        and self.current_state == self.State.DISCUSSION_ONGOING):
                self.discussion_finish()
                
            case "endDiscussion" if (player.role == Player.Role.MODERATOR
                                     and self.current_state == self.State.DISCUSSION_FINISHED):
                self.end()
            
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def discussion_start(self):
        self.current_state = self.State.DISCUSSION_ONGOING
        self.discussion_end_time = datetime.now(timezone.utc) + self.INITIAL_DURATION
        self.save(update_fields=["current_state", "discussion_end_time"])
        
        self.update_ongoing_view_for_all_players()
    
    def discussion_extend(self):
        self.discussion_end_time = self.discussion_end_time + self.EXTENSION
        self.save(update_fields=["discussion_end_time"])
        
        self.update_ongoing_view_for_all_players()
    
    def discussion_finish(self):
        self.current_state = self.State.DISCUSSION_FINISHED
        self.save(update_fields=["current_state"])
        
        view = self.get_finished_view()
        
        for player in self.game.players.all():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()
            
    def end(self):
        self.current_state = self.State.EVENT_FINISHED
        self.save(update_fields=["current_state"])
        
        self.day_event.discussion_end()
    
    def update_ongoing_view_for_all_players(self):
        for player in self.game.players.all():
            player.view = self.get_ongoing_view()
            player.save(update_fields=["view"])
            player.update_view()
    
    def get_ongoing_view(self):
        return {
            "view": "discussion",
            "data": {
                "mode": "ongoing",
                "data": {
                    "endTime": self.discussion_end_time.isoformat(),
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
    
    def get_finished_view(self):
        return {
            "view": "discussion",
            "data": {
                "mode": "finished",
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
        
        