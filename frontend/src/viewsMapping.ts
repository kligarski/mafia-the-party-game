import Lobby from "./lib/views/Lobby.svelte";
import Loading from "./lib/views/Loading.svelte";
import EventInfo from "./lib/views/EventInfo.svelte";
import Reveal from "./lib/views/Reveal.svelte";
import MafiaVote from "./lib/views/MafiaVote.svelte";
import RoleRevealMainView from "./lib/views/modes/role_reveal/RoleRevealMainView.svelte";
import RoleRevealPlayerWait from "./lib/views/modes/role_reveal/RoleRevealPlayerWait.svelte";
import MafiaVoteWakeUp from "./lib/views/modes/mafia_vote/MafiaVoteWakeUp.svelte";
import NoPeeking from "./lib/views/NoPeeking.svelte";
import MafiaVoteMainView from "./lib/views/modes/mafia_vote/MafiaVoteMainView.svelte";
import BackToSleep from "./lib/views/BackToSleep.svelte";
import MafiaVoteResult from "./lib/views/modes/mafia_vote/MafiaVoteResult.svelte";
import ProtectorPickWakeUp from "./lib/views/modes/protector_pick/ProtectorPickWakeUp.svelte";
import ProtectorPick from "./lib/views/ProtectorPick.svelte";
import ProtectorPickModeratorWait from "./lib/views/modes/protector_pick/ProtectorPickModeratorWait.svelte";
import ProtectorPickResult from "./lib/views/modes/protector_pick/ProtectorPickResult.svelte";
import ProtectorPickPick from "./lib/views/modes/protector_pick/ProtectorPickPick.svelte";

export const views: any = {
    loading: Loading,
    lobby: Lobby,
    eventInfo: EventInfo,
    reveal: Reveal,
    noPeeking: NoPeeking,
    mafiaVote: MafiaVote,
    backToSleep: BackToSleep,
    protectorPick: ProtectorPick,
}

export const roleRevealModes: any = {
  moderatorInfo: RoleRevealMainView,
  moderatorWait: RoleRevealMainView,
  playerReveal: RoleRevealMainView,
  playerWaitBefore: RoleRevealPlayerWait,
  playerWaitAfter: RoleRevealPlayerWait,
}

export const mafiaVoteModes: any = {
    moderatorInfo: MafiaVoteWakeUp,
    moderatorWait: MafiaVoteMainView,
    vote: MafiaVoteMainView,
    moderatorResult: MafiaVoteResult,
}

export const protectorPickModes: any = {
  moderatorInfo: ProtectorPickWakeUp,
  moderatorWait: ProtectorPickModeratorWait,
  pick: ProtectorPickPick,
  moderatorResult: ProtectorPickResult,
}