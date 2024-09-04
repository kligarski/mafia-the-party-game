from django.db import models
from enum import Enum
from . import GameState, Player, NightOutcome, Game, End

class Day(GameState):
    class StateType(models.IntegerChoices):
        EVENT_INFO = 1
        NIGHT_OUTCOME = 2
        DISCUSSION = 3
        VOTE = 4
        EVENT_FINISHED = 5
    
    state_type = models.IntegerField(choices=StateType, default=StateType.EVENT_INFO)
    current_state = models.OneToOneField(GameState, on_delete=models.SET_NULL, 
                                         related_name="+", null=True, blank=True)
    
    previous_night = models.ForeignKey("Night", on_delete=models.CASCADE, related_name="next_day")
    
    def start(self):
        view = {
            "view": "eventInfo",
            "data": {
                "mode": "dayInfo",
                "data": {}
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save(update_fields=["view"])
            player.update_view()
    
    def handle_action(self, player, action_type, action_data):
        match self.state_type:
            case self.StateType.EVENT_INFO if (action_type == "startDay" 
                                               and player.role == Player.Role.MODERATOR):
                self.start_day()
            
            case self.StateType.EVENT_FINISHED:
                self.unknown_action(player, action_type, action_data)
                
            case _ if self.current_state is not None:
                self.current_state.handle_action(player, action_type, action_data)
                
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def start_day(self):
        night_outcome = NightOutcome.objects.create(game=self.game, night_event=self.previous_night,
                                                    day_event=self)
        
        self.current_state = night_outcome
        self.state_type = self.StateType.NIGHT_OUTCOME
        
        self.save(update_fields=["current_state", "state_type"])
        
        night_outcome.start()
        
    def night_outcome_end(self):
        status = self.check_game_status()
        match status:
            case Game.GameStatus.CONTINUE:
                self.continue_game()
            
            case Game.GameStatus.MAFIA_WINS | Game.GameStatus.VILLAGE_WINS:
                self.end_game(status)
    
    def continue_game(self):
        # TODO
        raise NotImplementedError
    
    def end_game(self, status):
        self.state_type = self.StateType.EVENT_FINISHED
        self.save(update_fields=["state_type"])
        
        self.game.refresh_from_db()
        
        end = End.objects.create(game=self.game, game_result=status)
        self.game.current_state = end
        
        self.game.save()
        
        end.start()
    
    def check_game_status(self):
        no_mafiosi = len(self.game.players.filter(role=Player.Role.MAFIA, is_alive=True))
        no_villagers = len(self.game.regular_players().filter(is_alive=True).exclude(role=Player.Role.MAFIA))
        
        if no_mafiosi >= no_villagers:
            return Game.GameStatus.MAFIA_WINS
        elif no_mafiosi == 0:
            return Game.GameStatus.VILLAGE_WINS
        else:
            return Game.GameStatus.CONTINUE
    
    