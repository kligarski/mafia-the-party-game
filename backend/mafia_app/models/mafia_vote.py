from polymorphic.models import PolymorphicManager
from django.db import models, transaction
from . import GameState, Player

class MafiaVoteManager(PolymorphicManager):
    def create_and_init(self, game):
        votes = dict()
        for player in game.regular_players():
            votes[str(player.id)] = 0
        
        no_mafiosi = 0
        mafia_confirm = dict()
        mafia_pick = dict()
        for mafioso in game.players.filter(role=Player.Role.MAFIA, is_alive=True):
            no_mafiosi += 1
            mafia_pick[str(mafioso.id)] = None
            mafia_confirm[str(mafioso.id)] = False
        
        mafia_vote = self.create(game=game, votes=votes, no_mafiosi=no_mafiosi, 
                                 mafia_pick=mafia_pick, mafia_confirm=mafia_confirm)
        return mafia_vote

class MafiaVote(GameState):
    class State(models.IntegerChoices):
        MODERATOR_INFO = 1
        VOTE = 2
        MODERATOR_RESULT = 3
        EVENT_FINISHED = 4
    
    current_state = models.IntegerField(choices=State, default=State.MODERATOR_INFO)
    votes = models.JSONField()
    mafia_pick = models.JSONField()
    mafia_confirm = models.JSONField()
    no_mafiosi = models.IntegerField()
    no_mafiosi_confirmed = models.IntegerField(default=0)
    vote_result = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    
    objects = MafiaVoteManager()
    
    def start(self):
        moderator_view = {
            "view": "mafiaVote",
            "data": {
                "mode": "moderatorInfo",
                "data": {
                    "mafia": [
                        {
                            "id": mafioso.id,
                            "username": mafioso.user.visible_username,
                            "alive": mafioso.is_alive
                        }
                        for mafioso in self.game.players.filter(role=Player.Role.MAFIA)
                    ]
                }
            }
        }
        
        player_view = {
            "view": "noPeeking",
            "data": {}
        }
        
        for player in self.game.regular_players():
            player.view = player_view
            player.save()
            player.update_view()
        
        self.game.moderator.view = moderator_view
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
    
    def handle_action(self, player, action_type, action_data):
        match action_type:
            case "startMafiaVote" if (player.role == Player.Role.MODERATOR
                                      and self.current_state == self.State.MODERATOR_INFO):
                self.start_mafia_vote()
            
            case "mafiaVote" if player.role == Player.Role.MAFIA:
                self.mafia_vote(player, action_data)
                
            case "mafiaUnvote" if player.role == Player.Role.MAFIA:
                self.mafia_unvote(player, action_data)
                
            case "mafiaConfirm" if player.role == Player.Role.MAFIA:
                self.mafia_do_confirm(player)
            
            case "mafiaCancel" if player.role == Player.Role.MAFIA:
                self.mafia_cancel(player)
            
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def start_mafia_vote(self):
        self.current_state = self.State.VOTE
        self.save(update_fields=["current_state"])
        
        with transaction.atomic():
            self.update_moderator_and_mafia_vote_view()
    
    def mafia_vote(self, mafioso, data):
        mafioso_id = str(mafioso.id)
        new_pick_id = str(data["id"])
        
        with transaction.atomic():
            if self.mafia_confirm[mafioso_id]:
                return
            
            if self.mafia_pick[mafioso_id] is not None:
                previous_pick_id = self.mafia_pick[mafioso_id]
                self.votes[previous_pick_id] -= 1
            
            self.mafia_pick[mafioso_id] = new_pick_id
            self.votes[new_pick_id] += 1
            
            self.save()
            
            self.update_moderator_and_mafia_vote_view()
    
    def mafia_unvote(self, mafioso, data):
        mafioso_id = str(mafioso.id)
        unvoted_player_id = str(data["id"])
        
        with transaction.atomic():
            if self.mafia_confirm[mafioso_id]:
                return
            
            if self.mafia_pick[mafioso_id] != unvoted_player_id:
                print(f"Integrity error: pick - {self.mafia_pick[mafioso_id]}, unvote - {unvoted_player_id}")
                return
            
            self.mafia_pick[mafioso_id] = None
            self.votes[unvoted_player_id] -= 1
            
            self.save()
            
            self.update_moderator_and_mafia_vote_view()      
    
    def mafia_do_confirm(self, mafioso):
        mafioso_id = str(mafioso.id)
        
        with transaction.atomic():
            if self.mafia_pick[mafioso_id] is None:
                return
            
            if self.mafia_confirm[mafioso_id]:
                return
            
            self.mafia_confirm[mafioso_id] = True
            self.no_mafiosi_confirmed += 1
            self.save()
            
            self.update_mafioso_vote_view(mafioso)
            
            if self.no_mafiosi_confirmed == self.no_mafiosi:
                self.check_end_condition()
            
    def mafia_cancel(self, mafioso):
        mafioso_id = str(mafioso.id)
        
        with transaction.atomic():
            if not self.mafia_confirm[mafioso_id]:
                return
            
            self.mafia_confirm[mafioso_id] = False
            self.no_mafiosi_confirmed -= 1
            self.save()
            
            self.update_mafioso_vote_view(mafioso)
    
    def end_vote_and_show_results(self, picked_player_id):
        self.vote_result = Player.objects.get(id=picked_player_id)
        self.current_state = self.State.MODERATOR_RESULT
        
        self.save(update_fields=["vote_result", "current_state"])
        
        moderator_view = {
            "view": "mafiaVote",
            "data": {
                "mode": "moderatorResult",
                "data": {
                    "pick": {
                        "id": self.vote_result.id,
                        "username": self.vote_result.user.visible_username
                    }
                }
            }
        }
        
        mafia_view = {
            "view": "backToSleep",
            "data": {}
        }
        
        self.game.moderator.view = moderator_view
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        for mafioso in self.game.players.filter(role=Player.Role.MAFIA, is_alive=True):
            mafioso.view = mafia_view
            mafioso.save(update_fields=["view"])
            mafioso.update_view()
    
    def update_moderator_and_mafia_vote_view(self):
        self.game.moderator.view = self.get_moderator_vote_view()
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        for mafioso in self.game.players.filter(role=Player.Role.MAFIA, is_alive=True):
            self.update_mafioso_vote_view(mafioso)
            
    def update_mafioso_vote_view(self, mafioso):
        mafioso.view = self.get_mafioso_vote_view(mafioso)
        mafioso.save(update_fields=["view"])
        mafioso.update_view()
        
    def check_end_condition(self):
        voted_player_id = None
        
        with transaction.atomic():
            for player_id, votes in self.votes.items():
                if votes == self.no_mafiosi:
                    voted_player_id = player_id
                    break
        
        if voted_player_id is not None:
            self.end_vote_and_show_results(voted_player_id)
    
    def get_moderator_vote_view(self):
        return {
            "view": "mafiaVote",
            "data": {
                "mode": "moderatorWait",
                "data": {
                    "noMafiosi": self.no_mafiosi,
                    "votes": [
                        {
                            "id": player.id,
                            "username": player.user.visible_username,
                            "votes": self.votes[str(player.id)]
                        }
                        for player in self.game.regular_players()
                    ]
                }
            }
        }
    
    def get_mafioso_vote_view(self, mafioso):
        return {
            "view": "mafiaVote",
            "data": {
                "mode": "vote",
                "data": {
                    "noMafiosi": self.no_mafiosi,
                    "confirmed": self.mafia_confirm[str(mafioso.id)],
                    "votes": [
                        {
                            "id": player.id,
                            "username": player.user.visible_username,
                            "votes": self.votes[str(player.id)],
                            "chosen": self.mafia_pick[str(mafioso.id)] == str(player.id)
                        }
                        for player in self.game.regular_players()
                    ]
                }
            }
        }