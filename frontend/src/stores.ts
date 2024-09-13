import { writable } from "svelte/store";

const WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/game/";

type WebSocketMessage = {
    action: string,
    data: any
}

export type View = {
    view: string,
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
    id: number,
    username: string,
    role?: string,
    alive?: boolean,
    chosen?: boolean,
    votes?: number
}

export type PlayerState = {
    id: number,
    username: string,
    role: string,
    playersDiscovered: Player[],
    alive: boolean,
    cycle: number,
}

let setPlayerState: (value: PlayerState) => void;

function createPlayerStateStore() {
    const { subscribe, set } = writable<PlayerState>({
        id: -1,
        username: "username",
        role: "role",
        playersDiscovered: [],
        alive: true,
        cycle: -1
    });

    setPlayerState = set;

    return {
        subscribe,
    }
}

export const playerState = createPlayerStateStore();

let setGameCode: (value: string) => void;

function createGameCodeStore() {
    const { subscribe, set } = writable<string>("");

    setGameCode = set;

    return {
        subscribe
    }
}

export const gameCode = createGameCodeStore();

let ws: WebSocket | undefined;

export const connect = function(gameCode: string) {
    setGameCode(gameCode);

    ws = new WebSocket(WEBSOCKET_URL + gameCode + "/");

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

export type Message = {
    action: string,
    data: any
}

export let sendMessage = function(data: Message) {
    if (ws !== undefined) {
        ws.send(JSON.stringify(data));
    } else {
        console.warn("Trying to send a message but there is no WebSocket connection!");
    }
}