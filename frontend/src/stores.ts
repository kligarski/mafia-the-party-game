import { writable } from "svelte/store";

const WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/game/";

type WebSocketMessage = {
    action: String,
    data: any
}

export type View = {
    view: String,
    data: any
}

let setView: (value: View) => void;

function createViewStore() {
    const { subscribe, set } = writable<View>({
        view: "loading",
        data: {}
    });

    setView = set;

    return {
        subscribe,
    }
}

export const view = createViewStore();

export type Player = {
    id: Number,
    username: String,
    role?: String
}

export type PlayerState = {
    id: Number,
    username: String,
    role: String,
    playersDiscovered: Player[],
    alive: boolean,
    cycle: Number
}

let setPlayerState: (value: PlayerState) => void;

function createPlayerStateStore() {
    const { subscribe, set } = writable<PlayerState>({
        id: -1,
        username: "username",
        role: "role",
        playersDiscovered: [],
        alive: false,
        cycle: -1
    });

    setPlayerState = set;

    return {
        subscribe,
    }
}

export const playerState = createPlayerStateStore();

export const connect = function(gameCode: string) {
    const ws = new WebSocket(WEBSOCKET_URL + gameCode + "/");

    ws.onopen = function (event) {
        console.log("Established WebSocket connection with the game server.");
    }

    ws.onmessage = function(event) {
        let message: WebSocketMessage = JSON.parse(event.data);
        
        switch (message.action) {
            case "changeView":
                setView(message.data);
                break;

            case "changePlayerState":
                setPlayerState(message.data);
                break;

            default:
                console.warn("Invalid message from the server.");
                console.log(JSON.parse(event.data));
                break;
        }
    }

    ws.onclose = function(event) {
        console.log("WebSocket connection closed.")
        console.log(event);

        // TODO: reconnect
    }
}


