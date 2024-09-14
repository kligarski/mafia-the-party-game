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
import SeerPick from "./lib/views/SeerPick.svelte";
import SeerPickWakeUp from "./lib/views/modes/seer_pick/SeerPickWakeUp.svelte";
import SeerPickModeratorWaitForPick from "./lib/views/modes/seer_pick/SeerPickModeratorWaitForPick.svelte";
import SeerPickModeratorWaitForConfirm from "./lib/views/modes/seer_pick/SeerPickModeratorWaitForConfirm.svelte";
import SeerPickPick from "./lib/views/modes/seer_pick/SeerPickPick.svelte";
import SeerPickResult from "./lib/views/modes/seer_pick/SeerPickResult.svelte";
import SeerPickModeratorEnd from "./lib/views/modes/seer_pick/SeerPickModeratorEnd.svelte";
import NightOutcome from "./lib/views/NightOutcome.svelte";
import Discussion from "./lib/views/Discussion.svelte";
import DayVote from "./lib/views/DayVote.svelte";
import DayVoteMainView from "./lib/views/modes/day_vote/DayVoteMainView.svelte";
import DayVoteResult from "./lib/views/modes/day_vote/DayVoteResult.svelte";
import End from "./lib/views/End.svelte";

export const views: any = {
    loading: Loading,
    lobby: Lobby,
    eventInfo: EventInfo,
    reveal: Reveal,
    noPeeking: NoPeeking,
    mafiaVote: MafiaVote,
    backToSleep: BackToSleep,
    protectorPick: ProtectorPick,
    seerPick: SeerPick,
    nightOutcome: NightOutcome,
    discussion: Discussion,
    dayVote: DayVote,
    end: End,
}

export const deadAllowedViews: any = {
  loading: Loading,
  lobby: Lobby,
  end: End,
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

export const seerPickModes: any = {
  moderatorInfo: SeerPickWakeUp,
  moderatorWaitForPick: SeerPickModeratorWaitForPick,
  moderatorWaitForConfirm: SeerPickModeratorWaitForConfirm,
  pick: SeerPickPick,
  result: SeerPickResult,
  moderatorEnd: SeerPickModeratorEnd,
}

export const dayVoteModes: any = {
  moderatorInfo: DayVoteMainView,
  playerWaitBefore: DayVoteMainView,
  playerWaitAfter: DayVoteMainView,
  moderatorWait: DayVoteMainView,
  playerVote: DayVoteMainView,
  playerVoteResult: DayVoteMainView,
  playerWaitSomebody: DayVoteMainView,
  playerWaitSomebodyResult: DayVoteMainView,
  moderatorResult: DayVoteMainView,
  result: DayVoteResult,
}