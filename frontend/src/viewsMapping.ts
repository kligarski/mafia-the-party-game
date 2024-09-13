import Lobby from "./lib/views/Lobby.svelte";
import Loading from "./lib/views/Loading.svelte";
import EventInfo from "./lib/views/EventInfo.svelte";
import Reveal from "./lib/views/Reveal.svelte";
import MafiaVote from "./lib/views/MafiaVote.svelte";
import RoleRevealMainView from "./lib/views/modes/role_reveal/RoleRevealMainView.svelte";
import RoleRevealPlayerWait from "./lib/views/modes/role_reveal/RoleRevealPlayerWait.svelte";
import MafiaWakeUp from "./lib/views/modes/mafia_vote/MafiaWakeUp.svelte";
import NoPeeking from "./lib/views/NoPeeking.svelte";

export const views: any = {
    loading: Loading,
    lobby: Lobby,
    eventInfo: EventInfo,
    reveal: Reveal,
    noPeeking: NoPeeking,
    mafiaVote: MafiaVote,
}

export const roleRevealModes: any = {
  moderatorInfo: RoleRevealMainView,
  moderatorWait: RoleRevealMainView,
  playerReveal: RoleRevealMainView,
  playerWaitBefore: RoleRevealPlayerWait,
  playerWaitAfter: RoleRevealPlayerWait,
}

export const mafiaVoteModes: any = {
    moderatorInfo: MafiaWakeUp,
}