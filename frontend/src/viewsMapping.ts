import Lobby from "./lib/views/Lobby.svelte";
import Loading from "./lib/views/Loading.svelte";
import EventInfo from "./lib/views/EventInfo.svelte";
import Reveal from "./lib/views/Reveal.svelte";

export const views: any = {
    loading: Loading,
    lobby: Lobby,
    eventInfo: EventInfo,
    reveal: Reveal
}