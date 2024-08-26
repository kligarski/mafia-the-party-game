from polymorphic.models import PolymorphicManager
from django.db import models
from random import shuffle

from . import GameState, Player

class RoleRevealManager(PolymorphicManager):
    def assign_mafia(self, players, no_mafia):        
        for _ in range(no_mafia):
            mafioso = players.pop()
            mafioso.role = Player.Role.MAFIA
            mafioso.save()
            
    def assign_protector(self, players):
        protector = players.pop()
        protector.role = Player.Role.PROTECTOR
        protector.save()
        
    def assign_seer(self, players):
        seer = players.pop()
        seer.role = Player.Role.SEER
        seer.save()
        
    def assign_villagers(self, players):
        for player in players:
            player.role = Player.Role.VILLAGER
            player.save()
    
    def assign_roles(self, game):
        players_in_random_order = list(game.regular_players())
        shuffle(players_in_random_order)
        
        self.assign_mafia(players_in_random_order, len(players_in_random_order) // 3)
        self.assign_protector(players_in_random_order)
        self.assign_seer(players_in_random_order)
        self.assign_villagers(players_in_random_order)
    
    def get_random_order_of_player_ids(self, game):
        ids = [player.id for player in game.regular_players()]
        shuffle(ids)
        return ids
       
    def create_and_init(self, game):
        self.assign_roles(game)
        order_of_players = self.get_random_order_of_player_ids(game)
        
        role_reveal = self.create(game=game, order_of_players=order_of_players)        
        return role_reveal

class RoleReveal(GameState):
    class State(models.IntegerChoices):
        EVENT_INFO = 1
        MODERATOR_INFO = 2
        MODERATOR_WAIT = 3
        EVENT_FINISHED = 4
        
    current_state = models.IntegerField(choices=State, default=State.EVENT_INFO)
    order_of_players = models.JSONField()
    current_player = models.IntegerField(default=-1)
    
    objects = RoleRevealManager()
    
    def start(self):
        # TODO
        print(self.order_of_players)
        for player in self.game.players.all():
            print(player.role)
        
        
        
        # remember to also send role to playerState
        pass
    
    def handle_action(self, action_type, action_data):
        # TODO
        pass