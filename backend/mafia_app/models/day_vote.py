from polymorphic.models import PolymorphicManager
from django.db import models
from random import shuffle

from . import GameState, Player

class DayVoteManager(PolymorphicManager):
    def get_random_order_of_player_ids(self, game):
        ids = [player.id for player in game.regular_players().filter(is_alive=True)]
        shuffle(ids)
        return ids
    
    def create_and_init(self, game, day_event):
        order_of_players = self.get_random_order_of_player_ids(game)
        
        votes = dict()
        for player in game.regular_players().filter(is_alive=True):
            votes[str(player.id)] = 0
        
        return self.create(game=game, day_event=day_event, 
                           order_of_players=order_of_players, votes=votes)

class DayVote(GameState):
    class State(models.IntegerChoices):
        EVENT_INFO = 1
        MODERATOR_INFO = 2
        MODERATOR_WAIT = 3
        MODERATOR_RESULT = 4
        VOTE_RESULT = 5
        EVENT_FINISHED = 6
    
    day_event = models.ForeignKey("Day", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    current_state = models.IntegerField(choices=State, default=State.EVENT_INFO)
    order_of_players = models.JSONField()
    current_player = models.IntegerField(default=-1)
    votes = models.JSONField()
    
    objects = DayVoteManager()
    
    def start(self):
        view = {
            "view": "eventInfo",
            "data": {
                "mode": "dayVoteInfo",
                "data": {}
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()
            
    def handle_action(self, player, action_type, action_data):
        match action_type:
            case "startDayVote" if (player.role == Player.Role.MODERATOR
                                    and self.current_state == self.State.EVENT_INFO):
                self.next_person()
            
            case "letPlayerVote" if (player.role == Player.Role.MODERATOR
                                     and self.current_state == self.State.MODERATOR_INFO):
                self.let_player_vote()
                
            case "dayPlayerVote" if (player.id == self.order_of_players[self.current_player]
                                     and self.current_state == self.State.MODERATOR_WAIT):
                self.handle_vote(action_data)
            
            case "dayPlayerSkipVote" if (player.id == self.order_of_players[self.current_player]
                                         and self.current_state == self.State.MODERATOR_WAIT):
                self.handle_vote(None)
                
            case "dayVoteNext" if (player.role == Player.Role.MODERATOR
                                   and self.current_state == self.State.MODERATOR_RESULT):
                self.next_person()
                
            case "endDayVote" if (player.role == Player.Role.MODERATOR
                                  and self.current_state == self.State.VOTE_RESULT):
                self.end()
            
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def next_person(self):
        if self.current_player < len(self.order_of_players) - 1:
            self.current_player += 1
            self.current_state = self.State.MODERATOR_INFO
            self.save(update_fields=["current_state", "current_player"])
            
            self.next_moderator_info()
        else:
            self.current_state = self.State.VOTE_RESULT
            self.save(update_fields=["current_state"])
            
            self.vote_result()
    
    def let_player_vote(self):
        self.current_state = self.State.MODERATOR_WAIT
        self.save(update_fields=["current_state"])
        
        self.game.moderator.view["data"]["mode"] = "moderatorWait"
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        player_voting = self.game.players.get(id=self.game.moderator.view["data"]["data"]["playerVoting"]["id"])
        
        for player in self.game.regular_players():
            if player == player_voting:
                player.view["data"]["mode"] = "playerVote"
            else:
                player.view["data"]["mode"] = "playerWaitSomebody"
                player.view["data"]["data"]["playerVoting"] = self.game.moderator.view["data"]["data"]["playerVoting"]
            
            player.save(update_fields=["view"])
            player.update_view()
            
    def handle_vote(self, data):
        self.current_state = self.State.MODERATOR_RESULT
        self.save(update_fields=["current_state"])
        
        player_voting = self.game.players.get(id=self.game.moderator.view["data"]["data"]["playerVoting"]["id"])
        
        if data is not None:
            voted_player_id = str(data["id"])
            self.votes[voted_player_id] += 1
            self.save(update_fields=["votes"])
        
        choice = {
            "id": int(voted_player_id),
            "username": Player.objects.get(id=voted_player_id).user.visible_username
        } if data is not None else None
        
        votes = self.get_votes()
        
        self.game.moderator.view["data"]["mode"] = "moderatorResult"
        self.game.moderator.view["data"]["data"]["votes"] = votes
        self.game.moderator.view["data"]["data"]["choice"] = choice
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
          
        for player in self.game.regular_players():
            if player == player_voting:
                player.view["data"]["mode"] = "playerVoteResult"
            else:
                player.view["data"]["mode"] = "playerWaitSomebodyResult"
            
            player.view["data"]["data"]["votes"] = votes
            player.view["data"]["data"]["choice"] = choice
            
            player.save(update_fields=["view"])
            player.update_view()
     
    def vote_result(self):
        most_votes_player_id = None
        most_votes = 0
        tie = True
        
        for player_id, no_votes in self.votes.items():
            if no_votes == most_votes:
                tie = True
            elif no_votes > most_votes:
                most_votes_player_id = player_id
                most_votes = no_votes
                tie = False
        
        no_players = len(self.game.regular_players().filter(is_alive=True))
        required_votes = no_players // 2
        
        voted_out_player = None
        if not tie and most_votes > required_votes:
            voted_out_player = Player.objects.get(id=most_votes_player_id)
            voted_out_player.is_alive = False
            voted_out_player.save(update_fields=["is_alive"])
            voted_out_player.update_state()

        view = {
            "view": "dayVote",
            "data": {
                "mode": "result",
                "data": {
                    "votedOut": {
                        "id": voted_out_player.id,
                        "username": voted_out_player.user.visible_username,
                    } if voted_out_player is not None else None
                }
            }
        }
        
        self.game.moderator.view = view
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        for player in self.game.regular_players():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()
               
    def end(self):
        self.current_state = self.State.EVENT_FINISHED
        self.save(update_fields=["current_state"])
        
        self.day_event.day_vote_end()
    
    def next_moderator_info(self):
        progress = self.get_current_progress()
        wait_before = self.get_wait_view(True, progress)
        wait_after = self.get_wait_view(False, progress)
        
        player_to_vote = None
        for index, player_id in enumerate(self.order_of_players):
            player = self.game.players.get(id=player_id)
            
            if index < self.current_player:
                player.view = wait_after
            else:
                player.view = wait_before
            
            if index == self.current_player:
                player_to_vote = player
            
            player.save()
            player.update_view()
        
        self.game.moderator.view = self.get_moderator_info_view(player_to_vote, progress)
        self.game.moderator.save()
        self.game.moderator.update_view()
    
    def get_current_progress(self):
        return f"{self.current_player + 1}/{len(self.order_of_players)}"
    
    def get_wait_view(self, before: bool, progress):
        return {
            "view": "dayVote",
            "data": {
                "mode": "playerWait" + ("Before" if before else "After"),
                "data": {
                    "progress": progress,
                    "noPlayers": len(self.order_of_players),
                    "votes": self.get_votes(),
                }
            }
        }
    
    def get_moderator_info_view(self, player_voting, progress):
        return {
            "view": "dayVote",
            "data": {
                "mode": "moderatorInfo",
                "data": {
                    "progress": progress,
                    "noPlayers": len(self.order_of_players),
                    "votes": self.get_votes(),
                    "playerVoting": {
                        "id": player_voting.id,
                        "username": player_voting.user.visible_username
                    }
                }    
            }
        }
    
    def get_votes(self):
        return [
            {
                "id": player.id,
                "username": player.user.visible_username,
                "votes": self.votes[str(player.id)]
            }
            for player in self.game.regular_players().filter(is_alive=True)
        ]