from polymorphic.models import PolymorphicManager
from django.db import models
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
                
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def start_mafia_vote(self):
        self.current_state = self.State.VOTE
        self.save(update_fields=["current_state"])
        self.update_moderator_and_mafia_view()
    
    def update_moderator_and_mafia_view(self):
        self.game.moderator.view = self.get_moderator_vote_view()
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
        
        for mafioso in self.game.players.filter(role=Player.Role.MAFIA, is_alive=True):
            mafioso.view = self.get_mafioso_vote_view(mafioso)
            mafioso.save(update_fields=["view"])
            mafioso.update_view()
    
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
                            "chosen": self.mafia_pick[str(mafioso.id)] == player.id
                        }
                        for player in self.game.regular_players()
                    ]
                }
            }
        }