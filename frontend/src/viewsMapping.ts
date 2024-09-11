import { readable } from "svelte/store";
import Lobby from "./lib/views/Lobby.svelte";
import Loading from "./lib/views/Loading.svelte";
import EventInfo from "./lib/views/EventInfo.svelte";

export const views: any = readable({
    loading: Loading,
    lobby: Lobby,
    eventInfo: EventInfo
})