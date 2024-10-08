import { WebSocket } from "partysocket";
import { writable } from "svelte/store";

const WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/game/";

interface WebSocketMessage {
    action: string,
    data: any
}

export interface View {
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

export interface Player {
    id: number,
    username: string,
    role?: string,
    team?: string,
    alive?: boolean,
    chosen?: boolean,
    votes?: number
}

export interface PlayerState {
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
}

export interface Message {
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

export let tryDisconnect = function() {
    if (ws !== undefined) {
        ws.close(1000);
    }
}