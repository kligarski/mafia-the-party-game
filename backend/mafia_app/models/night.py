from django.db import models
from . import GameState, Player, MafiaVote       

class Night(GameState):
    class StateType(models.IntegerChoices):
        EVENT_INFO = 1
        MAFIA_VOTE = 2
        PROTECTOR_PICK = 3
        SEER_PICK = 4
        EVENT_FINISHED = 5
        
    state_type = models.IntegerField(choices=StateType, default=StateType.EVENT_INFO)
    current_state = models.OneToOneField(GameState, on_delete=models.SET_NULL, 
                                         related_name="+", null=True, blank=True)
    
    # TODO: state-related data (mafia's pick, ...)
    mafia_pick = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    
    def start(self):
        self.game.cycle += 1
        self.game.save(update_fields=["cycle"])
        
        view = {
            "view": "eventInfo",
            "data": {
                "mode": "nightInfo",
                "data": {}
            }
        }
        
        for player in self.game.players.all():
            player.view = view
            player.save()
            player.update_view()
            player.update_state()
        
    def handle_action(self, player, action_type, action_data):
        match self.state_type:
            case self.StateType.EVENT_INFO if (action_type == "startNight" 
                                               and player.role == Player.Role.MODERATOR):
                self.start_night()
            
            case self.StateType.EVENT_FINISHED:
                self.unknown_action(player, action_type, action_data)
                
            case _ if self.current_state is not None:
                self.current_state.handle_action(player, action_type, action_data)
                
            case _:
                self.unknown_action(player, action_type, action_data)
    
    def start_night(self):
        mafia_vote = MafiaVote.objects.create_and_init(game=self.game, night_event=self)
        
        self.current_state = mafia_vote
        self.state_type = self.StateType.MAFIA_VOTE
        
        self.save()
        
        mafia_vote.start()
    
    def mafia_vote_end(self):
        # TODO
        raise NotImplementedError
        
    