from polymorphic.models import PolymorphicManager
from django.db import models
from random import shuffle

from . import GameState, Player, Night

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
        view = {
            "view": "eventInfo",
            "data": {
                "mode": "roleRevealInfo",
                "data": {}
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save()
            player.update_view()
        
        self.game.moderator.refresh_from_db()
        self.game.moderator.players_discovered.add(*self.game.regular_players())
        self.game.moderator.save()
        self.game.moderator.update_state()
    
    def handle_action(self, player, action_type, action_data):
        match action_type:
            case "startRoleReveal" if (player.role == Player.Role.MODERATOR 
                                       and self.current_state == self.State.EVENT_INFO):
                self.next_person()
            
            case "revealToPlayer" if (player.role == Player.Role.MODERATOR
                                      and self.current_state == self.State.MODERATOR_INFO):
                self.reveal_to_player()
            
            case "revealContinue" if (player.id == self.order_of_players[self.current_player]
                                      and self.current_state == self.State.MODERATOR_WAIT):
                self.next_person()
            
            case _:
                self.unknown_action(player, action_type, action_data)

    def next_person(self):
        if self.current_player < len(self.order_of_players) - 1:
            self.current_player += 1
            self.current_state = self.State.MODERATOR_INFO
            self.save()
            
            self.next_moderator_info()
        else:
            self.current_state = self.State.EVENT_FINISHED
            self.save()
            
            self.end()
            
    def reveal_to_player(self):
        self.current_state = self.State.MODERATOR_WAIT 
        self.save()
        
        self.game.moderator.refresh_from_db()
        
        progress = self.game.moderator.view["data"]["data"]["progress"]
        role = self.game.moderator.view["data"]["data"]["role"]
        
        player_view = {
            "view": "reveal",
            "data": {
                "mode": "playerReveal",
                "data": {
                    "progress": progress,
                    "role": role
                }
            }
        }
        
        player = self.game.players.get(id=self.order_of_players[self.current_player])
        
        player.view = player_view
        if role == "mafia":
            player.players_discovered.add(*self.game.players.filter(role=Player.Role.MAFIA))
        else:
            player.players_discovered.add(player)
        player.save()
        
        player.update_state()
        player.update_view()
        
        self.game.moderator.view["data"]["mode"] = "moderatorWait"
        self.game.moderator.save(update_fields=["view"])
        self.game.moderator.update_view()
    
    def end(self):
        self.game.refresh_from_db()
        
        night = Night.objects.create(game=self.game)
        self.game.current_state = night
        
        self.game.save()
        
        night.start()
    
    def next_moderator_info(self):
        progress = self.get_current_progress()
        wait_before = self.get_wait_view(True, progress)
        wait_after = self.get_wait_view(False, progress)
        
        player_to_reveal = None
        for index, player_id in enumerate(self.order_of_players):
            player = self.game.players.get(id=player_id)
            
            if index < self.current_player:
                player.view = wait_after
            else:
                player.view = wait_before
            
            if index == self.current_player:
                player_to_reveal = player
            
            player.save()
            player.update_view()
        
        self.game.moderator.view = self.get_moderator_info_view(player_to_reveal, progress)
        self.game.moderator.save()
        self.game.moderator.update_view()
    
    def get_current_progress(self):
        return f"{self.current_player + 1}/{len(self.order_of_players)}"
    
    def get_wait_view(self, before: bool, progress):
        return {
            "view": "reveal",
            "data": {
                "mode": "playerWait" + ("Before" if before else "After"),
                "data": {
                    "progress": progress,
                }
            }
        }
    
    def get_moderator_info_view(self, player, progress):
        player_data = self.get_revealed_player_data(player)
        return {
            "view": "reveal",
            "data": {
                "mode": "moderatorInfo",
                "data": {
                    "progress": progress,
                    "role": player_data["role"],
                    "username": player_data["username"]
                }    
            }
        }

    def get_revealed_player_data(self, player):
        return {
            "role": player.role,
            "username": player.user.visible_username
        }
    
    
    
        
        
        
        
        
            
            
        